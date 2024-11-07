from typing import TypedDict, List, Dict
import os
import json


class SearchResult(TypedDict):
    title: str
    url: str
    description: str


class ProviderResult(TypedDict):
    id: str
    question: str
    result: str
    search_results: List[SearchResult]
    response_time: int


PROVIDERS = {
    # "datura_nova": "datura_10_results.jsonl",
    # "datura_orbit": "datura_30_results.jsonl",
    # "datura_horizon": "datura_120_results.jsonl",
    "perplexity": "perplexity_ai_100_result.jsonl",
    # "andi": "andi_result.jsonl",
    # "chatgpt": "chatgpt_search_200_result.jsonl",
}

current_dir = os.path.dirname(os.path.abspath(__file__))


def parse_datura(item):
    result = item.get("result", "{}")

    data = []

    # Split the result by newlines and process each line
    for line in result.splitlines():
        line = line.strip()  # Remove leading/trailing whitespace

        if line.startswith("data: "):
            json_str = line[len("data: ") :].strip()  # Remove the prefix

            try:
                json_obj = json.loads(json_str)  # Parse the JSON
                data.append(json_obj)  # Collect the parsed JSON objects
            except json.JSONDecodeError:
                # Handle JSON parsing error if needed
                continue

    completion = data[-1].get("content") if data else None  # Get the last JSON object

    return {
        "id": item.get("id"),
        "question": item.get("question"),
        "summary": completion,
        "urls": item.get("srcs", []),
        "response_time": item.get("response_time", 0),
    }


def parse_generic(item):
    return {
        "id": item.get("id"),
        "question": item.get("question"),
        "summary": item.get("result"),
        "urls": [sr.get("url") for sr in item.get("search_results", [])],
        "response_time": item.get("response_time", 0),
        "search_results": item.get("search_results", []),
    }


results = {}

# Read and parse results from each provider
for provider, filename in PROVIDERS.items():
    results_file_path = os.path.join(os.path.dirname(current_dir), "results", filename)

    with open(results_file_path) as f:
        items = [json.loads(line) for line in f]
        items = sorted(items, key=lambda x: x["question"])
        items = items[:10]  # Adjust as needed

        for item in items:
            parsed_item = parse_generic(item)

            if parsed_item:
                id = parsed_item.get("id")
                question = parsed_item.get("question")
                summary = parsed_item.get("summary")
                urls = parsed_item.get("urls")
                response_time = parsed_item.get("response_time", 0)
                search_results = parsed_item.get("search_results", [])

                if question not in results:
                    results[question] = {
                        "id": id,
                        "question": question,
                        "providers": [],
                    }

                results[question]["providers"].append(
                    {
                        "name": provider,
                        "urls": urls,
                        "summary": summary,
                        "link_relevance": 0,  # Will be updated later
                        "summary_relevance": 0,
                        "embedding_relevance": 0,
                        "response_time": response_time,
                        "search_results": search_results,  # Include search_results
                    }
                )
