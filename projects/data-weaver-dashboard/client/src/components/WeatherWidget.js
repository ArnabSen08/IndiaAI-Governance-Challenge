import React from 'react';

const WeatherWidget = ({ data }) => {
  if (!data || !data.current) {
    return (
      <div className="bg-white rounded-lg shadow-md p-6">
        <h2 className="text-xl font-semibold mb-4 text-gray-800">🌤️ Weather Data</h2>
        <p className="text-gray-500">No weather data available</p>
      </div>
    );
  }

  const { current, forecast } = data;
  const weather = current.weather[0];
  
  return (
    <div className="bg-white rounded-lg shadow-md p-6">
      <h2 className="text-xl font-semibold mb-4 text-gray-800">🌤️ Weather Data</h2>
      
      {/* Current Weather */}
      <div className="mb-6">
        <div className="flex items-center justify-between mb-2">
          <h3 className="text-lg font-medium text-gray-700">{current.name}</h3>
          <span className="text-2xl">{getWeatherEmoji(weather.main)}</span>
        </div>
        
        <div className="grid grid-cols-2 gap-4">
          <div className="bg-blue-50 rounded-lg p-3">
            <p className="text-sm text-gray-600">Temperature</p>
            <p className="text-2xl font-bold text-blue-600">{Math.round(current.main.temp)}°C</p>
          </div>
          
          <div className="bg-green-50 rounded-lg p-3">
            <p className="text-sm text-gray-600">Feels Like</p>
            <p className="text-2xl font-bold text-green-600">{Math.round(current.main.feels_like)}°C</p>
          </div>
          
          <div className="bg-purple-50 rounded-lg p-3">
            <p className="text-sm text-gray-600">Humidity</p>
            <p className="text-xl font-bold text-purple-600">{current.main.humidity}%</p>
          </div>
          
          <div className="bg-orange-50 rounded-lg p-3">
            <p className="text-sm text-gray-600">Pressure</p>
            <p className="text-xl font-bold text-orange-600">{current.main.pressure} hPa</p>
          </div>
        </div>
        
        <div className="mt-4 p-3 bg-gray-50 rounded-lg">
          <p className="text-sm text-gray-600">Condition</p>
          <p className="text-lg font-medium text-gray-800 capitalize">{weather.description}</p>
        </div>
      </div>

      {/* 5-Day Forecast Preview */}
      {forecast && forecast.list && (
        <div>
          <h4 className="text-md font-medium text-gray-700 mb-3">5-Day Forecast</h4>
          <div className="grid grid-cols-5 gap-2">
            {forecast.list.slice(0, 5).map((item, index) => (
              <div key={index} className="text-center p-2 bg-gray-50 rounded">
                <p className="text-xs text-gray-600">
                  {new Date(item.dt * 1000).toLocaleDateString('en', { weekday: 'short' })}
                </p>
                <span className="text-lg">{getWeatherEmoji(item.weather[0].main)}</span>
                <p className="text-sm font-medium">{Math.round(item.main.temp)}°</p>
              </div>
            ))}
          </div>
        </div>
      )}
    </div>
  );
};

const getWeatherEmoji = (condition) => {
  const emojiMap = {
    'Clear': '☀️',
    'Clouds': '☁️',
    'Rain': '🌧️',
    'Drizzle': '🌦️',
    'Thunderstorm': '⛈️',
    'Snow': '❄️',
    'Mist': '🌫️',
    'Fog': '🌫️',
    'Haze': '🌫️'
  };
  return emojiMap[condition] || '🌤️';
};

export default WeatherWidget;