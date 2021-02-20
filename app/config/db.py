from fastapi import FastAPI
from tortoise.contrib.fastapi import register_tortoise

from app.config.settings import Settings, get_settings

settings: Settings = get_settings()

TORTOISE_ORM = {
    "connections": {"default": settings.DATABASE_URL},
    "apps": {
        "models": {
            "models": settings.MODELS,
            "default_connection": "default",
        },
    },
}


def init_db(app: FastAPI) -> None:
    register_tortoise(
        app,
        config=TORTOISE_ORM,
        generate_schemas=False,
        add_exception_handlers=True,
    )
