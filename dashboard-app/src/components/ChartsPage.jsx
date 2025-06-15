import React, { useEffect, useState } from 'react';
import { LineChart, Line, XAxis, YAxis, CartesianGrid, Tooltip, Legend, ResponsiveContainer } from 'recharts';
import '../App.css'; // Assuming App.css has general styles

const sensorDataMap = {
  'fuel-consumed': {
    name: 'Asset - Fuel Consumed',
    data: [
      { name: 'Янв', value: 200 },
      { name: 'Фев', value: 250 },
      { name: 'Мар', value: 220 },
      { name: 'Апр', value: 280 },
      { name: 'Май', value: 300 },
    ],
    unit: '(л)',
    color: '#8884d8'
  },
  'odometer': {
    name: 'Asset - Odometer',
    data: [
      { name: 'Янв', value: 1000 },
      { name: 'Фев', value: 1200 },
      { name: 'Мар', value: 1100 },
      { name: 'Апр', value: 1300 },
      { name: 'Май', value: 1400 },
    ],
    unit: '(км)',
    color: '#82ca9d'
  },
  'runtime': {
    name: 'Asset - Runtime',
    data: [
      { name: 'Янв', value: 50 },
      { name: 'Фев', value: 60 },
      { name: 'Мар', value: 55 },
      { name: 'Апр', value: 65 },
      { name: 'Май', value: 70 },
    ],
    unit: '(ч)',
    color: '#ffc658'
  },
  'speed': {
    name: 'Asset - Speed',
    data: [
      { name: 'Янв', value: 80 },
      { name: 'Фев', value: 85 },
      { name: 'Мар', value: 75 },
      { name: 'Апр', value: 90 },
      { name: 'Май', value: 95 },
    ],
    unit: '(км/ч)',
    color: '#ff7300'
  },
  'engine-temp': {
    name: 'Engine Temperature',
    data: [
      { name: 'Янв', value: 90 },
      { name: 'Фев', value: 92 },
      { name: 'Мар', value: 88 },
      { name: 'Апр', value: 95 },
      { name: 'Май', value: 93 },
    ],
    unit: '(°C)',
    color: '#387902'
  },
};

const ChartsPage = () => {
  const [chartsToDisplay, setChartsToDisplay] = useState([]);

  useEffect(() => {
    const storedSensors = localStorage.getItem('selectedSensorsForCharts');
    if (storedSensors) {
      const selectedSensorIds = JSON.parse(storedSensors);
      const charts = selectedSensorIds.map(id => sensorDataMap[id]).filter(Boolean);
      setChartsToDisplay(charts);
    }
  }, []);

  return (
    <div className="charts-page-container">
      <h2>Графики по выбранным датчикам</h2>
      {chartsToDisplay.length > 0 ? (
        <div className="charts-grid">
          {chartsToDisplay.map((chartInfo, index) => (
            <div key={index} className="chart-card">
              <h3>{chartInfo.name} {chartInfo.unit}</h3>
              <ResponsiveContainer width="100%" height={300}>
                <LineChart
                  data={chartInfo.data}
                  margin={{
                    top: 5,
                    right: 30,
                    left: 20,
                    bottom: 5,
                  }}
                >
                  <CartesianGrid strokeDasharray="3 3" />
                  <XAxis dataKey="name" />
                  <YAxis />
                  <Tooltip />
                  <Legend />
                  <Line type="monotone" dataKey="value" stroke={chartInfo.color} activeDot={{ r: 8 }} />
                </LineChart>
              </ResponsiveContainer>
            </div>
          ))}
        </div>
      ) : (
        <p>Выберите датчики для отображения графиков в предыдущем окне.</p>
      )}
    </div>
  );
};

export default ChartsPage; 