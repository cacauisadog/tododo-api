import os
import pytest

from typing import Generator

from starlette.testclient import TestClient
from tortoise.contrib.test import initializer, finalizer

from app.config import Settings, get_settings
from app.main import create_application


def get_settings_override():
    return Settings(testing=1, database_url=os.environ.get("DATABASE_TEST_URL"))


@pytest.fixture(scope="module")
def client() -> Generator:
    # set up
    app = create_application()
    app.dependency_overrides[get_settings] = get_settings_override
    initializer(['app.models'], db_url=os.getenv('DATABASE_TEST_URL'))

    with TestClient(app) as test_client:

        # testing
        yield test_client

    # tear down
    finalizer()


@pytest.fixture(scope='module')
def event_loop(client: TestClient) -> Generator:
    yield client.task.get_loop()
