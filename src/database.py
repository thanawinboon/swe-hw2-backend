import os

from dotenv import load_dotenv
from sqlmodel import Session, SQLModel, create_engine, select

from src.models.users import User
from src.utils import hasher

load_dotenv()

DB_USER = os.environ.get("DB_USER", "postgres")
DB_PASSWORD = os.environ.get("DB_PASSWORD", "postgres")
DB_HOST = os.environ.get("DB_HOST", "localhost")
DB_PORT = os.environ.get("DB_PORT", 5432)
DB_NAME = os.environ.get("DB_NAME", "postgres")

DATABASE_URL = f"postgresql://{DB_USER}:{DB_PASSWORD}@{DB_HOST}:{DB_PORT}/{DB_NAME}"

engine = create_engine(DATABASE_URL)


def init_db():
    SQLModel.metadata.create_all(engine)

    with Session(engine) as session:
        query = select(User).where(User.username == "admin")
        result = session.exec(query).one_or_none()

        if result is None:
            admin = User(
                username="admin",
                hashed_password=hasher.hash("bigchungus"),
                full_name="Admin Istrator",
                is_admin=True,
            )
            session.add(admin)
            session.commit()


def get_session():
    with Session(engine) as session:
        yield session
