import React from 'react';

const StockWidget = ({ data }) => {
  if (!data || !data.quote || !data.quote['Global Quote']) {
    return (
      <div className="bg-white rounded-lg shadow-md p-6">
        <h2 className="text-xl font-semibold mb-4 text-gray-800">📈 Stock Market Data</h2>
        <p className="text-gray-500">No stock data available</p>
      </div>
    );
  }

  const quote = data.quote['Global Quote'];
  const symbol = quote['01. symbol'];
  const price = parseFloat(quote['05. price']);
  const change = parseFloat(quote['09. change']);
  const changePercent = quote['10. change percent'];
  const volume = parseInt(quote['06. volume']);
  const high = parseFloat(quote['03. high']);
  const low = parseFloat(quote['02. low']);
  const open = parseFloat(quote['04. open']);
  
  const isPositive = change >= 0;
  
  return (
    <div className="bg-white rounded-lg shadow-md p-6">
      <h2 className="text-xl font-semibold mb-4 text-gray-800">📈 Stock Market Data</h2>
      
      {/* Stock Header */}
      <div className="mb-6">
        <div className="flex items-center justify-between mb-2">
          <h3 className="text-lg font-medium text-gray-700">{symbol}</h3>
          <span className="text-2xl">{isPositive ? '📈' : '📉'}</span>
        </div>
        
        <div className="flex items-baseline gap-2 mb-4">
          <span className="text-3xl font-bold text-gray-800">${price.toFixed(2)}</span>
          <span className={`text-lg font-medium ${isPositive ? 'text-green-600' : 'text-red-600'}`}>
            {isPositive ? '+' : ''}{change.toFixed(2)} ({changePercent})
          </span>
        </div>
      </div>

      {/* Stock Metrics */}
      <div className="grid grid-cols-2 gap-4 mb-4">
        <div className="bg-blue-50 rounded-lg p-3">
          <p className="text-sm text-gray-600">Open</p>
          <p className="text-xl font-bold text-blue-600">${open.toFixed(2)}</p>
        </div>
        
        <div className="bg-green-50 rounded-lg p-3">
          <p className="text-sm text-gray-600">High</p>
          <p className="text-xl font-bold text-green-600">${high.toFixed(2)}</p>
        </div>
        
        <div className="bg-red-50 rounded-lg p-3">
          <p className="text-sm text-gray-600">Low</p>
          <p className="text-xl font-bold text-red-600">${low.toFixed(2)}</p>
        </div>
        
        <div className="bg-purple-50 rounded-lg p-3">
          <p className="text-sm text-gray-600">Volume</p>
          <p className="text-lg font-bold text-purple-600">{formatVolume(volume)}</p>
        </div>
      </div>

      {/* Market Status */}
      <div className="p-3 bg-gray-50 rounded-lg">
        <div className="flex justify-between items-center">
          <span className="text-sm text-gray-600">Market Status</span>
          <span className="flex items-center gap-1">
            <div className="w-2 h-2 bg-green-500 rounded-full animate-pulse"></div>
            <span className="text-sm font-medium text-green-600">Live Data</span>
          </span>
        </div>
        <p className="text-xs text-gray-500 mt-1">
          Last updated: {new Date().toLocaleTimeString()}
        </p>
      </div>

      {/* Performance Indicator */}
      <div className="mt-4">
        <div className="flex justify-between text-sm text-gray-600 mb-1">
          <span>Day's Range</span>
          <span>${low.toFixed(2)} - ${high.toFixed(2)}</span>
        </div>
        <div className="w-full bg-gray-200 rounded-full h-2">
          <div 
            className={`h-2 rounded-full ${isPositive ? 'bg-green-500' : 'bg-red-500'}`}
            style={{ 
              width: `${((price - low) / (high - low)) * 100}%` 
            }}
          ></div>
        </div>
      </div>
    </div>
  );
};

const formatVolume = (volume) => {
  if (volume >= 1000000) {
    return `${(volume / 1000000).toFixed(1)}M`;
  } else if (volume >= 1000) {
    return `${(volume / 1000).toFixed(1)}K`;
  }
  return volume.toString();
};

export default StockWidget;