from typing import Annotated

from fastapi.security import OAuth2PasswordBearer, OAuth2PasswordRequestForm
from sqlmodel import Session

from src.services.users import UserService
from src.utils import hasher
from src.database import get_session
from fastapi import APIRouter, Depends, HTTPException, status

from src.models.users import User
from src.schemas.users import UserCreate

router = APIRouter()
oauth2_scheme = OAuth2PasswordBearer(tokenUrl="token")


async def get_current_user(
    token: Annotated[str, Depends(oauth2_scheme)],
    session: Session = Depends(get_session),
):
    user = UserService(session).get_user_by_username(username=token)
    if not user:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Invalid authentication credentials",
            headers={"WWW-Authenticate": "Bearer"},
        )
    return user


@router.post("/register", tags=["users"])
async def register(user_info: UserCreate, session: Session = Depends(get_session)):
    """
    Creates a user account.
    """
    if (
        UserService(session).get_user_by_username(username=user_info.username)
        is not None
    ):
        raise HTTPException(
            status_code=status.HTTP_409_CONFLICT, detail="Username already taken."
        )

    user: User = User(
        username=user_info.username,
        full_name=user_info.full_name,
        hashed_password=hasher.hash(user_info.password),
    )
    UserService(session).create_user(user=user)


@router.post("/token", tags=["users"])
async def login(
    form_data: Annotated[OAuth2PasswordRequestForm, Depends()],
    session: Session = Depends(get_session),
):
    """
    Logs a user into their account.
    """
    user: User = UserService(session).get_user_by_username(username=form_data.username)
    if not user or not hasher.verify(form_data.password, user.hashed_password):
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Incorrect username or password.",
        )

    return {"access_token": user.username, "token_type": "bearer"}