from datetime import datetime
from fastapi import APIRouter, Depends
from pydantic import BaseModel
from sqlalchemy.orm import Session
from DataBase.conn import get_db


router = APIRouter()


class Chat(BaseModel):
    chat_idx: int
    # croom_idx: int
    # chatter: str
    # chat_content: str
    # chat_file: str
    # chat_emotion: str
    # created_at: datetime

    class Config:
        orm_mode = True


# 사용자 생성 API
@router.post("/chat")
async def create_chat(chat: Chat, db: Session = Depends(get_db)):

    chat_dict = {
        "chat_idx": chat.chat_idx
    }
    return chat_dict


