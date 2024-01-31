from datetime import datetime

from pydantic import BaseModel


class LeaveRequestCreate(BaseModel):
    start_date: datetime
    end_date: datetime
    reason: str
