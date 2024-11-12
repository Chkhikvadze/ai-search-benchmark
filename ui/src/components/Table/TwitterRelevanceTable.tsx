import React from "react";
import Table from "./Table";
import { StyledHeader, StyledWrapper } from "./ProviderPerformanceTable";
import twitterBenchmark from "../../../../docs/benchmark/twitter_benchmark.json";

const TwitterRelevanceTable = () => {
  const columns = React.useMemo(
    () => [
      {
        Header: "Provider",
        accessor: "Provider",
        width: 150,
        minWidth: 150,
      },
      {
        Header: "Summary Text Relevance",
        accessor: "Summary Text Relevance",
        sort: true,
      },
      {
        Header: "Link Content Relevance",
        accessor: "Link Content Relevance",
        sort: true,
        defaultSort: "desc",
      },
      {
        Header: "Performance (s)",
        accessor: "Performance (s)",
        sort: true,
      },
      {
        Header: "Embedding Similarity",
        accessor: "Embedding Similarity",
        sort: true,
      },
    ],
    []
  );

  return (
    <StyledWrapper>
      <StyledHeader>🐦 Twitter Relevance Results</StyledHeader>
      <Table columns={columns} data={twitterBenchmark.results_table} />
    </StyledWrapper>
  );
};

export default TwitterRelevanceTable;
