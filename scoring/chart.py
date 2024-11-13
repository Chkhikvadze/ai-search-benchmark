import matplotlib.pyplot as plt
import os

# Define a color map for providers
provider_colors = {
    "andi": "#1f77b4",  # Blue
    "you": "#ff7f0e",  # Orange
    "chatgpt": "#2ca02c",  # Green
    "perplexity": "#d62728",  # Red
    "gemini": "#9467bd",  # Purple
    "grok": "#8c564b",  # Brown
    "datura_nova": "#bcbd22",  # Yellow
    "datura_orbit": "#d62728",  # Reddish
    "datura_horizon": "#7f7f7f",  # Gray
}


def generate_performance_chart(provider_stats, provider_name, provider_display_names):
    # Extract data and sort by average response time
    sorted_providers = sorted(
        provider_stats.items(), key=lambda x: x[1]["response_time_avg"]
    )

    # Extract labels, values, and colors for the chart
    labels = [provider_display_names.get(name, name) for name, _ in sorted_providers]
    values = [stats["response_time_avg"] for _, stats in sorted_providers]
    colors = [provider_colors.get(name, "#ffffff") for name, _ in sorted_providers]

    # Plotting the vertical bar chart
    plt.figure(figsize=(12, 8))
    ax = plt.gca()
    ax.set_facecolor("#1a1a1a")  # Dark background for axes
    plt.bar(labels, values, color=colors)

    # Increase text sizes
    plt.ylabel("Average Response Time (seconds)", color="white", fontsize=16)
    plt.title(
        f"{provider_name.capitalize()} Performance Comparison",
        color="white",
        fontsize=20,
    )
    plt.xticks(rotation=45, ha="right", color="white", fontsize=14)  # X-axis labels
    plt.yticks(color="white", fontsize=14)  # Y-axis tick labels

    plt.tight_layout()
    plt.gcf().set_facecolor("#1a1a1a")  # Dark background for figure

    # Save the chart as a PNG file in the specified directory
    output_dir = "docs/assets"
    os.makedirs(output_dir, exist_ok=True)
    output_chart_path = os.path.join(
        output_dir, f"{provider_name}_performance_chart.png"
    )

    plt.savefig(output_chart_path, facecolor=plt.gcf().get_facecolor())
    plt.close()
    print(f"Performance chart saved to {output_chart_path}")


def generate_link_content_relevance_chart(
    provider_stats, provider_name, provider_display_names
):
    # Extract data and sort by link_relevance_avg in descending order
    sorted_providers = sorted(
        provider_stats.items(), key=lambda x: x[1]["link_relevance_avg"]
    )

    # Extract labels, values, and colors
    labels = [provider_display_names.get(name, name) for name, _ in sorted_providers]
    values = [stats["link_relevance_avg"] for _, stats in sorted_providers]
    colors = [provider_colors.get(name, "#ffffff") for name, _ in sorted_providers]

    # Plotting the bar chart
    plt.figure(figsize=(12, 8))
    ax = plt.gca()
    ax.set_facecolor("#1a1a1a")  # Dark background
    plt.bar(labels, values, color=colors)

    # Increase text sizes
    plt.ylabel("Average Link Content Relevance", color="white", fontsize=16)
    plt.title(
        f"{provider_name.capitalize()} Link Content Relevance Comparison",
        color="white",
        fontsize=20,
    )
    plt.xticks(rotation=45, ha="right", color="white", fontsize=14)
    plt.yticks(color="white", fontsize=14)

    plt.tight_layout()
    plt.gcf().set_facecolor("#1a1a1a")  # Dark background for figure

    # Save the chart
    output_dir = "docs/assets"
    os.makedirs(output_dir, exist_ok=True)
    output_chart_path = os.path.join(
        output_dir, f"{provider_name}_link_content_relevance_chart.png"
    )

    plt.savefig(output_chart_path, facecolor=plt.gcf().get_facecolor())
    plt.close()
    print(f"Link Content Relevance chart saved to {output_chart_path}")


def generate_summary_text_relevance_chart(
    provider_stats, provider_name, provider_display_names
):
    # Extract data and sort by summary_relevance_avg in descending order
    sorted_providers = sorted(
        provider_stats.items(),
        key=lambda x: x[1]["summary_relevance_avg"],
    )

    # Extract labels, values, and colors
    labels = [provider_display_names.get(name, name) for name, _ in sorted_providers]
    values = [stats["summary_relevance_avg"] for _, stats in sorted_providers]
    colors = [provider_colors.get(name, "#ffffff") for name, _ in sorted_providers]

    # Plotting the bar chart
    plt.figure(figsize=(12, 8))
    ax = plt.gca()
    ax.set_facecolor("#1a1a1a")  # Dark background
    plt.bar(labels, values, color=colors)

    # Increase text sizes
    plt.ylabel("Average Summary Text Relevance", color="white", fontsize=16)
    plt.title(
        f"{provider_name.capitalize()} Summary Text Relevance Comparison",
        color="white",
        fontsize=20,
    )
    plt.xticks(rotation=45, ha="right", color="white", fontsize=14)
    plt.yticks(color="white", fontsize=14)

    plt.tight_layout()
    plt.gcf().set_facecolor("#1a1a1a")  # Dark background for figure

    # Save the chart
    output_dir = "docs/assets"
    os.makedirs(output_dir, exist_ok=True)
    output_chart_path = os.path.join(
        output_dir, f"{provider_name}_summary_text_relevance_chart.png"
    )

    plt.savefig(output_chart_path, facecolor=plt.gcf().get_facecolor())
    plt.close()
    print(f"Summary Text Relevance chart saved to {output_chart_path}")


def generate_embedding_similarity_chart(
    provider_stats, provider_name, provider_display_names
):
    # Extract data and sort by embedding_relevance_avg in descending order
    sorted_providers = sorted(
        provider_stats.items(),
        key=lambda x: x[1]["embedding_relevance_avg"],
    )

    # Extract labels, values, and colors
    labels = [provider_display_names.get(name, name) for name, _ in sorted_providers]
    values = [stats["embedding_relevance_avg"] for _, stats in sorted_providers]
    colors = [provider_colors.get(name, "#ffffff") for name, _ in sorted_providers]

    # Plotting the bar chart
    plt.figure(figsize=(12, 8))
    ax = plt.gca()
    ax.set_facecolor("#1a1a1a")  # Dark background
    plt.bar(labels, values, color=colors)

    # Increase text sizes
    plt.ylabel("Average Embedding Similarity", color="white", fontsize=16)
    plt.title(
        f"{provider_name.capitalize()} Embedding Similarity Comparison",
        color="white",
        fontsize=20,
    )
    plt.xticks(rotation=45, ha="right", color="white", fontsize=14)
    plt.yticks(color="white", fontsize=14)

    plt.tight_layout()
    plt.gcf().set_facecolor("#1a1a1a")  # Dark background for figure

    # Save the chart
    output_dir = "docs/assets"
    os.makedirs(output_dir, exist_ok=True)
    output_chart_path = os.path.join(
        output_dir, f"{provider_name}_embedding_similarity_chart.png"
    )

    plt.savefig(output_chart_path, facecolor=plt.gcf().get_facecolor())
    plt.close()
    print(f"Embedding Similarity chart saved to {output_chart_path}")


def generate_expected_answer_relevance_chart(
    provider_stats, provider_name, provider_display_names
):
    # Extract data and sort by expected_answer_relevance_avg in descending order
    sorted_providers = sorted(
        provider_stats.items(),
        key=lambda x: x[1]["expected_answer_relevance_avg"],
    )

    # Extract labels, values, and colors
    labels = [provider_display_names.get(name, name) for name, _ in sorted_providers]
    values = [stats["expected_answer_relevance_avg"] for _, stats in sorted_providers]
    colors = [provider_colors.get(name, "#ffffff") for name, _ in sorted_providers]

    # Plotting the bar chart
    plt.figure(figsize=(12, 8))
    ax = plt.gca()
    ax.set_facecolor("#1a1a1a")  # Dark background
    plt.bar(labels, values, color=colors)

    # Increase text sizes
    plt.ylabel("Average Expected Answer Relevance", color="white", fontsize=16)
    plt.title(
        f"{provider_name.capitalize()} Expected Answer Relevance Comparison",
        color="white",
        fontsize=20,
    )
    plt.xticks(rotation=45, ha="right", color="white", fontsize=14)
    plt.yticks(color="white", fontsize=14)

    plt.tight_layout()
    plt.gcf().set_facecolor("#1a1a1a")  # Dark background for figure

    # Save the chart
    output_dir = "docs/assets"
    os.makedirs(output_dir, exist_ok=True)
    output_chart_path = os.path.join(
        output_dir, f"{provider_name}_expected_answer_relevance_chart.png"
    )

    plt.savefig(output_chart_path, facecolor=plt.gcf().get_facecolor())
    plt.close()
    print(f"Expected Answer Relevance chart saved to {output_chart_path}")


def generate_charts(provider_stats, provider_name, provider_display_names):
    generate_performance_chart(provider_stats, provider_name, provider_display_names)
    generate_link_content_relevance_chart(
        provider_stats, provider_name, provider_display_names
    )
    generate_summary_text_relevance_chart(
        provider_stats, provider_name, provider_display_names
    )
    generate_embedding_similarity_chart(
        provider_stats, provider_name, provider_display_names
    )
    generate_expected_answer_relevance_chart(
        provider_stats, provider_name, provider_display_names
    )
