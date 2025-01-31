from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session
from DataBase.conn import get_db
from DataBase.models import TB_CROOM
from pydantic import BaseModel
from datetime import datetime

router = APIRouter()

class Croom(BaseModel):
    croom_idx: int
    croom_title: str
    croom_info: str
    user_id: str
    croom_limit: int
    croom_status: str
    created_at: datetime

    class Config:
        orm_mode = True  # SQLAlchemy 모델과 호환되도록 설정

@router.post("/croom")
async def create_croom(croom: Croom, db: Session = Depends(get_db)):
    croom_dict = {
        "croom_idx": croom.croom_idx,
        "croom_title": croom.croom_title,
        "croom_info": croom.croom_info,
        "user_id": croom.user_id,
        "croom_limit": croom.croom_limit,
        "croom_status": croom.croom_status,
        "created_at": croom.created_at
    }
    return croom_dict
