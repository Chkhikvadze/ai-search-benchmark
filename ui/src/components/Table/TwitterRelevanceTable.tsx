import React from "react";
import Table from "./Table";
import { StyledHeader, StyledWrapper } from "./ProviderPerformanceTalble";

const TwitterRelevanceTable = () => {
  const data = React.useMemo(
    () => [
      {
        Provider: "Grok 2",
        "Summary Text Relevance": "96.67%",
        "Link Content Relevance": "27.14%",
        "Performance (s)": "8.86s",
        "Embedding Similarity": "77.92%",
      },
      {
        Provider: "Datura Nova 1.0",
        "Summary Text Relevance": "67.33%",
        "Link Content Relevance": "24.57%",
        "Performance (s)": "8.21s",
        "Embedding Similarity": "69.34%",
      },
      {
        Provider: "Datura Orbit 1.0",
        "Summary Text Relevance": "78.33%",
        "Link Content Relevance": "49.57%",
        "Performance (s)": "26.04s",
        "Embedding Similarity": "71.31%",
      },
    ],
    []
  );

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
      <Table columns={columns} data={data} />
    </StyledWrapper>
  );
};

export default TwitterRelevanceTable;
