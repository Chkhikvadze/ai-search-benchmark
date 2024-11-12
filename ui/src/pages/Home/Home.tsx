import styled from "styled-components";
import TwitterRelevanceTable from "../../components/Table/TwitterRelevanceTable";
import ProviderPerformanceTable from "../../components/Table/ProviderPerformanceTalble";
import BarChartComponent from "../../components/charts/BarchartComponent";
import { webBenchmark } from "../../components/Table/constants";

const Home = () => {
  const data = webBenchmark.results_table.map((item) => ({
    name: item.Provider,
    value: parseFloat(item["Summary Text Relevance"]),
  }));

  return (
    <StyledRoot>
      {/* <Typography>Home</Typography> */}

      <TwitterRelevanceTable />

      <div>
        <BarChartComponent data={data} />
      </div>

      <ProviderPerformanceTable />
    </StyledRoot>
  );
};

export default Home;

const StyledRoot = styled.div`
  width: 100%;
  height: 100%;

  padding: 20px;

  overflow-y: auto;

  display: flex;
  flex-direction: column;
  gap: 100px;
`;
