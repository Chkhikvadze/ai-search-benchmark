// src/components/charts/PieChartComponent.tsx

import React from "react";
import { PieChart, Pie, Cell, Tooltip, ResponsiveContainer } from "recharts";
import { styled, useTheme } from "styled-components";
import Typography from "../Typography";
import { BAR_CHART_COLORS } from "./constants";

type PieChartComponentProps = {
  data: Array<{ name: string; value: number }>;
  title: string;
  tooltipText?: string;
};

const PieChartComponent: React.FC<PieChartComponentProps> = ({
  data,
  title,
  tooltipText,
}) => {
  const theme = useTheme();

  return (
    <StyledContainer>
      <StyledTitleWrapper>
        <Typography kind="secondary" semibold tooltipText={tooltipText}>
          {title}
        </Typography>
      </StyledTitleWrapper>
      <ResponsiveContainer width="100%" height={400}>
        <PieChart>
          <Pie
            data={data}
            dataKey="value"
            nameKey="name"
            cx="50%"
            cy="50%"
            outerRadius={120}
            fontSize={10}
            label={({ name }) => name}
            stroke={"transparent"}
          >
            {data.map((entry, index) => (
              <Cell
                key={`cell-${index}-${entry.name}`}
                fill={BAR_CHART_COLORS[index % BAR_CHART_COLORS.length]}
              />
            ))}
          </Pie>

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
            formatter={(value: number) => `${value.toFixed(1)}%`}
          />
        </PieChart>
      </ResponsiveContainer>
    </StyledContainer>
  );
};

export default PieChartComponent;

const StyledContainer = styled.div`
  width: 100%;
  height: 400px;

  display: flex;
  flex-direction: column;
  gap: 10px;
`;

const StyledTitleWrapper = styled.div``;
