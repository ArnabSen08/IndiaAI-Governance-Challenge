#!/usr/bin/env python3
"""
Direct API test using HTTP requests
"""
import requests
import json
import os
from dotenv import load_dotenv

load_dotenv()

def test_direct_api():
    """Test Gemini API directly with HTTP requests"""
    
    api_key = input("Enter your Gemini API key: ").strip()
    if not api_key:
        print("❌ No API key provided")
        print("🔑 Get your free API key from: https://makersuite.google.com/app/apikey")
        return False
    
    # Try the direct REST API approach with Gemini 3 Flash Preview
    url = f"https://generativelanguage.googleapis.com/v1beta/models/gemini-3-flash-preview:generateContent?key={api_key}"
    
    headers = {
        'Content-Type': 'application/json',
    }
    
    data = {
        "contents": [{
            "parts": [{
                "text": "Hello! Can you help me with a social good project using AI?"
            }]
        }]
    }
    
    try:
        print("🧪 Testing direct API call...")
        print(f"🔗 URL: {url[:80]}...")
        
        response = requests.post(url, headers=headers, json=data)
        
        print(f"📊 Status Code: {response.status_code}")
        
        if response.status_code == 200:
            result = response.json()
            if 'candidates' in result and result['candidates']:
                text = result['candidates'][0]['content']['parts'][0]['text']
                print("✅ SUCCESS!")
                print(f"🤖 Response: {text[:200]}...")
                return True
            else:
                print("❌ No content in response")
                print(f"Response: {result}")
        else:
            print(f"❌ API Error: {response.status_code}")
            print(f"Response: {response.text}")
            
    except Exception as e:
        print(f"❌ Exception: {e}")
    
    return False

if __name__ == "__main__":
    success = test_direct_api()
    if success:
        print("\n🎉 Direct API test successful!")
    else:
        print("\n❌ Direct API test failed")