from datetime import datetime
from fastapi import APIRouter, Depends, HTTPException
from pydantic import BaseModel
from sqlalchemy.orm import Session
from DataBase.conn import get_db
from DataBase.models import TB_REVIEW

router = APIRouter()


class Review(BaseModel):
    REVIEW_IDX: int
    POI_IDX: int
    USER_ID: str
    REVIEW_CONTENT: str
    CREATED_AT: datetime
    UPDATED_AT: datetime

    class Config:
        from_attributes = True


# ✅ 리뷰 생성
@router.post("/reviews")
async def create_review(review: Review, db: Session = Depends(get_db)):
    db_review = TB_REVIEW(**review.dict())
    db.add(db_review)
    db.commit()
    db.refresh(db_review)
    return db_review


# ✅ 전체 리뷰 조회
@router.get("/reviews")
async def get_all_reviews(db: Session = Depends(get_db)):
    return db.query(TB_REVIEW).all()


# ✅ 특정 리뷰 조회
@router.get("/reviews/{REVIEW_IDX}")
async def get_review(REVIEW_IDX: int, db: Session = Depends(get_db)):
    review = db.query(TB_REVIEW).filter(TB_REVIEW.REVIEW_IDX == REVIEW_IDX).first()
    if not review:
        raise HTTPException(status_code=404, detail="Review not found")
    return review


# ✅ 특정 여행지의 리뷰 조회
@router.get("/reviews/poi/{POI_IDX}")
async def get_reviews_by_poi(POI_IDX: int, db: Session = Depends(get_db)):
    reviews = db.query(TB_REVIEW).filter(TB_REVIEW.POI_IDX == POI_IDX).all()
    return reviews


# ✅ 리뷰 수정
@router.put("/reviews/{REVIEW_IDX}")
async def update_review(REVIEW_IDX: int, review: Review, db: Session = Depends(get_db)):
    db_review = db.query(TB_REVIEW).filter(TB_REVIEW.REVIEW_IDX == REVIEW_IDX).first()
    if not db_review:
        raise HTTPException(status_code=404, detail="Review not found")

    for key, value in review.dict().items():
        setattr(db_review, key, value)

    db.commit()
    db.refresh(db_review)
    return db_review


# ✅ 리뷰 삭제
@router.delete("/reviews/{REVIEW_IDX}")
async def delete_review(REVIEW_IDX: int, db: Session = Depends(get_db)):
    db_review = db.query(TB_REVIEW).filter(TB_REVIEW.REVIEW_IDX == REVIEW_IDX).first()
    if not db_review:
        raise HTTPException(status_code=404, detail="Review not found")

    db.delete(db_review)
    db.commit()
    return {"detail": "Review deleted successfully"}
