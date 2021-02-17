from app.schemas import Status, UserCreate, UserUpdate
from fastapi import APIRouter, HTTPException

from tortoise.contrib.fastapi import HTTPNotFoundError

from app.models import User_Pydantic, Users

router = APIRouter()


@router.get('/', response_model=list[User_Pydantic])
async def get_users():
    return await User_Pydantic.from_queryset(Users.all())


@router.post('/', response_model=User_Pydantic)
async def create_user(user: UserCreate):
    user_obj = await Users.create(**user.dict())
    return await User_Pydantic.from_tortoise_orm(user_obj)


@router.get('/{user_id}', response_model=User_Pydantic, responses={404: {'model': HTTPNotFoundError}})
async def get_user(user_id: int):
    return await User_Pydantic.from_queryset_single(Users.get(id=user_id))


@router.put('/{user_id}', response_model=User_Pydantic, responses={404: {'model': HTTPNotFoundError}})
async def update_user(user_id: int, user: UserUpdate):
    await Users.filter(id=user_id).update(**user.dict(exclude_none=True))
    return await User_Pydantic.from_queryset_single(Users.get(id=user_id))


@router.delete('/{user_id}', response_model=Status, responses={404: {'model': HTTPNotFoundError}})
async def delete_user(user_id: int):
    deleted_count = await Users.filter(id=user_id).delete()
    if not deleted_count:
        raise HTTPException(status_code=404, detail=f'User {user_id} not found.')
    return Status(message=f'Deleted user {user_id}')
