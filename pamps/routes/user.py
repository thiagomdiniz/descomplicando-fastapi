from fastapi import APIRouter, status, HTTPException
from fastapi.exceptions import HTTPException
from sqlmodel import Session, select
from sqlalchemy.exc import IntegrityError
from psycopg2.errors import UniqueViolation

from ..db import ActiveSession
from ..models.user import User, UserRequest, UserResponse

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
        match e.orig:
            case UniqueViolation():
                raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail=f"{e.orig.diag.message_detail}")
            case _:
                raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST)
