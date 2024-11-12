from typing import TypedDict, List, Optional, Union, Dict
import os
import json
import logging


class SearchResult(TypedDict):
    title: Optional[str]
    url: str
    description: str


class ProviderResult(TypedDict):
    id: str
    question: str
    result: str
    search_results: List[SearchResult]
    response_time: int


WEB_PROVIDERS = {
    "name": "web",
    "files": {
        "datura_nova": "datura_nova_web_results.jsonl",
        "datura_orbit": "datura_orbit_web_results.jsonl",
        "datura_horizon": "datura_horizon_web_results.jsonl",
        "perplexity": "perplexity_ai_results.jsonl",
        "andi": "andi_search_result.jsonl",
        "chatgpt": "chatgpt_search_result.jsonl",
        "you": "you_results.jsonl",
        "gemini": "gemini_results.jsonl",
    },
    "table_order": [
        "andi",
        "you",
        "chatgpt",
        "perplexity",
        "gemini",
        "datura_nova",
        "datura_orbit",
        "datura_horizon",
    ],
}

TWITTER_PROVIDERS = {
    "name": "twitter",
    "files": {
        "datura_nova": "datura_nova_twitter_results.jsonl",
        "datura_orbit": "datura_orbit_twitter_results.jsonl",
        "datura_horizon": "datura_horizon_twitter_results.jsonl",
        "grok": "grok_search_result.jsonl",
    },
    "table_order": ["grok", "datura_nova", "datura_orbit", "datura_horizon"],
}


current_dir = os.path.dirname(os.path.abspath(__file__))


def load_questions_data():
    data_path = os.path.join(os.path.dirname(current_dir), "dataset", "data.jsonl")

    """Load JSONL data from the file and return as a list of dictionaries."""
    if not os.path.exists(data_path):
        logging.warning(f"Data file not found at {data_path}")
        return {}

    questions_map = {}

    with open(data_path, "r") as json_file:
        for line in json_file:
            try:
                item = json.loads(line)
                questions_map[item.get("question")] = item
            except json.JSONDecodeError as e:
                logging.error(f"Error decoding JSON: {e}")

    logging.info(f"Loaded {len(questions_map)} records from {data_path}")
    return questions_map


questions_map = load_questions_data()


def parse_generic(item):
    return {
        "id": item.get("id"),
        "question": item.get("question"),
        "summary": item.get("result"),
        "urls": [sr.get("url") for sr in item.get("search_results", [])],
        "response_time": item.get("response_time", 0),
        "search_results": item.get("search_results", []),
    }


def parse_provider(
    providers: dict[str, Union[Dict, List]], provider_with_least_results: str
):
    results = {}

    providers = providers["files"]

    # First, get the set of questions from perplexity
    ### Comment after full dataset
    perplexity_questions = set()
    perplexity_file_path = os.path.join(
        os.path.dirname(current_dir), "results", providers[provider_with_least_results]
    )

    with open(perplexity_file_path) as f:
        items = [json.loads(line) for line in f]
        perplexity_questions = {item["question"] for item in items}
    ###

    # Read and parse results from each provider
    for provider, filename in providers.items():
        results_file_path = os.path.join(
            os.path.dirname(current_dir), "results", filename
        )

        with open(results_file_path) as f:
            items = []
            for line in f:
                try:
                    item = json.loads(line)
                    items.append(item)
                except json.JSONDecodeError as e:
                    print("Error decoding line:", line)
            items = [item for item in items if item["question"] in perplexity_questions]
            items = sorted(items, key=lambda x: x["question"])
            items = items[:20]

            for item in items:
                parsed_item = parse_generic(item)

                if parsed_item:
                    id = parsed_item.get("id")
                    question = parsed_item.get("question")
                    summary = parsed_item.get("summary")
                    urls = parsed_item.get("urls")
                    response_time = parsed_item.get("response_time", 0)
                    search_results = parsed_item.get("search_results", [])

                    question_item = questions_map.get(question, {})

                    if question not in results:
                        results[question] = {
                            "id": id,
                            "question": question,
                            "expected_answer": question_item.get("expected_answer"),
                            "category": question_item.get("category"),
                            "area": question_item.get("area"),
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
    for provider in providers:
        provider_count = sum(
            1
            for q in results.values()
            if any(p["name"] == provider for p in q["providers"])
        )
        print(f"{provider}: {provider_count} questions")

    print("\nTotal unique questions:", len(results))
    print("Parsed results successfully!")

    return results


twitter_results = parse_provider(
    providers=TWITTER_PROVIDERS, provider_with_least_results="grok"
)

web_results = parse_provider(
    providers=WEB_PROVIDERS, provider_with_least_results="datura_nova"
)
