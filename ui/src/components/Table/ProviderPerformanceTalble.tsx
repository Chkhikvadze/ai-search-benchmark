import React from "react";
import Table from "./Table";

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
        Header: "Link Title & Description Relevance",
        accessor: "Link Title & Description Relevance",
        sort: true,
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

  const data = React.useMemo(
    () => [
      {
        Provider: "Andi Search",
        "Summary Text Relevance": "23.75%",
        "Link Title & Description Relevance": "66.42%",
        "Performance (s)": "6.47s",
        "Embedding Similarity": "21.47%",
      },
      {
        Provider: "You.com",
        "Summary Text Relevance": "43.84%",
        "Link Title & Description Relevance": "65.07%",
        "Performance (s)": "1.69s",
        "Embedding Similarity": "57.07%",
      },
      {
        Provider: "OpenAI ChatGPT",
        "Summary Text Relevance": "92.05%",
        "Link Title & Description Relevance": "65.04%",
        "Performance (s)": "2.31s",
        "Embedding Similarity": "73.15%",
      },
      {
        Provider: "Perplexity",
        "Summary Text Relevance": "94.71%",
        "Link Title & Description Relevance": "63.85%",
        "Performance (s)": "5.61s",
        "Embedding Similarity": "75.38%",
      },
      {
        Provider: "Google Gemini",
        "Summary Text Relevance": "0.00%",
        "Link Title & Description Relevance": "0.00%",
        "Performance (s)": "0.00s",
        "Embedding Similarity": "0.00%",
      },
      {
        Provider: "Grok 2",
        "Summary Text Relevance": "0.00%",
        "Link Title & Description Relevance": "0.00%",
        "Performance (s)": "0.00s",
        "Embedding Similarity": "0.00%",
      },
      {
        Provider: "Datura Nova 1.0",
        "Summary Text Relevance": "88.15%",
        "Link Title & Description Relevance": "74.06%",
        "Performance (s)": "8.89s",
        "Embedding Similarity": "73.04%",
      },
      {
        Provider: "Datura Orbit 1.0",
        "Summary Text Relevance": "92.95%",
        "Link Title & Description Relevance": "76.00%",
        "Performance (s)": "18.92s",
        "Embedding Similarity": "72.97%",
      },
      {
        Provider: "Datura Horizon 1.0",
        "Summary Text Relevance": "0.00%",
        "Link Title & Description Relevance": "0.00%",
        "Performance (s)": "0.00s",
        "Embedding Similarity": "0.00%",
      },
    ],
    []
  );

  return <Table columns={columns} data={data} />;
};

export default ProviderPerformanceTable;
