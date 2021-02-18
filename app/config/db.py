from fastapi import FastAPI
from tortoise.contrib.fastapi import register_tortoise

from app.config.settings import Settings, get_settings

settings: Settings = get_settings()


def init_db(app: FastAPI) -> None:
    register_tortoise(
        app,
        db_url=settings.DATABASE_URL,
        modules={'models': settings.MODELS},
        generate_schemas=True,
        add_exception_handlers=True,
    )
