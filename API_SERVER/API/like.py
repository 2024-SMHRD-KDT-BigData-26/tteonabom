from datetime import datetime
from fastapi import APIRouter, Depends, HTTPException
from pydantic import BaseModel
from sqlalchemy.orm import Session
from typing import Optional
from DataBase.conn import get_db
from DataBase.models import TB_LIKE

router = APIRouter()


# ✅ 좋아요 요청 모델 (입력 시 `LIKE_IDX`, `CREATED_AT` 제외)
class LikeCreate(BaseModel):
    USER_ID: str
    MALL_IDX: Optional[int] = None
    POI_IDX: Optional[int] = None

    class Config:
        from_attributes = True


# ✅ 좋아요 응답 모델 (모든 필드 포함)
class LikeResponse(LikeCreate):
    LIKE_IDX: int
    CREATED_AT: datetime


# ✅ 좋아요 추가
@router.post("/like", response_model=LikeResponse)
async def create_like(like: LikeCreate, db: Session = Depends(get_db)):
    db_like = TB_LIKE(**like.dict())
    db.add(db_like)
    db.commit()
    db.refresh(db_like)
    return db_like


# ✅ 전체 좋아요 조회
@router.get("/like", response_model=list[LikeResponse])
async def get_all_likes(db: Session = Depends(get_db)):
    return db.query(TB_LIKE).all()


# ✅ 특정 사용자의 좋아요 조회
@router.get("/like/user/{USER_ID}", response_model=list[LikeResponse])
async def get_likes_by_user(USER_ID: str, db: Session = Depends(get_db)):
    likes = db.query(TB_LIKE).filter(TB_LIKE.USER_ID == USER_ID).all()
    return likes


# ✅ 특정 여행지의 좋아요 조회
@router.get("/like/poi/{POI_IDX}", response_model=list[LikeResponse])
async def get_likes_by_poi(POI_IDX: int, db: Session = Depends(get_db)):
    likes = db.query(TB_LIKE).filter(TB_LIKE.POI_IDX == POI_IDX).all()
    return likes


# ✅ 특정 쇼핑몰의 좋아요 조회
@router.get("/like/mall/{MALL_IDX}", response_model=list[LikeResponse])
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
