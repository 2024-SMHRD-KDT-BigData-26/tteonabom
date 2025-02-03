from datetime import datetime
from fastapi import APIRouter, Depends, HTTPException
from pydantic import BaseModel
from sqlalchemy.orm import Session
from DataBase.conn import get_db
from DataBase.models import TB_USERS

router = APIRouter()

class User(BaseModel):
    USER_ID: str
    USER_PW: str
    USER_NICK: str
    USER_PROFILE_IMG: str
    KAKAO_ID: int
    AUTH_PROVIDER: str
    CREATED_AT: datetime
    UPDATED_AT: datetime

    class Config:
        from_attributes = True

# ✅ 사용자 생성 API
@router.post("/users")
async def create_user(user: User, db: Session = Depends(get_db)):
    db_user = TB_USERS(**user.dict())
    db.add(db_user)
    db.commit()
    db.refresh(db_user)
    return db_user


# ✅ 사용자 조회 API (단일 사용자)
@router.get("/users/{USER_ID}")
async def get_user(USER_ID: str, db: Session = Depends(get_db)):
    user = db.query(TB_USERS).filter(TB_USERS.USER_ID == USER_ID).first()
    if not user:
        raise HTTPException(status_code=404, detail="User not found")
    return user


# ✅ 사용자 전체 조회 API
@router.get("/users")
async def get_all_users(db: Session = Depends(get_db)):
    users = db.query(TB_USERS).all()
    return users

# ✅ 사용자 정보 수정 API
@router.put("/users/{USER_ID}")
async def update_user(USER_ID: str, user: User, db: Session = Depends(get_db)):
    db_user = db.query(TB_USERS).filter(TB_USERS.USER_ID == USER_ID).first()
    if not db_user:
        raise HTTPException(status_code=404, detail="User not found")
    for key, value in user.dict().items():
        setattr(db_user, key, value)
    db.commit()
    db.refresh(db_user)
    return db_user

# ✅ 사용자 삭제 API
@router.delete("/users/{USER_ID}")
async def delete_user(USER_ID: str, db: Session = Depends(get_db)):
    db_user = db.query(TB_USERS).filter(TB_USERS.USER_ID == USER_ID).first()
    if not db_user:
        raise HTTPException(status_code=404, detail="User not found")
    db.delete(db_user)
    db.commit()
    return {"detail": "User deleted successfully"}
