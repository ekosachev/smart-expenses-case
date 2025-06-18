import React, { useState } from 'react';
import { useNavigate } from 'react-router-dom';
import './Register.css';

const Register = () => {
  const navigate = useNavigate();
  const [formData, setFormData] = useState({
    username: '',
    password: '',
    confirmPassword: ''
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
    } else if (formData.username.length < 3) {
      newErrors.username = 'Имя пользователя должно содержать минимум 3 символа';
    }

    if (!formData.password) {
      newErrors.password = 'Пароль обязателен для заполнения';
    } else if (formData.password.length < 6) {
      newErrors.password = 'Пароль должен содержать минимум 6 символов';
    }

    if (formData.password !== formData.confirmPassword) {
      newErrors.confirmPassword = 'Пароли не совпадают';
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
      await new Promise(resolve => setTimeout(resolve, 2000));
      
      // Здесь будет реальная логика регистрации
      console.log('Данные для регистрации:', formData);
      
      // Перенаправляем на главную страницу после успешной регистрации
      navigate('/');
    } catch (error) {
      console.error('Ошибка при регистрации:', error);
    } finally {
      setIsLoading(false);
    }
  };

  const handleLoginClick = () => {
    navigate('/login');
  };

  return (
    <div className="register-container">
      <div className="register-background">
        <div className="register-card">
          <div className="register-header">
            <div className="logo-section">
              <img src="/src/assets/ppr logo.svg" alt="ППР Logo" className="logo-icon" />
              <h1>ППР</h1>
            </div>
            <p className="register-subtitle">Управление расходами на автопарк</p>
          </div>

          <form onSubmit={handleSubmit} className="register-form">
            <div className="form-group">
              <label htmlFor="username">Имя пользователя *</label>
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
              <label htmlFor="password">Пароль *</label>
              <input
                type="password"
                id="password"
                name="password"
                value={formData.password}
                onChange={handleInputChange}
                className={errors.password ? 'error' : ''}
                placeholder="Минимум 6 символов"
              />
              {errors.password && <span className="error-message">{errors.password}</span>}
            </div>

            <div className="form-group">
              <label htmlFor="confirmPassword">Подтвердите пароль *</label>
              <input
                type="password"
                id="confirmPassword"
                name="confirmPassword"
                value={formData.confirmPassword}
                onChange={handleInputChange}
                className={errors.confirmPassword ? 'error' : ''}
                placeholder="Повторите пароль"
              />
              {errors.confirmPassword && <span className="error-message">{errors.confirmPassword}</span>}
            </div>

            <div className="form-actions">
              <button 
                type="submit" 
                className="register-btn"
                disabled={isLoading}
              >
                {isLoading ? (
                  <div className="loading-spinner">
                    <div className="spinner"></div>
                    <span>Регистрация...</span>
                  </div>
                ) : (
                  'Зарегистрироваться'
                )}
              </button>
            </div>
          </form>

          <div className="login-link">
            <p>
              Уже есть аккаунт? 
              <button 
                type="button" 
                className="link-btn"
                onClick={handleLoginClick}
              >
                Войти
              </button>
            </p>
          </div>

          <div className="register-features">
            <h3>Преимущества регистрации:</h3>
            <ul>
              <li>📊 Детальная аналитика расходов</li>
              <li>🚗 Управление автопарком</li>
              <li>📈 Прогнозирование затрат</li>
              <li>🔔 Уведомления о ТО</li>
              <li>📱 Мобильное приложение</li>
            </ul>
          </div>
        </div>
      </div>
    </div>
  );
};

export default Register; 