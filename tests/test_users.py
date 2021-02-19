from app.models import Users
import asyncio

from fastapi.testclient import TestClient


def test_create_user(client: TestClient, event_loop: asyncio.AbstractEventLoop):
    payload = {'email': 'admin@tododo.com', 'password': 'safepassword'}
    _create_user(client, event_loop, payload)


def _create_user(client: TestClient, event_loop: asyncio.AbstractEventLoop, payload: dict):
    response = client.post('/users/', json={'email': 'admin@tododo.com', 'password': 'safepassword'})
    assert response.status_code == 200, response.text
    data = response.json()
    assert data['email'] == payload['email']
    assert 'id' in data
    user_id = data['id']

    async def get_user_by_db():
        user = await Users.get(id=user_id)
        return user

    user_obj = event_loop.run_until_complete(get_user_by_db())
    assert user_obj.id == user_id

    return user_obj
