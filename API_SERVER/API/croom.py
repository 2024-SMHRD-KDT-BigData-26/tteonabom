from datetime import datetime
from fastapi import APIRouter, Depends, HTTPException
from pydantic import BaseModel
from sqlalchemy.orm import Session
from DataBase.conn import get_db
from DataBase.models import TB_CROOM

router = APIRouter()

class Croom(BaseModel):
    CROOM_IDX: int
    CROOM_TITLE: str
    CROOM_INFO: str
    USER_ID: str
    CROOM_LIMIT: int
    CREATED_AT: datetime
    CROOM_STATUS: str

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
@router.get("/crooms/{CROOM_IDX}")
async def get_croom(CROOM_IDX: int, db: Session = Depends(get_db)):
    croom = db.query(TB_CROOM).filter(TB_CROOM.CROOM_IDX == CROOM_IDX).first()
    if not croom:
        raise HTTPException(status_code=404, detail="Croom not found")
    return croom

# ✅ 특정 사용자가 만든 채팅방 조회
@router.get("/crooms/user/{USER_ID}")
async def get_crooms_by_user(USER_ID: str, db: Session = Depends(get_db)):
    crooms = db.query(TB_CROOM).filter(TB_CROOM.USER_ID == USER_ID).all()
    return crooms

# ✅ 채팅방 정보 수정
@router.put("/crooms/{CROOM_IDX}")
async def update_croom(CROOM_IDX: int, croom: Croom, db: Session = Depends(get_db)):
    db_croom = db.query(TB_CROOM).filter(TB_CROOM.CROOM_IDX == CROOM_IDX).first()
    if not db_croom:
        raise HTTPException(status_code=404, detail="Croom not found")

    for key, value in croom.dict().items():
        setattr(db_croom, key, value)

    db.commit()
    db.refresh(db_croom)
    return db_croom

# ✅ 채팅방 삭제
@router.delete("/crooms/{CROOM_IDX}")
async def delete_croom(CROOM_IDX: int, db: Session = Depends(get_db)):
    db_croom = db.query(TB_CROOM).filter(TB_CROOM.CROOM_IDX == CROOM_IDX).first()
    if not db_croom:
        raise HTTPException(status_code=404, detail="Croom not found")

    db.delete(db_croom)
    db.commit()
    return {"detail": "Croom deleted successfully"}
