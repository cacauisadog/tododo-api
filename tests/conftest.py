import pytest

from typing import Generator

from starlette.testclient import TestClient
from tortoise.contrib.test import initializer, finalizer

from app.config.settings import Settings, get_settings
from app.main import create_application

settings: Settings = get_settings()


@pytest.fixture(scope="module")
def client() -> Generator:
    # set up
    app = create_application()
    initializer(settings.MODELS, db_url=settings.DATABASE_URL)

    with TestClient(app) as test_client:

        # testing
        yield test_client

    # tear down
    finalizer()


@pytest.fixture(scope='module')
def event_loop(client: TestClient) -> Generator:
    yield client.task.get_loop()
