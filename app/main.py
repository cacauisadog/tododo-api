from app.config import Settings, get_settings
from fastapi import FastAPI, Depends

app = FastAPI()


@app.get('/ping')
async def pong(settings: Settings = Depends(get_settings)):
    return {
        'ping': 'pong',
        'environment': settings.environment,
        'testing': settings.testing,
    }
