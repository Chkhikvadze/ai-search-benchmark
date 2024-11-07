import asyncio
import json
import os
from scoring.parser import results
from scoring.reward_llm import RewardLLM
from scoring.link_relevance import LinkRelevanceModel
from scoring.summary_relevance import SummaryRelevanceModel

llm_reward = RewardLLM()

link_relevance_model = LinkRelevanceModel(llm_reward)
summary_relevance_model = SummaryRelevanceModel(llm_reward)

current_dir = os.path.dirname(os.path.abspath(__file__))


async def compute_relevance():
    for question, data in results.items():
        prompt = question
        providers = data.get("providers", [])

        # Prepare results in the expected format
        results_list = []
        for provider_data in providers:
            result = {
                "urls": provider_data.get("urls", []),
                "search_results": provider_data.get("search_results", []),
                "summary": provider_data.get("summary", ""),
                "link_relevance": 0,  # Will be updated
                "summary_relevance": 0,  # Will be updated
            }
            results_list.append(result)

        # Call get_rewards to compute link_relevance
        await link_relevance_model.get_rewards(prompt, results_list)
        # Call get_rewards to compute summary_relevance
        await summary_relevance_model.get_rewards(prompt, results_list)

        # Update provider_data with computed link_relevance and summary_relevance
        for i, provider_data in enumerate(providers):
            provider_data["link_relevance"] = results_list[i].get("link_relevance", 0)
            provider_data["summary_relevance"] = results_list[i].get(
                "summary_relevance", 0
            )


# Run the asynchronous function
asyncio.run(compute_relevance())

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
                "response_time_total": 0,
                "num_questions": 0,
            }
        provider_stats[provider_name]["link_relevance_total"] += provider_data.get(
            "link_relevance", 0
        )
        provider_stats[provider_name]["summary_relevance_total"] += provider_data.get(
            "summary_relevance", 0
        )
        provider_stats[provider_name]["embedding_relevance_total"] += provider_data.get(
            "embedding_relevance", 0
        )
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
    stats["response_time_avg"] = (
        stats["response_time_total"] / num_questions if num_questions else 0
    )

# Map provider names to display names and products
provider_display_names = {
    "andi": ("Andi Search", "-"),
    "you": ("You.com", "-"),
    "chatgpt": ("OpenAI ChatGPT", "-"),
    "perplexity": ("Perplexity", "-"),
    "google_gemini": ("Google Gemini", "-"),
    "datura_nova": ("Datura", "Nova 1.0"),
    "datura_orbit": ("Datura", "Orbit 1.0"),
    "datura_horizon": ("Datura", "Horizon 1.0"),
}

# Prepare table entries
providers_order = [
    "andi",
    "you",
    "chatgpt",
    "perplexity",
    "google_gemini",
    "datura_nova",
    "datura_orbit",
    "datura_horizon",
]

table_entries = []

for provider_name in providers_order:
    display_name, product = provider_display_names.get(
        provider_name, (provider_name, "-")
    )
    stats = provider_stats.get(
        provider_name,
        {
            "link_relevance_avg": 0,
            "summary_relevance_avg": 0,
            "embedding_relevance_avg": 0,
            "response_time_avg": 0,
        },
    )
    entry = {
        "Provider": display_name,
        "Product": product,
        "Summary Text Relevance": f"{stats['summary_relevance_avg']:.2f}",
        "Link Title & Description Relevance": f"{stats['link_relevance_avg']:.2f}",
        "Performance (ms)": f"{stats['response_time_avg']:.2f}",
        "Embedding Similarity": f"{stats['embedding_relevance_avg']:.2f}",
    }
    table_entries.append(entry)

# Generate Markdown content
md_content = "## 📊 Results Table\n\n"
md_content += "Below is a table showcasing the results of each provider in various aspects of our scoring mechanism:\n\n"
md_content += "| Provider          | Product            | Summary Text Relevance | Link Title & Description Relevance | Performance (ms) | Embedding Similarity |\n"
md_content += "|-------------------|--------------------|------------------------|------------------------------------|------------------|----------------------|\n"

prev_display_name = None

for entry in table_entries:
    provider_cell = entry["Provider"]
    if provider_cell == prev_display_name:
        provider_cell = ""
    else:
        prev_display_name = provider_cell
    md_content += f"| {provider_cell:<17} | {entry['Product']:<18} | {entry['Summary Text Relevance']:<22} | {entry['Link Title & Description Relevance']:<34} | {entry['Performance (ms)']:<16} | {entry['Embedding Similarity']:<22} |\n"

# Write Markdown file
md_file_path = os.path.join(os.path.dirname(current_dir), "results", "benchmark.md")
with open(md_file_path, "w") as f:
    f.write(md_content)

# Write JSON file
json_output = {
    "results_table": table_entries,
    "provider_stats": provider_stats,
}

output_file_path = os.path.join(
    os.path.dirname(current_dir), "results", "benchmark.json"
)

with open(output_file_path, "w") as f:
    json.dump(json_output, f, indent=2)

print("Benchmark results have been written to the Markdown and JSON files.")
