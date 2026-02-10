#!/usr/bin/env python3
"""
List available Gemini models
"""
import google.genai as genai
import os
from dotenv import load_dotenv

load_dotenv()

def list_available_models():
    """List all available Gemini models"""
    try:
        api_key = os.getenv("GEMINI_API_KEY")
        client = genai.Client(api_key=api_key)
        
        print("🔍 Available Gemini Models:")
        print("=" * 40)
        
        models = client.models.list()
        for model in models:
            print(f"📋 {model.name}")
            if hasattr(model, 'display_name'):
                print(f"   Display: {model.display_name}")
            if hasattr(model, 'supported_generation_methods'):
                print(f"   Methods: {model.supported_generation_methods}")
            print()
            
    except Exception as e:
        print(f"❌ Error listing models: {e}")

if __name__ == "__main__":
    list_available_models()