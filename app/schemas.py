from typing import Optional
from pydantic import BaseModel, EmailStr, validator, constr

from passlib.hash import bcrypt
from pydantic.class_validators import root_validator


class Status(BaseModel):
    message: str


# Properties to receive via API on creation
class UserCreate(BaseModel):
    email: EmailStr
    password: constr(min_length=8, max_length=128)

    @validator('password')
    def hash_password(cls, password):
        return bcrypt.hash(password)


# Properties to receive via API on update
class UserUpdate(BaseModel):
    email: Optional[EmailStr]
    password: Optional[constr(min_length=8, max_length=128)]

    @root_validator
    def validate_email_and_password_cant_both_be_empty(cls, values):
        assert any(values.values()), 'Either email or password is required.'
        return values

    @validator('password')
    def hash_password(cls, password):
        return bcrypt.hash(password)
