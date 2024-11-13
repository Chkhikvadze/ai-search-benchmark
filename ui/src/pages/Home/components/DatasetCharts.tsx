import { styled } from "styled-components";
import categoryAreaPercentages from "../../../../../category_area_percentages.json";
import BarChartComponent from "../../../components/charts/BarchartComponent";
import {
  StyledHeader,
  StyledWrapper,
} from "../../../components/Table/ProviderPerformanceTable";
import PieChartComponent from "../../../components/charts/PieChartComponent";

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
  const barChartData = transformData(categoryAreaPercentages);
  const pieChartData = transformDataForPieChart(categoryAreaPercentages);

  return (
    <StyledWrapper>
      <StyledHeader>📂 Dataset Source</StyledHeader>

      <StyledRow>
        <StyledBarChartWrapper>
          <BarChartComponent
            data={barChartData}
            verticalLabels
            title="Areas"
            tooltipText="Category Area Percentages by Subcategory"
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
