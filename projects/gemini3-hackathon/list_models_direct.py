#!/usr/bin/env python3
"""
List available models using direct API
"""
import requests
import json
import os
from dotenv import load_dotenv

load_dotenv()

def list_models():
    """List available models"""
    
    api_key = input("Enter your Gemini API key: ").strip()
    if not api_key:
        print("❌ No API key provided")
        print("🔑 Get your free API key from: https://makersuite.google.com/app/apikey")
        return
    
    # List models endpoint
    url = f"https://generativelanguage.googleapis.com/v1beta/models?key={api_key}"
    
    try:
        print("🔍 Fetching available models...")
        response = requests.get(url)
        
        print(f"📊 Status Code: {response.status_code}")
        
        if response.status_code == 200:
            result = response.json()
            print("✅ Available Models:")
            print("=" * 50)
            
            if 'models' in result:
                for model in result['models']:
                    name = model.get('name', 'Unknown')
                    display_name = model.get('displayName', 'No display name')
                    methods = model.get('supportedGenerationMethods', [])
                    
                    print(f"📋 {name}")
                    print(f"   Display: {display_name}")
                    print(f"   Methods: {methods}")
                    print()
            else:
                print("No models found in response")
                print(f"Response: {result}")
        else:
            print(f"❌ API Error: {response.status_code}")
            print(f"Response: {response.text}")
            
    except Exception as e:
        print(f"❌ Exception: {e}")

if __name__ == "__main__":
    list_models()