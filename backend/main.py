from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
import uvicorn
from services import get_all_users  # services에서 데이터 처리 함수 호출
from database import get_db_connection  # DB 연결 함수 임포트

app = FastAPI()

# CORS 미들웨어 추가
origins = [
    "http://localhost:9001",  # 프론트엔드가 실행되는 주소
    "http://127.0.0.1:9001"  # 같은 주소, 127.0.0.1로도 가능
]

app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,  # 허용할 출처
    allow_credentials=True,
    allow_methods=["*"],  # 모든 HTTP 메소드 허용
    allow_headers=["*"],  # 모든 헤더 허용
)

@app.get("/")
def read_root():
    return {"message": "Welcome to the homepage!"}

@app.get("/api/data")
def get_data():
    """DB에서 사용자 목록 가져오기"""
    users = get_all_users()
    return {"users": users}

@app.get("/api/db-status")
def db_status():
    """DB 연결 상태 확인"""
    connection = get_db_connection()  # DB 연결 함수 호출
    if connection:
        return {"status": "success", "message": "Connected to the database!"}
    else:
        return {"status": "error", "message": "Failed to connect to the database!"}

# 서버를 9000번 포트로 자동 실행
if __name__ == "__main__":
    uvicorn.run(app, host="127.0.0.1", port=9000)  # 포트 9000번으로 실행
