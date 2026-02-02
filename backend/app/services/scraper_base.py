from abc import ABC, abstractmethod
from typing import List, Dict, Any
from datetime import datetime
from sqlalchemy.orm import Session

from ..models.database import Skill, SkillMetrics, ScrapeLog


class BaseScraper(ABC):
    def __init__(self, db: Session):
        self.db = db

    @abstractmethod
    async def scrape(self) -> List[Dict[str, Any]]:
        pass

    @abstractmethod
    def get_source_name(self) -> str:
        pass

    def _log_scrape(
        self, items_scraped: int, status: str = "success", error_message: str = None
    ):
        scrape_log = ScrapeLog(
            source=self.get_source_name(),
            items_scraped=items_scraped,
            status=status,
            error_message=error_message,
            completed_at=datetime.utcnow(),
        )
        self.db.add(scrape_log)
        self.db.commit()

    async def run(self) -> Dict[str, Any]:
        try:
            items = await self.scrape()
            skills_created = 0
            skills_updated = 0

            for item in items:
                skill = (
                    self.db.query(Skill)
                    .filter(
                        Skill.name == item["name"],
                        Skill.source == self.get_source_name(),
                    )
                    .first()
                )

                if not skill:
                    skill = Skill(
                        name=item["name"],
                        source=self.get_source_name(),
                        description=item.get("description", ""),
                        url=item["url"],
                        language=item.get("language"),
                    )
                    self.db.add(skill)
                    skills_created += 1
                else:
                    skill.description = item.get("description", skill.description)
                    skill.url = item["url"]
                    skill.language = item.get("language", skill.language)
                    skill.updated_at = datetime.utcnow()
                    skills_updated += 1

                self.db.flush()

                metrics = SkillMetrics(
                    skill_id=skill.id,
                    stars=item.get("stars"),
                    forks=item.get("forks"),
                    downloads_day=item.get("downloads_day"),
                    downloads_week=item.get("downloads_week"),
                    downloads_month=item.get("downloads_month"),
                    likes=item.get("likes"),
                    last_activity=item.get("last_activity"),
                )
                self.db.add(metrics)

            self.db.commit()
            self._log_scrape(items_scraped=len(items))

            return {
                "status": "success",
                "items_scraped": len(items),
                "skills_created": skills_created,
                "skills_updated": skills_updated,
            }
        except Exception as e:
            self.db.rollback()
            self._log_scrape(items_scraped=0, status="error", error_message=str(e))
            raise
