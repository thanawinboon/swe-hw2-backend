import os

from sqlmodel import SQLModel, Session, create_engine, select
from dotenv import load_dotenv

from src.models.users import User
from src.utils import hasher

load_dotenv()

DATABASE_USER = os.getenv("DATABASE_USER")
DATABASE_PASSWORD = os.getenv("DATABASE_PASSWORD")
DATABASE_DB = os.getenv("DATABASE_DB")
DATABASE_PORT = os.getenv("DATABASE_PORT")

DATABASE_URL = (
    f"mysql://{DATABASE_USER}:{DATABASE_PASSWORD}"
    f"@localhost:{DATABASE_PORT}/{DATABASE_DB}"
)

engine = create_engine(DATABASE_URL)


def init_db():
    SQLModel.metadata.create_all(engine)

    with Session(engine) as session:
        query = select(User).where(User.username == "admin")
        result = session.exec(query).one_or_none()

        if result is None:
            admin = User(username="admin", hashed_password=hasher.hash("bigchungus"), full_name="Admin Istrator",
                         is_admin=True)
            session.add(admin)
            session.commit()


def get_session():
    with Session(engine) as session:
        yield session
