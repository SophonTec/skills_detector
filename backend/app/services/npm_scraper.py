import httpx
from typing import List, Dict, Any, Optional
from datetime import datetime, timedelta

from .scraper_base import BaseScraper


class NpmScraper(BaseScraper):
    def get_source_name(self) -> str:
        return "npm"

    async def scrape(self) -> List[Dict[str, Any]]:
        results = []
        queries = ["ai", "machine-learning", "tensorflow", "openai", "langchain"]

        async with httpx.AsyncClient() as client:
            for query in queries:
                search_url = f"https://registry.npmjs.org/-/v1/search"
                params = {
                    "text": query,
                    "size": 20,
                    "popularity": 1.0,
                    "quality": 0.5,
                    "maintenance": 1.0,
                }

                response = await client.get(search_url, params=params)
                response.raise_for_status()
                data = response.json()

                for item in data.get("objects", []):
                    package = item.get("package", {})
                    results.append(await self._parse_package(client, package))

        return results[:50]

    async def _parse_package(
        self, client: httpx.AsyncClient, package: Dict[str, Any]
    ) -> Dict[str, Any]:
        name = package.get("name", "")
        description = package.get("description", "")

        downloads_url = f"https://api.npmjs.org/downloads/point/last-week/{name}"
        downloads_data = {"downloads": 0}
        try:
            response = await client.get(downloads_url)
            response.raise_for_status()
            downloads_data = response.json()
        except Exception:
            pass

        return {
            "name": name,
            "description": description,
            "url": f"https://www.npmjs.com/package/{name}",
            "language": "JavaScript",
            "stars": None,
            "forks": None,
            "downloads_day": None,
            "downloads_week": downloads_data.get("downloads", 0),
            "downloads_month": None,
            "likes": None,
            "last_activity": self._parse_datetime(
                package.get("date", {}).get("modified")
            ),
        }

    def _parse_datetime(self, date_str: Optional[str]) -> Optional[datetime]:
        if not date_str:
            return None
        try:
            return datetime.fromisoformat(date_str.replace("Z", "+00:00"))
        except (ValueError, AttributeError):
            return None
