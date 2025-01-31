# poi.py
from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session
from DataBase.conn import get_db
from DataBase.models import TB_POI
from pydantic import BaseModel
from datetime import datetime
from decimal import Decimal

router = APIRouter()

class POI(BaseModel):
    poi_idx: int
    poi_nm: str
    poi_info: str
    poi_addr: str
    poi_url: str
    poi_region: str
    poi_tel: str
    poi_period: str
    lat: Decimal
    lon: Decimal
    poi_likes: int
    created_at: datetime
    updated_at: datetime

    class Config:
        orm_mode = True

@router.post("/poi")
async def create_poi(poi: POI, db: Session = Depends(get_db)):
    poi_dict = {
        "poi_idx": poi.poi_idx,
        "poi_nm": poi.poi_nm,
        "poi_info": poi.poi_info,
        "poi_addr": poi.poi_addr,
        "poi_url": poi.poi_url,
        "poi_region": poi.poi_region,
        "poi_tel": poi.poi_tel,
        "poi_period": poi.poi_period,
        "lat": poi.lat,
        "lon": poi.lon,
        "poi_likes": poi.poi_likes,
        "created_at": poi.created_at,
        "updated_at": poi.updated_at
    }
    return poi_dict
