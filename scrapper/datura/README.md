# TweetAnalyzer

TweetAnalyzer is a Python application designed to analyze tweets by sending requests to an external API and saving the results. It processes data in chunks and supports asynchronous operations for efficient data handling.

## Features

- Asynchronous HTTP requests using `httpx` and `asyncio`.
- JSON data loading and processing.
- Error handling and logging.
- Results are saved in JSONL format.

## Requirements

- Python 3.7+
- `httpx`
- `aiofiles`
- `asyncio`

## Installation

1. **Clone the repository**:

   ```bash
   git clone https://github.com/Datura-ai/meta-benchmark.git
   cd meta-benchmark/scrapper/datura
   ```

 2. **Create and activate a virtual environment**:

    ```bash
    python3 -m venv venv
    source venv/bin/activate
    ```

3. **Install the required packages**:

   ```bash
   pip install httpx aiofiles
   ```

## Usage

1. **Prepare your dataset in the `dataset/data.jsonl` file. Each line should be a valid JSON object containing a `question` field**.

2. **Run the application**:

   ```bash
   python3 datura.py
   ```

3. **The results will be saved in the `results` directory, with separate files for each execution time**.

## Configuration

- The API URL and data path can be configured in the `TweetAnalyzerScrapper` class constructor.
- Modify the `max_execution_time` list to adjust the execution times for requests.

## Logging

- The application uses Python's built-in logging module to log information and errors. Logs are printed to the console.

## Contributing

Contributions are welcome! Please open an issue or submit a pull request for any improvements or bug fixes.

## License

This project is licensed under the MIT License. See the [LICENSE](LICENSE) file for details.

## Support

For any questions or issues, please open an issue on the GitHub repository.