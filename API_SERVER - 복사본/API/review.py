# review.py
from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session
from DataBase.conn import get_db
from DataBase.models import TB_REVIEW
from pydantic import BaseModel
from datetime import datetime

router = APIRouter()

class Review(BaseModel):
    review_idx: int
    poi_idx: int
    user_id: str
    review_content: str
    review_views: int
    review_likes: int
    created_at: datetime
    updated_at: datetime

    class Config:
        orm_mode = True

@router.post("/review")
async def create_review(review: Review, db: Session = Depends(get_db)):
    review_dict = {
        "review_idx": review.review_idx,
        "poi_idx": review.poi_idx,
        "user_id": review.user_id,
        "review_content": review.review_content,
        "review_views": review.review_views,
        "review_likes": review.review_likes,
        "created_at": review.created_at,
        "updated_at": review.updated_at
    }
    return review_dict
