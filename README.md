# 🚗 Smart Expenses Case

Smart Expenses Case — это современная платформа для управления и анализа расходов автопарка, которая экономит время, снижает издержки и обеспечивает прозрачность бизнес-процессов. Наше решение легко интегрируется, масштабируется и уже готово к промышленной эксплуатации.

---

## 🚀 Быстрый старт через Docker Compose

```bash
docker-compose up --build
```

---

## 📊 Описание

Платформа включает:
- Веб-интерфейс для мониторинга и аналитики автопарка
- Гибкую загрузку и обработку данных
- Интеграцию с REST API
- Разделение на фронтенд (`dashboard-app`) и бэкенд (`app`) для масштабируемости и надежности

---

## Ключевые неочевидные решения бэкенда

- **Динамические схемы Pydantic**  
  Автогенерация CRUD-схем для исключения дублирования кода.
- **Гибридное удаление**  
  Автоопределение soft/hard delete на основе модели.
- **Умный импорт данных**  
  Адаптивная обработка CSV/XLSX/JSON с автопреобразованием типов и созданием связей.

---

## Технологический стек (бэкенд)

- **Ядро:** Python 3.11, FastAPI, SQLAlchemy 2.0
- **База данных:** PostgreSQL
- **Инфраструктура:** Docker

---

## Фронтенд: современный и удобный интерфейс

- **Технологии:** React, Vite, Recharts, React Router
- **Возможности:**
  - Интерактивные графики и визуализация данных
  - Удобная навигация и адаптивный дизайн
  - Импорт/экспорт данных, drag-and-drop, мгновенная фильтрация
  - Модульная архитектура для легкой доработки

---

## Стилистика и фирменный стиль

- **Шрифт:** Onest Regular (кастомный, современный, легко читается)
- **Дизайн:**
  - Светлый, минималистичный интерфейс сделанный по предоставленному брендбуку
  - Четкие акценты для важных элементов
  - Современные иконки и плавные анимации

![Фирменный стиль](img/stilistic.png)

---

## Генерация и особенности данных

Для демонстрации возможностей используются синтетические, но реалистичные данные: расходы, характеристики и пробег автомобилей, а также бюджеты. Данные генерируются с учетом сезонности, случайных событий и связности между таблицами. Это позволяет сразу увидеть ценность платформы без необходимости интеграции с реальными системами.

---

## Примеры SQL-запросов для анализа данных

- Общие расходы по категориям за год:
`sql
SELECT c.name AS category, SUM(e.amount) AS total
FROM expenses e
JOIN categories c ON e.category_id = c.id
WHERE strftime('%Y', e.date) = '2024'
GROUP BY c.name
ORDER BY total DESC;
`

- Средний пробег по каждому автомобилю:
`sql
SELECT v.plate_number, v.manufacturer, v.model, v.total_mileage
FROM vehicles v
ORDER BY v.total_mileage DESC;
`

- Процент выполнения плана по бюджету:
`sql
SELECT * FROM monthly_budget WHERE Год = '2024' ORDER BY Процент_от_плана DESC;`


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

--- 

## Примечание

Все названия автомобилей и значения, отображаемые на дашборде, сгенерированы случайным образом и не отражают реальные данные. 