import asyncio
import pytest
import tortoise

from fastapi.testclient import TestClient

from app.models import Users


def test_create_user(client: TestClient, event_loop: asyncio.AbstractEventLoop):
    payload = {'email': 'admin@tododo.com', 'password': 'safepassword'}

    response = client.post('/users', json=payload)
    assert response.status_code == 200, response.text
    data = response.json()
    assert data['email'] == payload['email']
    assert 'id' in data
    user_id = data['id']

    user_obj = event_loop.run_until_complete(_get_user_from_db(user_id))
    assert user_obj.id == user_id


def test_get_all_users_empty(client: TestClient):
    response = client.get('/users')
    assert response.status_code == 200, response.text
    data = response.json()
    assert data == []


def test_get_all_users(client: TestClient, user_joe: Users):
    response = client.get('/users')
    assert response.status_code == 200, response.text
    joe_json = user_joe.to_pydantic().json(separators=(',', ':'))
    assert joe_json in response.text


def test_update_user(client: TestClient, event_loop: asyncio.AbstractEventLoop, user_joe: Users):
    payload = {'email': 'superjoe@tododo.com', 'password': 'evensaferpassword'}

    response = client.put(f'/users/{user_joe.id}', json=payload)
    assert response.status_code == 200, response.text
    data = response.json()
    assert data['email'] == payload['email']

    joe = event_loop.run_until_complete(_get_user_from_db(user_joe.id))
    assert joe.email == payload['email']
    assert joe.password != user_joe.password


def test_delete_user(client: TestClient, event_loop: asyncio.AbstractEventLoop, user_joe: Users):
    response = client.delete(f'/users/{user_joe.id}')
    assert response.status_code == 200, response.text
    data = response.json()
    assert data['message'] == f'Deleted user {user_joe.id}'

    with pytest.raises(tortoise.exceptions.DoesNotExist):
        event_loop.run_until_complete(_get_user_from_db(user_joe.id))


def test_get_nonexistant_user(client: TestClient):
    response = client.get('/users/66')
    assert response.status_code == 404, response.text
    data = response.json()
    assert data['detail'] == 'User not found.'


def test_update_nonexistant_user(client: TestClient):
    response = client.put('/users/66', json={'password': 'whateveritwontworkanyway'})
    assert response.status_code == 404, response.text
    data = response.json()
    assert data['detail'] == 'User not found.'


def test_delete_nonexistant_user(client: TestClient):
    response = client.delete('/users/66')
    assert response.status_code == 404, response.text
    data = response.json()
    assert data['detail'] == 'User not found.'


async def _get_user_from_db(user_id):
    user = await Users.get(id=user_id)
    return user
