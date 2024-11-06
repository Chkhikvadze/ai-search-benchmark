# Scrape Data:

Scrape data from each providers: 

1. Andi Search
2. ChatGPT Search
3. Google Gemini
4. Perplexity 
5. You.com
6. Datura


Dataset: Questions are stored in `dataset/data.jsonl` and responses are stored in the `results` folder as `[provider]_result.jsonl`.

Result format: Each result should be a JSON object with the following structure:
{
    "id": "Unique identifier for the query",
    "question": "The question posed to the search provider",
    "result": "A summary of the text and links obtained from the search",
    "search_results": [
        {
            "title": "Title of the search result",
            "url": "URL of the search result",
            "description": "Description of the search result"
        }
    ]
}


Use semantic commits: https://gist.github.com/joshbuchea/6f47e86d2510bce28f8e7f42ae84c716


Reference:
https://github.com/Talc-AI/search-bench



Important Note:
1. Add all running instructions in the README, and send a PR


