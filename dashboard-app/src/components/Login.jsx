import React, { useState } from 'react';
import { useNavigate } from 'react-router-dom';
import './Login.css';

const Login = () => {
  const navigate = useNavigate();
  const [formData, setFormData] = useState({
    username: '',
    password: ''
  });
  const [errors, setErrors] = useState({});
  const [isLoading, setIsLoading] = useState(false);

  const handleInputChange = (e) => {
    const { name, value } = e.target;
    setFormData(prev => ({
      ...prev,
      [name]: value
    }));
    // Очищаем ошибку при вводе
    if (errors[name]) {
      setErrors(prev => ({
        ...prev,
        [name]: ''
      }));
    }
  };

  const validateForm = () => {
    const newErrors = {};

    if (!formData.username.trim()) {
      newErrors.username = 'Имя пользователя обязательно для заполнения';
    }

    if (!formData.password) {
      newErrors.password = 'Пароль обязателен для заполнения';
    }

    setErrors(newErrors);
    return Object.keys(newErrors).length === 0;
  };

  const handleSubmit = async (e) => {
    e.preventDefault();
    
    if (!validateForm()) {
      return;
    }

    setIsLoading(true);
    
    // Имитация отправки данных на сервер
    try {
      await new Promise(resolve => setTimeout(resolve, 1500));
      
      // Здесь будет реальная логика входа
      console.log('Данные для входа:', formData);
      
      // Перенаправляем на главную страницу после успешного входа
      navigate('/');
    } catch (error) {
      console.error('Ошибка при входе:', error);
    } finally {
      setIsLoading(false);
    }
  };

  const handleRegisterClick = () => {
    navigate('/register');
  };

  return (
    <div className="login-container">
      <div className="login-background">
        <div className="login-card">
          <div className="login-header">
            <div className="logo-section">
              <img src="/vite.svg" alt="Logo" className="logo-icon" />
              <h1>Smart Expenses</h1>
            </div>
            <p className="login-subtitle">Добро пожаловать обратно!</p>
          </div>

          <form onSubmit={handleSubmit} className="login-form">
            <div className="form-group">
              <label htmlFor="username">Имя пользователя</label>
              <input
                type="text"
                id="username"
                name="username"
                value={formData.username}
                onChange={handleInputChange}
                className={errors.username ? 'error' : ''}
                placeholder="Введите имя пользователя"
              />
              {errors.username && <span className="error-message">{errors.username}</span>}
            </div>

            <div className="form-group">
              <label htmlFor="password">Пароль</label>
              <input
                type="password"
                id="password"
                name="password"
                value={formData.password}
                onChange={handleInputChange}
                className={errors.password ? 'error' : ''}
                placeholder="Введите пароль"
              />
              {errors.password && <span className="error-message">{errors.password}</span>}
            </div>

            <div className="form-actions">
              <button 
                type="submit" 
                className="login-btn"
                disabled={isLoading}
              >
                {isLoading ? (
                  <div className="loading-spinner">
                    <div className="spinner"></div>
                    <span>Вход...</span>
                  </div>
                ) : (
                  'Войти'
                )}
              </button>
            </div>
          </form>

          <div className="register-link">
            <p>
              Нет аккаунта? 
              <button 
                type="button" 
                className="link-btn"
                onClick={handleRegisterClick}
              >
                Зарегистрироваться
              </button>
            </p>
          </div>

          <div className="login-features">
            <h3>Что вас ждет:</h3>
            <ul>
              <li>📊 Аналитика расходов в реальном времени</li>
              <li>🚗 Полное управление автопарком</li>
              <li>📈 Умное прогнозирование затрат</li>
              <li>🔔 Автоматические уведомления</li>
              <li>📱 Синхронизация с мобильным приложением</li>
            </ul>
          </div>
        </div>
      </div>
    </div>
  );
};

export default Login; 