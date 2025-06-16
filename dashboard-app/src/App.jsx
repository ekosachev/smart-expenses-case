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
import car1 from './img_cars/2014-mercedes-benz-m-class-2012-mercedes-benz-m-class-2008-mercedes-benz-m-class-sport-utility-vehicle-mercedes-car-png-image-8230b0372dd015bcf5312eb17e2751ee-1.png';
import car2 from './img_cars/car-audi-a3-audi-a4-car-3822c2bc08e2c2bce1d8ead0e70c7ddb-1.png';
import car3 from './img_cars/maruti-suzuki-dzire-car-suzuki-ertiga-swift-dzire-f8a7d4ae19bd1c349dc080d9081ffd31.png';
import car4 from './img_cars/suzuki-ertiga-maruti-car-suzuki-ciaz-suzuki-dcac04d3f676c91c7ca6f2d195b86ff3.png';
import car5 from './img_cars/toyota-innova-toyota-avanza-car-rush-toyota-seven-cars-a3650fca54041ac1aaae4fe013ac79ca 1.png';
import car6 from './img_cars/white car.png';
import car7 from './img_cars/2014-mercedes-benz-m-class-2012-mercedes-benz-m-class-2008-mercedes-benz-m-class-sport-utility-vehicle-mercedes-car-png-image-8230b0372dd015bcf5312eb17e2751ee.png';
import car8 from './img_cars/car-audi-a3-audi-a4-car-3822c2bc08e2c2bce1d8ead0e70c7ddb.png';
import './App.css'

function App() {
  const navigate = useNavigate();

  const handleSelectCar = (car) => {
    navigate(`/autopark/${car.id}`, { state: { carData: car } });
  };

  const handleBackToAutopark = () => {
    navigate('/autopark');
  };

  const carImages = [car1, car2, car3, car4, car5, car6, car7, car8];

  const DashboardContent = () => (
    <>
      {/* Основные виджеты */}
      <section className="widgets-grid">
        <div className="widget fuel">
          <img src="/placeholder-fuel.svg" alt="Иконка Топлива" />
          <h3>Топливо</h3>
          <CircularProgressBar percentage={45} color="#4facfe" />
        </div>
        <div className="widget taxes">
          <img src="/placeholder-taxes.svg" alt="Иконка Налогов" />
          <h3>Налоги</h3>
          <CircularProgressBar percentage={50} color="#f06292" />
        </div>
        <div className="widget repair">
          <img src="/placeholder-repair.svg" alt="Иконка Ремонта" />
          <h3>Ремонт</h3>
          <CircularProgressBar percentage={9} color="#a770ef" />
        </div>
        <div className="widget other">
          <img src="/placeholder-other.svg" alt="Иконка Прочее" />
          <h3>Прочее</h3>
          <CircularProgressBar percentage={25} color="#ffd700" />
        </div>
      </section>

      {/* Статистика пробега */}
      <section className="mileage-stats">
        <h3>Статистика пробега</h3>
        <div className="time-filters">
          <button className="active">День</button>
          <button>Неделя</button>
          <button>Месяц</button>
        </div>
        <div className="chart-placeholder">
          <MileageChart />
        </div>
      </section>

      {/* Использование машин */}
      <section className="car-usage">
        <h3>Использование машин</h3>
        <div className="time-filters">
          <button className="active">День</button>
          <button>Неделя</button>
          <button>Месяц</button>
        </div>
        <p className="date">20 Мая 2025</p>
        <div className="chart-placeholder">
          <CarUsageChart />
        </div>
      </section>

      {/* Рекомендации по автомобилям */}
      <section className="car-recommendations">
        <div className="car-card">
          <p>64% рекомендаций</p>
          <div className="car-image-placeholder">
            <img src={carImages[0]} alt="Mini Cooper" className="car-image-recommendation" />
          </div>
          <h4>Mini Cooper</h4>
          <p>132k</p>
          <p>₽2500/ч</p>
        </div>
        <div className="car-card">
          <p>74% рекомендаций</p>
          <div className="car-image-placeholder">
            <img src={carImages[1 % carImages.length]} alt="Porsche 911 Carrera" className="car-image-recommendation" />
          </div>
          <h4>Porsche 911 Carrera</h4>
          <p>130K</p>
          <p>₽2800/ч</p>
        </div>
        <div className="car-card">
          <p>74% рекомендаций</p>
          <div className="car-image-placeholder">
            <img src={carImages[2 % carImages.length]} alt="Porsche 911 Carrera" className="car-image-recommendation" />
          </div>
          <h4>Porsche 911 Carrera</h4>
          <p>130K</p>
          <p>₽2800/ч</p>
        </div>
      </section>
    </>
  );

  const CarDetailsWrapper = () => {
    const { carId } = useParams();
    const location = useLocation();
    const car = location.state?.carData; // Get car data from location state
    return <CarDetails carId={carId} car={car} onBack={handleBackToAutopark} />;
  };

  return (
    <div className="dashboard-container">
      <aside className="sidebar">
        {/* Боковая панель */}
        <div className="logo">
          <img src="/placeholder-logo.svg" alt="Motiv. Logo" />
          <span>Motiv.</span>
        </div>
        <nav className="nav-menu">
          <ul>
            <li onClick={() => navigate('/')}>
              <img src="/placeholder-dashboard.svg" alt="Дашборд Иконка" />
              <span>Дашборд</span>
            </li>
            <li onClick={() => navigate('/autopark')}>
              <img src="/placeholder-autopark.svg" alt="Автопарк Иконка" />
              <span>Автопарк</span>
            </li>
            <li onClick={() => navigate('/calendar')}>
              <img src="/placeholder-calendar.svg" alt="Календарь Иконка" />
              <span>Calendar</span>
            </li>
            <li onClick={() => navigate('/messages')}>
              <img src="/placeholder-messages.svg" alt="Сообщения Иконка" />
              <span>Messages</span>
            </li>
          </ul>
        </nav>
        <div className="settings-logout">
          <ul>
            <li onClick={() => navigate('/settings')}>
              <img src="/placeholder-settings.svg" alt="Настройки Иконка" />
              <span>Settings</span>
            </li>
            <li>
              <img src="/placeholder-logout.svg" alt="Выход Иконка" />
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
            <img src="/placeholder-search.svg" alt="Иконка Поиска" />
          </div>
          <div className="user-profile">
            <img src="/placeholder-bell.svg" alt="Иконка Уведомлений" />
            <img src="/placeholder-user.svg" alt="Иконка Пользователя" />
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
        </Routes>

      </main>
    </div>
  )
}

export default App
