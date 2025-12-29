# Data Weaver Setup Guide

## Quick Start

### 1. Get API Keys

**OpenWeatherMap API** (Free tier available)
1. Visit https://openweathermap.org/api
2. Sign up for a free account
3. Get your API key from the dashboard

**Alpha Vantage API** (Free tier available)
1. Visit https://www.alphavantage.co/support/#api-key
2. Sign up for a free account
3. Get your API key

### 2. Environment Setup

```bash
# Clone the repository
git clone <your-repo-url>
cd data-weaver-dashboard

# Copy environment template
cp .env.example .env

# Edit .env file and add your API keys:
WEATHER_API_KEY=your_openweathermap_api_key_here
STOCK_API_KEY=your_alphavantage_api_key_here
```

### 3. Install Dependencies

```bash
# Install backend dependencies
npm install

# Install frontend dependencies
cd client
npm install
cd ..
```

### 4. Run the Application

```bash
# Start both backend and frontend
npm run dev

# Or run separately:
# Backend: npm run server
# Frontend: npm run client
```

### 5. Access the Dashboard

- Frontend: http://localhost:3000
- Backend API: http://localhost:3001

## API Endpoints

- `GET /api/weather/:city` - Weather data for a city
- `GET /api/stocks/:symbol` - Stock data for a symbol
- `GET /api/correlation/:city/:symbol` - Correlation analysis
- `GET /api/health` - Health check

## Default Configuration

- Default city: New York
- Default stock: SPY (S&P 500 ETF)
- Server port: 3001
- Client port: 3000

## Troubleshooting

### API Rate Limits
- OpenWeatherMap: 60 calls/minute (free tier)
- Alpha Vantage: 5 calls/minute (free tier)

### Common Issues
1. **CORS errors**: Make sure backend is running on port 3001
2. **API key errors**: Check your .env file configuration
3. **Module not found**: Run `npm install` in both root and client directories

## Production Deployment

1. Build the React app: `cd client && npm run build`
2. Set NODE_ENV=production
3. Configure your production API keys
4. Deploy to your preferred platform (Heroku, AWS, etc.)

## Features to Explore

1. Try different cities and stock symbols
2. Look for patterns in the correlation charts
3. Check how weather affects different market sectors
4. Explore the 5-day forecast vs stock trends