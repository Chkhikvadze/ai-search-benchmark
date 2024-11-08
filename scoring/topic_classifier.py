import asyncio
import json
from typing import List
from .llm import call_openai_beta
from .prompts import topic_classification_prompt, ClassificationResult

class TopicClassifier:
    def __init__(self):
        self.system_prompt = topic_classification_prompt

    async def classify_category_by_openai(self, results: List[dict]):
        try:
            query_tasks = []
            for result in results:
                question = result.get("question", "")
                messages = [{"role": "system", "content": topic_classification_prompt.format(question)}]

                async def query_openai(message):
                    try:
                        return await call_openai_beta(
                            messages=message,
                            temperature=0.0001,
                            model="gpt-4o-mini",
                            response_format=ClassificationResult
                        )
                    except Exception as e:
                        print(f"Error sending message to OpenAI: {e}")
                        return ""  # Return an empty string to indicate failure

                task = query_openai(messages)
                query_tasks.append(task)

            query_responses = await asyncio.gather(*query_tasks, return_exceptions=True)
            
            knowledge_categories = {"Architecture", "Arts", "Fashion", "Astronomy", "Anime", "Auto (Automotive)"}
            
            for i, response in enumerate(query_responses):
                if isinstance(response, str) and response:
                    category = json.loads(response).get("category", "")
                    results[i]["category"] = category
                    if category == '':
                        results[i]["area"] = ''
                    else:
                        results[i]["area"] = "Knowledge" if category in knowledge_categories else "News"

            return results

        except Exception as e:
            print(f"Error processing OpenAI queries: {e}")
            return None


# example_questions = [
#     {"question": "what is the google stock price?"},
#     {"question": "Do you know AI?"}
# ]
# # Example usage
# async def main(questions):
#     classifier = TopicClassifier()
    
#     categorized_results = await classifier.classify_category_by_openai(questions)
    
#     return categorized_results

# # Run the example
# asyncio.run(main(example_questions))  # Uncomment this line to run the example