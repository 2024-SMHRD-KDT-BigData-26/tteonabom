from datetime import datetime
from fastapi import APIRouter, Depends, HTTPException
from pydantic import BaseModel
from sqlalchemy.orm import Session
from DataBase.conn import get_db
from DataBase.models import TB_MALL_RECO

router = APIRouter()


class MallReco(BaseModel):
    RECO_IDX: int
    CHAT_IDX: int
    MALL_IDX: int
    CREATED_AT: datetime
    USER_ID: str

    class Config:
        from_attributes = True


# ✅ 쇼핑몰 추천 추가
@router.post("/mall_reco")
async def create_mall_reco(mall_reco: MallReco, db: Session = Depends(get_db)):
    db_mall_reco = TB_MALL_RECO(**mall_reco.dict())
    db.add(db_mall_reco)
    db.commit()
    db.refresh(db_mall_reco)
    return db_mall_reco


# ✅ 전체 쇼핑몰 추천 조회
@router.get("/mall_reco")
async def get_all_mall_reco(db: Session = Depends(get_db)):
    return db.query(TB_MALL_RECO).all()


# ✅ 특정 쇼핑몰 추천 조회
@router.get("/mall_reco/{MALL_IDX}")
async def get_mall_reco_by_mall(MALL_IDX: int, db: Session = Depends(get_db)):
    mall_recos = db.query(TB_MALL_RECO).filter(TB_MALL_RECO.MALL_IDX == MALL_IDX).all()
    return mall_recos


# ✅ 특정 사용자의 쇼핑몰 추천 조회
@router.get("/mall_reco/user/{USER_ID}")
async def get_mall_reco_by_user(USER_ID: str, db: Session = Depends(get_db)):
    mall_recos = db.query(TB_MALL_RECO).filter(TB_MALL_RECO.USER_ID == USER_ID).all()
    return mall_recos


# ✅ 쇼핑몰 추천 수정
@router.put("/mall_reco/{RECO_IDX}")
async def update_mall_reco(RECO_IDX: int, mall_reco: MallReco, db: Session = Depends(get_db)):
    db_mall_reco = db.query(TB_MALL_RECO).filter(TB_MALL_RECO.RECO_IDX == RECO_IDX).first()
    if not db_mall_reco:
        raise HTTPException(status_code=404, detail="Mall recommendation not found")

    for key, value in mall_reco.dict().items():
        setattr(db_mall_reco, key, value)

    db.commit()
    db.refresh(db_mall_reco)
    return db_mall_reco


# ✅ 쇼핑몰 추천 삭제
@router.delete("/mall_reco/{RECO_IDX}")
async def delete_mall_reco(RECO_IDX: int, db: Session = Depends(get_db)):
    db_mall_reco = db.query(TB_MALL_RECO).filter(TB_MALL_RECO.RECO_IDX == RECO_IDX).first()
    if not db_mall_reco:
        raise HTTPException(status_code=404, detail="Mall recommendation not found")

    db.delete(db_mall_reco)
    db.commit()
    return {"detail": "Mall recommendation deleted successfully"}
