import google.generativeai as genai
import pandas as pd
import time
import json
import os
from dotenv import load_dotenv

load_dotenv()

YOUR_API_KEY = os.getenv("GEMINI_API_KEY")

input_path = os.path.join("..", "..", "dataset", "data.jsonl")
output_path = os.path.join("..", "..", "results", "gemini_results.jsonl")

questions = []
with open(input_path, 'r') as file:
    for line in file:
        questions.append(json.loads(line.strip()))
df = pd.DataFrame(questions, columns=['id', 'question', 'expected_answer'])

questions_list = df['question'].to_list()

genai.configure(api_key=YOUR_API_KEY)

final_results = []
question_number = 1
total_time = 0


with open(output_path, "a") as file:
     
     for index, question in enumerate(questions_list):
        item = {}
        start_time = time.time()

        model = genai.GenerativeModel(model_name="gemini-1.5-flash")
        response = model.generate_content(
            f"""Please answer the following question '{question}' in json format, with only the fields provided. Do not include any additional information outside this structure:
                {{
                "id":"",
                "question": "<insert question here>",
                "result": "<Provide a concise summary here, including any relevant links>",
                "search_results":[
                    {{
                        "title":"<Title of relevant article or page>",
                        "url": "<URL of the article or page>",
                        "description": "<Brief description of the content>"

                    }}
                ],
                "response_time":""}}
            
            Instructions:
            Keep the id and response_time fields empty.
            cite source related to the answer. Please provide source urls in https format. If source is copyrighted or invalid, assign following value to url key:'Url is copyrighted, unable to provide it'
            Ensure the result field includes a summary and any links needed for further reading.
            Populate the search_results field with relevant articles, each with a title, url, and description.
            Make sure to follow this format exactly without extra fields or text. """
        )

        execution_time = time.time() - start_time
        try:
            json_response = json.loads(response.text)
            json_response["id"] =  df["id"].iloc[index]
            json_response["response_time"] = execution_time
            json_response['question'] = question
        except Exception as e:
            json_response= {
                "id": df["id"].iloc[index],
                "question": question,
                "result": "Error, Model gave no response as it was reciting from copyrighted material",
                "search_results":[
                    {
                        "title":"",
                        "url": "",
                        "description": ""

                    }
                ],
                "response_time":execution_time}
        
        file.write(json.dumps(json_response) + '\n')
        time.sleep(3)