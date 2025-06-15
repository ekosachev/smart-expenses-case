import React from 'react';
import { AreaChart, Area, XAxis, YAxis, Tooltip, ResponsiveContainer } from 'recharts';

const data = [
  { name: '07:00', uv: 4000, pv: 2400, amt: 2400 },
  { name: '09:00', uv: 3000, pv: 1398, amt: 2210 },
  { name: '11:00', uv: 2000, pv: 9800, amt: 2290 },
  { name: '13:00', uv: 2780, pv: 3908, amt: 2000 },
  { name: '15:00', uv: 1890, pv: 4800, amt: 2181 },
  { name: '17:00', uv: 2390, pv: 3800, amt: 2500 },
  { name: '19:00', uv: 3490, pv: 4300, amt: 2100 },
  { name: '21:00', uv: 2500, pv: 2400, amt: 2400 },
];

const CarUsageChart = () => {
  return (
    <ResponsiveContainer width="100%" height={200}>
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
        <Area type="monotone" dataKey="uv" stroke="#8884d8" fill="url(#colorUv)" fillOpacity={0.6} isAnimationActive={true} animationEasing="ease-out" />
        <defs>
          <linearGradient id="colorUv" x1="0" y1="0" x2="0" y2="1">
            <stop offset="5%" stopColor="#8884d8" stopOpacity={0.8} />
            <stop offset="95%" stopColor="#8884d8" stopOpacity={0} />
          </linearGradient>
        </defs>
      </AreaChart>
    </ResponsiveContainer>
  );
};

export default CarUsageChart; 