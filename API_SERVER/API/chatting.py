from datetime import datetime
from fastapi import APIRouter, Depends, HTTPException
from pydantic import BaseModel
from sqlalchemy.orm import Session
from DataBase.conn import get_db
from DataBase.models import TB_CHATTING

router = APIRouter()

class Chat(BaseModel):
    chat_idx: int
    #croom_idx: int
    #chatter: str
    #chat_content: str
    #chat_file: str = None
    #chat_emotion: str = None
    #created_at: datetime

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
@router.get("/chats/{croom_idx}")
async def get_chats_by_croom(croom_idx: int, db: Session = Depends(get_db)):
    chats = db.query(TB_CHATTING).filter(TB_CHATTING.croom_idx == croom_idx).all()
    return chats

# ✅ 특정 사용자의 메시지 조회 (채팅방 내)
@router.get("/chats/{croom_idx}/{chatter}")
async def get_chats_by_user(croom_idx: int, chatter: str, db: Session = Depends(get_db)):
    chats = db.query(TB_CHATTING).filter(
        TB_CHATTING.croom_idx == croom_idx,
        TB_CHATTING.chatter == chatter
    ).all()
    return chats

# ✅ 특정 채팅방의 최근 N개 메시지 조회
@router.get("/chats/recent/{croom_idx}")
async def get_recent_chats(croom_idx: int, limit: int = 10, db: Session = Depends(get_db)):
    chats = db.query(TB_CHATTING).filter(TB_CHATTING.croom_idx == croom_idx)\
        .order_by(TB_CHATTING.created_at.desc())\
        .limit(limit)\
        .all()
    return chats

# ✅ 특정 메시지 조회
@router.get("/chats/message/{chat_idx}")
async def get_chat(chat_idx: int, db: Session = Depends(get_db)):
    chat = db.query(TB_CHATTING).filter(TB_CHATTING.chat_idx == chat_idx).first()
    if not chat:
        raise HTTPException(status_code=404, detail="Chat message not found")
    return chat

# ✅ 메시지 수정
@router.put("/chats/{chat_idx}")
async def update_chat(chat_idx: int, chat: Chat, db: Session = Depends(get_db)):
    db_chat = db.query(TB_CHATTING).filter(TB_CHATTING.chat_idx == chat_idx).first()
    if not db_chat:
        raise HTTPException(status_code=404, detail="Chat message not found")

    for key, value in chat.dict().items():
        setattr(db_chat, key, value)

    db.commit()
    db.refresh(db_chat)
    return db_chat

# ✅ 메시지 삭제
@router.delete("/chats/{chat_idx}")
async def delete_chat(chat_idx: int, db: Session = Depends(get_db)):
    db_chat = db.query(TB_CHATTING).filter(TB_CHATTING.chat_idx == chat_idx).first()
    if not db_chat:
        raise HTTPException(status_code=404, detail="Chat message not found")

    db.delete(db_chat)
    db.commit()
    return {"detail": "Chat message deleted successfully"}

# ✅ 🔥 **테스트용 API (주석 처리된 간단한 버전)**
@router.post("/chat/test")
async def create_chat_test(chat: Chat, db: Session = Depends(get_db)):
    chat_dict = {
        "chat_idx": chat.chat_idx
        # "croom_idx": chat.croom_idx,
        # "chatter": chat.chatter,
        # "chat_content": chat.chat_content,
        # "chat_file": chat.chat_file,
        # "chat_emotion": chat.chat_emotion,
        # "created_at": chat.created_at
    }
    return chat_dict
