from fastapi import FastAPI, Request
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import JSONResponse
from fastapi.exceptions import RequestValidationError
from starlette.exceptions import HTTPException as StarletteHTTPException
from datetime import datetime

from .core.config import settings
from .models.database import init_db, get_db
from .api import skills, system
from .services.scheduler import ScrapingScheduler


scheduler = ScrapingScheduler()


def create_app() -> FastAPI:
    app = FastAPI(
        title="AI Skills Tracker API",
        description="API for tracking and ranking AI skills from various sources",
        version="1.0.0",
    )

    app.add_middleware(
        CORSMiddleware,
        allow_origins=[settings.frontend_url],
        allow_credentials=True,
        allow_methods=["*"],
        allow_headers=["*"],
    )

    app.include_router(skills.router)
    app.include_router(system.router)

    @app.on_event("startup")
    async def startup_event():
        init_db()
        scheduler.start()

    @app.on_event("shutdown")
    async def shutdown_event():
        scheduler.stop()

    @app.exception_handler(StarletteHTTPException)
    async def http_exception_handler(request: Request, exc: StarletteHTTPException):
        return JSONResponse(
            status_code=exc.status_code,
            content={"detail": exc.detail, "timestamp": datetime.utcnow().isoformat()},
        )

    @app.exception_handler(RequestValidationError)
    async def validation_exception_handler(
        request: Request, exc: RequestValidationError
    ):
        return JSONResponse(
            status_code=422,
            content={
                "detail": exc.errors(),
                "timestamp": datetime.utcnow().isoformat(),
            },
        )

    @app.post("/api/v1/scrape/{source}")
    async def trigger_scrape(source: str):
        if source not in ["github", "npm", "pypi", "huggingface"]:
            return JSONResponse(
                status_code=400, content={"detail": f"Invalid source: {source}"}
            )
        await scheduler.trigger_scrape(source)
        return {"status": "scraping started", "source": source}

    return app


app = create_app()
