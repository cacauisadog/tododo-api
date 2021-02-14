import logging

from app.db import init_db
from fastapi import FastAPI

from app.api import ping, users

log = logging.getLogger(__name__)


def create_application() -> FastAPI:
    app = FastAPI()
    app.include_router(ping.router)
    app.include_router(users.router, tags=['users'])

    return app


app = create_application()


@app.on_event('startup')
async def startup_event():
    log.info('Starting up...')
    init_db(app)


@app.on_event('shutdown')
async def shutdown_event():
    log.info('Shutting down...')
