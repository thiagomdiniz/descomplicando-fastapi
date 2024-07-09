from fastapi import APIRouter, status
from fastapi.exceptions import HTTPException
from sqlmodel import Session, select
from sqlalchemy.exc import IntegrityError

from ..auth import AuthenticatedUser
from ..db import ActiveSession
from ..models.post import (
    Post,
    PostRequest,
    PostResponse,
    PostResponseWithReplies,
    Like,
)
from ..models.user import User

router = APIRouter()


@router.get("/", response_model=list[PostResponse])
async def list_posts(*, session: Session = ActiveSession):
    """List all posts without replies"""
    query = select(Post).where(Post.parent == None)
    posts = session.exec(query).all()
    return posts


@router.get("/{post_id}/", response_model=PostResponseWithReplies)
async def get_post_by_post_id(
    *,
    session: Session = ActiveSession,
    post_id: int,
):
    """Get post by post_id"""
    query = select(Post).where(Post.id == post_id)
    post = session.exec(query).first()
    if not post:
        raise HTTPException(status_code=404, detail="Post not found")
    return post


@router.get("/user/{username}/", response_model=list[PostResponse])
async def get_posts_by_username(
    *,
    session: Session = ActiveSession,
    username: str,
    include_replies: bool = False,
):
    """Get posts by username"""
    filters = [User.username == username]
    if not include_replies:
        filters.append(Post.parent == None)
    query = select(Post).join(User).where(*filters)
    posts = session.exec(query).all()
    return posts


@router.post("/", response_model=PostResponse, status_code=201)
async def create_post(
    *,
    session: Session = ActiveSession,
    user: User = AuthenticatedUser,
    post: PostRequest,
):
    """Creates new post"""

    post.user_id = user.id

    db_post = Post.model_validate(post)  # transform PostRequest in Post

    if post.parent_id:
        query = select(Post.id).where(Post.id == post.parent_id)
        parent = session.exec(query).first()
        if not parent:
            db_post.parent_id = None
    
    session.add(db_post)
    session.commit()
    session.refresh(db_post)
    return db_post


@router.post("/like/{post_id}", status_code=status.HTTP_204_NO_CONTENT, responses={400: {"model": None}})
async def like_post(
    *,
    session: Session = ActiveSession,
    user: User = AuthenticatedUser,
    post_id: int,
):
    """Likes a post"""
    like = Like()
    like.user_id = user.id
    like.post_id = post_id

    try:
        session.add(like)
        session.commit()
        session.refresh(like)
    except IntegrityError as e:
        session.rollback()
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail=f"{e.orig.diag.message_detail}")


@router.get("/likes/{username}", response_model=list[PostResponse])
async def get_likes_by_username(
    *,
    session: Session = ActiveSession,
    username: str,
):
    """Get likes by username"""
    query = select(Post).join(
            Like, Post.id == Like.post_id
        ).join(
            User, Like.user_id == User.id
        ).where(
            User.username == username
        ).where(
            Post.parent == None
        )
    posts = session.exec(query).all()
    return posts