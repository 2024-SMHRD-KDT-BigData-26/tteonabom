# poi_reco.py
from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session
from DataBase.conn import get_db
from DataBase.models import TB_POI_RECO
from pydantic import BaseModel
from datetime import datetime

router = APIRouter()

class POIReco(BaseModel):
    reco_idx: int
    user_id: str
    poi_idx: int
    created_at: datetime
    reco_reason: str

    class Config:
        orm_mode = True

@router.post("/poi_reco")
async def create_poi_reco(poi_reco: POIReco, db: Session = Depends(get_db)):
    poi_reco_dict = {
        "reco_idx": poi_reco.reco_idx,
        "user_id": poi_reco.user_id,
        "poi_idx": poi_reco.poi_idx,
        "created_at": poi_reco.created_at,
        "reco_reason": poi_reco.reco_reason
    }
    return poi_reco_dict
