import React, { useState } from 'react'
import { Routes, Route, useNavigate, useParams, useLocation } from 'react-router-dom'
import reactLogo from './assets/react.svg'
import viteLogo from '/vite.svg'
import MileageChart from './components/MileageChart'
import CarUsageChart from './components/CarUsageChart'
import CircularProgressBar from './components/CircularProgressBar'
import Autopark from './components/Autopark'
import CarDetails from './components/CarDetails'
import Settings from './components/Settings'
import Calendar from './components/Calendar'
import Messages from './components/Messages'
import ChartsPage from './components/ChartsPage'
import CategoryStatisticsPage from './components/CategoryStatisticsPage'
import ApiTest from './components/ApiTest'
import Register from './components/Register'
import Login from './components/Login'
import FileUpload from './components/FileUpload'
import car1 from './img_cars/car1.png';
import car2 from './img_cars/car2.png';
import car3 from './img_cars/car3.png';
const car4 = car1;
const car5 = car2; 
const car6 = car3;
const car7 = car1;
const car8 = car2;
import fuelIcon from './assets/fuel.svg';
import taxesIcon from './assets/taxes.svg';
import repairIcon from './assets/repair.svg';
import otherIcon from './assets/other.svg';
import dashboardIcon from './assets/dashboard icon.svg';
import homeIcon from './assets/home.svg';
import messagesIcon from './assets/messages.svg';
import settingsIcon from './assets/settings.svg';
import signOutIcon from './assets/sign out.svg';
import notificationIcon from './assets/notification.svg';
import userOneIcon from './assets/user one.svg';
import linealDisplayIcon from './assets/lineal display.svg';
import paperClipIcon from './assets/paper clip attechment.svg';
import autoIcon from './assets/auto.svg';
import pprLogo from './assets/ppr logo.svg';
import './App.css'

function App() {
  const navigate = useNavigate();
  const [selectedMileagePeriod, setSelectedMileagePeriod] = useState('day');
  const [selectedUsagePeriod, setSelectedUsagePeriod] = useState('day');

  const handleSelectCar = (car) => {
    navigate(`/autopark/${car.id}`, { state: { carData: car } });
  };

  const handleBackToAutopark = () => {
    navigate('/autopark');
  };

  const handleWidgetClick = (category) => {
    navigate(`/statistics/${category}`);
  };

  const handleMileagePeriodChange = (period) => {
    setSelectedMileagePeriod(period);
  };

  const handleUsagePeriodChange = (period) => {
    setSelectedUsagePeriod(period);
  };

  const handleLogout = () => {
    localStorage.removeItem('token');
    navigate('/login');
  };

  const carImages = [car1, car2, car3];

  const mileageData = {
    day: [
      { name: '08:00', uv: 10 },
      { name: '10:00', uv: 15 },
      { name: '12:00', uv: 20 },
      { name: '14:00', uv: 3, isLow: true },
      { name: '16:00', uv: 18 },
      { name: '18:00', uv: 12 },
      { name: '20:00', uv: 8 },
    ],
    week: [
      { name: 'ПН', uv: 100 },
      { name: 'ВТ', uv: 120 },
      { name: 'СР', uv: 90 },
      { name: 'ЧТ', uv: 150 },
      { name: 'ПТ', uv: 110 },
      { name: 'СБ', uv: 180 },
      { name: 'ВС', uv: 130 },
    ],
    month: [
      { name: 'Нед 1', uv: 500 },
      { name: 'Нед 2', uv: 600 },
      { name: 'Нед 3', uv: 450 },
      { name: 'Нед 4', uv: 700 },
    ],
    year: [
      { name: 'Янв', uv: 2000 },
      { name: 'Фев', uv: 2200 },
      { name: 'Мар', uv: 1800 },
      { name: 'Апр', uv: 2500 },
      { name: 'Май', uv: 2300 },
      { name: 'Июн', uv: 2700 },
      { name: 'Июл', uv: 2400 },
      { name: 'Авг', uv: 2800 },
      { name: 'Сен', uv: 2100 },
      { name: 'Окт', uv: 2600 },
      { name: 'Ноя', uv: 2000 },
      { name: 'Дек', uv: 2900 },
    ],
  };

  const carUsageData = {
    day: [
      { name: '07:00', uv: 4000 },
      { name: '09:00', uv: 3000 },
      { name: '11:00', uv: 2000 },
      { name: '13:00', uv: 2780 },
      { name: '15:00', uv: 1890 },
      { name: '17:00', uv: 2390 },
      { name: '19:00', uv: 3490 },
      { name: '21:00', uv: 2500 },
    ],
    week: [
      { name: 'ПН', uv: 20000 },
      { name: 'ВТ', uv: 22000 },
      { name: 'СР', uv: 18000 },
      { name: 'ЧТ', uv: 25000 },
      { name: 'ПТ', uv: 21000 },
      { name: 'СБ', uv: 28000 },
      { name: 'ВС', uv: 23000 },
    ],
    month: [
      { name: 'Нед 1', uv: 80000 },
      { name: 'Нед 2', uv: 90000 },
      { name: 'Нед 3', uv: 5000, isLow: true },
      { name: 'Нед 4', uv: 95000 },
    ],
    year: [
      { name: 'Янв', uv: 300000 },
      { name: 'Фев', uv: 320000 },
      { name: 'Мар', uv: 280000 },
      { name: 'Апр', uv: 350000 },
      { name: 'Май', uv: 330000 },
      { name: 'Июн', uv: 370000 },
      { name: 'Июл', uv: 340000 },
      { name: 'Авг', uv: 380000 },
      { name: 'Сен', uv: 310000 },
      { name: 'Окт', uv: 360000 },
      { name: 'Ноя', uv: 300000 },
      { name: 'Дек', uv: 390000 },
    ],
  };

  const DashboardContent = () => {
    const problematicCars = [
      {
        id: 10,
        model: "Fiat Punto",
        recommendation: 25,
        status: "needs-repair", // 'needs-repair' or 'idle'
        image: carImages[3 % carImages.length], // Using car4 for Fiat Punto
        mileage: "180k",
        price: "₽1500/ч",
        type: "Хэтчбек"
      },
      {
        id: 11,
        model: "Volkswagen Golf",
        recommendation: 35,
        status: "idle", // 'needs-repair' or 'idle'
        image: carImages[4 % carImages.length], // Using car5 for VW Golf
        mileage: "150k",
        price: "₽1200/ч",
        type: "Хэтчбек"
      },
      {
        id: 12,
        model: "Opel Astra",
        recommendation: 15,
        status: "needs-repair", // 'needs-repair' or 'idle'
        image: carImages[5 % carImages.length], // Using car6 for Opel Astra
        mileage: "200k",
        price: "₽1000/ч",
        type: "Седан"
      },
    ];

    return (
      <>
        {/* Основные виджеты */}
        <section className="widgets-grid">
          <div className="widget fuel" onClick={() => handleWidgetClick('fuel')}> 
            <img src={fuelIcon} alt="Иконка Топлива" />
            <h3>Топливо</h3>
            <CircularProgressBar percentage={45} color="#4facfe" />
          </div>
          <div className="widget taxes" onClick={() => handleWidgetClick('taxes')}> 
            <img src={taxesIcon} alt="Иконка Налогов" />
            <h3>Налоги</h3>
            <CircularProgressBar percentage={50} color="#f06292" />
          </div>
          <div className="widget repair" onClick={() => handleWidgetClick('repair')}> 
            <img src={repairIcon} alt="Иконка Ремонта" />
            <h3>Ремонт</h3>
            <CircularProgressBar percentage={9} color="#a770ef" />
          </div>
          <div className="widget other" onClick={() => handleWidgetClick('other')}> 
            <img src={otherIcon} alt="Иконка Прочее" />
            <h3>Прочее</h3>
            <CircularProgressBar percentage={25} color="#ffd700" />
          </div>
        </section>

        {/* Статистика пробега */}
        <section className="mileage-stats">
          <h3>Статистика пробега</h3>
          <div className="time-filters">
            <button 
              className={selectedMileagePeriod === 'day' ? 'active' : ''}
              onClick={() => handleMileagePeriodChange('day')}
            >
              День
            </button>
            <button 
              className={selectedMileagePeriod === 'week' ? 'active' : ''}
              onClick={() => handleMileagePeriodChange('week')}
            >
              Неделя
            </button>
            <button 
              className={selectedMileagePeriod === 'month' ? 'active' : ''}
              onClick={() => handleMileagePeriodChange('month')}
            >
              Месяц
            </button>
            <button 
              className={selectedMileagePeriod === 'year' ? 'active' : ''}
              onClick={() => handleMileagePeriodChange('year')}
            >
              Год
            </button>
          </div>
          <div className="chart-placeholder">
            <MileageChart data={mileageData[selectedMileagePeriod]} />
          </div>
        </section>

        {/* Использование машин */}
        <section className="car-usage">
          <h3>Использование машин</h3>
          <div className="time-filters">
            <button 
              className={selectedUsagePeriod === 'day' ? 'active' : ''}
              onClick={() => handleUsagePeriodChange('day')}
            >
              День
            </button>
            <button 
              className={selectedUsagePeriod === 'week' ? 'active' : ''}
              onClick={() => handleUsagePeriodChange('week')}
            >
              Неделя
            </button>
            <button 
              className={selectedUsagePeriod === 'month' ? 'active' : ''}
              onClick={() => handleUsagePeriodChange('month')}
            >
              Месяц
            </button>
            <button 
              className={selectedUsagePeriod === 'year' ? 'active' : ''}
              onClick={() => handleUsagePeriodChange('year')}
            >
              Год
            </button>
          </div>
          <p className="date">20 Мая 2025</p>
          <div className="chart-placeholder">
            <CarUsageChart data={carUsageData[selectedUsagePeriod]} />
          </div>
        </section>

        {/* Рекомендации по автомобилям */}
        <section className="car-recommendations">
          {problematicCars.map(car => (
            <div className="car-card" key={car.id} onClick={() => handleSelectCar(car)}>
              <p className={car.recommendation <= 25 ? "recommendation-low-red" : (car.recommendation <= 50 ? "recommendation-low-yellow" : "")}>
                {car.recommendation}% рекомендаций
              </p>
              <div className="car-image-placeholder">
                <img src={car.image} alt={car.model} className="car-image-recommendation" />
              </div>
              <h4>{car.model}</h4>
              <p>{car.mileage}</p>
              <p>{car.price}</p>
            </div>
          ))}
        </section>
      </>
    );
  };

  const CarDetailsWrapper = () => {
    const { carId } = useParams();
    const location = useLocation();
    const car = location.state?.carData; // Get car data from location state
    return <CarDetails carId={carId} car={car} onBack={handleBackToAutopark} />;
  };

  return (
    <Routes>
      <Route path="/register" element={<Register />} />
      <Route path="/login" element={<Login />} />
      <Route path="/*" element={
        <div className="dashboard-container">
          <aside className="sidebar">
            {/* Боковая панель */}
            <div className="logo">
              <img src={pprLogo} alt="ППР Logo" />
              <span>ППР</span>
            </div>
            <nav className="nav-menu">
              <ul>
                <li onClick={() => navigate('/')}>
                  <img src={dashboardIcon} alt="Дашборд Иконка" />
                  <span>Дашборд</span>
                </li>
                <li onClick={() => navigate('/autopark')}>
                  <img src={autoIcon} alt="Автопарк Иконка" />
                  <span>Автопарк</span>
                </li>
                <li onClick={() => navigate('/calendar')}>
                  <img src={homeIcon} alt="Календарь Иконка" />
                  <span>Calendar</span>
                </li>
                <li onClick={() => navigate('/messages')}>
                  <img src={messagesIcon} alt="Сообщения Иконка" />
                  <span>Messages</span>
                </li>
                <li onClick={() => navigate('/api-test')}>
                  <img src={settingsIcon} alt="API Тест Иконка" />
                  <span>API Test</span>
                </li>
                <li onClick={() => navigate('/import')}>
                  <img src={paperClipIcon} alt="Импорт Иконка" />
                  <span>Импорт данных</span>
                </li>
              </ul>
            </nav>
            <div className="settings-logout">
              <ul>
                <li onClick={() => navigate('/settings')}>
                  <img src={settingsIcon} alt="Настройки Иконка" />
                  <span>Settings</span>
                </li>
                <li onClick={handleLogout}>
                  <img src={signOutIcon} alt="Выход Иконка" />
                  <span>Log out</span>
                </li>
              </ul>
            </div>
          </aside>
          <main className="main-content">
            {/* Верхний бар */}
            <header className="top-bar">
              <div className="search-bar">
                <input type="text" placeholder="Search or type" />
                <img src={otherIcon} alt="Иконка Поиска" />
              </div>
              <div className="user-profile">
                <img src={notificationIcon} alt="Иконка Уведомлений" />
                <img src={userOneIcon} alt="Иконка Пользователя" />
                <span></span> {/* Имя пользователя или другая информация */}
              </div>
            </header>

            <Routes>
              <Route path="/" element={<DashboardContent />} />
              <Route path="/autopark" element={<Autopark onSelectCar={handleSelectCar} />} />
              <Route path="/autopark/:carId" element={<CarDetailsWrapper />} />
              <Route path="/settings" element={<Settings />} />
              <Route path="/calendar" element={<Calendar />} />
              <Route path="/messages" element={<Messages />} />
              <Route path="/charts" element={<ChartsPage />} />
              <Route path="/statistics/:category" element={<CategoryStatisticsPage />} />
              <Route path="/api-test" element={<ApiTest />} />
              <Route path="/import" element={<FileUpload />} />
            </Routes>
          </main>
        </div>
      } />
    </Routes>
  )
}

export default App
