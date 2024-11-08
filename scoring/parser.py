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
    "datura_nova": "datura_10_results_2.jsonl",
    "datura_orbit": "datura_30_results_2.jsonl",
    # "datura_horizon": "datura_120_results.jsonl",
    "perplexity": "perplexity_ai_results.jsonl",
    "andi": "andi_search_result.jsonl",
    "chatgpt": "chatgpt_search_200_result.jsonl",
    "you": "you_results.jsonl",
}


current_dir = os.path.dirname(os.path.abspath(__file__))


def parse_datura_results(type, data):
    standardized_results = []

    if type == "search":
        for result in data.get("organic_results", []):
            standardized_results.append(
                {
                    "title": result.get("title"),
                    "url": result.get("link"),
                    "description": result.get("snippet"),
                }
            )
    elif "arxiv_search" in data:
        for result in data:
            standardized_results.append(
                {
                    "title": result.get("title"),
                    "link": result.get("url"),
                    "snippet": result.get("snippet"),
                }
            )
    elif "hacker_news_search" in data:
        for result in data:
            standardized_results.append(
                {
                    "title": result.get("title"),
                    "link": result.get("url"),
                    "snippet": result.get("snippet"),
                }
            )
    else:
        pass
        # print(f"Parse datura results unknown type: {type}")

    return standardized_results


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

    search_results = []

    for chunk in data:
        type = chunk.get("type")
        content = chunk.get("content")
        results = parse_datura_results(type, content)
        search_results.extend(results)

    completion = next(
        (d.get("content") for d in data if d.get("type") == "completion"), ""
    )

    # Extract text after **Summary**
    summary_start = completion.find("Summary:**")
    summary_text = None

    if summary_start != -1:
        summary_text = completion[summary_start + len("Summary:**") :].strip()

    return {
        "id": item.get("id"),
        "question": item.get("question"),
        "summary": summary_text,
        "urls": [sr.get("url") for sr in search_results],
        "response_time": item.get("response_time", 0),
        "search_results": search_results,
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


# First, get the set of questions from perplexity
### Comment after full dataset
perplexity_questions = set()
perplexity_file_path = os.path.join(
    os.path.dirname(current_dir), "results", PROVIDERS["chatgpt"]
)

with open(perplexity_file_path) as f:
    items = [json.loads(line) for line in f]
    perplexity_questions = {item["question"] for item in items[:200]}
###

# Read and parse results from each provider
for provider, filename in PROVIDERS.items():
    results_file_path = os.path.join(os.path.dirname(current_dir), "results", filename)

    with open(results_file_path) as f:
        # items = [json.loads(line) for line in f]
        # items = sorted(items, key=lambda x: x["question"])
        # items = items[:10]  # Adjust as needed

        ### Comment after full dataset
        items = [json.loads(line) for line in f]
        items = [item for item in items if item["question"] in perplexity_questions]
        items = sorted(items, key=lambda x: x["question"])
        ###

        for item in items:
            parsed_item = None

            if provider.startswith("datura"):
                parsed_item = parse_datura(item)
            else:
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


# Print some statistics
for provider in PROVIDERS:
    provider_count = sum(
        1
        for q in results.values()
        if any(p["name"] == provider for p in q["providers"])
    )
    print(f"{provider}: {provider_count} questions")

print("\nTotal unique questions:", len(results))
print("Parsed results successfully!")


# find item with providers length == 3
for question, data in results.items():
    if len(data.get("providers", [])) == 1:
        print(question)
        break
