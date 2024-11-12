import { styled } from "styled-components";
import BarChartComponent from "../../../components/charts/BarchartComponent";
import webBenchmark from "../../../../../docs/benchmark/4/web_benchmark.json";
import twitterBenchmark from "../../../../../docs/benchmark/4/twitter_benchmark.json";

const Charts = () => {
  const data = webBenchmark.results_table
    .map((item) => ({
      name: item.Provider,
      value: parseFloat(item["Summary Text Relevance"]),
    }))
    .sort((a, b) => a.value - b.value)
    .slice(-5); // Show first 5 items

  const data2 = webBenchmark.results_table
    .map((item) => ({
      name: item.Provider,
      value: parseFloat(item["Link Content Relevance"]),
    }))
    .sort((a, b) => a.value - b.value)
    .slice(-5);

  const data3 = twitterBenchmark.results_table
    .map((item) => ({
      name: item.Provider,
      value: parseFloat(item["Link Content Relevance"]),
    }))
    .sort((a, b) => a.value - b.value)
    .slice(-5);

  const data4 = webBenchmark.results_table
    .map((item) => ({
      name: item.Provider,
      value: parseFloat(item["Embedding Similarity"]),
    }))
    .sort((a, b) => a.value - b.value)
    .slice(-5);

  const data5 = webBenchmark.results_table
    .map((item) => ({
      name: item.Provider,
      value: parseFloat(item["Performance (s)"]),
    }))
    .sort((a, b) => b.value - a.value) // Sort in ascending order
    .slice(-5); // Show first 5 items

  return (
    <>
      <StyledContainer>
        <StyledTitle>Top Search AI Providers</StyledTitle>
        <StyledChartContainer>
          <BarChartComponent
            data={data}
            title="Best in Search Summary"
            yAxisDomain={[0, 100]}
          />
          <BarChartComponent
            data={data2}
            title="Best in Web Link Content Relevance"
            yAxisDomain={[0, 100]}
          />
          <BarChartComponent
            data={data3}
            title="Best in Twitter Content Relevance"
            yAxisDomain={[0, 100]}
          />
          <BarChartComponent
            data={data4}
            title="Best in Embedding Similarity"
            yAxisDomain={[0, 100]}
          />
        </StyledChartContainer>
      </StyledContainer>

      <StyledContainer>
        <StyledTitle>Fastest and Most Affordable Providers</StyledTitle>
        <StyledChartContainer>
          <BarChartComponent data={data5} title="Lowest Latency (TTFT)" />
        </StyledChartContainer>
      </StyledContainer>
    </>
  );
};

export default Charts;

const StyledContainer = styled.div`
  display: flex;
  flex-direction: column;
  gap: 38px;

  width: 100%;
`;

const StyledChartContainer = styled.div`
  display: grid;
  grid-template-columns: repeat(2, 1fr);
  gap: 20px;
  width: 100%;

  @media (max-width: 1080px) {
    grid-template-columns: repeat(1, 1fr);
  }
`;

const StyledTitle = styled.h1`
  font-size: 30px;
  color: ${({ theme }) => theme.body.textColorPrimary};

  margin-left: 45px;
`;
