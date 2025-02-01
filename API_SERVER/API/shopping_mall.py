from datetime import datetime
from fastapi import APIRouter, Depends, HTTPException
from pydantic import BaseModel
from sqlalchemy.orm import Session
from DataBase.conn import get_db
from DataBase.models import TB_SHOPPING_MALL

router = APIRouter()

class ShoppingMall(BaseModel):
    mall_idx: int
    category: str
    mall_nm: str
    mall_url: str
    mall_img: str
    mall_likes: int
    created_at: datetime
    updated_at: datetime

    class Config:
        orm_mode = True

# ✅ 쇼핑몰 추가
@router.post("/shopping")
async def create_mall(mall: ShoppingMall, db: Session = Depends(get_db)):
    db_mall = TB_SHOPPING_MALL(**mall.dict())
    db.add(db_mall)
    db.commit()
    db.refresh(db_mall)
    return db_mall

# ✅ 전체 쇼핑몰 조회
@router.get("/shopping")
async def get_all_malls(db: Session = Depends(get_db)):
    return db.query(TB_SHOPPING_MALL).all()

# ✅ 특정 쇼핑몰 조회
@router.get("/shopping/{mall_idx}")
async def get_mall(mall_idx: int, db: Session = Depends(get_db)):
    mall = db.query(TB_SHOPPING_MALL).filter(TB_SHOPPING_MALL.mall_idx == mall_idx).first()
    if not mall:
        raise HTTPException(status_code=404, detail="Mall not found")
    return mall

# ✅ 특정 카테고리의 쇼핑몰 조회
@router.get("/shopping/category/{category}")
async def get_malls_by_category(category: str, db: Session = Depends(get_db)):
    malls = db.query(TB_SHOPPING_MALL).filter(TB_SHOPPING_MALL.category == category).all()
    return malls

# ✅ 쇼핑몰 정보 수정
@router.put("/shopping/{mall_idx}")
async def update_mall(mall_idx: int, mall: ShoppingMall, db: Session = Depends(get_db)):
    db_mall = db.query(TB_SHOPPING_MALL).filter(TB_SHOPPING_MALL.mall_idx == mall_idx).first()
    if not db_mall:
        raise HTTPException(status_code=404, detail="Mall not found")

    for key, value in mall.dict().items():
        setattr(db_mall, key, value)

    db.commit()
    db.refresh(db_mall)
    return db_mall

# ✅ 쇼핑몰 삭제
@router.delete("/shopping/{mall_idx}")
async def delete_mall(mall_idx: int, db: Session = Depends(get_db)):
    db_mall = db.query(TB_SHOPPING_MALL).filter(TB_SHOPPING_MALL.mall_idx == mall_idx).first()
    if not db_mall:
        raise HTTPException(status_code=404, detail="Mall not found")

    db.delete(db_mall)
    db.commit()
    return {"detail": "Mall deleted successfully"}

# ✅ 쇼핑몰 좋아요 증가
@router.put("/shopping/{mall_idx}/like")
async def like_mall(mall_idx: int, db: Session = Depends(get_db)):
    db_mall = db.query(TB_SHOPPING_MALL).filter(TB_SHOPPING_MALL.mall_idx == mall_idx).first()
    if not db_mall:
        raise HTTPException(status_code=404, detail="Mall not found")

    db_mall.mall_likes += 1  # 좋아요 수 증가
    db.commit()
    db.refresh(db_mall)
    return {"detail": "Mall liked successfully", "mall_likes": db_mall.mall_likes}
