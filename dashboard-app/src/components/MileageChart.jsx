import React from 'react';
import { BarChart, Bar, XAxis, YAxis, Tooltip, ResponsiveContainer } from 'recharts';

const CustomBar = (props) => {
  const { x, y, width, height, fill, payload } = props;
  if (payload.isLow) {
    return <rect x={x} y={y} width={width} height={height} fill="red" />;
  }
  return <rect x={x} y={y} width={width} height={height} fill={fill} />;
};

const MileageChart = ({ data }) => {
  return (
    <ResponsiveContainer width="100%" height={200}>
      <BarChart data={data} margin={{ top: 5, right: 0, left: 0, bottom: 5 }}>
        <XAxis dataKey="name" axisLine={false} tickLine={false} />
        <YAxis hide={true} />
        <Tooltip cursor={{ fill: 'transparent' }} />
        <Bar dataKey="uv" fill="#4facfe" barSize={20} radius={[5, 5, 0, 0]} isAnimationActive={true} animationEasing="ease-out" shape={<CustomBar />} />
      </BarChart>
    </ResponsiveContainer>
  );
};

export default MileageChart; 