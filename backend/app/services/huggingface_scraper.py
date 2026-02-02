import httpx
from typing import List, Dict, Any, Optional
from datetime import datetime

from .scraper_base import BaseScraper


class HuggingFaceScraper(BaseScraper):
    def get_source_name(self) -> str:
        return "huggingface"

    async def scrape(self) -> List[Dict[str, Any]]:
        results = []
        base_url = "https://huggingface.co/api/models"

        queries = [
            {"sort": "downloads", "direction": -1, "limit": 50},
            {"sort": "likes", "direction": -1, "limit": 30},
        ]

        async with httpx.AsyncClient() as client:
            for params in queries:
                response = await client.get(base_url, params=params)
                response.raise_for_status()
                data = response.json()

                for model in data:
                    results.append(self._parse_model(model))

        return results[:60]

    def _parse_model(self, model: Dict[str, Any]) -> Dict[str, Any]:
        model_id = model.get("modelId", "")
        card_data = model.get("cardData", {})

        return {
            "name": model_id,
            "description": card_data.get("description", "")[:500],
            "url": f"https://huggingface.co/{model_id}",
            "language": card_data.get("language", "Python") or "Python",
            "stars": None,
            "forks": None,
            "downloads_day": None,
            "downloads_week": None,
            "downloads_month": model.get("downloads", 0),
            "likes": model.get("likes", 0),
            "last_activity": self._parse_datetime(model.get("lastModified")),
        }

    def _parse_datetime(self, date_str: Optional[str]) -> Optional[datetime]:
        if not date_str:
            return None
        try:
            return datetime.fromisoformat(date_str.replace("Z", "+00:00"))
        except (ValueError, AttributeError):
            return None
