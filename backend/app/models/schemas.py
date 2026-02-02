from pydantic import BaseModel, Field
from datetime import datetime
from typing import Optional, Literal


class SkillMetrics(BaseModel):
    stars: Optional[int] = None
    forks: Optional[int] = None
    downloads_day: Optional[int] = None
    downloads_week: Optional[int] = None
    downloads_month: Optional[int] = None
    likes: Optional[int] = None
    last_activity: Optional[datetime] = None


class SkillBase(BaseModel):
    name: str = Field(..., min_length=1, max_length=255)
    source: Literal["github", "npm", "pypi", "huggingface"]
    description: str = Field(..., max_length=1000)
    url: str = Field(..., max_length=500)
    language: Optional[str] = Field(None, max_length=50)


class SkillCreate(SkillBase):
    pass


class SkillUpdate(SkillBase):
    name: Optional[str] = None


class Skill(SkillBase):
    id: int
    created_at: datetime
    updated_at: datetime
    metrics: Optional[SkillMetrics] = None

    class Config:
        from_attributes = True


class SkillMetricsCreate(BaseModel):
    skill_id: int
    stars: Optional[int] = None
    forks: Optional[int] = None
    downloads_day: Optional[int] = None
    downloads_week: Optional[int] = None
    downloads_month: Optional[int] = None
    likes: Optional[int] = None
    last_activity: Optional[datetime] = None


class ScrapeLogCreate(BaseModel):
    source: str
    items_scraped: int
    status: str = "success"
    error_message: Optional[str] = None


class ScrapeLog(BaseModel):
    id: int
    source: str
    items_scraped: int
    status: str
    error_message: Optional[str] = None
    started_at: datetime
    completed_at: Optional[datetime] = None

    class Config:
        from_attributes = True


class SkillsQueryParams(BaseModel):
    sort: Literal["latest", "hot", "used"] = "latest"
    source: Literal["github", "npm", "pypi", "huggingface", "all"] = "all"
    limit: int = Field(50, ge=1, le=100)


class SkillsResponse(BaseModel):
    skills: list[Skill]
    total: int
    sort_by: str
    updated_at: datetime


class StatsResponse(BaseModel):
    total_skills: int
    skills_by_source: dict[str, int]
    last_updated: datetime


class HealthResponse(BaseModel):
    status: str
    timestamp: datetime
    database: str
