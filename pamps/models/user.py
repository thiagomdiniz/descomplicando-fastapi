from typing import TYPE_CHECKING, Annotated
from datetime import datetime
from sqlmodel import Field, SQLModel, Relationship, UniqueConstraint
from pydantic import BaseModel, BeforeValidator

from ..security import get_password_hash

if TYPE_CHECKING:
    from .post import Post, Like


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

    # it populates the .user attribute on the Like Model
    likes: list["Like"] = Relationship(back_populates="user")


class UserResponse(BaseModel):
    """Serializer for User Response"""

    username: str
    avatar: str | None = None
    bio: str | None = None


class UserRequest(UserBase):
    """Serializer for User request payload"""
    
    password: Annotated[str, HashedPassword]


class Social(SQLModel, table=True):
    """Represents the Social Model"""
    __table_args__ = (
        UniqueConstraint("from_id", "to_id", name="unique_follow_constraint"),
    )
    id: int | None = Field(default=None, primary_key=True)
    from_id: int = Field(foreign_key="user.id")
    to_id: int = Field(foreign_key="user.id")
    date: datetime = Field(default_factory=datetime.utcnow, nullable=False)


# class SocialRequest(BaseModel):
#     """Serializer for Social request payload"""
#     to_id: int

#     class Config:
#         extra = Extra.allow