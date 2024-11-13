import { styled } from "styled-components";
import categoryAreaPercentages from "../../../../../category_area_percentages.json";
import BarChartComponent from "../../../components/charts/BarchartComponent";
import {
  StyledHeader,
  StyledWrapper,
} from "../../../components/Table/ProviderPerformanceTable";

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

const DatasetCharts = () => {
  const data = transformData(categoryAreaPercentages);

  return (
    <StyledWrapper>
      <StyledHeader>📂 Dataset Source</StyledHeader>

      <StyledRow>
        <BarChartComponent
          data={data}
          verticalLabels
          title="📈 Areas"
          tooltipText="Percentage of each subcategory"
        />
      </StyledRow>
    </StyledWrapper>
  );
};

export default DatasetCharts;

const StyledRow = styled.div`
  display: flex;
  flex-direction: row;
  gap: 20px;
`;
