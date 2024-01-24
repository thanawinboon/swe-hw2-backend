from sqlmodel import Field, SQLModel
from typing import Optional


class User(SQLModel, table=True):
    id: Optional[int] = Field(default=None, primary_key=True)
    full_name: str
    username: str = Field(index=True)
    hashed_password: bytes
    remaining_leave_days: int = Field(default=10)
    is_admin: bool = Field(default=False)
