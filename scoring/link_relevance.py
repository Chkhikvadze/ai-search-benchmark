from reward_llm import RewardLLM
import traceback
from prompts import (
    SearchSummaryRelevancePrompt,
)

LINKS = 10


class LinkRelevanceModel:
    def __init__(self, llm_reward: RewardLLM):
        super().__init__()
        self.reward_llm = llm_reward

    async def llm_process_validator_links(self, prompt, links_with_metadata):
        scoring_messages = []
        url_list = []

        for link_with_metadata in links_with_metadata:
            url = link_with_metadata.get("url")
            title = link_with_metadata.get("title", "")
            description = link_with_metadata.get("description", "")

            result = self.get_scoring_text(
                prompt=prompt,
                content=f"Title: {title}, Description: {description}",
            )
            if result:
                scoring_prompt, messages = result  # messages is a list of dicts
                scoring_messages.append({url: messages})
                url_list.append(url)

        # Now call the LLM to get scores
        score_responses = await self.reward_llm.get_score_by_openai(scoring_messages)
        # Map the scores back to URLs
        url_to_score = {}

        for url, score_result in score_responses.items():
            url_to_score[url] = score_result
        return url_to_score

    def get_scoring_text(self, prompt: str, content: str):
        try:
            if content is None:
                print("Search Content is empty.")
                return None

            scoring_prompt = SearchSummaryRelevancePrompt()
            scoring_prompt_text = scoring_prompt.text(prompt, content)

            return scoring_prompt, [
                {"role": "system", "content": scoring_prompt.get_system_message()},
                {"role": "user", "content": scoring_prompt_text},
            ]
        except Exception as e:
            print(f"Error in Prompt reward method: {str(e)}")
            return None

    async def get_rewards(self, prompt: str, results):
        try:
            print("Computing link relevance rewards")

            # Collect all links_with_metadata and map URLs to their respective results
            all_links_with_metadata = []
            url_to_results = {}  # Map from URL to list of results that include it

            for result in results:
                search_results = result.get("search_results", [])
                if not search_results:
                    result["link_relevance"] = 0
                    continue

                links_with_metadata = []
                for sr in search_results[:LINKS]:
                    url = sr.get("url")
                    title = sr.get("title", "")
                    description = sr.get("description", "")
                    link_with_metadata = {
                        "url": url,
                        "title": title,
                        "description": description,
                    }
                    links_with_metadata.append(link_with_metadata)

                    if url not in url_to_results:
                        url_to_results[url] = []
                    url_to_results[url].append(result)

                all_links_with_metadata.extend(links_with_metadata)

            # Remove duplicates
            unique_links_with_metadata = {
                link["url"]: link for link in all_links_with_metadata
            }.values()

            # Process links and get scores
            val_score_responses = await self.llm_process_validator_links(
                prompt, unique_links_with_metadata
            )

            scoring_prompt = SearchSummaryRelevancePrompt()

            # Now, for each result, compute the average score
            for result in results:
                print(result)
                total_score = 0
                num_links = 0
                search_results = result.get("search_results", [])
                for sr in search_results[:LINKS]:
                    url = sr.get("url")
                    score_result = val_score_responses.get(url, None)
                    if score_result is not None:
                        score = scoring_prompt.extract_score(score_result)
                        print(f"score_result: {score_result}")
                        print(f"score: {score}")
                        total_score += score / 10.0  # Adjust score scaling as needed
                        num_links += 1
                if num_links > 0:
                    average_score = total_score / num_links
                    print(f"total_score: {total_score}, num_links: {num_links}, average_score: {average_score}")
                    reward = min(average_score, 1.0)
                    result["link_relevance"] = reward
                else:
                    result["link_relevance"] = 0
        except Exception as e:
            error_message = f"Search Summary Relevance get_rewards: {str(e)}"
            tb_str = traceback.format_exception(type(e), e, e.__traceback__)
            print("\n".join(tb_str) + error_message)
