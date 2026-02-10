from fastapi import FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from fastapi.staticfiles import StaticFiles
from fastapi.responses import FileResponse
from pydantic import BaseModel
import google.generativeai as genai
import os
from typing import Optional
from dotenv import load_dotenv

# Load environment variables
load_dotenv()

app = FastAPI(title="Gemini 3 Hackathon API", version="1.0.0")

# Enable CORS for web interface
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Serve static files (HTML, CSS, JS)
app.mount("/static", StaticFiles(directory="."), name="static")

class ChatMessage(BaseModel):
    message: str
    api_key: Optional[str] = None

class ChatResponse(BaseModel):
    response: str
    status: str

@app.get("/")
async def serve_homepage():
    """Serve the main HTML page"""
    return FileResponse('index.html')

@app.get("/health")
def health_check():
    """Health check endpoint"""
    return {'status': 'healthy', 'message': 'Gemini 3 Hackathon API is running!'}

@app.post("/chat", response_model=ChatResponse)
async def chat_with_gemini(chat_message: ChatMessage):
    """
    Chat endpoint that integrates with Gemini 3 API
    Showcases multimodal reasoning and reduced latency
    """
    try:
        # Use provided API key (user must provide their own)
        api_key = chat_message.api_key
        
        if not api_key:
            return ChatResponse(
                response="Please provide your Gemini API key to use the chat feature. Get your free API key from Google AI Studio: https://makersuite.google.com/app/apikey",
                status="error"
            )
        
        # Configure Gemini API
        genai.configure(api_key=api_key)
        
        # Use Gemini 3 Flash Preview model (latest for hackathon)
        model = genai.GenerativeModel('gemini-3-flash-preview')
        
        # Generate response with enhanced prompt for social good context
        enhanced_prompt = f"""
        You are an AI assistant built for social good as part of the Gemini 3 Hackathon. 
        Your responses should be helpful, ethical, and focused on positive impact.
        
        User message: {chat_message.message}
        
        Please provide a thoughtful and helpful response.
        """
        
        response = model.generate_content(enhanced_prompt)
        
        return ChatResponse(
            response=response.text,
            status="success"
        )
        
    except Exception as e:
        raise HTTPException(
            status_code=500, 
            detail=f"Error generating response: {str(e)}"
        )

@app.get("/demo-info")
def get_demo_info():
    """Get information about the demo and hackathon submission"""
    return {
        "project_name": "Gemini 3 AI Assistant for Social Good",
        "hackathon": "Gemini 3 Hackathon by Google DeepMind & Devpost",
        "features": [
            "Multimodal AI reasoning with Gemini 3",
            "Reduced latency for real-time interactions",
            "Social good focused applications",
            "Interactive web interface",
            "RESTful API architecture"
        ],
        "tech_stack": {
            "backend": ["FastAPI", "Google Generative AI", "Python"],
            "frontend": ["HTML5", "Tailwind CSS", "Vanilla JavaScript"],
            "deployment": ["GitHub Pages", "Vercel/Railway ready"]
        },
        "submission_requirements": {
            "repo_link": "https://github.com/ArnabSen08/gemini3-hackathon",
            "demo_link": "Live demo available via GitHub Pages",
            "video_demo": "3-minute demonstration video",
            "integration_writeup": "200-word Gemini 3 integration description"
        }
    }