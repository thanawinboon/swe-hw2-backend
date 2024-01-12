from pydantic import BaseModel
from sqlmodel import Field, SQLModel
from typing import Optional


class UserCreate(BaseModel):
    full_name: str
    username: str
    password: str


class User(SQLModel, table=True):
    id: Optional[int] = Field(default=None, primary_key=True)
    full_name: str
    username: str = Field(index=True)
    hashed_password: str
