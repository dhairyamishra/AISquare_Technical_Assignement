import subprocess
import json
import getpass
import requests
import wikipedia
import re
from datetime import datetime

BASE_URL = "http://127.0.0.1:8000/api"

def register_user(username, password):
    print("📝 Registering user...")
    response = requests.post(
        f"{BASE_URL}/register/",
        headers={"Content-Type": "application/json"},
        json={"username": username, "password": password}
    )
    if response.status_code == 201:
        print("✅ User registered successfully.")
    elif response.status_code == 400 and "already exists" in response.text:
        print("ℹ️ User already exists, continuing...")
    else:
        print(f"❌ Registration failed: {response.text}")
        exit()

def get_token(username, password):
    print("🔐 Fetching auth token...")
    response = requests.post(
        f"{BASE_URL}/token-auth/",
        headers={"Content-Type": "application/json"},
        json={"username": username, "password": password}
    )
    if response.status_code == 200:
        token = response.json().get("token")
        print("✅ Token retrieved.")
        return token
    else:
        print(f"❌ Failed to authenticate: {response.text}")
        exit()

def get_random_wikipedia_article():
    print("🎲 Fetching random Wikipedia article...")
    while True:
        try:
            title = wikipedia.random()
            page = wikipedia.page(title)
            print(f"📚 Selected article: {title}")
            return title, page.content[:3000]
        except wikipedia.exceptions.DisambiguationError:
            continue
        except Exception as e:
            print(f"❌ Wikipedia error: {e}")
            exit()

def run_curl(endpoint, token, text):
    curl_command = [
        "curl", "-s", "-X", "POST", f"{BASE_URL}/{endpoint}/",
        "-H", f"Authorization: Token {token}",
        "-H", "Content-Type: application/json",
        "-d", json.dumps({"text": text})
    ]
    result = subprocess.run(curl_command, capture_output=True, text=True)
    try:
        return json.loads(result.stdout)
    except json.JSONDecodeError:
        print(f"❌ Invalid JSON from {endpoint}:")
        print(result.stdout)
        exit()

def save_to_markdown(title, summary, bullets):
    safe_title = re.sub(r"[^\w\-]+", "_", title.lower())
    filename = f"summary_{safe_title}.md"
    with open(filename, "w", encoding="utf-8") as f:
        f.write(f"# {title}\n")
        f.write(f"*Generated on {datetime.now().strftime('%Y-%m-%d %H:%M')}*\n\n")
        f.write("## 🧠 Summary\n")
        f.write(summary.strip() + "\n\n")
        f.write("## 📌 Bullet Points\n")
        for bp in bullets:
            f.write(f"- {bp.strip()}\n")
    print(f"✅ Output saved to `{filename}`")

def main():
    print("🤖 Auto Wiki Demo: Register, Token, Summarize, Save\n")

    username = input("Enter username: ")
    password = getpass.getpass("Enter password: ")

    register_user(username, password)
    token = get_token(username, password)

    title, text = get_random_wikipedia_article()
    summary_result = run_curl("generate-summary", token, text)
    bullet_result = run_curl("generate-bullet-points", token, text)

    summary = summary_result.get("summary", "[No summary]")
    bullets = bullet_result.get("bullet_points", [])

    print("\n🧠 Summary:\n", summary)
    print("\n📌 Bullet Points:")
    for bp in bullets:
        print("•", bp)

    save_to_markdown(title, summary, bullets)

if __name__ == "__main__":
    main()
