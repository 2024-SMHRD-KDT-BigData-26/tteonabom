from datetime import datetime
from fastapi import APIRouter, Depends, HTTPException, Body
from pydantic import BaseModel
from sqlalchemy.orm import Session
from fastapi.responses import FileResponse
from DataBase.conn import get_db
from DataBase.models import TB_CROOM, TB_CHATTING, TB_SHOPPING_MALL
from config import OPENAI_API_KEY
import openai
import pandas as pd

router = APIRouter()

# ✅ OpenAI API 키 설정
openai.api_key = OPENAI_API_KEY


# ✅ 사용자가 입력하는 데이터 모델
class ChatCreate(BaseModel):
    USER_ID: str
    TRAVEL_DATA: dict  # 🟢 여행 데이터 (JSON 형식)

    class Config:
        from_attributes = True


# ✅ 저장 요청 시 사용하는 데이터 모델
class ChatSaveRequest(BaseModel):
    CROOM_IDX: int
    USER_ID: str

    class Config:
        from_attributes = True


# ✅ GPT 응답을 HTML로 변환하는 함수
def format_gpt_response_to_html(response: str) -> str:
    """GPT 응답을 HTML 태그로 변환하여 저장"""
    response = response.replace("**", "<strong>").replace("\n", "<br>")
    return response


# ✅ GPT 프롬프트 생성 함수 (HTML 변환 포함)
def generate_travel_prompt(travel_data: dict) -> str:
    """사용자 입력 데이터를 기반으로 GPT에 보낼 프롬프트 생성 (날짜별 일정 구분)"""
    try:
        start_date = travel_data["start_date"]
        end_date = travel_data["end_date"]
        companion = travel_data["companion"]
        region = travel_data["region"]
        style = travel_data["style"]
        schedule = travel_data["schedule"]

        prompt = (
            f"다음은 사용자가 요청한 여행 정보입니다.<br>"
            f"📅 <strong>여행 기간:</strong> {start_date} ~ {end_date}<br>"
            f"👥 <strong>동반자:</strong> {companion}<br>"
            f"📍 <strong>여행 지역:</strong> {region}<br>"
            f"🎭 <strong>선호 여행 스타일:</strong> {style}<br>"
            f"⏳ <strong>일정 스타일:</strong> {schedule}<br><br>"
            f"🔥 <strong>각 날짜별로 상세 일정을 추천해 주세요.</strong> 날짜별로 아침, 점심, 저녁으로 나누어 주세요.<br>"
            f"👉 <strong>HTML 형식으로 작성해 주세요.</strong>"
        )

        return prompt

    except KeyError as e:
        raise ValueError(f"필수 키가 누락되었습니다: {e}")


# ✅ GPT API 호출 함수 (HTML 변환 적용)
async def generate_gpt_response(travel_data: dict) -> str:
    """OpenAI GPT API를 호출하여 응답을 생성하는 함수"""
    try:
        prompt = generate_travel_prompt(travel_data)
        response = openai.ChatCompletion.create(
            model="gpt-4-turbo",
            messages=[{"role": "user", "content": prompt}]
        )
        gpt_response = response["choices"][0]["message"]["content"]
        return format_gpt_response_to_html(gpt_response)  # ✅ HTML 변환 후 반환
    except Exception as e:
        print(f"GPT API 호출 오류: {e}")
        return "죄송합니다. 현재 응답을 생성할 수 없습니다."


# ✅ 사용자 입력 데이터를 기반으로 GPT 응답을 생성하고 TB_CROOM에 저장
@router.post("/chat")
async def create_chat(chat: ChatCreate, db: Session = Depends(get_db)):
    """사용자 입력 데이터를 기반으로 GPT 응답을 생성 후 TB_CROOM에 저장"""
    try:
        gpt_response = await generate_gpt_response(chat.TRAVEL_DATA)
    except ValueError as e:
        raise HTTPException(status_code=400, detail=str(e))

    db_croom = TB_CROOM(
        CROOM_TITLE=f"채팅방_{chat.USER_ID}_{datetime.utcnow()}",
        CROOM_INFO="사용자의 채팅 데이터",
        USER_ID=chat.USER_ID,
        CROOM_LIMIT=0,
        CROOM_STATUS="active",
        GPT_RESPONSE=gpt_response,
        CREATED_AT=datetime.utcnow(),
    )
    db.add(db_croom)
    db.commit()
    db.refresh(db_croom)

    return {
        "croom_id": db_croom.CROOM_IDX,
        "user_id": chat.USER_ID,
        "user_message": chat.TRAVEL_DATA,
        "gpt_response": gpt_response
    }


# ✅ TB_CROOM의 최신 GPT 응답을 TB_CHATTING에 저장
@router.post("/chat/save")
async def save_chat_response(request: ChatSaveRequest, db: Session = Depends(get_db)):
    """사용자가 '저장' 버튼을 눌렀을 때 CROOM_IDX 기준 최신 GPT 응답을 TB_CHATTING에 저장"""
    latest_chat = db.query(TB_CROOM).filter(
        TB_CROOM.CROOM_IDX == request.CROOM_IDX
    ).order_by(TB_CROOM.CREATED_AT.desc()).first()

    if not latest_chat or not latest_chat.GPT_RESPONSE:
        raise HTTPException(status_code=404, detail="해당 채팅방에서 저장할 GPT 응답이 없습니다.")

    db_chat = TB_CHATTING(
        CROOM_IDX=request.CROOM_IDX,
        USER_ID=request.USER_ID,
        TRAVEL_DATA=latest_chat.GPT_RESPONSE,  # ✅ HTML 변환된 데이터 저장
        GPT_RESPONSE=latest_chat.GPT_RESPONSE,
        CREATED_AT=datetime.utcnow(),
    )
    db.add(db_chat)
    db.commit()
    db.refresh(db_chat)

    return {"detail": "GPT 응답이 저장되었습니다.", "chat_id": db_chat.CHAT_IDX}


# ✅ TB_SHOPPING_MALL 카테고리 목록 제공 API
@router.get("/shopping_malls/categories")
async def get_shopping_mall_categories(db: Session = Depends(get_db)):
    """쇼핑몰 테마 카테고리 목록 조회 API"""
    categories = db.query(TB_SHOPPING_MALL.CATEGORY).distinct().all()

    if not categories:
        raise HTTPException(status_code=404, detail="등록된 쇼핑몰 카테고리가 없습니다.")

    return [category[0] for category in categories]


# ✅ 특정 카테고리 쇼핑몰 추천 API
@router.get("/shopping_malls/category/{category}")
async def get_shopping_malls_by_category(category: str, db: Session = Depends(get_db)):
    """특정 카테고리의 쇼핑몰 추천 API"""
    malls = db.query(TB_SHOPPING_MALL).filter(TB_SHOPPING_MALL.CATEGORY == category).all()

    if not malls:
        raise HTTPException(status_code=404, detail=f"'{category}' 카테고리의 쇼핑몰이 없습니다.")

    return [
        {
            "mall_name": mall.MALL_NM,
            "mall_url": mall.MALL_URL,
            "mall_img": mall.MALL_IMG,
        }
        for mall in malls
    ]


# ✅ TB_CHATTING의 특정 GPT 응답을 엑셀로 다운로드
@router.get("/chat/download/{CHAT_IDX}")
async def download_gpt_response(CHAT_IDX: int, db: Session = Depends(get_db)):
    """TB_CHATTING의 특정 GPT 응답을 엑셀 파일로 다운로드"""
    chat = db.query(TB_CHATTING).filter(TB_CHATTING.CHAT_IDX == CHAT_IDX).first()

    if not chat or not chat.GPT_RESPONSE:
        raise HTTPException(status_code=404, detail="해당 채팅이 존재하지 않거나 GPT 응답이 없습니다.")

    data = [{
        "채팅 ID": chat.CHAT_IDX,
        "사용자 ID": chat.USER_ID,
        "GPT 응답": chat.GPT_RESPONSE,
        "생성 날짜": chat.CREATED_AT,
    }]

    file_path = f"gpt_response_{CHAT_IDX}.xlsx"
    df = pd.DataFrame(data)
    df.to_excel(file_path, index=False)

    return FileResponse(file_path, filename=f"GPT_Response_{CHAT_IDX}.xlsx",
                        media_type="application/vnd.openxmlformats-officedocument.spreadsheetml.sheet")
