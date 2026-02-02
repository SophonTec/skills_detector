from sqlalchemy import (
    Column,
    Integer,
    Text,
    String,
    DateTime,
    ForeignKey,
    create_engine,
)
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker, relationship
from datetime import datetime
import os

Base = declarative_base()


class Skill(Base):
    __tablename__ = "skills"

    id = Column(Integer, primary_key=True, index=True)
    name = Column(String(255), unique=True, nullable=False, index=True)
    source = Column(String(50), nullable=False, index=True)
    description = Column(Text)
    url = Column(String(500))
    language = Column(String(50))
    created_at = Column(DateTime, default=datetime.utcnow)
    updated_at = Column(DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)

    metrics = relationship(
        "SkillMetrics", back_populates="skill", cascade="all, delete-orphan"
    )


class SkillMetrics(Base):
    __tablename__ = "skill_metrics"

    id = Column(Integer, primary_key=True)
    skill_id = Column(Integer, ForeignKey("skills.id"), nullable=False, index=True)
    stars = Column(Integer, default=0)
    forks = Column(Integer, default=0)
    downloads_day = Column(Integer, default=0)
    downloads_week = Column(Integer, default=0)
    downloads_month = Column(Integer, default=0)
    likes = Column(Integer, default=0)
    last_activity = Column(DateTime)
    recorded_at = Column(DateTime, default=datetime.utcnow, index=True)

    skill = relationship("Skill", back_populates="metrics")


class ScrapeLog(Base):
    __tablename__ = "scrapes"

    id = Column(Integer, primary_key=True)
    source = Column(String(50), nullable=False, index=True)
    items_scraped = Column(Integer, default=0)
    status = Column(String(20), default="success")
    error_message = Column(Text)
    started_at = Column(DateTime, default=datetime.utcnow)
    completed_at = Column(DateTime, index=True)


DATABASE_URL = f"sqlite:///{os.getenv('DATABASE_PATH', './skills.db')}"

engine = create_engine(
    DATABASE_URL, connect_args={"check_same_thread": False}, echo=False
)

SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)


def init_db():
    Base.metadata.create_all(bind=engine)


def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()
