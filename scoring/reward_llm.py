import asyncio
import time
from .llm import call_openai
from .prompts import ScoringPrompt


class RewardLLM:
    def __init__(self):
        self.scoring_prompt = ScoringPrompt()

    async def get_score_by_openai(self, messages):
        try:
            start_time = time.time()  # Start timing for query execution
            query_tasks = []
            for message_dict in messages:  # Iterate over each dictionary in the list
                ((key, message_list),) = message_dict.items()

                async def query_openai(message):
                    try:
                        return await call_openai(
                            messages=message,
                            temperature=0.0001,
                            top_p=0.0001,
                            model="gpt-4o-mini",
                        )
                    except Exception as e:
                        print(f"Error sending message to OpenAI: {e}")
                        return ""  # Return an empty string to indicate failure

                task = query_openai(message_list)
                query_tasks.append(task)

            query_responses = await asyncio.gather(*query_tasks, return_exceptions=True)

            result = {}
            for response, message_dict in zip(query_responses, messages):
                if isinstance(response, Exception):
                    print(f"Query failed with exception: {response}")
                    response = (
                        ""  # Replace the exception with an empty string in the result
                    )
                ((key, message_list),) = message_dict.items()
                result[key] = response

            execution_time = time.time() - start_time  # Calculate execution time
            # print(f"Execution time for OpenAI queries: {execution_time} seconds")
            return result
        except Exception as e:
            print(f"Error processing OpenAI queries: {e}")
            return None

    async def llm_processing(self, messages, source):
        # Initialize score_responses as an empty dictionary to hold the scoring results
        score_responses = {}

        # Attempt to score with the current source
        current_score_responses = await self.get_score_by_openai(messages=messages)

        if current_score_responses:
            # Update the score_responses with the new scores
            score_responses.update(current_score_responses)
        else:
            print(
                f"Scoring with {source} failed or returned no results. Attempting next source."
            )

        return score_responses
