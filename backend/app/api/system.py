from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session
from sqlalchemy import func
from datetime import datetime

from ..models.database import get_db
from ..models.schemas import StatsResponse, HealthResponse
from ..models import database as db_models

router = APIRouter(prefix="/api/v1", tags=["system"])


@router.get("/stats", response_model=StatsResponse)
async def get_stats(db: Session = Depends(get_db)):
    total_skills = db.query(func.count(db_models.Skill.id)).scalar()

    skills_by_source = (
        db.query(db_models.Skill.source, func.count(db_models.Skill.id))
        .group_by(db_models.Skill.source)
        .all()
    )

    last_updated = db.query(func.max(db_models.Skill.updated_at)).scalar()

    return StatsResponse(
        total_skills=total_skills,
        skills_by_source={source: count for source, count in skills_by_source},
        last_updated=last_updated or datetime.utcnow(),
    )


@router.get("/health", response_model=HealthResponse)
async def health_check():
    try:
        from ..models.database import engine

        with engine.connect() as conn:
            from sqlalchemy import text

            conn.execute(text("SELECT 1"))
        return HealthResponse(
            status="healthy", timestamp=datetime.utcnow(), database="connected"
        )
    except Exception as e:
        return HealthResponse(
            status="unhealthy", timestamp=datetime.utcnow(), database=f"error: {str(e)}"
        )


@router.get("/scrapes")
async def get_scrapes(limit: int = 20, db: Session = Depends(get_db)):
    scrapes = (
        db.query(db_models.ScrapeLog)
        .order_by(db_models.ScrapeLog.started_at.desc())
        .limit(limit)
        .all()
    )

    return {
        "scrapes": [
            {
                "id": s.id,
                "source": s.source,
                "items_scraped": s.items_scraped,
                "status": s.status,
                "error_message": s.error_message,
                "started_at": s.started_at,
                "completed_at": s.completed_at,
            }
            for s in scrapes
        ]
    }
