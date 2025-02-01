from datetime import datetime
from fastapi import APIRouter, Depends, HTTPException
from pydantic import BaseModel
from sqlalchemy.orm import Session
from DataBase.conn import get_db
from DataBase.models import TB_REVIEW

router = APIRouter()

class Review(BaseModel):
    review_idx: int
    poi_idx: int
    user_id: str
    review_content: str
    review_views: int = 0
    review_likes: int = 0
    created_at: datetime
    updated_at: datetime

    class Config:
        orm_mode = True

# ✅ 리뷰 추가
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
@router.get("/reviews/{review_idx}")
async def get_review(review_idx: int, db: Session = Depends(get_db)):
    review = db.query(TB_REVIEW).filter(TB_REVIEW.review_idx == review_idx).first()
    if not review:
        raise HTTPException(status_code=404, detail="Review not found")
    return review

# ✅ 특정 여행지의 리뷰 조회
@router.get("/reviews/poi/{poi_idx}")
async def get_reviews_by_poi(poi_idx: int, db: Session = Depends(get_db)):
    reviews = db.query(TB_REVIEW).filter(TB_REVIEW.poi_idx == poi_idx).all()
    return reviews

# ✅ 특정 사용자의 리뷰 조회
@router.get("/reviews/user/{user_id}")
async def get_reviews_by_user(user_id: str, db: Session = Depends(get_db)):
    reviews = db.query(TB_REVIEW).filter(TB_REVIEW.user_id == user_id).all()
    return reviews

# ✅ 리뷰 수정
@router.put("/reviews/{review_idx}")
async def update_review(review_idx: int, review: Review, db: Session = Depends(get_db)):
    db_review = db.query(TB_REVIEW).filter(TB_REVIEW.review_idx == review_idx).first()
    if not db_review:
        raise HTTPException(status_code=404, detail="Review not found")

    for key, value in review.dict().items():
        setattr(db_review, key, value)

    db.commit()
    db.refresh(db_review)
    return db_review

# ✅ 리뷰 삭제
@router.delete("/reviews/{review_idx}")
async def delete_review(review_idx: int, db: Session = Depends(get_db)):
    db_review = db.query(TB_REVIEW).filter(TB_REVIEW.review_idx == review_idx).first()
    if not db_review:
        raise HTTPException(status_code=404, detail="Review not found")

    db.delete(db_review)
    db.commit()
    return {"detail": "Review deleted successfully"}

# ✅ 리뷰 좋아요 증가
@router.put("/reviews/{review_idx}/like")
async def like_review(review_idx: int, db: Session = Depends(get_db)):
    db_review = db.query(TB_REVIEW).filter(TB_REVIEW.review_idx == review_idx).first()
    if not db_review:
        raise HTTPException(status_code=404, detail="Review not found")

    db_review.review_likes += 1  # 좋아요 수 증가
    db.commit()
    db.refresh(db_review)
    return {"detail": "Review liked successfully", "review_likes": db_review.review_likes}
