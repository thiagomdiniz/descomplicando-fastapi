"""Post related data models"""

from datetime import datetime
from typing import TYPE_CHECKING, Optional

from pydantic import BaseModel, ConfigDict
from sqlmodel import Field, Relationship, SQLModel, UniqueConstraint

from .user import User

if TYPE_CHECKING:
    from .user import User


class Post(SQLModel, table=True):
    """Represents the Post Model"""

    id: Optional[int] = Field(default=None, primary_key=True)
    text: str
    date: datetime = Field(default_factory=datetime.utcnow, nullable=False)

    user_id: Optional[int] = Field(foreign_key="user.id")
    parent_id: Optional[int] = Field(foreign_key="post.id")

    # It populates a `.posts` attribute to the `User` model.
    user: Optional["User"] = Relationship(back_populates="posts")

    # It populates `.replies` on this model
    parent: Optional["Post"] = Relationship(
        back_populates="replies",
        sa_relationship_kwargs=dict(remote_side="Post.id"),
    )
    # This lists all children to this post
    replies: list["Post"] = Relationship(back_populates="parent")

    def __lt__(self, other):
        """This enables post.replies.sort() to sort by date"""
        return self.date < other.date


class PostResponse(BaseModel):
    """Serializer for Post Response"""

    id: int
    text: str
    date: datetime
    user_id: int
    parent_id: Optional[int]


class PostResponseWithReplies(PostResponse):
    model_config = ConfigDict(from_attributes=True)

    replies: Optional[list["PostResponse"]] = None


class PostRequest(BaseModel):
    """Serializer for Post request payload"""
    model_config = ConfigDict(extra="allow", json_schema_extra={'examples': [{'parent_id': 0, 'text': 'string'}]})

    parent_id: int | None = None
    text: str


class Like(SQLModel, table=True):
    """Represents the Like Model"""
    __table_args__ = (
        UniqueConstraint("user_id", "post_id", name="unique_like_constraint"),
    )

    id: int | None = Field(default=None, primary_key=True)
    user_id: int = Field(foreign_key="user.id")
    post_id: int = Field(foreign_key="post.id")

    # It populates a `.likes` attribute to the `User` model.
    user: User | None = Relationship(back_populates="likes")