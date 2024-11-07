# import traceback
# import time
# import torch
# import bittensor as bt
# import random
# import asyncio
# import re
# from typing import List, Tuple
# from neurons.validators.reward.config import RewardModelType, RewardScoringType
# from neurons.validators.reward.reward import BaseRewardModel, BaseRewardEvent
# from neurons.validators.utils.prompts import (
#     SummaryRelevancePrompt,
#     LinkContentPrompt,
#     LinkContentAndDescriptionPrompt,
# )

# from datura.protocol import ScraperStreamingSynapse, ScraperTextRole
# from neurons.validators.reward.reward_llm import RewardLLM
# from datura.services.twitter_utils import TwitterUtils
# from datura.services.web_search_utils import WebSearchUtils
# import json
# from neurons.validators.reward.config import DefaultSummaryRelevanceWeightConfig
# from datura.utils import clean_text
import traceback
import asyncio
from typing import List, Dict
from .reward_llm import RewardLLM
from .prompts import SummaryRelevancePrompt


class SummaryRelevanceModel:
    def __init__(self, llm_reward: RewardLLM):
        super().__init__()
        self.reward_llm = llm_reward

    def get_scoring_text(self, prompt: str, summary: str):
        try:
            if not summary:
                print("Summary is empty.")
                return None

            scoring_prompt = SummaryRelevancePrompt()
            scoring_prompt_text = scoring_prompt.text(prompt, summary)

            return scoring_prompt, [
                {"role": "system", "content": scoring_prompt.get_system_message()},
                {"role": "user", "content": scoring_prompt_text},
            ]
        except Exception as e:
            print(f"Error in get_scoring_text: {str(e)}")
            return None

    async def get_rewards(self, prompt: str, results: List[Dict]):
        try:
            print("Computing Summary Relevance rewards")

            scoring_messages = []
            index_to_result = {}

            for index, result in enumerate(results):
                summary = result.get("summary", "")

                if not summary:
                    result["summary_relevance"] = 0
                    continue

                scoring_text = self.get_scoring_text(prompt, summary)

                if scoring_text:
                    scoring_prompt, messages = scoring_text
                    scoring_messages.append({str(index): messages})
                    index_to_result[str(index)] = result
                else:
                    result["summary_relevance"] = 0

            # Now call the LLM to get scores
            if scoring_messages:
                score_responses = await self.reward_llm.get_score_by_openai(
                    scoring_messages
                )
                scoring_prompt = SummaryRelevancePrompt()

                for index, score_result in score_responses.items():
                    result = index_to_result.get(index)
                    if result:
                        score = scoring_prompt.extract_score(score_result)
                        # Scale score to 0-1 range and cap at 1.0
                        result["summary_relevance"] = min(score / 10.0, 1.0)
            return results
        except Exception as e:
            error_message = f"Summary Relevance get_rewards: {str(e)}"
            tb_str = traceback.format_exception(type(e), e, e.__traceback__)
            print("\n".join(tb_str) + error_message)
            return results
