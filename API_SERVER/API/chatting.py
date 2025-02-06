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


class ChatCreate(BaseModel):
    CROOM_IDX: int
    USER_ID: str
    TRAVEL_DATA: dict  # 🟢 여행 데이터 (JSON 형식)
    CREATED_AT: datetime = datetime.utcnow()

    class Config:
        from_attributes = True


def generate_travel_prompt(travel_data: dict) -> str:
    """사용자 입력 데이터를 기반으로 GPT에 보낼 프리프롬프트 생성"""
    try:
        return (
            f"사용자가 여행 일정을 추천받고 싶어합니다.\n"
            f"- 출발 날짜: {travel_data['start_date']}\n"
            f"- 도착 날짜: {travel_data['end_date']}\n"
            f"- 동반자: {travel_data['companion']}\n"
            f"- 여행 지역: {travel_data['region']}\n"
            f"- 선호 여행 스타일: {travel_data['style']}\n"
            f"- 일정 스타일: {travel_data['schedule']}\n\n"
            f"위 정보를 바탕으로 상세한 여행 일정을 추천해 주세요."
        )
    except KeyError as e:
        raise ValueError(f"필수 키가 누락되었습니다: {e}")


async def generate_gpt_response(travel_data: dict) -> str:
    """OpenAI GPT API를 호출하여 응답을 생성하는 함수"""
    try:
        prompt = generate_travel_prompt(travel_data)
        response = openai.ChatCompletion.create(
            model="gpt-4-turbo",
            messages=[{"role": "user", "content": prompt}]
        )
        return response["choices"][0]["message"]["content"]
    except Exception as e:
        print(f"GPT API 호출 오류: {e}")
        return "죄송합니다. 현재 응답을 생성할 수 없습니다."


@router.post("/chat")
async def create_chat(chat: ChatCreate, db: Session = Depends(get_db)):
    """사용자 데이터를 저장하고, GPT 응답을 생성하여 저장하는 API"""

    # 1️⃣ GPT 응답 생성
    try:
        gpt_response = await generate_gpt_response(chat.TRAVEL_DATA)
    except ValueError as e:
        raise HTTPException(status_code=400, detail=str(e))

    # 2️⃣ 사용자 입력 및 GPT 응답 저장
    db_chat = TB_CHATTING(
        CROOM_IDX=chat.CROOM_IDX,
        USER_ID=chat.USER_ID,
        TRAVEL_DATA=chat.TRAVEL_DATA,
        GPT_RESPONSE=gpt_response,
        CREATED_AT=chat.CREATED_AT
    )
    db.add(db_chat)
    db.commit()
    db.refresh(db_chat)

    return {
        "user_message": chat.TRAVEL_DATA,
        "gpt_response": gpt_response
    }


@router.get("/chat/croom/{CROOM_IDX}")
async def get_chats_by_room(CROOM_IDX: int, db: Session = Depends(get_db)):
    """특정 채팅방의 모든 채팅 기록 조회"""
    chats = db.query(TB_CHATTING).filter(TB_CHATTING.CROOM_IDX == CROOM_IDX).all()
    if not chats:
        raise HTTPException(status_code=404, detail="해당 채팅방에 대화 기록이 없습니다.")
    return chats
