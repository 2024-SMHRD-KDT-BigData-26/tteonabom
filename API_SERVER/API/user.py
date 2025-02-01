from datetime import datetime
from fastapi import APIRouter, Depends
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

    user_dict = {
        "user_id": user.user_id,
        "user_pw": user.user_pw

    }
    return user_dict


