from typing import Optional, TYPE_CHECKING, Annotated
from sqlmodel import Field, SQLModel, Relationship
from pydantic import BaseModel, BeforeValidator

from ..security import get_password_hash
#from ..security import HashedPassword # pydantic <2

if TYPE_CHECKING:
    from .post import Post


HashedPassword = BeforeValidator(get_password_hash)

class User(SQLModel, table=True):
    """Represents the User Model"""
    
    id: Optional[int] = Field(default=None, primary_key=True)
    email: str = Field(unique=True, nullable=False)
    username: str = Field(unique=True, nullable=False)
    avatar: Optional[str] = None
    bio: Optional[str] = None
    password: Annotated[str, HashedPassword]
    #password: HashedPassword # pydantic <2

    # it populates the .user attribute on the Post Model
    posts: list["Post"] = Relationship(back_populates="user")


class UserResponse(BaseModel):
    """Serializer for User Response"""

    username: str
    avatar: Optional[str] = None
    bio: Optional[str] = None


class UserRequest(BaseModel):
    """Serializer for User request payload"""

    email: str
    username: str
    password: str
    avatar: Optional[str] = None
    bio: Optional[str] = None