import styled from "styled-components";
import TwitterRelevanceTable from "../../components/Table/TwitterRelevanceTable";
import ProviderPerformanceTable from "../../components/Table/ProviderPerformanceTable";
import BarChartComponent from "../../components/charts/BarchartComponent";
import webBenchmark from "../../../../docs/benchmark/4/web_benchmark.json";

const Home = () => {
  const data = webBenchmark.results_table
    .map((item) => ({
      name: item.Provider,
      value: parseFloat(item["Summary Text Relevance"]),
    }))
    .sort((a, b) => b.value - a.value); // Sort in descending order

  return (
    <StyledRoot>
      {/* <Typography>Home</Typography> */}
      <div>
        <BarChartComponent data={data} />
      </div>

      <TwitterRelevanceTable />

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
