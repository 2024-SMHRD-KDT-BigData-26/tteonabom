# shopping_mall.py
from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session
from DataBase.conn import get_db
from DataBase.models import TB_SHOPPING_MALL
from pydantic import BaseModel
from datetime import datetime

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

@router.post("/shopping_mall")
async def create_shopping_mall(mall: ShoppingMall, db: Session = Depends(get_db)):
    mall_dict = {
        "mall_idx": mall.mall_idx,
        "category": mall.category,
        "mall_nm": mall.mall_nm,
        "mall_url": mall.mall_url,
        "mall_img": mall.mall_img,
        "mall_likes": mall.mall_likes,
        "created_at": mall.created_at,
        "updated_at": mall.updated_at
    }
    return mall_dict
