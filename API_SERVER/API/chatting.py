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
    CHATTER: str
    CHAT_CONTENT: str
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


# ✅ 사용자 메시지 저장 + GPT 응답 저장 API
@router.post("/chat/gpt")
async def chat_with_gpt(chat: Chat, db: Session = Depends(get_db)):
    """ 사용자의 입력을 DB에 저장하고, GPT 응답을 생성하여 저장하는 API """

    # 1️⃣ 사용자 입력을 DB에 저장 (CHAT_IDX 없이 저장)
    db_user_chat = TB_CHATTING(
        CROOM_IDX=chat.CROOM_IDX,
        CHATTER=chat.CHATTER,
        CHAT_CONTENT=chat.CHAT_CONTENT,
        CHAT_FILE=chat.CHAT_FILE,
        CHAT_EMOTION=chat.CHAT_EMOTION,
        CREATED_AT=chat.CREATED_AT
    )
    db.add(db_user_chat)
    db.commit()
    db.refresh(db_user_chat)

    # 2️⃣ GPT 응답 생성
    gpt_response = await generate_gpt_response(chat.CHAT_CONTENT)

    # 3️⃣ GPT 응답을 DB에 저장 (CHAT_IDX 자동 증가)
    db_gpt_chat = TB_CHATTING(
        CROOM_IDX=chat.CROOM_IDX,
        CHATTER="GPT",
        CHAT_CONTENT=gpt_response,
        CHAT_FILE=None,
        CHAT_EMOTION=None,
        CREATED_AT=datetime.utcnow()
    )
    db.add(db_gpt_chat)
    db.commit()
    db.refresh(db_gpt_chat)

    return {
        "user_message": chat.CHAT_CONTENT,
        "gpt_response": gpt_response
    }
