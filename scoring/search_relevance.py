from typing import List

# from scoring.reward import BaseRewardModel, BaseRewardEvent
# from .config import RewardModelType
from .reward_llm import RewardLLM

# from datura.protocol import ScraperStreamingSynapse
import traceback

# import bittensor as bt
# from datura.utils import clean_text
from .apify.cheerio_scraper_actor import CheerioScraperActor
from .apify.reddit_scraper_actor import RedditScraperActor
import asyncio
from .prompts import (
    SearchSummaryRelevancePrompt,
)
import random
import json
import time
import math


class LinkRelevanceModel:
    # reward_model_name: str = "VMware/open-llama-7b-open-instruct"

    # @property
    # def name(self) -> str:
    #     return RewardModelType.search_content_relevance.value

    def __init__(self, llm_reward: RewardLLM):
        super().__init__()
        self.reward_llm = llm_reward

    async def llm_process_validator_links(self, prompt, links_with_metadata):
        scoring_messages = []

        for link_with_metadata in links_with_metadata:
            url = link_with_metadata.get("url")
            title = link_with_metadata.get("title", "")
            description = link_with_metadata.get("description", "")

            result = self.get_scoring_text(
                prompt=prompt,
                content=f"Title: {title}, Description: {description}",
            )
            if result:
                scoring_prompt, scoring_text = result
                scoring_messages.append({url: scoring_text})

        score_responses = await self.reward_llm.get_score_by_openai(scoring_messages)
        return score_responses

    async def scrape_with_retries(
        self, urls, scraper_actor_class, group_size, max_attempts
    ):
        fetched_links_with_metadata = []
        non_fetched_links = urls.copy()
        attempt = 1

        while attempt <= max_attempts and non_fetched_links:
            print(
                f"Attempt {attempt}/{max_attempts} for {scraper_actor_class.__name__}, processing {len(non_fetched_links)} links."
            )

            url_groups = [
                non_fetched_links[i : i + group_size]
                for i in range(0, len(non_fetched_links), group_size)
            ]

            tasks = [
                asyncio.create_task(scraper_actor_class().scrape_metadata(urls=group))
                for group in url_groups
            ]

            # Wait for tasks to complete
            results = await asyncio.gather(*tasks, return_exceptions=True)

            # Combine results and handle exceptions
            for result in results:
                if isinstance(result, Exception):
                    print(
                        f"Error in {scraper_actor_class.__name__} scraper attempt {attempt}: {str(result)}"
                    )
                    continue
                fetched_links_with_metadata.extend(result)

            # Update non-fetched links
            fetched_urls = {link.get("url") for link in fetched_links_with_metadata}
            non_fetched_links = [
                url for url in non_fetched_links if url not in fetched_urls
            ]

            attempt += 1

        return fetched_links_with_metadata, non_fetched_links

    async def scrape_links_with_retries(self, urls):
        # Separate Reddit URLs from other URLs
        reddit_urls = []
        other_urls = []

        for url in urls:
            if "reddit.com" in url and "comments" in url:
                reddit_urls.append(url)
            else:
                other_urls.append(url)

        # Scrape Reddit URLs with retries
        reddit_fetched_links_with_metadata = []
        reddit_non_fetched_links = []

        if reddit_urls:
            reddit_fetched_links_with_metadata, reddit_non_fetched_links = (
                await self.scrape_with_retries(
                    urls=reddit_urls,
                    scraper_actor_class=RedditScraperActor,
                    group_size=200,
                    max_attempts=2,
                )
            )

        # Scrape other URLs with retries
        other_fetched_links_with_metadata = []
        other_non_fetched_links = []

        if other_urls:
            other_fetched_links_with_metadata, other_non_fetched_links = (
                await self.scrape_with_retries(
                    urls=other_urls,
                    scraper_actor_class=CheerioScraperActor,
                    group_size=100,
                    max_attempts=2,
                )
            )

        # Combine non-fetched links
        non_fetched_links = reddit_non_fetched_links + other_non_fetched_links

        # Combine all fetched links
        fetched_links_with_metadata = (
            reddit_fetched_links_with_metadata + other_fetched_links_with_metadata
        )

        # Filter out any entries without a URL
        fetched_links_with_metadata = [
            link for link in fetched_links_with_metadata if link.get("url")
        ]

        return fetched_links_with_metadata, non_fetched_links

    async def process_links(
        self,
        prompt: str,
        results,
    ):
        all_links = []
        start_time = time.time()

        for result in results:
            urls = result.get("urls", [])

            links = random.sample(
                urls,
                min(3, len(urls)),
            )

            all_links.extend(links)

        unique_links = list(set(all_links))

        if len(unique_links) == 0:
            print("No unique links found to process.")
            return {}

        links_with_metadata, non_fetched_links = await self.scrape_links_with_retries(
            unique_links
        )

        # for response in responses:
        #     for link_with_metadata in links_with_metadata:
        #         url = link_with_metadata.get("url")

        #         if url in response.search_completion_links:
        #             response.validator_links.append(link_with_metadata)

        val_score_responses = await self.llm_process_validator_links(
            prompt, links_with_metadata
        )

        end_time = time.time()
        print(
            f"Fetched Web links method took {end_time - start_time} seconds. "
            f"All links count: {len(all_links)}, Unique links count: {len(unique_links)}, "
            f"APIFY fetched web links count: {len(links_with_metadata)}"
        )

        print(
            f"Web links not fetched amount: {len(non_fetched_links)}; List: {non_fetched_links}; For prompt: [{prompt}]"
        )
        if len(non_fetched_links):
            print(
                f"Unique Web Links Amount: {len(unique_links)}; List: {unique_links};"
            )

        return val_score_responses

    def get_scoring_text(self, prompt: str, content: str):
        try:
            if content is None:
                print("Search Content is empty.")
                return None

            # content = clean_text(content)

            scoring_prompt_text = None
            scoring_prompt = SearchSummaryRelevancePrompt()

            if not scoring_prompt_text:
                scoring_prompt_text = scoring_prompt.text(prompt, content)

            return scoring_prompt, [
                {"role": "system", "content": scoring_prompt.get_system_message()},
                {"role": "user", "content": scoring_prompt_text},
            ]
        except Exception as e:
            print(f"Error in Prompt reward method: {str(e)}")
            return None

    async def get_rewards(
        self,
        prompt: str,
        results,
    ):
        try:
            print(
                f"WebSearchContentRelevanceModel | Calculating {len(results)} rewards (typically < 1 sec/reward)."
            )
            print(
                f"WebSearchContentRelevanceModel | prompt: {repr(prompt[:50])} ... {repr(prompt[-50:])}"
            )

            val_score_responses = await self.process_links(
                prompt=prompt, results=results
            )

            print(
                f"WebSearchContentRelevanceModel | Keys in val_score_responses: {len(val_score_responses.keys()) if val_score_responses else 'No val_score_responses available'}"
            )

            scoring_prompt = SearchSummaryRelevancePrompt()

            for result in results:
                reward = 0

                urls = result.get("urls", [])

                total_score = 0
                num_links = len(urls)

                # max_links_considered = max(num_links, links_expected)

                if num_links > 0 and val_score_responses:
                    for url in urls:
                        score_result = val_score_responses.get(url, None)

                        if score_result is not None:
                            score = scoring_prompt.extract_score(score_result)

                            total_score += (
                                score / 10.0
                            )  # Adjust score scaling as needed

                    if total_score > 0:
                        average_score = total_score / 3
                        reward = average_score

                        # reward_event.reward = self.calculate_adjusted_score(
                        #     links_count=len(response.search_completion_links),
                        #     score=average_score,
                        #     max_links_threshold=links_expected,
                        # )
                else:
                    # print(f"has no validator links.")
                    reward = 0  # Handle case with no validator links

                reward = min(reward, 1.0)

                result["link_relevance"] = reward

                # zero_scores = {}
                # non_zero_scores = {}

            # for (index, response), uid_tensor, reward_e in zip(
            #     enumerate(responses), uids, reward_events
            # ):
            #     uid = uid_tensor.item()
            #     if reward_e.reward == 0:
            #         # score_explain = score_responses.get(str(uid), "")
            #         zero_scores[uid] = reward_e.reward
            #     else:
            #         non_zero_scores[uid] = reward_e.reward

            # print(
            #     f"==================================Web Search Content Relevance scoring Zero Scores  ({len(zero_scores)} cases)=================================="
            # )
            # print(json.dumps(zero_scores))
            # print(
            #     f"==================================Web Search Content Relevance scoring Non-Zero Scores ({len(non_zero_scores)} cases)=================================="
            # )
            # print(json.dumps(non_zero_scores))
            # return reward_events, grouped_val_score_responses
        except Exception as e:
            error_message = f"Search Summary Relevance get_rewards: {str(e)}"
            tb_str = traceback.format_exception(type(e), e, e.__traceback__)
            print("\n".join(tb_str) + error_message)
            reward_events = []
            # for result in results:
            #     reward_event = BaseRewardEvent()
            #     reward_event.reward = 0
            #     reward_events.append(reward_event)
            # return reward_events, {}
