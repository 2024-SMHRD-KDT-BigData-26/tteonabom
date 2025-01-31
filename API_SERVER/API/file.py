# file.py
from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session
from DataBase.conn import get_db
from DataBase.models import TB_FILE
from pydantic import BaseModel
from datetime import datetime

router = APIRouter()

class File(BaseModel):
    file_idx: int
    poi_idx: int
    file_nm: str
    file_size: int
    file_ext: str
    created_at: datetime
    updated_at: datetime
    user_id: str
    disp_order: int
    review_idx: int

    class Config:
        orm_mode = True

@router.post("/file")
async def create_file(file: File, db: Session = Depends(get_db)):
    file_dict = {
        "file_idx": file.file_idx,
        "poi_idx": file.poi_idx,
        "file_nm": file.file_nm,
        "file_size": file.file_size,
        "file_ext": file.file_ext,
        "created_at": file.created_at,
        "updated_at": file.updated_at,
        "user_id": file.user_id,
        "disp_order": file.disp_order,
        "review_idx": file.review_idx
    }
    return file_dict
