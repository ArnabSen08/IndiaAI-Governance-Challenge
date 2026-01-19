#!/usr/bin/env python3
"""
Simple script to run the Gemini 3 Hackathon demo locally
"""
import uvicorn
import webbrowser
import time
import threading

def open_browser():
    """Open browser after a short delay"""
    time.sleep(2)
    webbrowser.open('http://localhost:8000')

if __name__ == "__main__":
    print("🚀 Starting Gemini 3 Hackathon Demo...")
    print("📱 Web interface will open at: http://localhost:8000")
    print("🔧 API docs available at: http://localhost:8000/docs")
    print("⚡ Press Ctrl+C to stop the server")
    
    # Open browser in background
    browser_thread = threading.Thread(target=open_browser)
    browser_thread.daemon = True
    browser_thread.start()
    
    # Start the server
    uvicorn.run(
        "app:app", 
        host="0.0.0.0", 
        port=8000, 
        reload=True,
        log_level="info"
    )