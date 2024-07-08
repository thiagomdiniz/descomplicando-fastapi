from fastapi import APIRouter, status, HTTPException
from fastapi.exceptions import HTTPException
from sqlmodel import Session, select
from sqlalchemy.exc import IntegrityError
# from psycopg2.errors import UniqueViolation, ForeignKeyViolation

from ..db import ActiveSession
from ..auth import AuthenticatedUser
from ..models.user import User, UserRequest, UserResponse, Social
from ..models.post import Post, PostResponse

router = APIRouter()


@router.get("/", response_model=list[UserResponse])
async def list_users(*, session: Session = ActiveSession):
    """List all users."""
    users = session.exec(select(User)).all()
    return users


@router.get("/{username}/", response_model=UserResponse)
async def get_user_by_username(
    *, session: Session = ActiveSession, username: str
):
    """Get user by username"""
    query = select(User).where(User.username == username)
    user = session.exec(query).first()
    if not user:
        raise HTTPException(status_code=404, detail="User not found")
    return user


@router.post("/", response_model=UserResponse, status_code=201, responses={400: {"model": None}})
async def create_user(*, session: Session = ActiveSession, user: UserRequest):
    """Creates new user"""
    db_user = User.model_validate(user)  # transform UserRequest in User
    try:
        session.add(db_user)
        session.commit()
        session.refresh(db_user)
        return db_user
    except IntegrityError as e:
        session.rollback()
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail=f"{e.orig.diag.message_detail}")
        # match e.orig:
        #     case UniqueViolation():
        #         raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail=f"{e.orig.diag.message_detail}")
        #     case _:
        #         raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST)


@router.post(
    "/follow/{id}",
    status_code=status.HTTP_204_NO_CONTENT,
    responses={400: {"model": None}},
)
async def follow_user(
    *,
    session: Session = ActiveSession,
    user: User = AuthenticatedUser,
    id: int,
):
    """Follow another user"""
    social = Social()
    social.from_id = user.id
    social.to_id = id
    if id == user.id:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail="You can't follow yourself")
    
    try:
        session.add(social)
        session.commit()
        session.refresh(social)
    except IntegrityError as e:
        session.rollback()
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail=f"{e.orig.diag.message_detail}")
        # match e.orig:
        #     case UniqueViolation():
        #         raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail="You already follow this user")
        #     case ForeignKeyViolation():
        #         raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail="The user you are trying to follow does not exist")
        #     case _:
        #         raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail=f"{e.orig.diag.message_detail}")


@router.get("/timeline", response_model=list[PostResponse])
async def timeline(
    *,
    session: Session = ActiveSession,
    user: User = AuthenticatedUser
):
    """List all posts from all users that the user follows"""
    query = select(Post).join(
        User, Post.user_id == User.id
        ).join(
            Social, Social.to_id == User.id
        ).where(
            Social.from_id == user.id
        ).where(
            Post.parent == None
        )
    posts = session.exec(query).all()
    return posts