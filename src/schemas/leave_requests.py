from pydantic import BaseModel
from datetime import datetime


class LeaveRequestCreate(BaseModel):
    start_date: datetime
    end_date: datetime
