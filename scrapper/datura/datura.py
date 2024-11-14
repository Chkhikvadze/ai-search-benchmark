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

BATCH_SIZE = 20

COUNT_LIMIT = (
    1000  # Set to an integer to limit the number of records processed for testing
)

ACCESS_KEY = os.environ.get("VALIDATOR_ACCESS_KEY", "test")


class TweetAnalyzerScrapper:
    def __init__(
        self,
        name,
        data_with_least_items_path=None,  # For example if Grok has 30 results and Datura has 100 twitter results, we can filter to take same 30 results for both
        url="https://api.smartscrape.ai/search",
        data_path="../../dataset/data.jsonl",
    ):
        self.url = url
        self.data_path = data_path
        self.models = ["NOVA", "ORBIT", "HORIZON"]
        self.results_dir = "../../results"
        self.name = name
        self.data_with_least_items_path = data_with_least_items_path

    async def send_request(self, client: httpx.AsyncClient, payload):
        """Send an HTTP POST request with the given payload."""
        try:
            response = await client.post(
                self.url,
                json=payload,
                headers={"Access-Key": ACCESS_KEY},
                timeout=120.0,
            )
            response.raise_for_status()  # Raise exception for HTTP errors
            response_time = response.elapsed.total_seconds()
            return response.text, response_time
        except httpx.RequestError as e:
            logging.error(f"Request error: {e}")
        except httpx.HTTPStatusError as e:
            logging.error(f"HTTP error: {e.response.status_code} for {e.request.url}")
        return "Request failed or response was None"

    def load_data_with_least_items(self):
        if not self.data_with_least_items_path:
            return None

        filter_data_with_least_items = {}

        with open(self.data_with_least_items_path, "r") as json_file:
            for line in json_file:
                try:
                    q = json.loads(line)
                    filter_data_with_least_items[q.get("id")] = 1
                except json.JSONDecodeError as e:
                    logging.error(f"Error decoding JSON: {e}")

        return filter_data_with_least_items

    def load_data(self):
        """Load JSONL data from the file and return as a list of dictionaries."""
        if not os.path.exists(self.data_path):
            logging.warning(f"Data file not found at {self.data_path}")
            return []

        filter_data_with_least_items = self.load_data_with_least_items()

        json_data = []
        with open(self.data_path, "r") as json_file:
            for line in json_file:
                try:
                    item = json.loads(line)

                    duplicate = next(
                        (x for x in json_data if x.get("id") == item.get("id")), None
                    )

                    if not duplicate:
                        if not filter_data_with_least_items:
                            json_data.append(item)
                        elif item.get("id") in filter_data_with_least_items:
                            json_data.append(item)
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
        elif type == "arxiv_search":
            for result in data:
                standardized_results.append(
                    {
                        "title": result.get("title"),
                        "link": result.get("url"),
                        "snippet": result.get("snippet"),
                    }
                )
        elif type == "hacker_news_search":
            for result in data:
                standardized_results.append(
                    {
                        "title": result.get("title"),
                        "link": result.get("url"),
                        "snippet": result.get("snippet"),
                    }
                )
        elif type == "wikipedia_search":
            for result in data:
                standardized_results.append(
                    {
                        "title": result.get("title"),
                        "link": result.get("url"),
                        "snippet": result.get("snippet"),
                    }
                )
        elif type == "tweets":
            for result in data:
                standardized_results.append(
                    {
                        "description": result.get("text"),
                        "url": result.get("url"),
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

        completion = ""

        for chunk in data:
            content_type = chunk.get("type")
            content = chunk.get("content")

            if content_type == "completion":
                completion = content or ""

            if "search" in content_type or "tweets" in content_type:
                results = self.parse_datura_results(content_type, content)
                search_results.extend(results)

        # Extract text after **Summary**
        summary_start = completion.find("Summary:**")
        summary_text = None

        if summary_start != -1:
            summary_text = completion[summary_start + len("Summary:**") :].strip()

        return {
            "result": (
                summary_text if summary_text else "Request failed or response was None"
            ),
            "search_results": search_results,
        }

    async def process_data_chunk(self, client, chunk, model):
        """Process a chunk of data by sending requests and collecting results."""
        tools = []

        if "twitter" in self.name:
            tools = ["Twitter Search"]
        elif "web" in self.name:
            tools = [
                "Google Search",
                "Google News Search",
                "Wikipedia Search",
                "ArXiv Search",
            ]

        tasks = [
            self.send_request(
                client,
                {
                    "model": model,
                    "prompt": question["question"],
                    "tools": tools,
                    "date_filter": "PAST_2_WEEKS",
                    "response_order": "LINKS_FIRST",
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
        data = data[:COUNT_LIMIT] if COUNT_LIMIT else data

        os.makedirs(self.results_dir, exist_ok=True)
        async with httpx.AsyncClient() as client:
            for model in self.models:
                logging.info(f"Processing with model: {model}")

                # Delete output file if it exists
                output_file = os.path.join(
                    self.results_dir,
                    f"datura_{model.lower()}_{self.name}_results.jsonl",
                )
                if os.path.exists(output_file):
                    os.remove(output_file)
                    logging.info(f"Deleted existing output file {output_file}")

                for i in range(0, len(data), BATCH_SIZE):
                    chunk = data[i : i + BATCH_SIZE]
                    results = await self.process_data_chunk(client, chunk, model)
                    await self.save_results(results, model)

    async def save_results(self, results, model):
        """Save results to a JSONL file."""
        output_file = os.path.join(
            self.results_dir, f"datura_{model.lower()}_{self.name}_results.jsonl"
        )
        async with aiofiles.open(output_file, mode="a") as f:
            results_str = "\n".join(json.dumps(result) for result in results)
            await f.write(results_str + "\n")
        logging.info(f"Results saved to {output_file}")


if __name__ == "__main__":
    analyzer = TweetAnalyzerScrapper(name="twitter")
    asyncio.run(analyzer.search_and_save_data())

    analyzer = TweetAnalyzerScrapper(name="web")
    asyncio.run(analyzer.search_and_save_data())
