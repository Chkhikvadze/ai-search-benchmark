import React from "react";
import Table from "./Table";
import { styled } from "styled-components";
import webBenchmark from "../../../../docs/benchmark/4/web_benchmark.json";

const ProviderPerformanceTable = () => {
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
      <StyledHeader>📊 Performance Comparison</StyledHeader>
      <Table columns={columns} data={webBenchmark.results_table} />
    </StyledWrapper>
  );
};

export default ProviderPerformanceTable;

export const StyledWrapper = styled.div`
  width: 100%;
  display: flex;
  flex-direction: column;
  text-align: center;
  gap: 32px;
`;

export const StyledHeader = styled.h1`
  font-size: 30px;
  font-weight: 700;
  color: ${({ theme }) => theme.body.textColorSecondary};
`;
