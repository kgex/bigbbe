from datetime import datetime
from pydantic import BaseModel
from typing import List, Optional


class QR_Attendance(BaseModel):
    type: str
    user_id: int
    in_time: datetime
    out_time: Optional[datetime]

    class Config:
        orm_mode = True
