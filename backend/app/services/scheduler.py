from apscheduler.schedulers.asyncio import AsyncIOScheduler
from apscheduler.triggers.interval import IntervalTrigger
from sqlalchemy.orm import Session

from .scraper_base import BaseScraper
from .github_scraper import GitHubScraper
from .npm_scraper import NpmScraper
from .pypi_scraper import PyPIScraper
from .huggingface_scraper import HuggingFaceScraper
from ..core.config import settings


class ScrapingScheduler:
    def __init__(self):
        self.scheduler = AsyncIOScheduler()
        self.scrapers = {
            "github": GitHubScraper,
            "npm": NpmScraper,
            "pypi": PyPIScraper,
            "huggingface": HuggingFaceScraper,
        }

    def start(self):
        self.scheduler.add_job(
            self._scrape_github,
            IntervalTrigger(minutes=settings.github_scrape_interval_minutes),
            id="github_scrape",
            replace_existing=True,
        )
        self.scheduler.add_job(
            self._scrape_npm,
            IntervalTrigger(hours=settings.npm_scrape_interval_hours),
            id="npm_scrape",
            replace_existing=True,
        )
        self.scheduler.add_job(
            self._scrape_pypi,
            IntervalTrigger(hours=settings.pypi_scrape_interval_hours),
            id="pypi_scrape",
            replace_existing=True,
        )
        self.scheduler.add_job(
            self._scrape_huggingface,
            IntervalTrigger(minutes=settings.huggingface_scrape_interval_minutes),
            id="huggingface_scrape",
            replace_existing=True,
        )
        self.scheduler.start()

    def stop(self):
        self.scheduler.shutdown()

    async def _scrape_github(self):
        await self._run_scraper("github")

    async def _scrape_npm(self):
        await self._run_scraper("npm")

    async def _scrape_pypi(self):
        await self._run_scraper("pypi")

    async def _scrape_huggingface(self):
        await self._run_scraper("huggingface")

    async def _run_scraper(self, source: str):
        from ..models.database import SessionLocal

        db = SessionLocal()
        try:
            scraper_class = self.scrapers.get(source)
            if scraper_class:
                scraper = scraper_class(db)
                result = await scraper.run()
                print(f"{source} scrape completed: {result}")
        except Exception as e:
            print(f"Error scraping {source}: {e}")
        finally:
            db.close()

    async def trigger_scrape(self, source: str):
        await self._run_scraper(source)
