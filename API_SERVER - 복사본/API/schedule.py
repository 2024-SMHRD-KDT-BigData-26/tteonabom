# schedule.py
from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session
from DataBase.conn import get_db
from DataBase.models import TB_SCHEDULE
from pydantic import BaseModel
from datetime import datetime, date

router = APIRouter()

class Schedule(BaseModel):
    sche_idx: str
    tour_nm: str
    tour_type: str
    tour_desc: str
    st_dt: date
    ed_dt: date
    user_id: str
    created_at: datetime
    updated_at: datetime

    class Config:
        orm_mode = True

@router.post("/schedule")
async def create_schedule(schedule: Schedule, db: Session = Depends(get_db)):
    schedule_dict = {
        "sche_idx": schedule.sche_idx,
        "tour_nm": schedule.tour_nm,
        "tour_type": schedule.tour_type,
        "tour_desc": schedule.tour_desc,
        "st_dt": schedule.st_dt,
        "ed_dt": schedule.ed_dt,
        "user_id": schedule.user_id,
        "created_at": schedule.created_at,
        "updated_at": schedule.updated_at
    }
    return schedule_dict
