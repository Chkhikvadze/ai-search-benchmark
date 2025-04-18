import asyncio
import json
import os
from parser import (
    TWITTER_PROVIDERS,
    WEB_PROVIDERS,
    web_results,
    twitter_results,
)
from reward_llm import RewardLLM
from link_relevance import LinkRelevanceModel
from summary_relevance import SummaryRelevanceModel
from chart import generate_charts

llm_reward = RewardLLM()

link_relevance_model = LinkRelevanceModel(llm_reward)
summary_relevance_model = SummaryRelevanceModel(llm_reward)

current_dir = os.path.dirname(os.path.abspath(__file__))

CONCURRENT_TASKS = 5  # Adjust this value as needed


async def process_question(semaphore, question, data):
    async with semaphore:
        prompt = question
        providers = data.get("providers", [])
        expected_answer = data.get("expected_answer")

        # Prepare results in the expected format
        results_list = []
        for provider_data in providers:
            result = {
                "urls": provider_data.get("urls", []),
                "search_results": provider_data.get("search_results", []),
                "summary": provider_data.get("summary", ""),
                "link_relevance": 0,  # Will be updated
                "summary_relevance": 0,  # Will be updated
                "embedding_relevance": 0,  # Will be updated
                "expected_answer_relevance": 0,  # Will be updated
            }
            results_list.append(result)

        # Call get_rewards to compute link_relevance and summary_relevance
        await link_relevance_model.get_rewards(prompt, results_list)
        await summary_relevance_model.get_rewards(prompt, expected_answer, results_list)
        # await expected_answer_relevance_model.get_rewards(expected_answer, results_list)

        # Update provider_data with computed link_relevance and summary_relevance
        for i, provider_data in enumerate(providers):
            provider_data["link_relevance"] = results_list[i].get("link_relevance", 0)
            provider_data["summary_relevance"] = results_list[i].get(
                "summary_relevance", 0
            )
            provider_data["embedding_relevance"] = results_list[i].get(
                "embedding_relevance", 0
            )
            provider_data["expected_answer_relevance"] = results_list[i].get(
                "expected_answer_relevance", 0
            )


async def compute_relevance(results):
    semaphore = asyncio.Semaphore(CONCURRENT_TASKS)  # Limit concurrent tasks
    tasks = [
        process_question(semaphore, question, data)
        for question, data in results.items()
    ]
    await asyncio.gather(*tasks)


provider_display_names = {
    "andi": "Andi Search",
    "you": "You.com",
    "chatgpt": "OpenAI ChatGPT",
    "perplexity": "Perplexity",
    "gemini": "Google Gemini",
    "grok": "Grok 2",
    "datura_nova": "Desearch Nova 1.0",
    "datura_orbit": "Desearch Orbit 1.0",
    "datura_horizon": "Desearch Horizon 1.0",
}


async def score_results(results, provider):
    await compute_relevance(results)

    # Collect provider stats
    provider_stats = {}

    for item in results.values():
        providers = item.get("providers", [])
        for provider_data in providers:
            provider_name = provider_data.get("name")
            if provider_name not in provider_stats:
                provider_stats[provider_name] = {
                    "link_relevance_total": 0,
                    "summary_relevance_total": 0,
                    "embedding_relevance_total": 0,
                    "expected_answer_relevance_total": 0,
                    "response_time_total": 0,
                    "num_questions": 0,
                }
            provider_stats[provider_name]["link_relevance_total"] += provider_data.get(
                "link_relevance", 0
            )
            provider_stats[provider_name][
                "summary_relevance_total"
            ] += provider_data.get("summary_relevance", 0)
            provider_stats[provider_name][
                "embedding_relevance_total"
            ] += provider_data.get("embedding_relevance", 0)
            provider_stats[provider_name][
                "expected_answer_relevance_total"
            ] += provider_data.get("expected_answer_relevance", 0)
            provider_stats[provider_name]["response_time_total"] += provider_data.get(
                "response_time", 0
            )
            provider_stats[provider_name]["num_questions"] += 1

    # Calculate averages
    for provider_name, stats in provider_stats.items():
        num_questions = stats["num_questions"]
        stats["link_relevance_avg"] = (
            stats["link_relevance_total"] / num_questions if num_questions else 0
        )
        stats["summary_relevance_avg"] = (
            stats["summary_relevance_total"] / num_questions if num_questions else 0
        )
        stats["embedding_relevance_avg"] = (
            stats["embedding_relevance_total"] / num_questions if num_questions else 0
        )
        stats["expected_answer_relevance_avg"] = (
            stats["expected_answer_relevance_total"] / num_questions
            if num_questions
            else 0
        )
        stats["response_time_avg"] = (
            stats["response_time_total"] / num_questions if num_questions else 0
        )

    # Map provider names to display names and products

    providers_order = provider["table_order"]

    table_entries = []

    for provider_name in providers_order:
        display_name = provider_display_names.get(provider_name, provider_name)

        stats = provider_stats.get(
            provider_name,
            {
                "link_relevance_avg": 0,
                "summary_relevance_avg": 0,
                "embedding_relevance_avg": 0,
                "expected_answer_relevance_avg": 0,
                "response_time_avg": 0,
            },
        )
        entry = {
            "Provider": display_name,
            "Summary Text Relevance": f"{stats['summary_relevance_avg'] * 100:.2f}%",
            "Link Content Relevance": f"{stats['link_relevance_avg'] * 100:.2f}%",
            "Performance (s)": f"{stats['response_time_avg']:.2f}s",
            "Embedding Similarity": f"{stats['embedding_relevance_avg'] * 100:.2f}%",
            "Expected Answer Relevance": f"{stats['expected_answer_relevance_avg'] * 100:.2f}%",
        }
        table_entries.append(entry)

    # Generate Markdown content
    md_content = "## 📊 Results Table\n\n"
    md_content += "Below is a table showcasing the results of each provider in various aspects of our scoring mechanism:\n\n"
    md_content += "| Provider            | Summary Text Relevance | Link Content Relevance             | Performance (s)  | Embedding Similarity   | Expected Answer Relevance \n"
    md_content += "|---------------------|------------------------|------------------------------------|------------------|------------------------|---------------------------\n"

    prev_display_name = None

    for entry in table_entries:
        provider_cell = entry["Provider"]
        if provider_cell == prev_display_name:
            provider_cell = ""
        else:
            prev_display_name = provider_cell
        md_content += f"| {provider_cell:<19} | {entry['Summary Text Relevance']:<22} | {entry['Link Content Relevance']:<34} | {entry['Performance (s)']:<16} | {entry['Embedding Similarity']:<22} | {entry['Expected Answer Relevance']:<25} |\n"

    # Write Markdown file
    md_file_path = os.path.join(
        os.path.dirname(current_dir),
        "docs/benchmark",
        f"{provider.get("name")}_benchmark.md",
    )

    with open(md_file_path, "w") as f:
        f.write(md_content)

    # Write JSON file
    json_output = {
        "results_table": table_entries,
        "provider_stats": provider_stats,
    }

    output_file_path = os.path.join(
        os.path.dirname(current_dir),
        "docs/benchmark",
        f"{provider.get("name")}_benchmark.json",
    )

    with open(output_file_path, "w") as f:
        json.dump(json_output, f, indent=2)

    # Generate performance chart
    generate_charts(provider_stats, provider.get("name"), provider_display_names)

    print("Benchmark results have been written to the Markdown and JSON files.")


# Run the asynchronous function
asyncio.run(score_results(twitter_results, TWITTER_PROVIDERS))
asyncio.run(score_results(web_results, WEB_PROVIDERS))
