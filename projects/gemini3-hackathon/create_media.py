#!/usr/bin/env python3
"""
Helper script to generate project media and screenshots
"""
import os
import webbrowser
import time

def create_media_guide():
    """Generate a guide for creating project media"""
    
    media_guide = """
# Project Media Creation Guide

## Screenshots Needed for Devpost

### 1. Main Interface (Hero Shot)
- Open: http://localhost:8000
- Show: Clean interface with chat ready
- Dimensions: 1200x800 (3:2 ratio)
- Focus: Professional, welcoming design

### 2. Chat Interaction
- Show: Active conversation with AI
- Include: User message + AI response
- Highlight: Typing indicators, smooth UX
- Dimensions: 1200x800

### 3. Mobile View
- Use browser dev tools (F12)
- Toggle device toolbar
- Show: Responsive design on phone
- Dimensions: 400x600, then crop to 3:2

### 4. API Documentation
- Open: http://localhost:8000/docs
- Show: FastAPI auto-generated docs
- Highlight: Gemini 3 integration endpoints
- Dimensions: 1200x800

### 5. Code Architecture
- Screenshot of key files in VS Code
- Show: Clean, well-documented code
- Files: app.py, script.js, index.html
- Dimensions: 1200x800

## Video Demo Script (3 minutes)

### Opening (30 seconds)
"Hi! I'm excited to show you my Gemini 3 Hackathon project - an AI assistant built for social good that leverages Gemini 3's multimodal reasoning and reduced latency."

### Demo (90 seconds)
1. Show the live website
2. Enter API key
3. Ask a social good question: "How can AI help with education accessibility?"
4. Show fast response time
5. Ask follow-up questions
6. Demonstrate mobile responsiveness

### Technical (45 seconds)
1. Show the code structure
2. Explain Gemini 3 integration
3. Highlight FastAPI backend
4. Show API documentation

### Wrap-up (15 seconds)
"This project shows how Gemini 3's enhanced capabilities can democratize AI for social good. Thank you!"

## Tools for Media Creation

### Screenshots
- Browser: Use Chrome/Firefox dev tools
- Tools: Lightshot, Snagit, or built-in screenshot tools
- Format: PNG for best quality
- Size: Max 5MB, 3:2 ratio preferred

### Video Recording
- Screen recording: OBS Studio (free), Loom, or Camtasia
- Length: Exactly 3 minutes
- Format: MP4, 1080p recommended
- Audio: Clear narration, no background music needed

### Image Editing
- Free: GIMP, Paint.NET
- Paid: Photoshop, Canva Pro
- Online: Canva, Figma

## Quick Media Checklist

- [ ] Hero shot of main interface
- [ ] Chat interaction screenshot
- [ ] Mobile responsive view
- [ ] API documentation page
- [ ] Code architecture view
- [ ] 3-minute demo video
- [ ] All images in 3:2 ratio
- [ ] File sizes under 5MB
- [ ] Professional, clean appearance

## Upload to Devpost

1. Go to your Devpost submission
2. Upload images to "Project Media" section
3. Add video link to "Video demo link" field
4. Use YouTube, Vimeo, or direct file upload
5. Test all links before submitting

Good luck with your submission! 🚀
"""
    
    with open('MEDIA_GUIDE.md', 'w') as f:
        f.write(media_guide)
    
    print("📸 Media creation guide saved to MEDIA_GUIDE.md")
    print("🚀 Starting local server for screenshots...")
    
    # Start the demo server
    os.system('python run_demo.py &')
    
    print("📱 Server starting at http://localhost:8000")
    print("📋 Follow the guide in MEDIA_GUIDE.md to create your project media")

if __name__ == "__main__":
    create_media_guide()