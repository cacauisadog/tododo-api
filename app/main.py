from app.config.settings import Settings, get_settings
import logging

from app.config.db import init_db
from fastapi import FastAPI

from app.api import ping, users

log = logging.getLogger(__name__)
settings: Settings = get_settings()


def create_application() -> FastAPI:
    app = FastAPI(title=settings.APP_NAME)
    app.include_router(ping.router)
    app.include_router(users.router, prefix='/users', tags=['Users'])

    return app


app = create_application()


@app.on_event('startup')
async def startup_event():
    log.info('Starting up...')
    init_db(app)


@app.on_event('shutdown')
async def shutdown_event():
    log.info('Shutting down...')
