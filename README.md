# 🚗 Smart Expenses Case

## 🚀 Быстрый запуск через Docker Compose

```bash
docker-compose up --build
```

---

## 📊 Описание

Проект представляет собой современную платформу для анализа и управления расходами автопарка. Включает веб-интерфейс на React с визуализацией данных, загрузкой файлов, управлением пользователями и интеграцией с серверной частью через REST API. Архитектура разделена на фронтенд (`dashboard-app`) и бэкенд (`app`), что облегчает масштабирование и поддержку.

## Интересные приемы, использованные в коде

- **Анимация SVG прогресса с помощью requestAnimationFrame**  
  В компоненте [`CircularProgressBar`](dashboard-app/src/components/CircularProgressBar.jsx) реализована плавная анимация прогресса через [requestAnimationFrame](https://developer.mozilla.org/ru/docs/Web/API/window/requestAnimationFrame) и функцию сглаживания (ease-in-out quadratic). Это обеспечивает нативную и производительную анимацию без сторонних библиотек.

- **Гибкая работа с файлами через drag-and-drop и рефы**  
  В [`FileUpload`](dashboard-app/src/components/FileUpload.jsx) реализована поддержка drag-and-drop, динамическое отображение иконок файлов, а также сброс input через ref. Это повышает UX при импорте данных.

- **CSS-анимации и адаптивность**  
  Используются кастомные анимации появления элементов (`fadeIn`, `fadeInUp`) и адаптивные сетки на CSS Grid/Flexbox для плавного отображения на разных устройствах ([MDN: CSS Animations](https://developer.mozilla.org/ru/docs/Web/CSS/animation), [MDN: Flexbox](https://developer.mozilla.org/ru/docs/Web/CSS/CSS_Flexible_Box_Layout/Basic_Concepts_of_Flexbox)).

- **Пользовательские SVG-иконки и шрифты**  
  В проекте используются собственные SVG-иконки и кастомный шрифт Onest (см. раздел "Шрифты").

- **Прокрутка и виртуализация списков**  
  Для длинных списков сообщений и контактов применяется [overflow-y: auto](https://developer.mozilla.org/ru/docs/Web/CSS/overflow), что обеспечивает производительную прокрутку без лишних рендеров.

- **Модульная архитектура компонентов**  
  Каждый UI-блок (календарь, сообщения, загрузка файлов, графики) реализован как отдельный компонент, что облегчает тестирование и повторное использование.

## Неочевидные технологии и библиотеки

- Vite — основной сборщик фронтенда для быстрой разработки и HMR ([Vite](https://vitejs.dev/)).
- Recharts — визуализация данных ([Recharts](https://recharts.org/)).
- React Router v7 — современная маршрутизация ([React Router](https://reactrouter.com/en/main)).
- ESLint с плагинами для React Hooks и Fast Refresh ([eslint-plugin-react-hooks](https://www.npmjs.com/package/eslint-plugin-react-hooks), [eslint-plugin-react-refresh](https://www.npmjs.com/package/eslint-plugin-react-refresh)).
- Docker Compose — для локального развертывания ([`docker-compose.yml`](docker-compose.yml)).
- Кастомный шрифт Onest (различные начертания) из [`dashboard-app/src`](dashboard-app/src), а также Google Fonts: [Inter](https://fonts.google.com/specimen/Inter) (подключается через [`index.html`](dashboard-app/index.html)).

## Внешние библиотеки и ресурсы

- [React](https://react.dev/)
- [Vite](https://vitejs.dev/)
- [Recharts](https://recharts.org/)
- [React Router](https://reactrouter.com/)
- [ESLint](https://eslint.org/)
- [Onest (шрифт)](https://onest.design/)
- [Inter (шрифт)](https://fonts.google.com/specimen/Inter)

## Структура проекта

```
.
├── app/                # Бэкенд-приложение (FastAPI, Alembic, requirements.txt)
├── dashboard-app/      # Фронтенд на React + Vite
│   ├── src/
│   │   ├── assets/     # SVG-иконки и изображения интерфейса
│   │   ├── components/ # UI-компоненты (календарь, сообщения, графики и др.)
│   │   ├── img_cars/   # Изображения автомобилей
│   │   ├── services/   # API-сервисы для работы с сервером
│   │   └── ...         # Стили, шрифты, главные файлы приложения
│   ├── public/         # Публичные ассеты (если используются)
│   └── ...             # Конфиги, package.json, vite.config.js
├── create_test/        # Скрипты для генерации тестовых данных
├── expences.csv        # Основной датасет расходов
├── vehicles.csv        # Датасет по транспортным средствам
├── expenses_small.csv  # Пример небольшого датасета
├── test_data.json      # Тестовые данные для разработки
├── docker-compose.yml  # Docker Compose для локального запуска
└── ...                 # Прочие служебные файлы
```

### Описание интересных каталогов

- [`dashboard-app/src/components/`](dashboard-app/src/components/) — основные UI-компоненты, каждый реализует отдельную бизнес-функцию.
- [`dashboard-app/src/assets/`](dashboard-app/src/assets/) — SVG-иконки, используемые в интерфейсе.
- [`dashboard-app/src/img_cars/`](dashboard-app/src/img_cars/) — изображения автомобилей для визуализации автопарка.
- [`dashboard-app/src/services/`](dashboard-app/src/services/) — модули для работы с API.
- [`app/`](app/) — серверная часть на Python (FastAPI), миграции Alembic, зависимости.
- [`create_test/`](create_test/) — генерация и обработка тестовых данных.

--- 

## Примечание

Все названия автомобилей и значения, отображаемые на дашборде, сгенерированы случайным образом и не отражают реальные данные. 