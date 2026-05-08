#!/usr/bin/env python3
"""Quick test of Gemma 4 API"""

from openai import OpenAI
import os
from dotenv import load_dotenv

load_dotenv()

client = OpenAI(
    api_key=os.getenv("LLM_API_KEY"),
    base_url=os.getenv("LLM_BASE_URL")
)

print("Testing Gemma 4 31B IT...")
print(f"Model: google/gemma-4-31b-it")
print()

try:
    response = client.chat.completions.create(
        model="google/gemma-4-31b-it",
        messages=[
            {"role": "user", "content": "Say hello in one sentence."}
        ],
        max_tokens=50,
        timeout=30
    )
    
    print("✅ Success!")
    print(f"Response: {response.choices[0].message.content}")
    
except Exception as e:
    print(f"❌ Error: {e}")
