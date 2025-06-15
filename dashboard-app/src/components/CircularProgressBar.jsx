import React, { useEffect, useState } from 'react';

const CircularProgressBar = ({ percentage, color }) => {
  const radius = 40;
  const circumference = 2 * Math.PI * radius;
  const [progress, setProgress] = useState(0);

  useEffect(() => {
    const targetProgress = (percentage / 100) * circumference;
    let start = null;
    const duration = 1000; // Анимация длится 1 секунду

    const animate = (timestamp) => {
      if (!start) start = timestamp;
      const progressTime = timestamp - start;
      const easedProgress = easeInOutQuad(progressTime, 0, 1, duration); // Используем функцию сглаживания
      const currentProgress = easedProgress * targetProgress;

      setProgress(currentProgress);

      if (progressTime < duration) {
        requestAnimationFrame(animate);
      }
    };

    requestAnimationFrame(animate);

    // Функция сглаживания (ease-in-out quadratic)
    function easeInOutQuad(t, b, c, d) {
      t /= d / 2;
      if (t < 1) return c / 2 * t * t + b;
      t--;
      return -c / 2 * (t * (t - 2) - 1) + b;
    }

  }, [percentage, circumference]);

  return (
    <svg width="100" height="100" viewBox="0 0 100 100">
      <circle
        stroke="#e0e0e0"
        fill="transparent"
        strokeWidth="8"
        r={radius}
        cx="50"
        cy="50"
      />
      <circle
        stroke={color}
        fill="transparent"
        strokeWidth="8"
        strokeDasharray={circumference}
        strokeDashoffset={circumference - progress}
        r={radius}
        cx="50"
        cy="50"
        strokeLinecap="round"
        style={{
          transition: 'stroke-dashoffset 0.0s linear', // Анимация управляется через requestAnimationFrame
        }}
      />
      <text
        x="50%"
        y="50%"
        dy=".3em"
        textAnchor="middle"
        fontSize="20px"
        fill="#333"
      >
        {Math.round((progress / circumference) * 100)}%
      </text>
    </svg>
  );
};

export default CircularProgressBar; 