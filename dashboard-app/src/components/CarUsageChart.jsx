import React, { useState } from 'react';
import { AreaChart, Area, XAxis, YAxis, Tooltip, ResponsiveContainer } from 'recharts';

const CustomDot = (props) => {
  const { cx, cy, stroke, payload, onClick } = props;
  if (payload.isLow) {
    return (
      <circle
        cx={cx}
        cy={cy}
        r={8}
        fill="#F79023"
        stroke="#F79023"
        strokeWidth={2}
        cursor="pointer"
        onClick={() => onClick(payload, cx, cy)}
      />
    );
  }
  return (
    <circle cx={cx} cy={cy} r={3} fill={stroke} stroke={stroke} strokeWidth={1} />
  );
};

const CarUsageChart = ({ data }) => {
  const [showRecommendationButton, setShowRecommendationButton] = useState(false);
  const [buttonPosition, setButtonPosition] = useState({ x: 0, y: 0 });
  const [selectedLowPoint, setSelectedLowPoint] = useState(null);

  const handleDotClick = (payload, cx, cy) => {
    if (payload.isLow) {
      setShowRecommendationButton(true);
      setButtonPosition({ x: cx + 15, y: cy });
      setSelectedLowPoint(payload);
    } else {
      setShowRecommendationButton(false);
      setSelectedLowPoint(null);
    }
  };

  const handleShowAIRecommendations = () => {
    if (selectedLowPoint) {
      alert(`Получить ИИ рекомендации для ${selectedLowPoint.name} (значение: ${selectedLowPoint.uv})`);
      setShowRecommendationButton(false);
    }
  };

  return (
    <div style={{ position: 'relative', width: '100%', height: '200px' }}>
      <ResponsiveContainer width="100%" height="100%">
        <AreaChart
          data={data}
          margin={{
            top: 10,
            right: 0,
            left: 0,
            bottom: 0,
          }}
        >
          <XAxis dataKey="name" axisLine={false} tickLine={false} />
          <YAxis hide={true} />
          <Tooltip />
          <Area 
            type="monotone" 
            dataKey="uv" 
            stroke="#0165C0" 
            fill="url(#colorUv)" 
            fillOpacity={0.6} 
            isAnimationActive={true} 
            animationEasing="ease-out"
            dot={<CustomDot onClick={handleDotClick} />}
          />
          <defs>
            <linearGradient id="colorUv" x1="0" y1="0" x2="0" y2="1">
              <stop offset="5%" stopColor="#0165C0" stopOpacity={0.8} />
              <stop offset="95%" stopColor="#B6D9FC" stopOpacity={0} />
            </linearGradient>
          </defs>
        </AreaChart>
      </ResponsiveContainer>
      {showRecommendationButton && (
        <button
          className="show-ai-recommendations-btn"
          style={{
            position: 'absolute',
            left: buttonPosition.x,
            top: buttonPosition.y,
            transform: 'translateY(-50%)',
            zIndex: 100,
          }}
          onClick={handleShowAIRecommendations}
        >
          Показать ИИ рекомендации
        </button>
      )}
    </div>
  );
};

export default CarUsageChart; 