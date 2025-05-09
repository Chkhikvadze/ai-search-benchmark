import os
from typing import List, Dict
from apify_client import ApifyClientAsync

APIFY_API_KEY = os.environ.get("APIFY_API_KEY")


class RedditScraperActor:
    def __init__(self) -> None:
        # Actor: https://apify.com/trudax/reddit-scraper-lite
        self.actor_id = "oAuCIx3ItNrs2okjQ"
        self.client = ApifyClientAsync(token=APIFY_API_KEY)

    async def scrape_metadata(self, urls: List[str]) -> List[Dict]:
        if not APIFY_API_KEY:
            print(
                "Please set the APIFY_API_KEY environment variable. See here: https://github.com/surcyf123/smart-scrape/blob/main/docs/env_variables.md. This will be required in the next release."
            )
            return []

        if not urls:
            return []

        try:
            run_input = {
                "includeNSFW": True,
                "debugMode": False,
                "maxItems": len(urls),
                "skipComments": True,
                "skipUserPosts": True,
                "proxyConfiguration": {
                    "useApifyProxy": True,
                    "apifyProxyGroups": ["RESIDENTIAL"],
                },
                "startUrls": [{"url": url} for url in urls],
            }

            run = await self.client.actor(self.actor_id).call(run_input=run_input)

            result = []

            async for item in self.client.dataset(
                run["defaultDatasetId"]
            ).iterate_items():
                if item.get("dataType") == "fake":
                    continue

                url = item.get("url")
                description = item.get("body")

                title = item.get("title")
                community_name = item.get("communityName")
                web_title = f"{title} : {community_name}" if title else None
                result.append(
                    {
                        "title": web_title,
                        "description": description,
                        "url": url,
                    }
                )

            return result
        except Exception as e:
            print(f"RedditScraperActor: Failed to scrape reddit links {urls}: {str(e)}")
            return []
