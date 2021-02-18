from fastapi import APIRouter, Depends
from app.config.settings import Settings, get_settings

router = APIRouter()


@router.get('/ping')
async def pong(settings: Settings = Depends(get_settings)):
    return {
        'ping': 'pong',
        'environment': settings.ENVIRONMENT,
        'testing': settings.TESTING,
    }
