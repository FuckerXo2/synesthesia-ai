#!/usr/bin/env python3
"""
Test script for NVIDIA Build API
Verifies your API key and model access before building Synesthesia
"""

import os
from openai import OpenAI
from dotenv import load_dotenv

# Load environment variables
load_dotenv()

def test_nvidia_api():
    """Test NVIDIA Build API connection and model"""
    
    api_key = os.getenv("LLM_API_KEY")
    base_url = os.getenv("LLM_BASE_URL", "https://integrate.api.nvidia.com/v1")
    model_name = os.getenv("LLM_MODEL_NAME", "deepseek-ai/deepseek-v4-flash")
    
    if not api_key:
        print("❌ Error: LLM_API_KEY not found in .env file")
        print("\n📝 Steps to fix:")
        print("1. Go to https://build.nvidia.com/")
        print("2. Sign in and get your API key")
        print("3. Copy .env.example to .env")
        print("4. Replace 'nvapi-YOUR_KEY_HERE' with your actual key")
        return False
    
    print("🔧 Testing NVIDIA Build API...")
    print(f"   Model: {model_name}")
    print(f"   Base URL: {base_url}")
    print()
    
    try:
        client = OpenAI(
            api_key=api_key,
            base_url=base_url
        )
        
        # Test with a simple prompt
        print("📡 Sending test request...")
        response = client.chat.completions.create(
            model=model_name,
            messages=[
                {
                    "role": "system",
                    "content": "You are a helpful AI assistant."
                },
                {
                    "role": "user",
                    "content": "Say 'Hello from NVIDIA Build!' and tell me your model name in one sentence."
                }
            ],
            temperature=0.7,
            max_tokens=100
        )
        
        result = response.choices[0].message.content
        
        print("✅ Success! API is working.")
        print(f"\n🤖 Model response:\n{result}\n")
        
        # Show usage stats
        if hasattr(response, 'usage'):
            print(f"📊 Token usage:")
            print(f"   Prompt: {response.usage.prompt_tokens}")
            print(f"   Completion: {response.usage.completion_tokens}")
            print(f"   Total: {response.usage.total_tokens}")
        
        return True
        
    except Exception as e:
        print(f"❌ Error: {str(e)}\n")
        
        if "401" in str(e) or "unauthorized" in str(e).lower():
            print("🔑 Authentication failed. Check your API key.")
        elif "404" in str(e) or "not found" in str(e).lower():
            print("🤔 Model not found. Try a different model name.")
        else:
            print("⚠️  Unknown error. Check your internet connection.")
        
        return False


def list_recommended_models():
    """Show recommended models for Synesthesia"""
    print("\n" + "="*60)
    print("🎯 RECOMMENDED MODELS FOR SYNESTHESIA")
    print("="*60)
    
    models = [
        {
            "name": "deepseek-ai/deepseek-v4-flash",
            "desc": "Fast, smart, 1M context - BEST FOR AGENTS",
            "recommended": True
        },
        {
            "name": "deepseek-ai/deepseek-v3_2",
            "desc": "Smartest (685B) - Best quality",
            "recommended": False
        },
        {
            "name": "deepseek-ai/deepseek-r1",
            "desc": "Reasoning focused - Complex decisions",
            "recommended": False
        },
        {
            "name": "meta/llama-3.1-70b-instruct",
            "desc": "Balanced - Fast and reliable",
            "recommended": False
        },
    ]
    
    for model in models:
        marker = "⭐" if model["recommended"] else "  "
        print(f"{marker} {model['name']}")
        print(f"   {model['desc']}")
        print()


if __name__ == "__main__":
    print("="*60)
    print("🚀 SYNESTHESIA - NVIDIA BUILD API TEST")
    print("="*60)
    print()
    
    success = test_nvidia_api()
    
    if success:
        print("\n✨ You're ready to build Synesthesia!")
        print("   Next step: Run the population generator")
    else:
        list_recommended_models()
        print("\n💡 Fix the issues above and try again.")
    
    print("\n" + "="*60)
