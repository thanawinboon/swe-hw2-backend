from pydantic import BaseModel


class UserCreate(BaseModel):
    full_name: str
    username: str
    password: str
