# Gemini 3 Hackathon Project

## Overview
This project is built for the Gemini 3 Hackathon hosted by Google DeepMind & Devpost.

**🌐 Live Demo:** [https://arnabsen08.github.io/gemini3-hackathon](https://arnabsen08.github.io/gemini3-hackathon) ✅ **LIVE**

### Features
- Uses Gemini 3 API for multimodal reasoning and reduced latency
- Built as a next-gen AI application for social good
- Interactive web interface with real-time chat
- RESTful API backend with FastAPI
- Responsive design optimized for all devices

### Tech Stack
- **Backend:** FastAPI, Google Generative AI SDK, Python
- **Frontend:** HTML5, Tailwind CSS, Vanilla JavaScript
- **Deployment:** GitHub Pages, Vercel/Railway ready

## Quick Start

### 1. Local Development
```bash
# Clone the repository
git clone https://github.com/ArnabSen08/gemini3-hackathon.git
cd gemini3-hackathon

# Set up virtual environment
python -m venv venv
source venv/bin/activate  # On Windows: venv\Scripts\activate

# Install dependencies
pip install -r requirements.txt

# Run the demo
python run_demo.py
```

### 2. Get Your API Key
1. Visit [Google AI Studio](https://makersuite.google.com/app/apikey)
2. Create a new API key
3. **For local development**: Copy `.env.example` to `.env` and add your key
4. **For web demo**: Enter your API key directly in the interface

**🔐 Security Note**: No API keys are stored in the repository. Users must provide their own keys.

### 3. Try the Live Demo
Visit the [GitHub Pages demo](https://arnabsen08.github.io/gemini3-hackathon) and enter your API key to experience the full Gemini 3 integration.

## API Endpoints

- `GET /` - Web interface
- `POST /chat` - Chat with Gemini 3 AI
- `GET /health` - Health check
- `GET /demo-info` - Project information
- `GET /docs` - Interactive API documentation

## Submission Requirements
- ✅ Public repo link: [GitHub Repository](https://github.com/ArnabSen08/gemini3-hackathon)
- ✅ Demo link: [Live Demo](https://arnabsen08.github.io/gemini3-hackathon)
- 📝 200-word Gemini integration write-up: See [demo.md](demo.md)
- 🎥 3-min demo video: Coming soon

## Deployment Options

### GitHub Pages (Current)
Already configured and live at the demo link above.

### Vercel
```bash
# Install Vercel CLI
npm i -g vercel

# Deploy
vercel --prod
```

### Railway
```bash
# Install Railway CLI
npm install -g @railway/cli

# Deploy
railway login
railway init
railway up
```

## Contributing
This project is part of the Gemini 3 Hackathon. Feel free to explore the code and suggest improvements!

## License
MIT License - Built for educational and hackathon purposes.