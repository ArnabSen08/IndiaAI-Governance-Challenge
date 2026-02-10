import React from 'react';
import {
  Chart as ChartJS,
  CategoryScale,
  LinearScale,
  PointElement,
  LineElement,
  BarElement,
  Title,
  Tooltip,
  Legend,
} from 'chart.js';
import { Line, Bar } from 'react-chartjs-2';

ChartJS.register(
  CategoryScale,
  LinearScale,
  PointElement,
  LineElement,
  BarElement,
  Title,
  Tooltip,
  Legend
);

const CorrelationChart = ({ data }) => {
  if (!data) {
    return (
      <div className="bg-white rounded-lg shadow-md p-6">
        <h2 className="text-xl font-semibold mb-4 text-gray-800">📊 Correlation Analysis</h2>
        <p className="text-gray-500">No correlation data available</p>
      </div>
    );
  }

  const { weather, stock, correlation } = data;

  // Sample historical data for demonstration
  const generateSampleData = () => {
    const days = 7;
    const labels = [];
    const temperatures = [];
    const stockPrices = [];
    
    for (let i = days - 1; i >= 0; i--) {
      const date = new Date();
      date.setDate(date.getDate() - i);
      labels.push(date.toLocaleDateString('en', { month: 'short', day: 'numeric' }));
      
      // Generate sample data with some correlation
      const baseTemp = weather.temperature + (Math.random() - 0.5) * 10;
      const basePrice = stock.price + (Math.random() - 0.5) * stock.price * 0.05;
      
      temperatures.push(baseTemp);
      stockPrices.push(basePrice);
    }
    
    return { labels, temperatures, stockPrices };
  };

  const { labels, temperatures, stockPrices } = generateSampleData();

  const lineChartData = {
    labels,
    datasets: [
      {
        label: 'Temperature (°C)',
        data: temperatures,
        borderColor: 'rgb(59, 130, 246)',
        backgroundColor: 'rgba(59, 130, 246, 0.1)',
        yAxisID: 'y',
      },
      {
        label: `${stock.symbol} Price ($)`,
        data: stockPrices,
        borderColor: 'rgb(34, 197, 94)',
        backgroundColor: 'rgba(34, 197, 94, 0.1)',
        yAxisID: 'y1',
      },
    ],
  };

  const lineChartOptions = {
    responsive: true,
    interaction: {
      mode: 'index',
      intersect: false,
    },
    plugins: {
      legend: {
        position: 'top',
      },
      title: {
        display: true,
        text: 'Weather vs Stock Price Trend (7 Days)',
      },
    },
    scales: {
      x: {
        display: true,
        title: {
          display: true,
          text: 'Date'
        }
      },
      y: {
        type: 'linear',
        display: true,
        position: 'left',
        title: {
          display: true,
          text: 'Temperature (°C)'
        },
      },
      y1: {
        type: 'linear',
        display: true,
        position: 'right',
        title: {
          display: true,
          text: 'Stock Price ($)'
        },
        grid: {
          drawOnChartArea: false,
        },
      },
    },
  };

  const correlationBarData = {
    labels: ['Temp vs Price', 'Temp vs Change'],
    datasets: [
      {
        label: 'Correlation Coefficient',
        data: [correlation.tempVsPrice, correlation.tempVsChange],
        backgroundColor: [
          correlation.tempVsPrice >= 0 ? 'rgba(34, 197, 94, 0.6)' : 'rgba(239, 68, 68, 0.6)',
          correlation.tempVsChange >= 0 ? 'rgba(34, 197, 94, 0.6)' : 'rgba(239, 68, 68, 0.6)',
        ],
        borderColor: [
          correlation.tempVsPrice >= 0 ? 'rgba(34, 197, 94, 1)' : 'rgba(239, 68, 68, 1)',
          correlation.tempVsChange >= 0 ? 'rgba(34, 197, 94, 1)' : 'rgba(239, 68, 68, 1)',
        ],
        borderWidth: 1,
      },
    ],
  };

  const correlationBarOptions = {
    responsive: true,
    plugins: {
      legend: {
        display: false,
      },
      title: {
        display: true,
        text: 'Correlation Coefficients',
      },
    },
    scales: {
      y: {
        beginAtZero: true,
        min: -1,
        max: 1,
        title: {
          display: true,
          text: 'Correlation (-1 to 1)'
        }
      },
    },
  };

  return (
    <div className="bg-white rounded-lg shadow-md p-6">
      <h2 className="text-xl font-semibold mb-6 text-gray-800">📊 Correlation Analysis</h2>
      
      {/* Current Data Summary */}
      <div className="grid grid-cols-1 md:grid-cols-3 gap-4 mb-6">
        <div className="bg-blue-50 rounded-lg p-4 text-center">
          <h3 className="text-sm font-medium text-gray-600 mb-1">Current Temperature</h3>
          <p className="text-2xl font-bold text-blue-600">{weather.temperature.toFixed(1)}°C</p>
          <p className="text-sm text-gray-500 capitalize">{weather.condition}</p>
        </div>
        
        <div className="bg-green-50 rounded-lg p-4 text-center">
          <h3 className="text-sm font-medium text-gray-600 mb-1">Stock Price</h3>
          <p className="text-2xl font-bold text-green-600">${stock.price.toFixed(2)}</p>
          <p className="text-sm text-gray-500">{stock.symbol}</p>
        </div>
        
        <div className="bg-purple-50 rounded-lg p-4 text-center">
          <h3 className="text-sm font-medium text-gray-600 mb-1">Price Change</h3>
          <p className={`text-2xl font-bold ${stock.change >= 0 ? 'text-green-600' : 'text-red-600'}`}>
            {stock.change >= 0 ? '+' : ''}{stock.change.toFixed(2)}
          </p>
          <p className="text-sm text-gray-500">{stock.changePercent}</p>
        </div>
      </div>

      {/* Charts */}
      <div className="grid grid-cols-1 lg:grid-cols-2 gap-6">
        <div>
          <Line data={lineChartData} options={lineChartOptions} />
        </div>
        
        <div>
          <Bar data={correlationBarData} options={correlationBarOptions} />
        </div>
      </div>

      {/* Insights */}
      <div className="mt-6 p-4 bg-gray-50 rounded-lg">
        <h3 className="text-lg font-medium text-gray-800 mb-2">🔍 Insights</h3>
        <div className="grid grid-cols-1 md:grid-cols-2 gap-4 text-sm">
          <div>
            <p className="font-medium text-gray-700">Weather Impact:</p>
            <p className="text-gray-600">
              {weather.condition === 'Rain' ? 'Rainy weather might affect consumer behavior' :
               weather.temperature > 25 ? 'Hot weather could boost energy sector stocks' :
               weather.temperature < 5 ? 'Cold weather might increase heating demand' :
               'Moderate weather conditions'}
            </p>
          </div>
          <div>
            <p className="font-medium text-gray-700">Market Correlation:</p>
            <p className="text-gray-600">
              {Math.abs(correlation.tempVsPrice) > 0.5 ? 
                `Strong ${correlation.tempVsPrice > 0 ? 'positive' : 'negative'} correlation detected` :
                'Weak correlation between temperature and stock price'}
            </p>
          </div>
        </div>
      </div>
    </div>
  );
};

export default CorrelationChart;