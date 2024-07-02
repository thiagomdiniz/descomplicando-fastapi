from typing import TYPE_CHECKING, Annotated
from datetime import datetime
from sqlmodel import Field, SQLModel, Relationship, UniqueConstraint
from pydantic import BaseModel, BeforeValidator

from ..security import get_password_hash

if TYPE_CHECKING:
    from .post import Post


HashedPassword = BeforeValidator(get_password_hash)

class UserBase(SQLModel):
    """Represents the User Model"""
    email: str = Field(unique=True, nullable=False)
    username: str = Field(unique=True, nullable=False)
    avatar: str | None = None
    bio: str | None = None
    password: str #Annotated[str, HashedPassword]


class User(UserBase, table=True):
    """Represents the User table in the database"""
    
    id: int | None = Field(default=None, primary_key=True)

    # it populates the .user attribute on the Post Model
    posts: list["Post"] = Relationship(back_populates="user")


class UserResponse(BaseModel):
    """Serializer for User Response"""

    username: str
    avatar: str | None = None
    bio: str | None = None


class UserRequest(UserBase):
    """Serializer for User request payload"""
    
    password: Annotated[str, HashedPassword]
