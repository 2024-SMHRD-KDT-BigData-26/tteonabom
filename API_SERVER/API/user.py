from datetime import datetime
from fastapi import APIRouter, Depends, HTTPException
from pydantic import BaseModel
from sqlalchemy.orm import Session
from DataBase.conn import get_db
from DataBase.models import TB_USERS

router = APIRouter()

class User(BaseModel):
    user_id: str
    user_pw: str
    user_nick: str
    user_profile_img: str
    kakao_id: int
    auth_provider: str
    created_at: datetime
    updated_at: datetime

    class Config:
        orm_mode = True

# 사용자 생성 API
@router.post("/users")
async def create_user(user: User, db: Session = Depends(get_db)):
    db_user = TB_USERS(**user.dict())
    db.add(db_user)
    db.commit()
    db.refresh(db_user)
    return db_user


# 사용자 조회 API (단일 사용자)
@router.get("/users/{user_id}")
async def get_user(user_id: str, db: Session = Depends(get_db)):
    user = db.query(TB_USERS).filter(TB_USERS.user_id == user_id).first()
    if not user:
        raise HTTPException(status_code=404, detail="User not found")
    return user


# 사용자 전체 조회 API
@router.get("/users")
async def get_all_users(db: Session = Depends(get_db)):
    users = db.query(TB_USERS).all()
    return users

# 사용자 정보 수정 API
@router.put("/users/{user_id}")
async def update_user(user_id: str, user: User, db: Session = Depends(get_db)):
    db_user = db.query(TB_USERS).filter(TB_USERS.user_id == user_id).first()
    if not db_user:
        raise HTTPException(status_code=404, detail="User not found")
    for key, value in user.dict().items():
        setattr(db_user, key, value)
    db.commit()
    db.refresh(db_user)
    return db_user

# 사용자 삭제 API
@router.delete("/users/{user_id}")
async def delete_user(user_id: str, db: Session = Depends(get_db)):
    db_user = db.query(TB_USERS).filter(TB_USERS.user_id == user_id).first()
    if not db_user:
        raise HTTPException(status_code=404, detail="User not found")
    db.delete(db_user)
    db.commit()
    return {"detail": "User deleted successfully"}
