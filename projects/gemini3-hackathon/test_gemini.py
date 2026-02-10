#!/usr/bin/env python3
"""
Test script to verify Gemini API integration
"""
import google.generativeai as genai
import os
from dotenv import load_dotenv
import time

# Load environment variables
load_dotenv()

def test_gemini_integration():
    """Test the Gemini API integration"""
    
    print("🧪 Testing Gemini API Integration...")
    print("=" * 50)
    
    # Get API key from user input (no default API key for security)
    api_key = input("Enter your Gemini API key: ").strip()
    if not api_key:
        print("❌ Error: No API key provided")
        print("🔑 Get your free API key from: https://makersuite.google.com/app/apikey")
        return False
    
    try:
        # Configure Gemini API
        genai.configure(api_key=api_key)
        print("✅ API key configured successfully")
        
        # Initialize model
        model = genai.GenerativeModel('gemini-3-flash-preview')
        print("✅ Gemini 3 Flash Preview model initialized")
        
        # Test message for social good context
        test_message = "How can AI technology be used to improve education accessibility for underserved communities?"
        
        print(f"\n📝 Test Query: {test_message}")
        print("\n⏳ Generating response...")
        
        start_time = time.time()
        
        # Enhanced prompt for social good
        enhanced_prompt = f"""
        You are an AI assistant built for social good as part of the Gemini 3 Hackathon. 
        Your responses should be helpful, ethical, and focused on positive impact.
        
        User message: {test_message}
        
        Please provide a thoughtful and helpful response.
        """
        
        response = model.generate_content(enhanced_prompt)
        
        end_time = time.time()
        response_time = end_time - start_time
        
        print(f"\n🤖 AI Response:")
        print("-" * 40)
        print(response.text)
        print("-" * 40)
        
        print(f"\n⚡ Response Time: {response_time:.2f} seconds")
        print("✅ Gemini integration test successful!")
        
        return True
        
    except Exception as e:
        print(f"❌ Error testing Gemini integration: {str(e)}")
        return False

def test_api_endpoints():
    """Test the FastAPI endpoints"""
    print("\n🌐 Testing API Endpoints...")
    print("=" * 50)
    
    try:
        import requests
        import json
        
        # Test health endpoint
        health_response = requests.get("http://localhost:8000/health")
        if health_response.status_code == 200:
            print("✅ Health endpoint working")
        else:
            print("❌ Health endpoint failed")
        
        # Test chat endpoint
        chat_data = {
            "message": "Hello, can you help me with a social good project?",
            "api_key": os.getenv("GEMINI_API_KEY")
        }
        
        chat_response = requests.post(
            "http://localhost:8000/chat",
            json=chat_data,
            headers={"Content-Type": "application/json"}
        )
        
        if chat_response.status_code == 200:
            result = chat_response.json()
            print("✅ Chat endpoint working")
            print(f"📝 Response: {result['response'][:100]}...")
        else:
            print(f"❌ Chat endpoint failed: {chat_response.status_code}")
            
    except requests.exceptions.ConnectionError:
        print("⚠️  Server not running. Start with: python run_demo.py")
    except Exception as e:
        print(f"❌ Error testing API endpoints: {str(e)}")

if __name__ == "__main__":
    print("🚀 Gemini 3 Hackathon - Integration Test")
    print("=" * 60)
    
    # Test Gemini integration
    gemini_success = test_gemini_integration()
    
    # Test API endpoints (optional - requires server running)
    test_api_endpoints()
    
    print("\n" + "=" * 60)
    if gemini_success:
        print("🎉 All tests passed! Your Gemini 3 integration is ready!")
        print("🌐 Start the demo with: python run_demo.py")
        print("🔗 Live demo: https://arnabsen08.github.io/gemini3-hackathon")
    else:
        print("❌ Some tests failed. Check your API key and try again.")