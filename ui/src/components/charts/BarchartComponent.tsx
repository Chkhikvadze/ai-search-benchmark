import React from "react";
import {
  BarChart,
  Bar,
  XAxis,
  YAxis,
  CartesianGrid,
  Tooltip,
  ResponsiveContainer,
  Cell,
} from "recharts";
import Typography from "../Typography";
import { styled, useTheme } from "styled-components";
import { BAR_CHART_COLORS } from "./constants";

interface BarChartComponentProps {
  data: Array<{ name: string; value: number }>;
  title: string;
  yAxisDomain?: [number, number];
  tooltipText?: string;
  verticalLabels?: boolean; // Add the new prop
}

const BarChartComponent: React.FC<BarChartComponentProps> = ({
  data,
  title,
  yAxisDomain,
  tooltipText,
  verticalLabels = false, // Default to false
}) => {
  const theme = useTheme();

  return (
    <StyledContainer verticalLabels={verticalLabels}>
      <StyledTitleWrapper>
        <Typography kind="secondary" semibold tooltipText={tooltipText}>
          {title}
        </Typography>
      </StyledTitleWrapper>
      <ResponsiveContainer>
        <BarChart
          data={data}
          margin={{
            top: 20,
            bottom: verticalLabels ? 120 : 20,
          }}
          barCategoryGap="35%"
        >
          <CartesianGrid strokeWidth={0.2} vertical={false} />
          <XAxis
            dataKey="name"
            tick={{ fontSize: 12 }}
            interval={0}
            tickLine={false}
            angle={verticalLabels ? -45 : 0} // Rotate labels if verticalLabels is true
            textAnchor={verticalLabels ? "end" : "middle"} // Adjust text anchor
          />
          <YAxis domain={yAxisDomain} tick={{ fontSize: 12 }} />
          <Tooltip
            cursor={{ fill: theme.body.detailCardBackgroundColor }}
            contentStyle={{
              backgroundColor: theme.body.backgroundColorPrimary,
              borderRadius: "5px",
              border: `1px solid ${theme.body.secondaryBorderBackground}`,
            }}
            labelStyle={{
              color: theme.body.textColorSecondary,
              fontWeight: 500,
              fontSize: "14px",
            }}
            itemStyle={{
              color: theme.body.textColorPrimary,
              fontSize: "14px",
            }}
          />
          <Bar dataKey="value">
            {data.map((entry, index) => (
              <Cell
                key={`cell-${index}${entry}`}
                fill={BAR_CHART_COLORS[index % BAR_CHART_COLORS.length]}
              />
            ))}
          </Bar>
        </BarChart>
      </ResponsiveContainer>
    </StyledContainer>
  );
};

export default BarChartComponent;

const StyledContainer = styled.div<{ verticalLabels: boolean }>`
  width: 100%;
  height: ${({ verticalLabels }) => (verticalLabels ? "500px" : "350px")};

  display: flex;
  flex-direction: column;
  gap: 10px;

  margin-left: -35px;

  @media (max-width: 1080px) {
    margin-left: 0px;
  }
`;

const StyledTitleWrapper = styled.div`
  margin-left: 35px;

  @media (max-width: 1080px) {
    margin-left: 0px;
  }
`;
