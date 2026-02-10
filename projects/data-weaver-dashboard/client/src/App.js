import React, { useState, useEffect } from 'react';
import axios from 'axios';
import WeatherWidget from './components/WeatherWidget';
import StockWidget from './components/StockWidget';
import CorrelationChart from './components/CorrelationChart';
import './App.css';

function App() {
  const [weatherData, setWeatherData] = useState(null);
  const [stockData, setStockData] = useState(null);
  const [correlationData, setCorrelationData] = useState(null);
  const [loading, setLoading] = useState(true);
  const [city, setCity] = useState('New York');
  const [symbol, setSymbol] = useState('SPY');

  const API_BASE = 'http://localhost:3001/api';

  useEffect(() => {
    fetchAllData();
  }, [city, symbol]);

  const fetchAllData = async () => {
    setLoading(true);
    try {
      const [weatherRes, stockRes, correlationRes] = await Promise.all([
        axios.get(`${API_BASE}/weather/${city}`),
        axios.get(`${API_BASE}/stocks/${symbol}`),
        axios.get(`${API_BASE}/correlation/${city}/${symbol}`)
      ]);

      setWeatherData(weatherRes.data);
      setStockData(stockRes.data);
      setCorrelationData(correlationRes.data);
    } catch (error) {
      console.error('Error fetching data:', error);
    } finally {
      setLoading(false);
    }
  };

  return (
    <div className="min-h-screen bg-gradient-to-br from-blue-50 to-indigo-100">
      <div className="container mx-auto px-4 py-8">
        {/* Header */}
        <header className="text-center mb-8">
          <h1 className="text-4xl font-bold text-gray-800 mb-2">
            🌦️ The Data Weaver 📈
          </h1>
          <p className="text-lg text-gray-600">
            Exploring correlations between Weather and Stock Market data
          </p>
        </header>

        {/* Controls */}
        <div className="flex flex-wrap justify-center gap-4 mb-8">
          <div className="flex items-center gap-2">
            <label className="text-sm font-medium text-gray-700">City:</label>
            <input
              type="text"
              value={city}
              onChange={(e) => setCity(e.target.value)}
              className="px-3 py-1 border border-gray-300 rounded-md focus:outline-none focus:ring-2 focus:ring-blue-500"
              placeholder="Enter city name"
            />
          </div>
          <div className="flex items-center gap-2">
            <label className="text-sm font-medium text-gray-700">Stock:</label>
            <input
              type="text"
              value={symbol}
              onChange={(e) => setSymbol(e.target.value.toUpperCase())}
              className="px-3 py-1 border border-gray-300 rounded-md focus:outline-none focus:ring-2 focus:ring-blue-500"
              placeholder="Stock symbol"
            />
          </div>
          <button
            onClick={fetchAllData}
            className="px-4 py-1 bg-blue-500 text-white rounded-md hover:bg-blue-600 focus:outline-none focus:ring-2 focus:ring-blue-500"
          >
            Refresh Data
          </button>
        </div>

        {loading ? (
          <div className="text-center py-12">
            <div className="inline-block animate-spin rounded-full h-8 w-8 border-b-2 border-blue-500"></div>
            <p className="mt-2 text-gray-600">Loading data...</p>
          </div>
        ) : (
          <div className="grid grid-cols-1 lg:grid-cols-2 gap-6 mb-8">
            {/* Weather Widget */}
            <WeatherWidget data={weatherData} />
            
            {/* Stock Widget */}
            <StockWidget data={stockData} />
          </div>
        )}

        {/* Correlation Analysis */}
        {correlationData && (
          <CorrelationChart data={correlationData} />
        )}

        {/* Footer */}
        <footer className="text-center mt-12 text-gray-500 text-sm">
          <p>Built with ❤️ using Kiro AI | Data sources: OpenWeatherMap & Alpha Vantage</p>
        </footer>
      </div>
    </div>
  );
}

export default App;
