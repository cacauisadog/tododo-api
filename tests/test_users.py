from app.models import Users
import asyncio

from fastapi.testclient import TestClient


def test_user_crud_operations(client: TestClient, event_loop: asyncio.AbstractEventLoop):
    payload = {'email': 'admin@tododo.com', 'password': 'safepassword'}

    assert _get_all_users(client) == []
    created_user_obj = _create_user(client, event_loop, payload)
    created_user_dict = _get_user(client, created_user_obj.id)
    assert created_user_dict in _get_all_users(client)

    update_payload = {'email': 'user@tododo.com'}
    updated_user_dict = _update_user(client, created_user_dict, update_payload)
    assert updated_user_dict in _get_all_users(client)

    _delete_user(client, updated_user_dict['id'])

    assert _get_all_users(client) == []
    _get_user(client, created_user_obj.id, expected_status_code=404)
    _update_user(client, created_user_dict, update_payload, expected_status_code=404)
    _delete_user(client, updated_user_dict['id'], expected_status_code=404)


def _create_user(client: TestClient, event_loop: asyncio.AbstractEventLoop, payload: dict):
    response = client.post('/users', json=payload)
    assert response.status_code == 200, response.text
    data = response.json()
    assert data['email'] == payload['email']
    assert 'id' in data
    user_id = data['id']

    user_obj = event_loop.run_until_complete(_get_user_by_db(user_id))
    assert user_obj.id == user_id

    return user_obj


def _get_all_users(client: TestClient):
    response = client.get('/users')
    assert response.status_code == 200, response.text
    return response.json()


def _get_user(client: TestClient, user_id: int, expected_status_code: int = 200):
    response = client.get(f'/users/{user_id}')
    assert response.status_code == expected_status_code, response.text

    if expected_status_code == 200:
        user_json = response.json()
        assert user_json['id'] == user_id

        return user_json


def _update_user(client: TestClient, user_dict: dict, update_payload: dict, expected_status_code: int = 200):
    response = client.put(f'/users/{user_dict["id"]}', json=update_payload)
    assert response.status_code == expected_status_code, response.text

    if expected_status_code == 200:
        updated_user_json = response.json()
        assert updated_user_json['id'] == user_dict['id']
        assert updated_user_json['email'] == update_payload['email']

        return updated_user_json


def _delete_user(client: TestClient, user_id: int, expected_status_code=200):
    response = client.delete(f'/users/{user_id}')
    assert response.status_code == expected_status_code, response.text

    if expected_status_code == 200:
        res = response.json()
        assert res['message'] == f'Deleted user {user_id}'


async def _get_user_by_db(user_id):
    user = await Users.get(id=user_id)
    return user
