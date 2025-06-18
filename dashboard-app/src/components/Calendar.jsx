import React, { useState } from 'react';
import './Calendar.css';

const Calendar = () => {
  // State for calendar logic
  const [currentMonth, setCurrentMonth] = useState(new Date(2022, 2, 1)); // March 2022 as per image
  const [activeDay, setActiveDay] = useState(16); // 16th March as per image
  const [activeView, setActiveView] = useState('month'); // 'month' or 'day'

  // Dummy data for events (you would fetch this from an API)
  const dailyEvents = [
    { time: '08:00 am', title: 'Moto Track Day', attendees: null, details: 'All Motorbikes', duration: null, value: '154K', color: '#8A2BE2' }, // Purple
    { time: '09:45 am', title: 'Drift Swries Second Round', attendees: null, details: 'JDM', duration: '1h 45 min', value: null, color: '#6A5ACD' }, // Darker Purple
    { time: '10:00 am', title: 'Moto Track Day', attendees: null, details: 'All Motorbikes', duration: null, value: '154K', color: '#4682B4' }, // Blue
    { time: '10:45 am', title: 'Moto Track Day', attendees: null, details: 'All Motorbikes', duration: null, value: '58K', color: '#F5F5F5' }, // Light Grey (for dashed)
    { time: '01:00 pm', title: 'Moto Track Day', attendees: null, details: 'All Motorbikes', duration: null, value: '145K', color: '#6BFCBA' }, // Светло-зеленый
    { time: '02:00 pm', title: 'Private Event', attendees: null, details: 'All Motorbikes', duration: null, value: '134K', color: '#FF6347' }, // Red-orange
    { time: '03:00 pm', title: null, attendees: null, details: null, duration: null, value: null, color: null }, // Empty slot
    { time: '03:45 pm', title: 'Drift Series Second Round', attendees: null, details: 'JDM', duration: null, value: '58K', color: '#F5F5F5' }, // Light Grey (for dashed)
  ];

  const upcomingEvents = [
    { time: '09:00', title: 'Drift Series Firs Round', type: 'JDM', users: ['/placeholder-user.svg', '/placeholder-user2.svg'], extraUsers: 8, color: '#8A2BE2' }, // Purple
    { time: '12:00', title: 'Drift Series Firs Round', type: 'JDM', users: ['/placeholder-user.svg', '/placeholder-user2.svg'], extraUsers: 5, color: '#6BFCBA' }, // Светло-зеленый
  ];

  const getDaysInMonth = (date) => {
    const year = date.getFullYear();
    const month = date.getMonth();
    return new Date(year, month + 1, 0).getDate();
  };

  const getFirstDayOfMonth = (date) => {
    const year = date.getFullYear();
    const month = date.getMonth();
    return new Date(year, month, 1).getDay(); // 0 for Sunday, 1 for Monday, etc.
  };

  const renderCalendarDays = () => {
    const daysInMonth = getDaysInMonth(currentMonth);
    const firstDay = getFirstDayOfMonth(currentMonth);
    const days = [];

    // Adjust firstDay to be 0 for Monday, 6 for Sunday if week starts on Monday
    const startDayOffset = (firstDay === 0) ? 6 : firstDay - 1;

    // Add empty cells for the days before the 1st of the month
    for (let i = 0; i < startDayOffset; i++) {
      days.push(<div key={`empty-${i}`} className="calendar-day empty"></div>);
    }

    // Add days of the month
    for (let i = 1; i <= daysInMonth; i++) {
      const isToday = currentMonth.getFullYear() === new Date().getFullYear() &&
                      currentMonth.getMonth() === new Date().getMonth() &&
                      i === new Date().getDate();
      const isActiveDay = i === activeDay && currentMonth.getMonth() === 2 && currentMonth.getFullYear() === 2022; // Hardcoding for Mar 16, 2022 from image

      days.push(
        <div
          key={i}
          className={`calendar-day ${isToday ? 'today' : ''} ${isActiveDay ? 'active' : ''}`}
          onClick={() => setActiveDay(i)}
        >
          {i}
        </div>
      );
    }
    return days;
  };

  const handlePrevMonth = () => {
    setCurrentMonth(prev => new Date(prev.getFullYear(), prev.getMonth() - 1, 1));
  };

  const handleNextMonth = () => {
    setCurrentMonth(prev => new Date(prev.getFullYear(), prev.getMonth() + 1, 1));
  };

  const monthNames = ["Январь", "Февраль", "Март", "Апрель", "Май", "Июнь", "Июль", "Август", "Сентябрь", "Октябрь", "Ноябрь", "Декабрь"];

  return (
    <div className="calendar-container">
      <h2>Calendar</h2>

      <div className="top-filters">
        <div className="dropdown">
          <span>Toyota</span>
          <img src="/placeholder-dropdown.svg" alt="Dropdown" />
        </div>
        <div className="dropdown">
          <span>Time</span>
          <img src="/placeholder-dropdown.svg" alt="Dropdown" />
        </div>
        <div className="dropdown">
          <span>Status</span>
          <img src="/placeholder-dropdown.svg" alt="Dropdown" />
        </div>
      </div>

      <div className="calendar-main-content">
        <div className="left-panel">
          <div className="calendar-header">
            <span className="month-year">{monthNames[currentMonth.getMonth()]} {currentMonth.getFullYear()}</span>
            <div className="nav-arrows">
              <button onClick={handlePrevMonth}>&lt;</button>
              <button onClick={handleNextMonth}>&gt;</button>
            </div>
          </div>
          <div className="calendar-controls">
            <button className="control-button">Week</button>
            <button className="control-button active">Month</button>
          </div>
          <div className="calendar-grid">
            <div className="calendar-weekdays">
              <div>Mon</div>
              <div>Tue</div>
              <div>Wed</div>
              <div>Thu</div>
              <div>Fri</div>
              <div>Sat</div>
              <div>Sun</div>
            </div>
            <div className="calendar-days">
              {renderCalendarDays()}
            </div>
          </div>

          <div className="upcoming-events">
            <h3>Upcoming Events</h3>
            <div className="events-list">
              {upcomingEvents.map((event, index) => (
                <div key={index} className="event-card" style={{ backgroundColor: event.color }}>
                  <div className="event-time">{event.time}</div>
                  <div className="event-details">
                    <div className="event-title">{event.title}</div>
                    <div className="event-type">{event.type}</div>
                  </div>
                  <div className="event-users">
                    {event.users.map((userImg, userIndex) => (
                      <img key={userIndex} src={userImg} alt="User" className="event-user-avatar" />
                    ))}
                    {event.extraUsers && <span className="extra-users">+{event.extraUsers}</span>}
                  </div>
                </div>
              ))}
              {/* Current time indicator - just for visual, not functional */}
              <div className="current-time-indicator" style={{ top: '50%' }}></div>
            </div>
          </div>
        </div>

        <div className="right-panel">
          <div className="daily-view-header">
            <div className="view-selector">
              <button className="day-button">Day</button>
              <img src="/placeholder-dropdown.svg" alt="Dropdown" />
            </div>
            <div className="date-navigation">
              <img src="/placeholder-calendar.svg" alt="Calendar Icon" className="calendar-icon" />
              <span>Mar 15, 2022</span>
              <button>&lt;</button>
              <button>&gt;</button>
            </div>
          </div>
          <div className="daily-schedule">
            {dailyEvents.map((event, index) => (
              <div key={index} className="schedule-item">
                <div className="time-slot">{event.time}</div>
                {event.title && (
                  <div className="event-block" style={{ backgroundColor: event.color }}>
                    {event.title && <div className="block-time-title">{event.time.split(' ')[0]}</div>}
                    {event.duration && <div className="block-duration">{event.duration}</div>}
                    {event.title && <div className="block-title">{event.title}</div>}
                    {event.details && <div className="block-details">{event.details}</div>}
                    {event.value && <div className="block-value">{event.value}</div>}
                  </div>
                )}
              </div>
            ))}
          </div>
        </div>
      </div>
    </div>
  );
};

export default Calendar; 