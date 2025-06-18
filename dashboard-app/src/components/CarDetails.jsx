import React, { useState } from 'react';
import { AreaChart, Area, XAxis, YAxis, Tooltip, ResponsiveContainer } from 'recharts';
import { useNavigate } from 'react-router-dom';

const activityData = [
  { name: '01/6', km: 30 },
  { name: '02/6', km: 40 },
  { name: '03/6', km: 25 },
  { name: '04/6', km: 55 },
  { name: '05/6', km: 35 },
  { name: '06/6', km: 50 },
  { name: '07/6', km: 45 },
  { name: '08/6', km: 60 },
  { name: '09/6', km: 40 },
  { name: '10/6', km: 30 },
  { name: '11/6', km: 20 },
  { name: '12/6', km: 10 },
];

const CarDetails = ({ carId, car }) => {
  // Используйте carId для получения данных о конкретном автомобиле
  // Пока заглушка
  const carInfo = {
    model: car ? car.model : "Porsche 718 Cayman S",
    fuelConsumption: "8,2 л / 100 км",
    mileage: "58 760 км",
    cost: "₽3 000 000",
    rent: "₽3.2K",
  };

  const [selectedSensors, setSelectedSensors] = useState(['fuel-consumed']); // Initialize with 'fuel-consumed' as it's checked by default in the original code
  const [startDate, setStartDate] = useState('');
  const [endDate, setEndDate] = useState('');
  const [showDownloadButton, setShowDownloadButton] = useState(false);
  const [statisticsData, setStatisticsData] = useState(null); // Добавляем состояние для данных статистики
  const navigate = useNavigate();

  const handleSensorChange = (event) => {
    const { id, checked } = event.target;
    setSelectedSensors((prevSelectedSensors) => {
      if (checked) {
        return [...prevSelectedSensors, id];
      } else {
        return prevSelectedSensors.filter((sensorId) => sensorId !== id);
      }
    });
  };

  const sensorsList = [
    { id: 'fuel-consumed', name: 'Asset - Fuel Consumed (10)' },
    { id: 'odometer', name: 'Asset - Odometer (km)' },
    { id: 'runtime', name: 'Asset - Runtime (km)' },
    { id: 'speed', name: 'Asset - Speed (hr)' },
    { id: 'engine-temp', name: 'Engine Temperature (deg C)' },
  ];

  const handleSeeAllClick = () => {
    localStorage.setItem('selectedSensorsForCharts', JSON.stringify(selectedSensors));
    navigate('/charts');
  };

  const handleShowStatistics = () => {
    if (startDate && endDate) {
      // Генерируем фиктивные данные статистики на основе дат
      const dummyStatistics = {
        carModel: carInfo.model,
        period: `${startDate} - ${endDate}`,
        fuelConsumption: `${Math.floor(Math.random() * 10) + 5} л / 100 км`, // Динамический расход
        mileage: `${Math.floor(Math.random() * 100000) + 10000} км`, // Динамический пробег
        recommendations: [
          "Проверьте давление в шинах для оптимального расхода топлива.",
          "Рассмотрите плановое ТО к концу выбранного периода.",
          "Рекомендуется провести диагностику двигателя для выявления аномалий."
        ],
        // Добавьте другие динамические данные статистики, если нужно
      };
      setStatisticsData(dummyStatistics);
      setShowDownloadButton(true);
    } else {
      setStatisticsData(null);
      setShowDownloadButton(false);
    }
  };

  const handleDownloadStatistics = () => {
    if (statisticsData) { // Используем данные из состояния
      const blob = new Blob([JSON.stringify(statisticsData, null, 2)], { type: 'application/json' });
      const url = window.URL.createObjectURL(blob);
      const a = document.createElement('a');
      a.href = url;
      a.download = `statistics_${carInfo.model}_${startDate}_${endDate}.json`;
      document.body.appendChild(a);
      a.click();
      document.body.removeChild(a);
      window.URL.revokeObjectURL(url);
    } else {
      alert("Нет данных для скачивания. Пожалуйста, сначала покажите ИИ рекомендации.");
    }
  };

  return (
    <div className="car-details-page">
      <h2>Автопарк/{carInfo.model}</h2>

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

      {statisticsData && (
        <div className="statistics-display-card">
          <h3>ИИ Рекомендации и Статистика за выбранный период</h3>
          <p>Модель автомобиля: <strong>{statisticsData.carModel}</strong></p>
          <p>Период: <strong>{statisticsData.period}</strong></p>
          <p>Расход топлива: <strong>{statisticsData.fuelConsumption}</strong></p>
          <p>Пробег: <strong>{statisticsData.mileage}</strong></p>
          {statisticsData.recommendations && statisticsData.recommendations.length > 0 && (
            <>
              <h4>Рекомендации:</h4>
              <ul>
                {statisticsData.recommendations.map((rec, index) => (
                  <li key={index}>{rec}</li>
                ))}
              </ul>
            </>
          )}
        </div>
      )}

      <div className="car-overview-grid">
        <div className="car-stats-card">
          <div className="stat-item">
            <h4>Расход топлива</h4>
            <span>{carInfo.fuelConsumption}</span>
          </div>
          <div className="stat-item">
            <h4>Пробег</h4>
            <span>{carInfo.mileage}</span>
          </div>
          <div className="stat-item">
            <h4>Стоимость</h4>
            <span>{carInfo.cost}</span>
          </div>
          <div className="stat-item">
            <h4>Аренда</h4>
            <span>{carInfo.rent}</span>
          </div>
        </div>

        <div className="car-image-large">
          <img src={car ? car.image : "/placeholder-large-car.svg"} alt={carInfo.model} />
        </div>

        <div className="car-activity-card">
          <h3>Активность</h3>
          <p className="driven-today">Проехано в этот день</p>
          <span className="today-km">50 км</span>
          <ResponsiveContainer width="100%" height={150}>
            <AreaChart data={activityData} margin={{ top: 10, right: 0, left: 0, bottom: 0 }}>
              <XAxis dataKey="name" axisLine={false} tickLine={false} />
              <YAxis hide={true} />
              <Tooltip />
              <Area type="monotone" dataKey="km" stroke="#0165C0" fill="url(#colorActivity)" fillOpacity={0.6} isAnimationActive={true} animationEasing="ease-out" />
              <defs>
                <linearGradient id="colorActivity" x1="0" y1="0" x2="0" y2="1">
                  <stop offset="5%" stopColor="#0165C0" stopOpacity={0.8} />
                  <stop offset="95%" stopColor="#B6D9FC" stopOpacity={0} />
                </linearGradient>
              </defs>
            </AreaChart>
          </ResponsiveContainer>
        </div>
      </div>

      <div className="car-additional-info-grid">
        <div className="event-log-card">
          <h3>Журнал событий</h3>
          <div className="event-item">
            <div className="event-icon"><img src="/placeholder-message-circle.svg" alt="Message"/></div>
            <div className="event-content">
              <p className="event-date">Понедельник, 7 апреля 2025</p>
              <p className="event-description">Машина записана на плановое ТО</p>
              <span className="event-status">Завершено</span>
            </div>
          </div>
          <div className="event-item">
            <div className="event-icon warning"><img src="/placeholder-alert-circle.svg" alt="Warning"/></div>
            <div className="event-content">
              <p className="event-date">Четверг, 20 марта 2025</p>
              <p className="event-description">Требуется ремонт по отзыву LV 001</p>
              <span className="event-link">14:07-22/05/2025</span>
            </div>
          </div>
          <div className="event-item">
            <div className="event-icon"><img src="/placeholder-tool.svg" alt="Tool"/></div>
            <div className="event-content">
              <p className="event-date">Вторник, 13 августа 2024</p>
              <p className="event-description">Техническое обслуживание завершено</p>
              <span className="event-link">15:17-13/08/2024</span>
            </div>
          </div>
        </div>

        <div className="available-sensors-card">
          <h3>Доступные датчики</h3>
          <div className="sensor-filter">
            <button>Активны <img src="/placeholder-chevron-down.svg" alt="Dropdown"/></button>
          </div>
          <div className="sensor-list">
            {sensorsList.map((sensor) => (
              <div className="sensor-item" key={sensor.id}>
                <input
                  type="checkbox"
                  id={sensor.id}
                  checked={selectedSensors.includes(sensor.id)}
                  onChange={handleSensorChange}
                />
                <label htmlFor={sensor.id}>{sensor.name}</label>
                <img src="/placeholder-line-chart.svg" alt="Chart" />
              </div>
            ))}
          </div>
          <button className="see-all-btn" onClick={handleSeeAllClick}>See All</button>
        </div>

        <div className="reminder-card">
          <h3>Reminder</h3>
          <button className="add-new-btn">+ Add New</button>
          <table className="reminder-table">
            <thead>
              <tr>
                <th>Description</th>
                <th>Due</th>
                <th>Overdue</th>
                <th>Notify</th>
                <th>Status</th>
              </tr>
            </thead>
            <tbody>
              <tr>
                <td>Urgent Safety Recall</td>
                <td>06/04/2022</td>
                <td>08/04/2022</td>
                <td>David Demo</td>
                <td className="status-completed">Completed</td>
              </tr>
              <tr>
                <td>Urgent Safety Recall</td>
                <td>06/04/2022</td>
                <td>08/04/2022</td>
                <td>David Demo</td>
                <td className="status-completed">Completed</td>
              </tr>
            </tbody>
          </table>
        </div>
      </div>
    </div>
  );
};

export default CarDetails; 