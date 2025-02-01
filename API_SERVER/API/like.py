# mall_reco.py
from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session
from DataBase.conn import get_db
from DataBase.models import TB_LIKE
from pydantic import BaseModel
from datetime import datetime

router = APIRouter()

class Like(BaseModel):
    like_idx: int
    user_idx: int
    mall_idx: int
    poi_idx: int
    created_at: datetime

    class Config:
        orm_mode = True

@router.post("/like")
async def create_like(like: Like, db: Session = Depends(get_db)):
    like_dict = {
        "like_idx": like.like_idx,
        "user_idx": like.user_idx,
        "mall_idx": like.mall_idx,
        "poi_idx": like.poi_idx,
        "created_at": like.created_at

    }
    return like_dict
