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
import { styled } from "styled-components";

interface BarChartComponentProps {
  data: Array<{ name: string; value: number }>;
  title: string;
  secondaryColor?: boolean;
  yAxisDomain?: [number, number];
}

const BarChartComponent: React.FC<BarChartComponentProps> = ({
  data,
  title,
  secondaryColor = false,
  yAxisDomain,
}) => {
  return (
    <StyledContainer>
      <StyledTitleWrapper>
        <Typography kind="secondary" bold>
          {title}
        </Typography>
      </StyledTitleWrapper>
      <ResponsiveContainer>
        <BarChart
          data={data}
          margin={{ top: 20, right: 30, left: 20, bottom: 50 }}
          barCategoryGap="35%" // Increase gap between bars
        >
          <CartesianGrid strokeWidth={0.2} vertical={false} />
          <XAxis
            dataKey="name"
            tick={{ fontSize: 12 }}
            interval={0}
            tickLine={false}
          />
          <YAxis
            domain={yAxisDomain}
            // ticks={[0, 10, 20, 30, 40, 50, 60, 70, 80, 90, 100]}
            tick={{ fontSize: 12 }}
          />
          <Tooltip />
          <Bar dataKey="value" fill={secondaryColor ? "#d1a41d" : "#4169E1"} />
        </BarChart>
      </ResponsiveContainer>
    </StyledContainer>
  );
};

export default BarChartComponent;

const StyledContainer = styled.div`
  width: 100%;
  height: 350px;

  display: flex;
  flex-direction: column;
  gap: 10px;
`;

const StyledTitleWrapper = styled.div`
  margin-left: 45px;
`;
