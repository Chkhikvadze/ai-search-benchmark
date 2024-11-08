# AI Snippets Processor

This Python scirpt processes entries in a JSONL file, queries an AI-powered API to retrieve relevant snippers based on each query, and saves the processed results in a new JSONL file with a nested structure.

## Features

 - Reads and processes each entry in a JSONL file.
 - Retrieves AI-generated snippets and additional metadata for each query.
 - Saves results, including snippets, respones times, and metadata, in a structued JSONL format.
 - Includes error handling for common issues like file not found and JSON decoding errors.

 ## Dependencies

 This script requires the following Python libraries:

 - `google-generativeai`: For making API requests to Gemini.
 - `json`: For handling JSON data (built-in)
 - `os`: For performing os related operations (built-in)
 - `time`: For measuring response times (built-in)
 - `pandas`: For data manipulation.
 - `python-dotenv`: For storing credentials.

 ### Installing Dependencies

 Install the required packages using `pip`:

 ```bash
 pip install google-generativeai pandas python-dotenv
 ```

 ### Running the Script

 Execute the script using the `python` command:

 ```bash
 python gemini.py