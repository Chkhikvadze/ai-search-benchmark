# Scoring

## Features:

-   Link relevance scoring
-   Summary relevance scoring
-   Summary embedding similarity to expected answer and prompt
-   Markdown tables and charts for visualization of scoring results

## Requirements

-   Python 3.10+

## Installation

1. **Clone the repository**:

    ```bash
    git clone https://github.com/Chkhikvadze/ai-search-benchmark.git
    cd meta-benchmark
    ```

2. **Create and activate a virtual environment**:

    ```bash
    python3 -m venv venv
    source venv/bin/activate
    ```

3. **Install the required packages**:

    ```bash
    pip install -r requirements.txt
    ```

## Environment Variables

```
export OPENAI_API_KEY="<your_openai_api_key>"
```

## Usage

1. **Run the application**:

    ```bash
    cd scoring
    python3 main.py
    ```

## Configuration

-   Concurrent tasks can be configured with `CONCURRENT_TASKS` constant.
-   At the end on file you can run both twitter and web providers, you can comment out the one you don't want to run.
