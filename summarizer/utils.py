from dotenv import dotenv_values
from openai import OpenAI

# Load ONLY from .env
env_vars = dotenv_values(".env")

OPENAI_API_KEY = env_vars.get("OPENAI_API_KEY")
GROQ_API_KEY = env_vars.get("GROQ_API_KEY")

if OPENAI_API_KEY:
    client = OpenAI(api_key=OPENAI_API_KEY)
    MODEL_NAME = "gpt-3.5-turbo"
    print("✅ Using OpenAI client from .env.")
elif GROQ_API_KEY:
    client = OpenAI(
        api_key=GROQ_API_KEY,
        base_url="https://api.groq.com/openai/v1"
    )
    MODEL_NAME = "llama3-8b-8192"
    print("✅ Using GROQ client from .env.")
else:
    raise EnvironmentError("❌ No API key found in .env. Please set OPENAI_API_KEY or GROQ_API_KEY.")

def generate_summary(text):
    response = client.chat.completions.create(
        model=MODEL_NAME,
        messages=[
            {"role": "system", "content": "You are a helpful assistant that summarizes text."},
            {"role": "user", "content": f"Summarize this:\n{text}"}
        ]
    )
    return response.choices[0].message.content.strip()

def generate_bullet_points(text):
    response = client.chat.completions.create(
        model=MODEL_NAME,
        messages=[
            {"role": "system", "content": "You are a helpful assistant that extracts key bullet points from text."},
            {"role": "user", "content": f"Extract bullet points from the following:\n{text}"}
        ]
    )
    raw_output = response.choices[0].message.content.strip()
    lines = raw_output.split("\n")
    return [line.strip("-• ").strip() for line in lines if line.strip()]
