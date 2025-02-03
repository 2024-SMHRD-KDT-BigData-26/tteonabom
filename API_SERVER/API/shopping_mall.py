from datetime import datetime
from fastapi import APIRouter, Depends, HTTPException
from pydantic import BaseModel
from sqlalchemy.orm import Session
from DataBase.conn import get_db
from DataBase.models import TB_SHOPPING_MALL

router = APIRouter()


class ShoppingMallCreate(BaseModel):
    CATEGORY: str
    MALL_NM: str
    MALL_URL: str
    MALL_IMG: str

    class Config:
        from_attributes = True


class ShoppingMallResponse(BaseModel):
    MALL_IDX: int
    CATEGORY: str
    MALL_NM: str
    MALL_URL: str
    MALL_IMG: str
    MALL_LIKES: int
    CREATED_AT: datetime
    UPDATED_AT: datetime | None  # 수정되지 않았을 경우 `None`

    class Config:
        from_attributes = True


# ✅ 쇼핑몰 추가
@router.post("/shopping", response_model=ShoppingMallResponse)
async def create_mall(mall: ShoppingMallCreate, db: Session = Depends(get_db)):
    db_mall = TB_SHOPPING_MALL(
        **mall.dict(),
        MALL_LIKES=0,  # 초기 좋아요 수 0
        CREATED_AT=datetime.utcnow(),
        UPDATED_AT=None
    )
    db.add(db_mall)
    db.commit()
    db.refresh(db_mall)
    return db_mall


# ✅ 전체 쇼핑몰 조회
@router.get("/shopping", response_model=list[ShoppingMallResponse])
async def get_all_malls(db: Session = Depends(get_db)):
    return db.query(TB_SHOPPING_MALL).all()


# ✅ 특정 쇼핑몰 조회
@router.get("/shopping/{MALL_IDX}", response_model=ShoppingMallResponse)
async def get_mall(MALL_IDX: int, db: Session = Depends(get_db)):
    mall = db.query(TB_SHOPPING_MALL).filter(TB_SHOPPING_MALL.MALL_IDX == MALL_IDX).first()
    if not mall:
        raise HTTPException(status_code=404, detail="Mall not found")
    return mall


# ✅ 특정 카테고리의 쇼핑몰 조회
@router.get("/shopping/category/{CATEGORY}", response_model=list[ShoppingMallResponse])
async def get_malls_by_category(CATEGORY: str, db: Session = Depends(get_db)):
    malls = db.query(TB_SHOPPING_MALL).filter(TB_SHOPPING_MALL.CATEGORY == CATEGORY).all()
    return malls


# ✅ 쇼핑몰 정보 수정
@router.put("/shopping/{MALL_IDX}", response_model=ShoppingMallResponse)
async def update_mall(MALL_IDX: int, mall: ShoppingMallCreate, db: Session = Depends(get_db)):
    db_mall = db.query(TB_SHOPPING_MALL).filter(TB_SHOPPING_MALL.MALL_IDX == MALL_IDX).first()
    if not db_mall:
        raise HTTPException(status_code=404, detail="Mall not found")

    for key, value in mall.dict().items():
        setattr(db_mall, key, value)

    db_mall.UPDATED_AT = datetime.utcnow()  # 수정 시간 업데이트
    db.commit()
    db.refresh(db_mall)
    return db_mall


# ✅ 쇼핑몰 삭제
@router.delete("/shopping/{MALL_IDX}")
async def delete_mall(MALL_IDX: int, db: Session = Depends(get_db)):
    db_mall = db.query(TB_SHOPPING_MALL).filter(TB_SHOPPING_MALL.MALL_IDX == MALL_IDX).first()
    if not db_mall:
        raise HTTPException(status_code=404, detail="Mall not found")

    db.delete(db_mall)
    db.commit()
    return {"detail": "Mall deleted successfully"}


# ✅ 쇼핑몰 좋아요 증가
@router.put("/shopping/{MALL_IDX}/like")
async def like_mall(MALL_IDX: int, db: Session = Depends(get_db)):
    db_mall = db.query(TB_SHOPPING_MALL).filter(TB_SHOPPING_MALL.MALL_IDX == MALL_IDX).first()
    if not db_mall:
        raise HTTPException(status_code=404, detail="Mall not found")

    db_mall.MALL_LIKES += 1  # 좋아요 수 증가
    db.commit()
    db.refresh(db_mall)
    return {"detail": "Mall liked successfully", "MALL_LIKES": db_mall.MALL_LIKES}
