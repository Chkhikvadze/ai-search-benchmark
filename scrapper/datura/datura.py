import httpx
import json
import os
import asyncio
import aiofiles
import uuid
import logging

# Configure logging
logging.basicConfig(
    level=logging.INFO, format="%(asctime)s - %(levelname)s - %(message)s"
)


class TweetAnalyzerScrapper:
    def __init__(
        self,
        url="https://api.smartscrape.ai/analyse-tweets-event",
        data_path="../../dataset/data.jsonl",
    ):
        self.url = url
        self.data_path = data_path
        self.max_execution_times = [10, 30, 120]
        self.results_dir = "../../results"

    async def send_request(self, client, payload):
        """Send an HTTP POST request with the given payload."""
        try:
            response = await client.post(self.url, json=payload, timeout=120.0)
            response.raise_for_status()  # Raise exception for HTTP errors
            return response.text
        except httpx.RequestError as e:
            logging.error(f"Request error: {e}")
        except httpx.HTTPStatusError as e:
            logging.error(f"HTTP error: {e.response.status_code} for {e.request.url}")
        return "Request failed or response was None"

    def load_data(self):
        """Load JSONL data from the file and return as a list of dictionaries."""
        if not os.path.exists(self.data_path):
            logging.warning(f"Data file not found at {self.data_path}")
            return []

        json_data = []
        with open(self.data_path, "r") as json_file:
            for line in json_file:
                try:
                    json_data.append(json.loads(line))
                except json.JSONDecodeError as e:
                    logging.error(f"Error decoding JSON: {e}")

        logging.info(f"Loaded {len(json_data)} records from {self.data_path}")
        return json_data

    async def process_data_chunk(self, client, chunk, execution_time):
        """Process a chunk of data by sending requests and collecting results."""
        tasks = [
            self.send_request(
                client,
                {
                    "max_execution_time": execution_time,
                    "messages": [
                        {
                            "role": "user",
                            "content": question["question"],
                            "tools": [
                                "Google Search",
                                "Google News Search",
                                "Wikipedia Search",
                                "ArXiv Search",
                                "Hacker News Search",
                            ],
                            "date_filter": "PAST_2_WEEKS",
                            "response_order": "SUMMARY_FIRST",
                        }
                    ],
                },
            )
            for question in chunk
        ]
        responses = await asyncio.gather(*tasks)
        results = [
            {
                "id": str(uuid.uuid4()),
                "question": question["question"],
                "result": (
                    response if response else "Request failed or response was None"
                ),
            }
            for response, question in zip(responses, chunk)
        ]
        return results

    async def search_and_save_data(self):
        """Load data, process in chunks, and save results for each execution time."""
        data = self.load_data()
        os.makedirs(self.results_dir, exist_ok=True)
        async with httpx.AsyncClient() as client:
            for execution_time in self.max_execution_times:
                logging.info(f"Processing with max execution time: {execution_time}")
                full_results = []
                for i in range(0, len(data), 100):
                    chunk = data[i : i + 100]
                    results = await self.process_data_chunk(
                        client, chunk, execution_time
                    )
                    full_results.extend(results)
                await self.save_results(full_results, execution_time)

    async def save_results(self, results, execution_time):
        """Save results to a JSONL file."""
        output_file = os.path.join(
            self.results_dir, f"datura_{execution_time}_results.jsonl"
        )
        async with aiofiles.open(output_file, mode="w") as f:
            results_str = "\n".join(json.dumps(result) for result in results)
            await f.write(results_str + "\n")
        logging.info(f"Results saved to {output_file}")


if __name__ == "__main__":
    analyzer = TweetAnalyzerScrapper()
    asyncio.run(analyzer.search_and_save_data())
