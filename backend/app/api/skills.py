from fastapi import APIRouter, Depends, Query
from sqlalchemy.orm import Session
from typing import Literal, Optional
from datetime import datetime

from ..models.database import get_db
from ..models.schemas import Skill, SkillsResponse, SkillsQueryParams
from ..models import database as db_models

router = APIRouter(prefix="/api/v1/skills", tags=["skills"])


@router.get("", response_model=SkillsResponse)
async def get_skills(
    sort: Literal["latest", "hot", "used"] = "latest",
    source: Literal["github", "npm", "pypi", "huggingface", "all"] = "all",
    limit: int = Query(50, ge=1, le=100),
    db: Session = Depends(get_db),
):
    query = db.query(db_models.Skill)

    if source != "all":
        query = query.filter(db_models.Skill.source == source)

    sort_column = None
    if sort == "latest":
        sort_column = db_models.Skill.updated_at.desc()
    elif sort == "hot":
        sort_column = db_models.SkillMetrics.downloads_week.desc()
    elif sort == "used":
        sort_column = db_models.SkillMetrics.downloads_month.desc()

    skills = (
        query.outerjoin(db_models.SkillMetrics).order_by(sort_column).limit(limit).all()
    )

    skill_list = []
    for skill in skills:
        metrics = skill.metrics[-1] if skill.metrics else None
        skill_data = Skill(
            id=skill.id,
            name=skill.name,
            source=skill.source,
            description=skill.description,
            url=skill.url,
            language=skill.language,
            created_at=skill.created_at,
            updated_at=skill.updated_at,
        )
        if metrics:
            skill_data.metrics = db_models.SkillMetrics(
                stars=metrics.stars,
                forks=metrics.forks,
                downloads_day=metrics.downloads_day,
                downloads_week=metrics.downloads_week,
                downloads_month=metrics.downloads_month,
                likes=metrics.likes,
                last_activity=metrics.last_activity,
            )
        skill_list.append(skill_data)

    return SkillsResponse(
        skills=skill_list,
        total=query.count(),
        sort_by=sort,
        updated_at=datetime.utcnow(),
    )


@router.get("/{skill_id}", response_model=Skill)
async def get_skill(skill_id: int, db: Session = Depends(get_db)):
    skill = db.query(db_models.Skill).filter(db_models.Skill.id == skill_id).first()
    if not skill:
        from fastapi import HTTPException

        raise HTTPException(status_code=404, detail="Skill not found")

    metrics = skill.metrics[-1] if skill.metrics else None
    skill_data = Skill(
        id=skill.id,
        name=skill.name,
        source=skill.source,
        description=skill.description,
        url=skill.url,
        language=skill.language,
        created_at=skill.created_at,
        updated_at=skill.updated_at,
    )
    if metrics:
        skill_data.metrics = db_models.SkillMetrics(
            stars=metrics.stars,
            forks=metrics.forks,
            downloads_day=metrics.downloads_day,
            downloads_week=metrics.downloads_week,
            downloads_month=metrics.downloads_month,
            likes=metrics.likes,
            last_activity=metrics.last_activity,
        )
    return skill_data


@router.get("/{skill_id}/history")
async def get_skill_history(
    skill_id: int, days: int = Query(30, ge=1, le=90), db: Session = Depends(get_db)
):
    skill = db.query(db_models.Skill).filter(db_models.Skill.id == skill_id).first()
    if not skill:
        from fastapi import HTTPException

        raise HTTPException(status_code=404, detail="Skill not found")

    from datetime import timedelta

    cutoff_date = datetime.utcnow() - timedelta(days=days)

    metrics = (
        db.query(db_models.SkillMetrics)
        .filter(
            db_models.SkillMetrics.skill_id == skill_id,
            db_models.SkillMetrics.recorded_at >= cutoff_date,
        )
        .order_by(db_models.SkillMetrics.recorded_at.desc())
        .all()
    )

    return {
        "skill_id": skill_id,
        "skill_name": skill.name,
        "days": days,
        "history": [
            {
                "recorded_at": m.recorded_at,
                "stars": m.stars,
                "forks": m.forks,
                "downloads_day": m.downloads_day,
                "downloads_week": m.downloads_week,
                "downloads_month": m.downloads_month,
                "likes": m.likes,
            }
            for m in metrics
        ],
    }
