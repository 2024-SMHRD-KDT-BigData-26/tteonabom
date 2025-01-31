# mall_reco.py
from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session
from DataBase.conn import get_db
from DataBase.models import TB_MALL_RECO
from pydantic import BaseModel
from datetime import datetime

router = APIRouter()

class MallReco(BaseModel):
    reco_idx: int
    chat_idx: int
    mall_idx: int
    created_at: datetime
    user_id: str

    class Config:
        orm_mode = True

@router.post("/mall_reco")
async def create_mall_reco(mall_reco: MallReco, db: Session = Depends(get_db)):
    mall_reco_dict = {
        "reco_idx": mall_reco.reco_idx,
        "chat_idx": mall_reco.chat_idx,
        "mall_idx": mall_reco.mall_idx,
        "created_at": mall_reco.created_at,
        "user_id": mall_reco.user_id
    }
    return mall_reco_dict
