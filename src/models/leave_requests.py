from sqlmodel import Field, SQLModel
from typing import Optional
from datetime import datetime


class LeaveRequest(SQLModel, table=True):
    id: Optional[int] = Field(default=None, primary_key=True)
    requester_id: Optional[int] = Field(default=None, foreign_key="user.id")
    start_date: datetime
    end_date: datetime
