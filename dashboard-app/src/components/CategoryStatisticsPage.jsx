import React, { useState, useEffect } from 'react';
import { useParams } from 'react-router-dom';
import { LineChart, Line, XAxis, YAxis, CartesianGrid, Tooltip, Legend, ResponsiveContainer } from 'recharts';
import { apiService } from '../services/api';
import '../App.css'; // Assume App.css has general styles and button styles

const categoryChartsData = {
  fuel: {
    "daily-consumption": {
      name: "Ежедневный расход",
      unit: "(л)",
      color: "#6BFCBA",
      data: [
        { name: '01/01', value: 10 }, { name: '02/01', value: 12 }, { name: '03/01', value: 11 },
        { name: '04/01', value: 15 }, { name: '05/01', value: 13 }, { name: '06/01', value: 14 },
      ],
    },
    "refuel-cost": {
      name: "Стоимость заправки",
      unit: "(₽)",
      color: "#B6D9FC",
      data: [
        { name: '01/01', value: 500 }, { name: '02/01', value: 600 }, { name: '03/01', value: 550 },
        { name: '04/01', value: 750 }, { name: '05/01', value: 650 }, { name: '06/01', value: 700 },
      ],
    },
  },
  taxes: {
    "monthly-taxes": {
      name: "Ежемесячные налоги",
      unit: "(₽)",
      color: "#82C4F8",
      data: [
        { name: 'Янв', value: 2000 }, { name: 'Фев', value: 2100 }, { name: 'Мар', value: 2050 },
        { name: 'Апр', value: 2200 }, { name: 'Май', value: 2150 },
      ],
    },
  },
  repair: {
    "repair-cost": {
      name: "Стоимость ремонта",
      unit: "(₽)",
      color: "#1D92C5",
      data: [
        { name: 'Март', value: 15000 }, { name: 'Апрель', value: 5000 }, { name: 'Май', value: 20000 },
      ],
    },
  },
  other: {
    "misc-expenses": {
      name: "Прочие расходы",
      unit: "(₽)",
      color: "#F79023",
      data: [
        { name: 'Янв', value: 1000 }, { name: 'Фев', value: 800 }, { name: 'Мар', value: 1200 },
      ],
    },
  },
};

const CategoryStatisticsPage = () => {
  const { category } = useParams();
  const [startDate, setStartDate] = useState('');
  const [endDate, setEndDate] = useState('');
  const [showDownloadButton, setShowDownloadButton] = useState(false);
  const [statisticsData, setStatisticsData] = useState(null);
  const [selectedCharts, setSelectedCharts] = useState([]);

  const categoryTitles = {
    fuel: "Топливо",
    taxes: "Налоги",
    repair: "Ремонт",
    other: "Прочее",
  };

  const currentCategoryTitle = categoryTitles[category] || "Статистика";
  const availableCharts = categoryChartsData[category] || {};

  const handleChartSelection = (event) => {
    const { id, checked } = event.target;
    setSelectedCharts((prevSelectedCharts) => {
      if (checked) {
        return [...prevSelectedCharts, id];
      } else {
        return prevSelectedCharts.filter((chartId) => chartId !== id);
      }
    });
  };

  const handleShowStatistics = async () => {
    if (startDate && endDate) {
      try {
        // category из useParams — это строка, например 'fuel', 'taxes', ...
        // Для универсальности передаём массив category_ids
        const response = await apiService.getCategoryStatistics({
          category_ids: [category],
          start_date: startDate,
          end_date: endDate
        });
        setStatisticsData(response);
        setShowDownloadButton(true);
      } catch (error) {
        setStatisticsData({ error: 'Ошибка при получении статистики' });
        setShowDownloadButton(false);
      }
    } else {
      setShowDownloadButton(false);
      setStatisticsData(null);
    }
  };

  const handleDownloadStatistics = () => {
    if (statisticsData) {
      const blob = new Blob([JSON.stringify(statisticsData, null, 2)], { type: 'application/json' });
      const url = window.URL.createObjectURL(blob);
      const a = document.createElement('a');
      a.href = url;
      a.download = `statistics_${category}_${startDate}_${endDate}.json`;
      document.body.appendChild(a);
      a.click();
      document.body.removeChild(a);
      window.URL.revokeObjectURL(url);
    }
  };

  useEffect(() => {
    // Сброс кнопки скачивания и данных статистики при изменении категории или дат
    setShowDownloadButton(false);
    setStatisticsData(null);
    setSelectedCharts([]); // Сброс выбранных графиков при изменении категории
  }, [category, startDate, endDate]);

  return (
    <div className="category-statistics-page">
      <h2>Статистика: {currentCategoryTitle}</h2>

      <div className="date-range-container">
        <div className="date-inputs">
          <div className="date-input">
            <label>С:</label>
            <input
              type="date"
              value={startDate}
              onChange={(e) => setStartDate(e.target.value)}
            />
          </div>
          <div className="date-input">
            <label>По:</label>
            <input
              type="date"
              value={endDate}
              onChange={(e) => setEndDate(e.target.value)}
            />
          </div>
        </div>
        <button 
          className="show-statistics-btn"
          onClick={handleShowStatistics}
          disabled={!startDate || !endDate}
        >
          Показать ИИ рекомендации
        </button>
        {showDownloadButton && (
          <button 
            className="download-statistics-btn"
            onClick={handleDownloadStatistics}
          >
            Скачать статистику
          </button>
        )}
      </div>

      <div className="chart-selection-card">
        <h3>Выберите графики:</h3>
        <div className="chart-checkboxes">
          {Object.entries(availableCharts).map(([chartId, chartInfo]) => (
            <div key={chartId}>
              <input
                type="checkbox"
                id={chartId}
                checked={selectedCharts.includes(chartId)}
                onChange={handleChartSelection}
              />
              <label htmlFor={chartId}>{chartInfo.name}</label>
            </div>
          ))}
        </div>
      </div>

      {statisticsData && !statisticsData.error && (
        <div className="statistics-display-card">
          <h3>Статистика за выбранный период</h3>
          <p>Категория: <strong>{statisticsData.category || currentCategoryTitle}</strong></p>
          <p>Период: <strong>{statisticsData.period || `${startDate} - ${endDate}`}</strong></p>
          <p>Общая сумма: <strong>{statisticsData.totalAmount}</strong></p>
          {statisticsData.transactions && (
            <>
              <h4>Транзакции:</h4>
              <ul>
                {statisticsData.transactions.map((item, index) => (
                  <li key={index}>{item.date}: {item.amount} - {item.description}</li>
                ))}
              </ul>
            </>
          )}
        </div>
      )}
      {statisticsData && statisticsData.error && (
        <div className="statistics-display-card">
          <p style={{color: 'red'}}>{statisticsData.error}</p>
        </div>
      )}

      <div className="charts-grid">
        {selectedCharts.length > 0 ? (
          selectedCharts.map((chartId) => {
            const chartInfo = availableCharts[chartId];
            return chartInfo ? (
              <div key={chartId} className="chart-card">
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
            ) : null;
          })
        ) : (
          <p>Выберите графики для отображения.</p>
        )}
      </div>
    </div>
  );
};

export default CategoryStatisticsPage; 