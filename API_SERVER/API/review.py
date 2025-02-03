from datetime import datetime
from fastapi import APIRouter, Depends, HTTPException
from pydantic import BaseModel
from sqlalchemy.orm import Session
from DataBase.conn import get_db
from DataBase.models import TB_REVIEW

router = APIRouter()


class ReviewCreate(BaseModel):
    POI_IDX: int
    USER_ID: str
    REVIEW_CONTENT: str

    class Config:
        from_attributes = True


class ReviewResponse(BaseModel):
    REVIEW_IDX: int
    POI_IDX: int
    USER_ID: str
    REVIEW_CONTENT: str
    CREATED_AT: datetime
    UPDATED_AT: datetime | None  # 업데이트가 없을 수도 있음

    class Config:
        from_attributes = True


# ✅ 리뷰 생성
@router.post("/reviews", response_model=ReviewResponse)
async def create_review(review: ReviewCreate, db: Session = Depends(get_db)):
    db_review = TB_REVIEW(
        **review.dict(),
        CREATED_AT=datetime.utcnow(),  # 생성 시간 자동 설정
        UPDATED_AT=None  # 초기 생성 시 업데이트 없음
    )
    db.add(db_review)
    db.commit()
    db.refresh(db_review)
    return db_review


# ✅ 전체 리뷰 조회
@router.get("/reviews", response_model=list[ReviewResponse])
async def get_all_reviews(db: Session = Depends(get_db)):
    return db.query(TB_REVIEW).all()


# ✅ 특정 리뷰 조회
@router.get("/reviews/{REVIEW_IDX}", response_model=ReviewResponse)
async def get_review(REVIEW_IDX: int, db: Session = Depends(get_db)):
    review = db.query(TB_REVIEW).filter(TB_REVIEW.REVIEW_IDX == REVIEW_IDX).first()
    if not review:
        raise HTTPException(status_code=404, detail="Review not found")
    return review


# ✅ 특정 여행지의 리뷰 조회
@router.get("/reviews/poi/{POI_IDX}", response_model=list[ReviewResponse])
async def get_reviews_by_poi(POI_IDX: int, db: Session = Depends(get_db)):
    reviews = db.query(TB_REVIEW).filter(TB_REVIEW.POI_IDX == POI_IDX).all()
    return reviews


# ✅ 리뷰 수정
@router.put("/reviews/{REVIEW_IDX}", response_model=ReviewResponse)
async def update_review(REVIEW_IDX: int, review: ReviewCreate, db: Session = Depends(get_db)):
    db_review = db.query(TB_REVIEW).filter(TB_REVIEW.REVIEW_IDX == REVIEW_IDX).first()
    if not db_review:
        raise HTTPException(status_code=404, detail="Review not found")

    for key, value in review.dict().items():
        setattr(db_review, key, value)

    db_review.UPDATED_AT = datetime.utcnow()  # 수정 시간 업데이트
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
