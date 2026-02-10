const express = require('express');
const cors = require('cors');
const axios = require('axios');
require('dotenv').config();

const app = express();
const PORT = process.env.PORT || 3001;

// Middleware
app.use(cors());
app.use(express.json());

// API Routes

// Weather Data Endpoint
app.get('/api/weather/:city?', async (req, res) => {
  try {
    const city = req.params.city || process.env.DEFAULT_CITY || 'New York';
    const apiKey = process.env.WEATHER_API_KEY;
    
    if (!apiKey) {
      return res.status(500).json({ error: 'Weather API key not configured' });
    }

    const weatherResponse = await axios.get(
      `${process.env.WEATHER_BASE_URL}/weather?q=${city}&appid=${apiKey}&units=metric`
    );

    const forecastResponse = await axios.get(
      `${process.env.WEATHER_BASE_URL}/forecast?q=${city}&appid=${apiKey}&units=metric`
    );

    res.json({
      current: weatherResponse.data,
      forecast: forecastResponse.data,
      timestamp: new Date().toISOString()
    });
  } catch (error) {
    console.error('Weather API Error:', error.message);
    res.status(500).json({ 
      error: 'Failed to fetch weather data',
      details: error.response?.data?.message || error.message
    });
  }
});

// Stock Market Data Endpoint
app.get('/api/stocks/:symbol?', async (req, res) => {
  try {
    const symbol = req.params.symbol || 'SPY'; // S&P 500 ETF as default
    const apiKey = process.env.STOCK_API_KEY;
    
    if (!apiKey) {
      return res.status(500).json({ error: 'Stock API key not configured' });
    }

    // Get real-time quote
    const quoteResponse = await axios.get(
      `${process.env.STOCK_BASE_URL}?function=GLOBAL_QUOTE&symbol=${symbol}&apikey=${apiKey}`
    );

    // Get daily time series for historical data
    const timeSeriesResponse = await axios.get(
      `${process.env.STOCK_BASE_URL}?function=TIME_SERIES_DAILY&symbol=${symbol}&apikey=${apiKey}`
    );

    res.json({
      quote: quoteResponse.data,
      timeSeries: timeSeriesResponse.data,
      timestamp: new Date().toISOString()
    });
  } catch (error) {
    console.error('Stock API Error:', error.message);
    res.status(500).json({ 
      error: 'Failed to fetch stock data',
      details: error.response?.data || error.message
    });
  }
});

// Combined Data Endpoint for Correlation Analysis
app.get('/api/correlation/:city?/:symbol?', async (req, res) => {
  try {
    const city = req.params.city || process.env.DEFAULT_CITY || 'New York';
    const symbol = req.params.symbol || 'SPY';

    // Fetch both weather and stock data
    const [weatherRes, stockRes] = await Promise.all([
      axios.get(`http://localhost:${PORT}/api/weather/${city}`),
      axios.get(`http://localhost:${PORT}/api/stocks/${symbol}`)
    ]);

    // Simple correlation calculation (temperature vs stock price change)
    const temperature = weatherRes.data.current.main.temp;
    const stockPrice = parseFloat(stockRes.data.quote['Global Quote']['05. price']);
    const priceChange = parseFloat(stockRes.data.quote['Global Quote']['09. change']);
    
    res.json({
      weather: {
        temperature,
        condition: weatherRes.data.current.weather[0].main,
        humidity: weatherRes.data.current.main.humidity,
        pressure: weatherRes.data.current.main.pressure
      },
      stock: {
        symbol,
        price: stockPrice,
        change: priceChange,
        changePercent: stockRes.data.quote['Global Quote']['10. change percent']
      },
      correlation: {
        tempVsPrice: calculateSimpleCorrelation(temperature, stockPrice),
        tempVsChange: calculateSimpleCorrelation(temperature, priceChange)
      },
      timestamp: new Date().toISOString()
    });
  } catch (error) {
    console.error('Correlation API Error:', error.message);
    res.status(500).json({ 
      error: 'Failed to fetch correlation data',
      details: error.message
    });
  }
});

// Health Check Endpoint
app.get('/api/health', (req, res) => {
  res.json({ 
    status: 'OK', 
    timestamp: new Date().toISOString(),
    apis: {
      weather: !!process.env.WEATHER_API_KEY,
      stock: !!process.env.STOCK_API_KEY
    }
  });
});

// Simple correlation calculation helper
function calculateSimpleCorrelation(x, y) {
  // This is a placeholder for demonstration
  // In a real app, you'd calculate correlation over multiple data points
  return Math.random() * 2 - 1; // Returns value between -1 and 1
}

// Serve static files in production
if (process.env.NODE_ENV === 'production') {
  app.use(express.static('client/build'));
  
  app.get('*', (req, res) => {
    res.sendFile(path.join(__dirname, 'client/build', 'index.html'));
  });
}

app.listen(PORT, () => {
  console.log(`🚀 Data Weaver Server running on port ${PORT}`);
  console.log(`📊 Weather API: ${process.env.WEATHER_API_KEY ? '✅ Configured' : '❌ Missing'}`);
  console.log(`📈 Stock API: ${process.env.STOCK_API_KEY ? '✅ Configured' : '❌ Missing'}`);
});