import httpx
from typing import List, Dict, Any, Optional
from datetime import datetime

from .scraper_base import BaseScraper
from ..core.config import settings


class GitHubScraper(BaseScraper):
    def get_source_name(self) -> str:
        return "github"

    async def scrape(self) -> List[Dict[str, Any]]:
        base_url = "https://api.github.com/search/repositories"
        headers = {}
        if settings.github_token:
            headers["Authorization"] = f"Bearer {settings.github_token}"

        results = []
        queries = [
            ("topic:ai+language:python", "stars"),
            ("topic:machine-learning+language:python", "stars"),
            ("topic:deep-learning+language:python", "stars"),
            ("topic:llm+language:python", "stars"),
        ]

        async with httpx.AsyncClient() as client:
            for query, sort_by in queries:
                params = {"q": query, "sort": sort_by, "order": "desc", "per_page": 50}

                response = await client.get(base_url, headers=headers, params=params)
                response.raise_for_status()
                data = response.json()

                for item in data.get("items", []):
                    results.append(self._parse_repo(item))

        return results[:100]

    def _parse_repo(self, repo: Dict[str, Any]) -> Dict[str, Any]:
        return {
            "name": f"{repo['owner']['login']}/{repo['name']}",
            "description": repo.get("description", ""),
            "url": repo["html_url"],
            "language": repo.get("language"),
            "stars": repo.get("stargazers_count", 0),
            "forks": repo.get("forks_count", 0),
            "downloads_day": None,
            "downloads_week": None,
            "downloads_month": None,
            "likes": None,
            "last_activity": self._parse_datetime(repo.get("updated_at")),
        }

    def _parse_datetime(self, date_str: Optional[str]) -> Optional[datetime]:
        if not date_str:
            return None
        try:
            return datetime.fromisoformat(date_str.replace("Z", "+00:00"))
        except (ValueError, AttributeError):
            return None
