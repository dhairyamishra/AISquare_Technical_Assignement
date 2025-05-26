import os
from openai import OpenAI
from dotenv import load_dotenv

# Load environment variables from .env
load_dotenv()

# Initialize OpenAI client with your API key
client = OpenAI(api_key=os.getenv("OPENAI_API_KEY"))

def generate_summary(text):
    response = client.chat.completions.create(
        model="gpt-3.5-turbo",
        messages=[
            {"role": "system", "content": "You are a helpful assistant that summarizes text."},
            {"role": "user", "content": f"Summarize this:\n{text}"}
        ]
    )
    return response.choices[0].message.content.strip()

def generate_bullet_points(text):
    response = client.chat.completions.create(
        model="gpt-3.5-turbo",
        messages=[
            {"role": "system", "content": "You are a helpful assistant that extracts key bullet points from text."},
            {"role": "user", "content": f"Extract bullet points from the following:\n{text}"}
        ]
    )
    raw_output = response.choices[0].message.content.strip()

    # Split into lines and normalize
    lines = raw_output.split("\n")
    return [line.strip("-• ").strip() for line in lines if line.strip()]
