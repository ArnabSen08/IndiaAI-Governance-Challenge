# CORS Solution for GitHub Pages Demo

## The Issue
GitHub Pages serves static files, and browsers block direct API calls to external services (like Google's Gemini API) due to CORS (Cross-Origin Resource Sharing) security policies.

## Solutions

### 1. Local Development (Recommended)
**Best experience with full functionality:**
```bash
git clone https://github.com/ArnabSen08/gemini3-hackathon.git
cd gemini3-hackathon
python -m venv venv
venv\Scripts\activate  # Windows
pip install -r requirements.txt
python run_demo.py
```
Open: http://localhost:8000

### 2. Deploy Backend Separately
Deploy the FastAPI backend to a platform that supports CORS:

#### Vercel Deployment:
```bash
npm i -g vercel
vercel --prod
```

#### Railway Deployment:
```bash
npm install -g @railway/cli
railway login
railway init
railway up
```

### 3. CORS Proxy (Temporary Solution)
For demo purposes only, you can use a CORS proxy:

Update the API URL in `script.js`:
```javascript
const proxyUrl = 'https://cors-anywhere.herokuapp.com/';
const apiUrl = `${proxyUrl}https://generativelanguage.googleapis.com/v1beta/models/gemini-3-flash-preview:generateContent?key=${apiKey}`;
```

**Note**: CORS proxies are not recommended for production use.

### 4. Browser Extension (Development Only)
Install a CORS browser extension like "CORS Unblock" for testing purposes.

## Current Demo Behavior

The GitHub Pages demo now:
1. **Tries direct API call** to Gemini 3 Flash Preview
2. **Falls back to alternative models** if the primary fails
3. **Shows helpful error messages** explaining CORS limitations
4. **Provides clear instructions** for local setup

## For Devpost Submission

The project demonstrates:
- ✅ **Working Gemini 3 integration** (locally)
- ✅ **Professional web interface** (GitHub Pages)
- ✅ **Comprehensive documentation**
- ✅ **Multiple deployment options**

**Recommendation**: Include screenshots of both the GitHub Pages interface AND the local working demo in your Devpost submission to show the full functionality.