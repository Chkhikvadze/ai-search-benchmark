import BarChartComponent from "../../../components/charts/BarchartComponent";
import PieChartComponent from "../../../components/charts/PieChartComponent";

import Typography from "../../../components/Typography";

import { styled } from "styled-components";
import { StyledHeader } from "../../../components/Table/ProviderPerformanceTable";

import categoryAreaAmount from "../../../../../category_area_amounts.json";

import { datasetUrl } from "../../../constants";

type CategoryData = {
  [category: string]: {
    [subcategory: string]: number;
  };
};

const transformData = (data: CategoryData) => {
  const transformedData: Array<{ name: string; value: number }> = [];
  for (const category in data) {
    for (const subcategory in data[category]) {
      transformedData.push({
        name: `${category} - ${subcategory}`,
        value: data[category][subcategory],
      });
    }
  }
  return transformedData;
};

const transformDataForPieChart = (data: CategoryData) => {
  const transformedData: Array<{ name: string; value: number }> = [];
  for (const category in data) {
    const totalValue = Object.values(data[category]).reduce(
      (sum, value) => sum + value,
      0
    );
    transformedData.push({
      name: category,
      value: totalValue,
    });
  }
  return transformedData;
};

const DatasetCharts = () => {
  const barChartData = transformData(categoryAreaAmount);
  const pieChartData = transformDataForPieChart(categoryAreaAmount);

  return (
    <StyledWrapper>
      <div>
        <StyledHeader>📂 Dataset Source</StyledHeader>

        <StyledDescription>
          <Typography kind="secondary" size="medium">
            This visualization provides insights into the distribution of
            articles across various categories and subcategories.
          </Typography>
          <Typography kind="secondary" size="medium">
            You can see detailed dataset
            <a href={datasetUrl} target="_blank">
              here
            </a>
          </Typography>
        </StyledDescription>
      </div>

      <StyledRow>
        <StyledBarChartWrapper>
          <BarChartComponent
            data={barChartData}
            verticalLabels
            title="Areas"
            tooltipText="Category Area Amounts by Subcategory"
          />
        </StyledBarChartWrapper>

        <StyledPieChartWrapper>
          <PieChartComponent
            data={pieChartData}
            title="Categories"
            tooltipText="Summary of Knowledge and News Categories"
          />
        </StyledPieChartWrapper>
      </StyledRow>
    </StyledWrapper>
  );
};

export default DatasetCharts;

const StyledWrapper = styled.div`
  width: 100%;
  display: flex;
  flex-direction: column;

  gap: 32px;
`;

const StyledRow = styled.div`
  display: flex;
  flex-direction: row;
  gap: 50px;

  @media (max-width: 1200px) {
    flex-direction: column;
  }
`;

const StyledBarChartWrapper = styled.div`
  width: 70%;

  @media (max-width: 1200px) {
    width: 100%;
  }
`;

const StyledPieChartWrapper = styled.div`
  width: 30%;

  @media (max-width: 1200px) {
    width: 100%;
  }
`;

const StyledDescription = styled.div`
  width: 100%;

  margin-top: 16px;

  display: flex;
  flex-direction: column;
  gap: 12px;
`;
