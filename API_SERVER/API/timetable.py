# timetable.py
from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session
from DataBase.conn import get_db
from DataBase.models import TB_TIMETABLE
from pydantic import BaseModel
from datetime import datetime, date, time

router = APIRouter()

class Timetable(BaseModel):
    tt_idx: int
    sche_idx: str
    tt_date: date
    st_time: time
    poi_idx: int
    tt_order: int
    created_at: datetime
    updated_at: datetime

    class Config:
        orm_mode = True

@router.post("/timetable")
async def create_timetable(timetable: Timetable, db: Session = Depends(get_db)):
    timetable_dict = {
        "tt_idx": timetable.tt_idx,
        "sche_idx": timetable.sche_idx,
        "tt_date": timetable.tt_date,
        "st_time": timetable.st_time,
        "poi_idx": timetable.poi_idx,
        "tt_order": timetable.tt_order,
        "created_at": timetable.created_at,
        "updated_at": timetable.updated_at
    }
    return timetable_dict
