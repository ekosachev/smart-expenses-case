import React, { useState } from 'react'
import reactLogo from './assets/react.svg'
import viteLogo from '/vite.svg'
import MileageChart from './components/MileageChart'
import CarUsageChart from './components/CarUsageChart'
import CircularProgressBar from './components/CircularProgressBar'
import Autopark from './components/Autopark'
import CarDetails from './components/CarDetails'
import './App.css'

function App() {
  const [currentPage, setCurrentPage] = useState('dashboard')
  const [selectedCarId, setSelectedCarId] = useState(null)

  const handleSelectCar = (carId) => {
    setSelectedCarId(carId)
    setCurrentPage('autopark') // Убедитесь, что мы на странице автопарка, чтобы отобразить детали
  }

  const handleBackToAutopark = () => {
    setSelectedCarId(null)
  }

  const renderContent = () => {
    switch (currentPage) {
      case 'dashboard':
        return (
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
                <div className="car-image-placeholder"></div>
                <h4>Mini Cooper</h4>
                <p>132k</p>
                <p>₽2500/ч</p>
              </div>
              <div className="car-card">
                <p>74% рекомендаций</p>
                <div className="car-image-placeholder"></div>
                <h4>Porsche 911 Carrera</h4>
                <p>130K</p>
                <p>₽2800/ч</p>
              </div>
              <div className="car-card">
                <p>74% рекомендаций</p>
                <div className="car-image-placeholder"></div>
                <h4>Porsche 911 Carrera</h4>
                <p>130K</p>
                <p>₽2800/ч</p>
              </div>
            </section>
          </>
        )
      case 'autopark':
        return selectedCarId !== null ? (
          <CarDetails carId={selectedCarId} onBack={handleBackToAutopark} />
        ) : (
          <Autopark onSelectCar={handleSelectCar} />
        )
      default:
        return null
    }
  }

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
            <li className={currentPage === 'dashboard' ? 'active' : ''} onClick={() => { setCurrentPage('dashboard'); setSelectedCarId(null); }}>
              <img src="/placeholder-dashboard.svg" alt="Дашборд Иконка" />
              <span>Дашборд</span>
            </li>
            <li className={currentPage === 'autopark' ? 'active' : ''} onClick={() => { setCurrentPage('autopark'); setSelectedCarId(null); }}>
              <img src="/placeholder-autopark.svg" alt="Автопарк Иконка" />
              <span>Автопарк</span>
            </li>
            <li>
              <img src="/placeholder-item.svg" alt="Иконка Продажи" />
              <span>Sell Cars</span>
            </li>
            <li>
              <img src="/placeholder-item.svg" alt="Иконка Покупки" />
              <span>Buy Cars</span>
            </li>
            <li>
              <img src="/placeholder-item.svg" alt="Иконка Услуг" />
              <span>Services</span>
            </li>
            <li>
              <img src="/placeholder-calendar.svg" alt="Календарь Иконка" />
              <span>Calendar</span>
            </li>
            <li>
              <img src="/placeholder-messages.svg" alt="Сообщения Иконка" />
              <span>Messages</span>
            </li>
          </ul>
        </nav>
        <div className="settings-logout">
          <ul>
            <li>
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

        {renderContent()}

      </main>
    </div>
  )
}

export default App
