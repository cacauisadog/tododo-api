import logging
from functools import lru_cache

from pydantic import AnyUrl, BaseSettings


log = logging.getLogger(__name__)


class Settings(BaseSettings):
    APP_NAME: str = 'Tododo API'
    ENVIRONMENT: str
    TESTING = 0
    DATABASE_URL: AnyUrl
    TEST_DATABASE_URL: AnyUrl
    SECRET_KEY: str
    TOKEN_ALGORITHM: str = 'HS256'
    HOST: str = 'localhost'
    PORT: int = 8000
    BASE_URL: str = '{}:{}/'.format(HOST, str(PORT))
    MODELS = ['app.models', 'aerich.models']

    class Config:
        env_file = '.env'


@lru_cache
def get_settings() -> BaseSettings:
    log.info('Loading config settings from the environment...')
    return Settings()
