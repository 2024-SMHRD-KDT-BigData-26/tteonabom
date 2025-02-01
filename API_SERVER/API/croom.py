from datetime import datetime
from fastapi import APIRouter, Depends, HTTPException
from pydantic import BaseModel
from sqlalchemy.orm import Session
from DataBase.conn import get_db
from DataBase.models import TB_CROOM

router = APIRouter()

class Croom(BaseModel):
    croom_idx: int
    croom_title: str
    croom_info: str
    user_id: str
    croom_limit: int
    created_at: datetime
    croom_status: str

    class Config:
        from_attributes = True



# ✅ 채팅방 생성
@router.post("/crooms")
async def create_croom(croom: Croom, db: Session = Depends(get_db)):
    db_croom = TB_CROOM(**croom.dict())
    db.add(db_croom)
    db.commit()
    db.refresh(db_croom)
    return db_croom

# ✅ 채팅방 목록 조회
@router.get("/crooms")
async def get_all_crooms(db: Session = Depends(get_db)):
    return db.query(TB_CROOM).all()

# ✅ 특정 채팅방 조회
@router.get("/crooms/{croom_idx}")
async def get_croom(croom_idx: int, db: Session = Depends(get_db)):
    croom = db.query(TB_CROOM).filter(TB_CROOM.croom_idx == croom_idx).first()
    if not croom:
        raise HTTPException(status_code=404, detail="Croom not found")
    return croom

# ✅ 특정 사용자가 만든 채팅방 조회
@router.get("/crooms/user/{user_id}")
async def get_crooms_by_user(user_id: str, db: Session = Depends(get_db)):
    crooms = db.query(TB_CROOM).filter(TB_CROOM.user_id == user_id).all()
    return crooms

# ✅ 채팅방 정보 수정
@router.put("/crooms/{croom_idx}")
async def update_croom(croom_idx: int, croom: Croom, db: Session = Depends(get_db)):
    db_croom = db.query(TB_CROOM).filter(TB_CROOM.croom_idx == croom_idx).first()
    if not db_croom:
        raise HTTPException(status_code=404, detail="Croom not found")

    for key, value in croom.dict().items():
        setattr(db_croom, key, value)

    db.commit()
    db.refresh(db_croom)
    return db_croom

# ✅ 채팅방 삭제
@router.delete("/crooms/{croom_idx}")
async def delete_croom(croom_idx: int, db: Session = Depends(get_db)):
    db_croom = db.query(TB_CROOM).filter(TB_CROOM.croom_idx == croom_idx).first()
    if not db_croom:
        raise HTTPException(status_code=404, detail="Croom not found")

    db.delete(db_croom)
    db.commit()
    return {"detail": "Croom deleted successfully"}
