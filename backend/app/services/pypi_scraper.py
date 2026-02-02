import httpx
from typing import List, Dict, Any, Optional
from datetime import datetime

from .scraper_base import BaseScraper


class PyPIScraper(BaseScraper):
    def get_source_name(self) -> str:
        return "pypi"

    async def scrape(self) -> List[Dict[str, Any]]:
        results = []
        queries = ["tensorflow", "pytorch", "scikit-learn", "transformers", "openai"]

        async with httpx.AsyncClient() as client:
            for query in queries:
                search_url = f"https://pypi.org/search/"
                params = {"q": query}

                response = await client.get(search_url, params=params)
                if response.status_code == 200:
                    package_names = self._extract_package_names(response.text)
                    for name in package_names[:10]:
                        try:
                            package_data = await self._fetch_package_data(client, name)
                            if package_data:
                                results.append(package_data)
                        except Exception as e:
                            print(f"Error fetching {name}: {e}")

        return results[:50]

    def _extract_package_names(self, html: str) -> List[str]:
        names = []
        for line in html.split("\n"):
            if '<a class="package-snippet"' in line:
                start = line.find('href="/project/')
                if start != -1:
                    start += 15
                    end = line.find("/", start)
                    if end != -1:
                        names.append(line[start:end])
        return names

    async def _fetch_package_data(
        self, client: httpx.AsyncClient, name: str
    ) -> Optional[Dict[str, Any]]:
        metadata_url = f"https://pypi.org/pypi/{name}/json"
        stats_url = f"https://pypistats.org/api/packages/{name}/recent"

        metadata_response = await client.get(metadata_url)
        metadata_response.raise_for_status()
        metadata = metadata_response.json()

        info = metadata.get("info", {})
        releases = metadata.get("releases", {})
        latest_release = max(
            releases.items(),
            key=lambda x: x[1][0]["upload_time"] if x[1] else "",
            default=(None, []),
        )

        downloads_data = {"data": {"last_day": 0, "last_week": 0, "last_month": 0}}
        try:
            stats_response = await client.get(stats_url)
            stats_response.raise_for_status()
            downloads_data = stats_response.json()
        except Exception:
            pass

        stats = downloads_data.get("data", {})

        return {
            "name": name,
            "description": info.get("summary", ""),
            "url": info.get("project_url", f"https://pypi.org/project/{name}/"),
            "language": "Python",
            "stars": None,
            "forks": None,
            "downloads_day": stats.get("last_day", 0),
            "downloads_week": stats.get("last_week", 0),
            "downloads_month": stats.get("last_month", 0),
            "likes": None,
            "last_activity": self._parse_datetime(
                latest_release[1][0]["upload_time"] if latest_release[1] else None
            ),
        }

    def _parse_datetime(self, date_str: Optional[str]) -> Optional[datetime]:
        if not date_str:
            return None
        try:
            return datetime.fromisoformat(date_str.replace("Z", "+00:00"))
        except (ValueError, AttributeError):
            return None
