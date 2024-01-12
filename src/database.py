import os

from sqlmodel import SQLModel, Session, create_engine, select
from dotenv import load_dotenv

from src.models import User

load_dotenv()

DATABASE_USER = os.getenv("DATABASE_USER")
DATABASE_PASSWORD = os.getenv("DATABASE_PASSWORD")
DATABASE_DB = os.getenv("DATABASE_DB")
DATABASE_PORT = os.getenv("DATABASE_PORT")

DATABASE_URL = f"mysql://{DATABASE_USER}:{DATABASE_PASSWORD}@localhost:{DATABASE_PORT}/{DATABASE_DB}"

engine = create_engine(DATABASE_URL)


def init_db():
    SQLModel.metadata.create_all(engine)


def get_session():
    with Session(engine) as session:
        yield session


def create_user(user: User, session: Session) -> None:
    """
    Inserts a new user into the database.
    :param user: The user object containing the user information.
    :param session: The database session.
    """
    session.add(user)
    session.commit()


def get_user_by_username(username: str, session: Session) -> User:
    """
    Queries the database for a user by their username.
    :param username: The username to query.
    :param session: The database session.
    :return: `User` corresponding to the username or `None` if no user with that username exists.
    """
    query = select(User).where(User.username == username)
    result = session.exec(query).one_or_none()

    return result
