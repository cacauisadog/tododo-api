import pytest
import asyncio

from typing import Generator

from starlette.testclient import TestClient
from tortoise.contrib.test import initializer, finalizer

from app.models import Users
from app.config.settings import Settings, get_settings
from app.main import create_application

settings: Settings = get_settings()


@pytest.fixture()
def client() -> Generator:
    # set up
    app = create_application()
    initializer(settings.MODELS, db_url=settings.TEST_DATABASE_URL)

    with TestClient(app) as test_client:

        # testing
        yield test_client

    # tear down
    finalizer()


@pytest.fixture()
def event_loop(client: TestClient) -> Generator:
    yield client.task.get_loop()


@pytest.fixture()
def user_joe(event_loop: asyncio.AbstractEventLoop) -> Users:
    async def create_user():
        user = await Users.create(email='joe@tododo.com', password='safepassword')
        return user

    return event_loop.run_until_complete(create_user())
