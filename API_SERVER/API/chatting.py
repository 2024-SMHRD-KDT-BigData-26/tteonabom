from datetime import datetime
from fastapi import APIRouter, Depends, HTTPException
from pydantic import BaseModel
from sqlalchemy.orm import Session
from DataBase.conn import get_db
from DataBase.models import TB_CHATTING
from config import OPENAI_API_KEY
import openai

router = APIRouter()

# ✅ OpenAI API 키 설정
openai.api_key = OPENAI_API_KEY


class Chat(BaseModel):
    CROOM_IDX: int
    USER_ID: str  # 🟢 사용자 ID (CHATTER → USER_ID로 변경)
    USER_CONTENT: str  # 🟢 사용자 입력 메시지
    CHAT_FILE: str = None
    CHAT_EMOTION: str = None
    CREATED_AT: datetime = datetime.utcnow()

    class Config:
        from_attributes = True


async def generate_gpt_response(user_input: str) -> str:
    """ OpenAI GPT API를 호출하여 응답을 생성하는 함수 """
    try:
        response = openai.ChatCompletion.create(
            model="gpt-4-turbo",
            messages=[{"role": "user", "content": user_input}]
        )
        return response["choices"][0]["message"]["content"]
    except Exception as e:
        print(f"GPT API 호출 오류: {e}")
        return "죄송합니다. 현재 응답을 생성할 수 없습니다."


# ✅ GPT와의 채팅 저장 API
@router.post("/chat/gpt")
async def chat_with_gpt(chat: Chat, db: Session = Depends(get_db)):
    """ 사용자의 입력을 DB에 저장하고, GPT 응답을 생성하여 저장하는 API """

    # 1️⃣ 사용자 입력 저장
    db_user_chat = TB_CHATTING(
        CROOM_IDX=chat.CROOM_IDX,
        USER_ID=chat.USER_ID,  # 🟢 사용자 ID 저장
        USER_CONTENT=chat.USER_CONTENT,  # 🟢 사용자 입력 메시지 저장
        CHAT_CONTENT=None,  # GPT 응답 부분 (None으로 유지)
        CHAT_FILE=chat.CHAT_FILE,
        CHAT_EMOTION=chat.CHAT_EMOTION,
        CREATED_AT=chat.CREATED_AT
    )
    db.add(db_user_chat)
    db.commit()
    db.refresh(db_user_chat)

    # 2️⃣ GPT 응답 생성
    gpt_response = await generate_gpt_response(chat.USER_CONTENT)

    # 3️⃣ GPT 응답 저장
    db_gpt_chat = TB_CHATTING(
        CROOM_IDX=chat.CROOM_IDX,
        USER_ID="GPT",  # GPT의 메시지 저장
        USER_CONTENT=None,  # GPT는 사용자 입력 없음
        CHAT_CONTENT=gpt_response,  # GPT 응답 저장
        CHAT_FILE=None,
        CHAT_EMOTION=None,
        CREATED_AT=datetime.utcnow()
    )
    db.add(db_gpt_chat)
    db.commit()
    db.refresh(db_gpt_chat)

    return {
        "user_message": chat.USER_CONTENT,
        "gpt_response": gpt_response
    }


# ✅ 특정 채팅방에서 GPT와 사용자의 대화 내역 조회
@router.get("/chat/gpt/{CROOM_IDX}")
async def get_gpt_chats(CROOM_IDX: int, db: Session = Depends(get_db)):
    """ 특정 채팅방에서 GPT와 사용자의 모든 대화 기록 조회 """
    chats = db.query(TB_CHATTING).filter(TB_CHATTING.CROOM_IDX == CROOM_IDX).all()
    return chats


# ✅ 특정 사용자의 모든 채팅 내역 조회
@router.get("/chat/user/{USER_ID}")
async def get_user_chats(USER_ID: str, db: Session = Depends(get_db)):
    """ 특정 사용자가 GPT와 나눈 모든 대화 조회 """
    chats = db.query(TB_CHATTING).filter(TB_CHATTING.USER_ID == USER_ID).all()
    return chats


# ✅ 특정 메시지 삭제
@router.delete("/chat/gpt/{CHAT_IDX}")
async def delete_chat(CHAT_IDX: int, db: Session = Depends(get_db)):
    """ 특정 GPT와의 채팅 메시지를 삭제 """
    db_chat = db.query(TB_CHATTING).filter(TB_CHATTING.CHAT_IDX == CHAT_IDX).first()
    if not db_chat:
        raise HTTPException(status_code=404, detail="Chat message not found")

    db.delete(db_chat)
    db.commit()
    return {"detail": "Chat message deleted successfully"}
