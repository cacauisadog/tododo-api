from app.schemas import Status, UserCreate, UserUpdate
from fastapi import APIRouter, HTTPException

from tortoise.contrib.fastapi import HTTPNotFoundError
from tortoise.exceptions import DoesNotExist

from app.models import User_Pydantic, Users

router = APIRouter()


@router.get('', response_model=list[User_Pydantic])
async def get_users():
    return await User_Pydantic.from_queryset(Users.all())


@router.post('', response_model=User_Pydantic)
async def create_user(user: UserCreate):
    user_obj = await Users.create(**user.dict())
    return await User_Pydantic.from_tortoise_orm(user_obj)


@router.get('/{user_id}', response_model=User_Pydantic, responses={404: {'model': HTTPNotFoundError}})
async def get_user(user_id: int):
    try:
        return await User_Pydantic.from_queryset_single(Users.get(id=user_id))
    except DoesNotExist:
        raise HTTPException(status_code=404, detail='User not found.')


@router.put('/{user_id}', response_model=User_Pydantic, responses={404: {'model': HTTPNotFoundError}})
async def update_user(user_id: int, user: UserUpdate):
    try:
        await Users.filter(id=user_id).update(**user.dict(exclude_none=True))
        return await User_Pydantic.from_queryset_single(Users.get(id=user_id))
    except DoesNotExist:
        raise HTTPException(status_code=404, detail='User not found.')


@router.delete('/{user_id}', response_model=Status, responses={404: {'model': HTTPNotFoundError}})
async def delete_user(user_id: int):
    deleted_count = await Users.filter(id=user_id).delete()
    if not deleted_count:
        raise HTTPException(status_code=404, detail='User not found.')
    return Status(message=f'Deleted user {user_id}')
