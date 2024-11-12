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
    .sort((a, b) => b.value - a.value)
    .slice(0, 5); // Show first 5 items

  const data2 = webBenchmark.results_table
    .map((item) => ({
      name: item.Provider,
      value: parseFloat(item["Link Content Relevance"]),
    }))
    .sort((a, b) => b.value - a.value)
    .slice(0, 5);

  const data3 = twitterBenchmark.results_table
    .map((item) => ({
      name: item.Provider,
      value: parseFloat(item["Link Content Relevance"]),
    }))
    .sort((a, b) => b.value - a.value)
    .slice(0, 5);

  const data4 = webBenchmark.results_table
    .map((item) => ({
      name: item.Provider,
      value: parseFloat(item["Embedding Similarity"]),
    }))
    .sort((a, b) => b.value - a.value)
    .slice(0, 5);

  const data5 = webBenchmark.results_table
    .map((item) => ({
      name: item.Provider,
      value: parseFloat(item["Performance (s)"]),
    }))
    .sort((a, b) => a.value - b.value) // Sort in ascending order
    .slice(0, 5); // Show first 5 items

  return (
    <StyledChartContainer>
      <BarChartComponent
        data={data}
        title="Top Model Per Search Summary"
        yAxisDomain={[0, 100]}
      />
      <BarChartComponent
        data={data2}
        title="Best Model Per Web Link Content Relevance"
        yAxisDomain={[0, 100]}
      />
      <BarChartComponent
        data={data3}
        title="Top Models Per Twitter Content"
        yAxisDomain={[0, 100]}
      />
      <BarChartComponent
        data={data4}
        title="Best Model Embedding Similarity"
        yAxisDomain={[0, 100]}
      />
      <BarChartComponent
        secondaryColor
        data={data5}
        title="Lowest Latency (TTFT)"
      />
    </StyledChartContainer>
  );
};

export default Charts;

const StyledChartContainer = styled.div`
  display: grid;
  grid-template-columns: repeat(2, 1fr);
  gap: 20px;
  width: 100%;
`;
