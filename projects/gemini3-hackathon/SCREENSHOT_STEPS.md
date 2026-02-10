# Step-by-Step Screenshot Guide

## Required Screenshots for Devpost (5 total)

### Screenshot 1: Hero Interface
**What to capture**: Main landing page
**Steps**:
1. Open https://arnabsen08.github.io/gemini3-hackathon
2. Wait for page to fully load
3. Take full-page screenshot (1200x800)
4. Save as "01-hero-interface.png"

### Screenshot 2: Chat Interaction
**What to capture**: Active conversation with Gemini 3
**Steps**:
1. Enter your API key from Google AI Studio: https://makersuite.google.com/app/apikey
2. Ask: "How can AI help with education accessibility?"
3. Wait for full response
4. Take screenshot showing both question and answer
5. Save as "02-chat-interaction.png"

### Screenshot 3: Mobile Responsive
**What to capture**: Mobile view of the interface
**Steps**:
1. Press F12 to open developer tools
2. Click device toolbar icon (phone/tablet icon)
3. Select "iPhone 12 Pro" or similar
4. Show the responsive design
5. Take screenshot and crop to 3:2 ratio
6. Save as "03-mobile-view.png"

### Screenshot 4: API Documentation
**What to capture**: FastAPI auto-generated docs
**Steps**:
1. Open http://localhost:8000/docs (make sure server is running)
2. Show the interactive API documentation
3. Expand the /chat endpoint if possible
4. Take full screenshot
5. Save as "04-api-docs.png"

### Screenshot 5: Code Architecture
**What to capture**: Clean code in VS Code
**Steps**:
1. Open VS Code with your project
2. Show app.py with the Gemini 3 integration
3. Make sure code is well-formatted and visible
4. Take screenshot showing the main integration code
5. Save as "05-code-architecture.png"

## Quick Commands

### Start Local Server (for API docs screenshot):
```bash
cd gemini3-hackathon
venv\Scripts\activate.bat
python run_demo.py
```

### Test API Key:
**Users must provide their own API key from Google AI Studio**
Get your free API key: https://makersuite.google.com/app/apikey

### Sample Questions for Screenshots:
- "How can AI help with education accessibility?"
- "What are ways AI can address climate change?"
- "How can AI support mental health initiatives?"

## File Naming Convention:
- 01-hero-interface.png
- 02-chat-interaction.png  
- 03-mobile-view.png
- 04-api-docs.png
- 05-code-architecture.png

All files should be:
- PNG format
- Under 5MB each
- 3:2 aspect ratio preferred
- High quality (1200x800 or similar)