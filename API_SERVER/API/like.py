from datetime import datetime
from fastapi import APIRouter, Depends, HTTPException
from pydantic import BaseModel
from sqlalchemy.orm import Session
from DataBase.conn import get_db
from DataBase.models import TB_LIKE

router = APIRouter()


class Like(BaseModel):
    LIKE_IDX: int
    USER_ID: str
    MALL_IDX: int
    POI_IDX: int
    CREATED_AT: datetime

    class Config:
        from_attributes = True


# ✅ 좋아요 추가
@router.post("/like")
async def create_like(like: Like, db: Session = Depends(get_db)):
    db_like = TB_LIKE(**like.dict())
    db.add(db_like)
    db.commit()
    db.refresh(db_like)
    return db_like


# ✅ 전체 좋아요 조회
@router.get("/like")
async def get_all_likes(db: Session = Depends(get_db)):
    return db.query(TB_LIKE).all()


# ✅ 특정 사용자의 좋아요 조회
@router.get("/like/user/{USER_ID}")
async def get_likes_by_user(USER_ID: str, db: Session = Depends(get_db)):
    likes = db.query(TB_LIKE).filter(TB_LIKE.USER_ID == USER_ID).all()
    return likes


# ✅ 특정 여행지의 좋아요 조회
@router.get("/like/poi/{POI_IDX}")
async def get_likes_by_poi(POI_IDX: int, db: Session = Depends(get_db)):
    likes = db.query(TB_LIKE).filter(TB_LIKE.POI_IDX == POI_IDX).all()
    return likes


# ✅ 특정 쇼핑몰의 좋아요 조회
@router.get("/like/mall/{MALL_IDX}")
async def get_likes_by_mall(MALL_IDX: int, db: Session = Depends(get_db)):
    likes = db.query(TB_LIKE).filter(TB_LIKE.MALL_IDX == MALL_IDX).all()
    return likes


# ✅ 좋아요 삭제
@router.delete("/like/{LIKE_IDX}")
async def delete_like(LIKE_IDX: int, db: Session = Depends(get_db)):
    db_like = db.query(TB_LIKE).filter(TB_LIKE.LIKE_IDX == LIKE_IDX).first()
    if not db_like:
        raise HTTPException(status_code=404, detail="Like not found")

    db.delete(db_like)
    db.commit()
    return {"detail": "Like removed successfully"}
