import sys

sys.path.append("/Users/sophon/workspace/skill_detector/backend")

from app.models.database import SessionLocal, init_db, Skill, SkillMetrics
from sqlalchemy import func
from datetime import datetime


def add_sample_skills():
    """添加示例 AI 技能到数据库"""

    db = SessionLocal()
    init_db()

    sample_skills = [
        {
            "name": "openai/openai",
            "source": "github",
            "description": "Python client for OpenAI API",
            "url": "https://github.com/openai/openai",
            "language": "Python",
            "metrics": {
                "stars": 120000,
                "forks": 20000,
                "last_activity": datetime.utcnow(),
            },
        },
        {
            "name": "langchain-ai/langchain",
            "source": "github",
            "description": "Building applications with LLMs through composability",
            "url": "https://github.com/langchain-ai/langchain",
            "language": "Python",
            "metrics": {
                "stars": 85000,
                "forks": 12000,
                "last_activity": datetime.utcnow(),
            },
        },
        {
            "name": "huggingface/transformers",
            "source": "github",
            "description": "🤗 Transformers: State-of-the-art Machine Learning for PyTorch, TensorFlow and JAX",
            "url": "https://github.com/huggingface/transformers",
            "language": "Python",
            "metrics": {
                "stars": 125000,
                "forks": 28000,
                "last_activity": datetime.utcnow(),
            },
        },
        {
            "name": "microsoft/semantic-kernel",
            "source": "github",
            "description": "Integrate cutting-edge LLM technology rapidly and easily into your code",
            "url": "https://github.com/microsoft/semantic-kernel",
            "language": "TypeScript",
            "metrics": {
                "stars": 18500,
                "forks": 3200,
                "last_activity": datetime.utcnow(),
            },
        },
        {
            "name": "ai",
            "source": "npm",
            "description": "AI SDK by Vercel - The AI Toolkit for TypeScript and JavaScript",
            "url": "https://www.npmjs.com/package/ai",
            "language": "TypeScript",
            "metrics": {
                "downloads_week": 70019828,
                "downloads_month": 257772351,
                "last_activity": datetime.utcnow(),
            },
        },
        {
            "name": "@google/generative-ai",
            "source": "npm",
            "description": "Google AI JavaScript SDK",
            "url": "https://www.npmjs.com/package/@google/generative-ai",
            "language": "TypeScript",
            "metrics": {
                "downloads_week": 2241270,
                "downloads_month": 7929955,
                "last_activity": datetime.utcnow(),
            },
        },
        {
            "name": "@ai-sdk/react",
            "source": "npm",
            "description": "React UI components for AI SDK",
            "url": "https://www.npmjs.com/package/@ai-sdk/react",
            "language": "TypeScript",
            "metrics": {
                "downloads_week": 3430719,
                "downloads_month": 13081858,
                "last_activity": datetime.utcnow(),
            },
        },
        {
            "name": "tensorflow",
            "source": "pypi",
            "description": "TensorFlow is an end-to-end open source machine learning platform",
            "url": "https://pypi.org/project/tensorflow/",
            "language": "Python",
            "metrics": {
                "downloads_week": 1946150,
                "downloads_month": 8233215,
                "last_activity": datetime.utcnow(),
            },
        },
        {
            "name": "torch",
            "source": "pypi",
            "description": "Tensors and Dynamic neural networks in Python with strong GPU acceleration",
            "url": "https://pypi.org/project/torch/",
            "language": "Python",
            "metrics": {
                "downloads_week": 2577210,
                "downloads_month": 10243680,
                "last_activity": datetime.utcnow(),
            },
        },
    ]

    created_count = 0
    updated_count = 0

    for sample in sample_skills:
        skill = (
            db.query(Skill)
            .filter(Skill.name == sample["name"], Skill.source == sample["source"])
            .first()
        )

        metrics_data = sample["metrics"]
        if not skill:
            skill = Skill(
                name=sample["name"],
                source=sample["source"],
                description=sample["description"],
                url=sample["url"],
                language=sample.get("language"),
                created_at=datetime.utcnow(),
                updated_at=datetime.utcnow(),
            )
            db.add(skill)
            db.flush()
            created_count += 1
        else:
            skill.description = sample["description"]
            skill.url = sample["url"]
            skill.language = sample.get("language")
            skill.updated_at = datetime.utcnow()
            updated_count += 1

        skill_metrics = SkillMetrics(
            skill_id=skill.id,
            stars=metrics_data.get("stars"),
            forks=metrics_data.get("forks"),
            downloads_day=metrics_data.get("downloads_day"),
            downloads_week=metrics_data.get("downloads_week"),
            downloads_month=metrics_data.get("downloads_month"),
            likes=metrics_data.get("likes"),
            last_activity=metrics_data.get("last_activity"),
            recorded_at=datetime.utcnow(),
        )
        db.add(skill_metrics)

    db.commit()

    total_skills = db.query(func.count(Skill.id)).scalar()

    print(f"\n{'=' * 60}")
    print(f"✅ 示例数据添加成功！")
    print(f"{'=' * 60}")
    print(f"\n📊 统计信息:")
    print(f"  • 新增技能: {created_count}")
    print(f"  • 更新技能: {updated_count}")
    print(f"  • 总技能数: {total_skills}")
    print(f"\n📚 添加的技能示例:")
    for skill in sample_skills:
        source_name = skill["source"].upper()
        print(f"  • [{source_name}] {skill['name']}")
    print(f"\n{'=' * 60}")


if __name__ == "__main__":
    add_sample_skills()
