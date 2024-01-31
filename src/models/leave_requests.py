import enum
from datetime import datetime
from typing import Optional

from sqlmodel import Column, Enum, Field, SQLModel


class LeaveRequestStatus(str, enum.Enum):
    pending = "pending"
    approved = "approved"
    denied = "denied"


class LeaveRequest(SQLModel, table=True):
    id: Optional[int] = Field(default=None, primary_key=True)
    requester_id: Optional[int] = Field(default=None, foreign_key="user.id")
    reason: str
    status: LeaveRequestStatus = Field(
        sa_column=Column(Enum(LeaveRequestStatus)), default=LeaveRequestStatus.pending
    )
    start_date: datetime
    end_date: datetime
