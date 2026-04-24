import httpx
from typing import List, Dict, Any, Optional
from datetime import datetime

from .scraper_base import BaseScraper
from ..core.config import settings


class GitHubSkillsScraper(BaseScraper):
    """GitHub 技能代码爬虫 - 搜索具体的 AI 技能实现代码"""

    def get_source_name(self) -> str:
        return "github"

    async def scrape(self) -> List[Dict[str, Any]]:
        base_url = "https://api.github.com/search/repositories"
        headers = {}
        if settings.github_token:
            headers["Authorization"] = f"Bearer {settings.github_token}"

        results = []
        queries = [
            ("awesome-openai+language:python", "stars"),
            ("awesome-chatgpt+language:python", "stars"),
            ("awesome-langchain+language:python", "stars"),
            ("awesome-llm+language:python", "stars"),
            ("awesome-anthropic+language:python", "stars"),
            ("openai+examples+language:python", "stars"),
            ("chatgpt+examples+language:python", "stars"),
            ("langchain+examples+language:python", "stars"),
            ("claude+examples+language:python", "stars"),
            ("cohere+examples+language:python", "stars"),
            ("rag+implementation+language:python", "stars"),
            ("rag+example+language:python", "stars"),
            ("agent+framework+language:python", "stars"),
            ("autonomous+agent+language:python", "stars"),
            ("function+calling+language:python", "stars"),
            ("prompt+engineering+language:python", "stars"),
            ("fine+tuning+examples+language:python", "stars"),
            ("api+integration+example+language:python", "stars"),
            ("streaming+implementation+language:python", "stars"),
        ]

        async with httpx.AsyncClient() as client:
            for query, sort_by in queries:
                params = {"q": query, "sort": sort_by, "order": "desc", "per_page": 30}

                response = await client.get(base_url, headers=headers, params=params)
                response.raise_for_status()
                data = response.json()

                for item in data.get("items", []):
                    results.append(self._parse_repo(item))

        return results[:100]

    def _parse_repo(self, repo: Dict[str, Any]) -> Dict[str, Any]:
        name = f"{repo['owner']['login']}/{repo['name']}"

        description = repo.get("description", "")
        keywords = repo.get("topics", [])

        is_skill_code = self._is_skill_code(repo, description, keywords)

        if is_skill_code:
            description = f"[Skill Code] {description}"

        return {
            "name": name,
            "description": description,
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

    def _is_skill_code(
        self, repo: Dict[str, Any], description: str, keywords: List[str]
    ) -> bool:
        """判断是否是技能代码实现而不是通用工具包"""

        name = repo.get("name", "").lower()
        description_lower = description.lower()
        keywords_lower = [k.lower() for k in keywords]

        skill_keywords = [
            "example",
            "tutorial",
            "cookbook",
            "guide",
            "boilerplate",
            "implementation",
            "integration",
            "sample",
            "demo",
            "pattern",
            "template",
            "snippet",
            "starter",
            "awesome",
            "list",
            "framework",
            "library",
            "api",
            "sdk",
            "client",
            "wrapper",
            "binding",
        ]

        tool_keywords = [
            "runtime",
            "engine",
            "platform",
            "container",
            "model",
            "checkpoint",
            "quantization",
            "acceleration",
            "deployment",
            "serving",
            "inference",
            "optimization",
        ]

        description_skill_indicators = [
            "how to",
            "build a",
            "create a",
            "implementing",
            "example of",
            "tutorial on",
            "guide for",
            "step by step",
            "walkthrough",
            "example code",
        ]

        has_skill_keywords = any(kw in description_lower for kw in skill_keywords)
        has_tool_keywords = any(
            kw in name or kw in description_lower for kw in tool_keywords
        )
        has_description_indicators = any(
            ind in description_lower for ind in description_skill_indicators
        )

        has_awesome = any(kw in name for kw in ["awesome", "list", "collection"])

        if has_awesome:
            return False

        if (
            has_tool_keywords
            and not has_skill_keywords
            and not has_description_indicators
        ):
            return False

        return has_skill_keywords or has_description_indicators

    def _parse_datetime(self, date_str: Optional[str]) -> Optional[datetime]:
        if not date_str:
            return None
        try:
            return datetime.fromisoformat(date_str.replace("Z", "+00:00"))
        except (ValueError, AttributeError):
            return None
