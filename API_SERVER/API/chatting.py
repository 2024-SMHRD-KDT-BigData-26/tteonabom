from datetime import datetime
from fastapi import APIRouter, Depends, HTTPException
from pydantic import BaseModel
from sqlalchemy.orm import Session
from DataBase.conn import get_db
from DataBase.models import TB_CHATTING

router = APIRouter()

class Chat(BaseModel):
    CHAT_IDX: int
    # CROOM_IDX: int
    # CHATTER: str
    # CHAT_CONTENT: str
    # CHAT_FILE: str = None
    # CHAT_EMOTION: str = None
    # CREATED_AT: datetime

    class Config:
        from_attributes = True


# ✅ 채팅 메시지 생성
@router.post("/chats")
async def create_chat(chat: Chat, db: Session = Depends(get_db)):
    db_chat = TB_CHATTING(**chat.dict())
    db.add(db_chat)
    db.commit()
    db.refresh(db_chat)
    return db_chat

# ✅ 특정 채팅방의 모든 메시지 조회
@router.get("/chats/{CROOM_IDX}")
async def get_chats_by_croom(CROOM_IDX: int, db: Session = Depends(get_db)):
    chats = db.query(TB_CHATTING).filter(TB_CHATTING.CROOM_IDX == CROOM_IDX).all()
    return chats

# ✅ 특정 사용자의 메시지 조회 (채팅방 내)
@router.get("/chats/{CROOM_IDX}/{CHATTER}")
async def get_chats_by_user(CROOM_IDX: int, CHATTER: str, db: Session = Depends(get_db)):
    chats = db.query(TB_CHATTING).filter(
        TB_CHATTING.CROOM_IDX == CROOM_IDX,
        TB_CHATTING.CHATTER == CHATTER
    ).all()
    return chats

# ✅ 특정 채팅방의 최근 N개 메시지 조회
@router.get("/chats/recent/{CROOM_IDX}")
async def get_recent_chats(CROOM_IDX: int, limit: int = 10, db: Session = Depends(get_db)):
    chats = db.query(TB_CHATTING).filter(TB_CHATTING.CROOM_IDX == CROOM_IDX)\
        .order_by(TB_CHATTING.CREATED_AT.desc())\
        .limit(limit)\
        .all()
    return chats

# ✅ 특정 메시지 조회
@router.get("/chats/message/{CHAT_IDX}")
async def get_chat(CHAT_IDX: int, db: Session = Depends(get_db)):
    chat = db.query(TB_CHATTING).filter(TB_CHATTING.CHAT_IDX == CHAT_IDX).first()
    if not chat:
        raise HTTPException(status_code=404, detail="Chat message not found")
    return chat

# ✅ 메시지 수정
@router.put("/chats/{CHAT_IDX}")
async def update_chat(CHAT_IDX: int, chat: Chat, db: Session = Depends(get_db)):
    db_chat = db.query(TB_CHATTING).filter(TB_CHATTING.CHAT_IDX == CHAT_IDX).first()
    if not db_chat:
        raise HTTPException(status_code=404, detail="Chat message not found")

    for key, value in chat.dict().items():
        setattr(db_chat, key, value)

    db.commit()
    db.refresh(db_chat)
    return db_chat

# ✅ 메시지 삭제
@router.delete("/chats/{CHAT_IDX}")
async def delete_chat(CHAT_IDX: int, db: Session = Depends(get_db)):
    db_chat = db.query(TB_CHATTING).filter(TB_CHATTING.CHAT_IDX == CHAT_IDX).first()
    if not db_chat:
        raise HTTPException(status_code=404, detail="Chat message not found")

    db.delete(db_chat)
    db.commit()
    return {"detail": "Chat message deleted successfully"}

# ✅ 🔥 **테스트용 API (주석 처리된 간단한 버전)**
@router.post("/chat/test")
async def create_chat_test(chat: Chat, db: Session = Depends(get_db)):
    chat_dict = {
        "CHAT_IDX": chat.CHAT_IDX
        # "CROOM_IDX": chat.CROOM_IDX,
        # "CHATTER": chat.CHATTER,
        # "CHAT_CONTENT": chat.CHAT_CONTENT,
        # "CHAT_FILE": chat.CHAT_FILE,
        # "CHAT_EMOTION": chat.CHAT_EMOTION,
        # "CREATED_AT": chat.CREATED_AT
    }
    return chat_dict
