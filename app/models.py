from tortoise import fields, models
from tortoise.contrib.pydantic import pydantic_model_creator
from passlib.hash import bcrypt


class Users(models.Model):
    """
    The User model.
    """

    # Tortoise-ORM automatically creates a FK called 'id' if it's not defined on the model
    email = fields.CharField(max_length=128, unique=True, index=True)
    password = fields.CharField(max_length=128)
    created_at = fields.DatetimeField(auto_now_add=True)
    modified_at = fields.DatetimeField(auto_now=True)

    class Meta:
        ordering = ['id']

    # class PydanticMeta:
    #     exclude = ['password_hash']

    def verify_password(self, password):
        return bcrypt.verify(password, self.password)

    def to_pydantic(self):
        return User_Pydantic.from_orm(self)

    def to_pydantic_simple(self):
        return UserSimple_Pydantic.from_orm(self)


User_Pydantic = pydantic_model_creator(Users, name='User')
UserSimple_Pydantic = pydantic_model_creator(Users, name='UserSimple', exclude_readonly=True)
