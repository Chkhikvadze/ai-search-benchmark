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

BATCH_SIZE = 100


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

    async def send_request(self, client: httpx.AsyncClient, payload):
        """Send an HTTP POST request with the given payload."""
        try:
            response = await client.post(self.url, json=payload, timeout=120.0)
            response.raise_for_status()  # Raise exception for HTTP errors
            response_time = response.elapsed.total_seconds()
            return response.text, response_time
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

    def parse_datura_results(self, type, data):
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

    def parse_datura(self, response: str):
        data = []

        # Split the result by newlines and process each line
        for line in response.splitlines():
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
            results = self.parse_datura_results(type, content)
            search_results.extend(results)

        completion = next(
            (d.get("content") for d in data if d.get("type") == "completion"), ""
        )

        print(completion)

        print("-------------------")

        # Extract text after **Summary**
        summary_start = completion.find("Summary:**")
        summary_text = None

        if summary_start != -1:
            summary_text = completion[summary_start + len("Summary:**") :].strip()

        print(summary_text)

        return {
            "result": (
                summary_text if summary_text else "Request failed or response was None"
            ),
            "search_results": search_results,
        }

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
                                # "Hacker News Search",
                            ],
                            "date_filter": "PAST_2_WEEKS",
                            "response_order": "LINKS_FIRST",
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
                **self.parse_datura(response),
                "response_time": response_time,
            }
            for (response, response_time), question in zip(responses, chunk)
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
                for i in range(0, len(data), BATCH_SIZE):
                    chunk = data[i : i + BATCH_SIZE]
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
