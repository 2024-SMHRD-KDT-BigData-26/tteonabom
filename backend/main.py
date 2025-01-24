from fastapi import FastAPI, Request  # FastAPI와 Request를 임포트
from fastapi.middleware.cors import CORSMiddleware  # CORS 미들웨어 임포트
import uvicorn  # 서버 실행을 위한 uvicorn 임포트
from services import generate_answer  # GPT API 호출을 위한 서비스 함수 임포트
from database import get_db_connection  # DB 연결 함수 임포트
from services import get_all_users
from dotenv import load_dotenv  # .env 파일을 불러오기 위한 라이브러리
import os  # 환경 변수 접근을 위한 라이브러리

# .env 파일에서 환경 변수 로드
load_dotenv()  # .env 파일을 로드하여 환경 변수들을 가져옵니다.

# API_KEY를 환경 변수에서 가져오기
API_KEY = os.getenv('API_KEY')  # .env 파일에서 API_KEY를 가져옵니다.

app = FastAPI()  # FastAPI 앱 객체 생성

# CORS 미들웨어 추가 (프론트엔드와 백엔드 간의 도메인 차이를 해결)
origins = [
    "http://localhost:9001",  # 프론트엔드 주소
    "http://127.0.0.1:9001"  # 로컬 주소로도 허용
]

app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,  # 허용할 출처
    allow_credentials=True,
    allow_methods=["*"],  # 모든 HTTP 메소드 허용
    allow_headers=["*"],  # 모든 헤더 허용
)


# 기본 홈 엔드포인트
@app.get("/")
def read_root():
    return {"message": "Welcome to the homepage!"}


# DB에서 사용자 목록을 가져오는 엔드포인트
@app.get("/api/data")
def get_data():
    """DB에서 사용자 목록을 가져옴"""
    users = get_all_users()  # DB에서 사용자 목록을 가져오는 함수 호출
    return {"users": users}


# DB 연결 상태를 확인하는 엔드포인트
@app.get("/api/db-status")
def db_status():
    """DB 연결 상태 확인"""
    connection = get_db_connection()  # DB 연결 함수 호출
    if connection:
        return {"status": "success", "message": "Connected to the database!"}
    else:
        return {"status": "error", "message": "Failed to connect to the database!"}


# GPT API를 호출하는 엔드포인트 (POST 요청을 통해 챗봇 응답 받기)
@app.post("/prompt")
async def generate_answer(request: Request):
    body = await request.json()  # 요청 데이터 받기
    prompt = body["prompt"]  # 받은 데이터에서 'prompt' 값 추출

    # services에서 정의한 generate_answer 함수 호출
    answer = await generate_answer(prompt)

    return {"answer": answer}  # GPT 응답 반환


# 서버 실행 (포트 9000번에서 실행)
if __name__ == "__main__":
    uvicorn.run(app, host="127.0.0.1", port=9000)  # 9000번 포트에서 FastAPI 서버 실행
