import React from 'react';
import { BarChart, Bar, XAxis, YAxis, Tooltip, ResponsiveContainer } from 'recharts';

const data = [
  { name: '13:00', uv: 100 },
  { name: '14:00', uv: 120 },
  { name: '15:00', uv: 157 },
  { name: '16:00', uv: 90 },
  { name: '17:00', uv: 110 },
  { name: '18:00', uv: 80 },
  { name: '19:00', uv: 60 },
];

const MileageChart = () => {
  return (
    <ResponsiveContainer width="100%" height={200}>
      <BarChart data={data} margin={{ top: 5, right: 0, left: 0, bottom: 5 }}>
        <XAxis dataKey="name" axisLine={false} tickLine={false} />
        <YAxis hide={true} />
        <Tooltip cursor={{ fill: 'transparent' }} />
        <Bar dataKey="uv" fill="#4facfe" barSize={20} radius={[5, 5, 0, 0]} isAnimationActive={true} animationEasing="ease-out" />
      </BarChart>
    </ResponsiveContainer>
  );
};

export default MileageChart; 