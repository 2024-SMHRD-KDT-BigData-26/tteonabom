# festival.py
from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session
from DataBase.conn import get_db
from DataBase.models import TB_FESTIVAL
from pydantic import BaseModel
from datetime import datetime

router = APIRouter()

class Festival(BaseModel):
    fest_idx: int
    fest_nm: str
    fest_desc: str
    fest_addr: str
    fest_url: str
    fest_tel: str
    fest_period: str
    fest_loc: str
    lat: float
    lon: float
    created_at: datetime
    updated_at: datetime

    class Config:
        orm_mode = True

@router.post("/festival")
async def create_festival(festival: Festival, db: Session = Depends(get_db)):
    festival_dict = {
        "fest_idx": festival.fest_idx,
        "fest_nm": festival.fest_nm,
        "fest_desc": festival.fest_desc,
        "fest_addr": festival.fest_addr,
        "fest_url": festival.fest_url,
        "fest_tel": festival.fest_tel,
        "fest_period": festival.fest_period,
        "fest_loc": festival.fest_loc,
        "lat": festival.lat,
        "lon": festival.lon,
        "created_at": festival.created_at,
        "updated_at": festival.updated_at
    }
    return festival_dict
