import React from "react";
import {
  BarChart,
  Bar,
  XAxis,
  YAxis,
  CartesianGrid,
  Tooltip,
  ResponsiveContainer,
} from "recharts";
import Typography from "../Typography";

interface BarChartComponentProps {
  data: Array<{ name: string; value: number }>;
}

const BarChartComponent: React.FC<BarChartComponentProps> = ({ data }) => {
  return (
    <div style={{ width: "40%", height: 300, position: "relative" }}>
      <Typography>Top Model Per Search Summary</Typography>
      <ResponsiveContainer>
        <BarChart
          data={data}
          margin={{ top: 20, right: 30, left: 20, bottom: 5 }}
        >
          <CartesianGrid strokeDasharray="3 3" />
          <XAxis dataKey="name" />
          <YAxis />
          <Tooltip />
          <Bar dataKey="value" fill="#8884d8" />
        </BarChart>
      </ResponsiveContainer>
    </div>
  );
};

export default BarChartComponent;
