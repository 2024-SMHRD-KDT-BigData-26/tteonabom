from datetime import datetime
from fastapi import APIRouter, Depends, HTTPException
from pydantic import BaseModel
from sqlalchemy.orm import Session
from DataBase.conn import get_db
from DataBase.models import TB_LIKE

router = APIRouter()


class Like(BaseModel):
    like_idx: int
    user_id: str
    mall_idx: int
    poi_idx: int
    created_at: datetime

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
@router.get("/like/user/{user_id}")
async def get_likes_by_user(user_id: str, db: Session = Depends(get_db)):
    likes = db.query(TB_LIKE).filter(TB_LIKE.user_id == user_id).all()
    return likes


# ✅ 특정 여행지의 좋아요 조회
@router.get("/like/poi/{poi_idx}")
async def get_likes_by_poi(poi_idx: int, db: Session = Depends(get_db)):
    likes = db.query(TB_LIKE).filter(TB_LIKE.poi_idx == poi_idx).all()
    return likes


# ✅ 특정 쇼핑몰의 좋아요 조회
@router.get("/like/mall/{mall_idx}")
async def get_likes_by_mall(mall_idx: int, db: Session = Depends(get_db)):
    likes = db.query(TB_LIKE).filter(TB_LIKE.mall_idx == mall_idx).all()
    return likes


# ✅ 좋아요 삭제
@router.delete("/like/{like_idx}")
async def delete_like(like_idx: int, db: Session = Depends(get_db)):
    db_like = db.query(TB_LIKE).filter(TB_LIKE.like_idx == like_idx).first()
    if not db_like:
        raise HTTPException(status_code=404, detail="Like not found")

    db.delete(db_like)
    db.commit()
    return {"detail": "Like removed successfully"}
