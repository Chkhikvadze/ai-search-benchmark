import requests, json, uuid, time
from tqdm import tqdm
import pandas as pd
import os
from dotenv import load_dotenv

load_dotenv()

YOUR_API_KEY = os.getenv("YOU_API_KEY")


def get_ai_snippets_for_query(query):
    headers = {"X-API-Key": YOUR_API_KEY}
    params = {"query": query}
    return requests.get(
        f"https://api.ydc-index.io/search?query={query}",
        params= params,
        headers=headers,
    ).json()

def process_jsonl_to_jsonl_nested(input_jsonl_path, output_jsonl_path):
    """
    Reads a JSONL file, process each entry to get AI snippets and similarity scores,
    and saves the results to a new JSONL file with a nested "search_results" list.

    Args:
        input_jsonl_path (str): Path to the input JSONL file.
        output_jsonl_path (str): Path where the output JSONL will be saved.
    """

    try:
        # First, determine the total number of lines for the progress bar
        with open(input_jsonl_path, 'r', encoding='utf-8') as infile:
            total_lines = sum(1 for _ in infile)
    except FileNotFoundError:
        print(f"Error: The file {input_jsonl_path} does not exist.")
        return
    except Exception as e:
        print(f"An error occurred while counting lines in the input file: {e}")
        return

    # Open the input and output JSONL files
    with open(input_jsonl_path, 'r', encoding='utf-8') as infile, \
        open(output_jsonl_path, 'w', encoding='utf-8') as outfile:

        for line in tqdm(infile, total=total_lines, desc="Processing entries"):
            try:
                data= json.loads(line)
            except json.JSONDecodeError as e:
                print(f"Error decoding JSON: {e}")
                continue

            # Extract required fields
            entry_id = data.get('id', '')
            question = data.get('question', '')

            print(f"Processing ID: {entry_id}, Question: {question}")

            start_time = time.time()
            # Call the AI function to get snippets
            response = get_ai_snippets_for_query(question)
            end_time = time.time() - start_time

            print(response)

            # Check if 'hits' key exists and is a list
            hits = response.get('hits', [])
            if not isinstance(hits, list):
                hits = []

            search_results=[]
            snippets_combined= ''

            if hits:
                for hit in hits:
                    # Combine snippets into a single string
                    snippets_combined = "; ".join(hit.get('snippets', []))

                    # Create the search result dictionary
                    search_result={
                        'title': hit.get('title', ''),
                        'url': hit.get('url', ''),
                        'description': hit.get('description', '')
                    }

                    search_results.append(search_result)
            
            if len(snippets_combined):
                extracted_hit = {
                    'id': entry_id,
                    'question': question,
                    'result': snippets_combined,
                    'search_results': search_results,
                    'response_time': end_time
                }
            else: 
                # Create the extracted_hit dictionary with nested 'search_results'
                extracted_hit = {
                    'id': entry_id,
                    'question': question,
                    'result': snippets_combined,
                    'search_results': search_results,
                    'response_time': end_time
                }

            # write the extracted_hit as a JSON line
            outfile.write(json.dumps(extracted_hit, ensure_ascii=False) + '\n')

    print(f'Data successfully saved to {output_jsonl_path}')
    

if __name__ == '__main__':
    # Define the paths to your input and output files
    input_path = os.path.join("..", "..", "dataset", "data.jsonl")
    output_path = os.path.join("..", "..", "results", "you_results.jsonl")

    process_jsonl_to_jsonl_nested(input_path, output_path)