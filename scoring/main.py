import asyncio
import json
import os

# from scoring.link_relevance import LinkRelevanceModel
from scoring.search_relevance import LinkRelevanceModel
from scoring.reward_llm import RewardLLM

# Read results file

PROVIDERS = {
    "datura_nova": "datura_10_results.jsonl",
    "datura_orbit": "datura_30_results.jsonl",
    "datura_horizon": "datura_120_results.jsonl",
    "perplexity": "perplexity_ai_result.jsonl",
    "andi": "andi_result.jsonl",
    "chatgpt": "chatgpt_search_200_result.jsonl",
}

current_dir = os.path.dirname(os.path.abspath(__file__))


# Define parsers for each provider
def parse_perplexity(item):
    return {
        "id": item.get("id"),
        "question": item.get("question"),
        "summary": item.get("result", {}).get("answerText"),
        "urls": item.get("result", {}).get("srcs", []),
    }


def parse_datura(item):
    # Placeholder for Datura parsing logic
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

    completion = (
        data[len(data) - 1].get("content") if data else None
    )  # Get the last JSON object

    return {
        "id": item.get("id"),
        "question": item.get("question"),
        "summary": completion,  # Updated to use the list of parsed data
        "urls": item.get("srcs", []),
    }


def parse_andi(item):
    # Placeholder for Andi parsing logic
    return {
        "id": item.get("id"),
        "question": item.get("question"),
        "summary": item.get("andi-answer"),
        "urls": item.get("andi-links", []),
    }


def parse_chatgpt(item):
    # Placeholder for ChatGPT parsing logic
    return {
        "id": item.get("id"),
        "question": item.get("question"),
        "summary": item.get("text"),
        "urls": item.get("sources", {}).get("searchResults", []),
    }


results = {}

sample_result = {
    "id": "Unique identifier for the query",
    "question": "The question posed to the search provider",
    "providers": [
        {
            "name": "Name of the search provider (Datura, Perplexity, etc.)",
            "urls": [
                "URL of the search result",
            ],
            "summary": "Summary of the search result",
            "link_relevance": 0,
            "summary_relevance": 0,
            "embedding_relevance": 0,
        }
    ],
}

# Read and parse results from each provider
for provider, filename in PROVIDERS.items():
    results_file_path = os.path.join(os.path.dirname(current_dir), "results", filename)
    with open(results_file_path) as f:
        items = [json.loads(line) for line in f]
        items = sorted(items, key=lambda x: x["question"])
        items = items[:10]

        for item in items:
            parsed_item = None

            if provider == "perplexity":
                parsed_item = parse_perplexity(item)
            elif (
                provider == "datura_nova"
                or provider == "datura_orbit"
                or provider == "datura_horizon"
            ):
                parsed_item = parse_datura(item)
            elif provider == "andi":
                parsed_item = parse_andi(item)
            elif provider == "chatgpt":
                parsed_item = parse_chatgpt(item)

            if parsed_item:
                id = parsed_item.get("id")
                question = parsed_item.get("question")
                summary = parsed_item.get("summary")
                urls = parsed_item.get("urls")

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
                        "link_relevance": 0,
                        "summary_relevance": 0,
                        "embedding_relevance": 0,
                    }
                )

# benchmark = [
#     {
#         "id": "Unique identifier for the query",
#         "question": "The question posed to the search provider",
#         "providers": [
#             {
#                 "name": "Name of the search provider (Datura, Perplexity, etc.)",
#                 "link_relevance": "Link relevance score",
#                 "summary_relevance": "Summary relevance score",
#                 "embedding_relevance": "Embedding relevance score",
#                 "results": [
#                     {
#                         "title": "Title of the search result",
#                         "url": "URL of the search result",
#                         "description": "Description of the search result",
#                     }
#                 ],
#             },
#         ],
#     },
# ]


async def main():
    reward_llm = RewardLLM()

    link_relevance_model = LinkRelevanceModel(
        llm_reward=reward_llm,
    )

    for _, item in results.items():
        prompt = item.get("question")
        providers = item.get("providers", [])

        await link_relevance_model.get_rewards(prompt, providers)

        # Perform scoring for each provider
        # summary_relevance = summary_relevance_model.get_rewards(prompt, summary)
        # embedding_relevance = embedding_relevance_model.get_rewards(prompt, summary)

    # write file
    output_file_path = os.path.join(
        os.path.dirname(current_dir), "results", "benchmark.jsonl"
    )

    with open(output_file_path, "w") as f:
        for result in results.values():
            f.write(json.dumps(result) + "\n")


asyncio.run(main())
