from fastapi import FastAPI, HTTPException, Form, Request
from fastapi.responses import HTMLResponse
from fastapi.templating import Jinja2Templates
from pydantic import BaseModel
import bcrypt
import mysql.connector
from mysql.connector import Error
import os
from dotenv import load_dotenv

# 환경 변수 로드
load_dotenv()

# FastAPI 앱 생성
app = FastAPI()

# 템플릿 설정
templates = Jinja2Templates(directory="templates")

# 데이터베이스 연결 함수
def get_db_connection():
    try:
        connection = mysql.connector.connect(
            host=os.getenv('DB_HOST'),
            port=int(os.getenv('DB_PORT', 3306)),
            user=os.getenv('DB_USER'),
            password=os.getenv('DB_PASSWORD'),
            database=os.getenv('DB_NAME')
        )
        if connection.is_connected():
            return connection
    except Error as e:
        print(f"[ERROR] 데이터베이스 연결 오류: {e}")
        raise

# 유저 모델 정의
class User(BaseModel):
    user_id: str
    user_pw: str
    user_pw_confirm: str
    user_nick: str
    user_profile_img: str = None
    kakao_id: int = None
    auth_provider: str = None

# GET 요청: 회원가입 폼 페이지 반환
@app.get("/join", response_class=HTMLResponse)
async def show_join_form(request: Request):
    """회원가입 폼을 렌더링"""
    return templates.TemplateResponse("Join.html", {"request": request})

# POST 요청: 회원가입 처리
@app.post("/join")
async def join(user: User):
    # 비밀번호 확인
    if user.user_pw != user.user_pw_confirm:
        raise HTTPException(status_code=400, detail="비밀번호가 일치하지 않습니다.")

    try:
        connection = get_db_connection()
        cursor = connection.cursor()

        # 아이디 중복 확인
        query = "SELECT COUNT(*) FROM TB_USERS WHERE USER_ID = %s"
        cursor.execute(query, (user.user_id,))
        result = cursor.fetchone()
        if result[0] > 0:
            raise HTTPException(status_code=400, detail="이미 존재하는 아이디입니다.")

        # 비밀번호 해싱
        hashed_pw = bcrypt.hashpw(user.user_pw.encode('utf-8'), bcrypt.gensalt()).decode('utf-8')

        # 데이터 삽입
        query = """
            INSERT INTO TB_USERS 
            (USER_ID, USER_PW, USER_NICK, USER_PROFILE_IMG, KAKAO_ID, AUTH_PROVIDER, CREATED_AT)
            VALUES (%s, %s, %s, %s, %s, %s, CURRENT_TIMESTAMP)
        """
        cursor.execute(query, (
            user.user_id,
            hashed_pw,
            user.user_nick,
            user.user_profile_img if user.user_profile_img else None,
            user.kakao_id,
            user.auth_provider
        ))
        connection.commit()

        return {"message": "회원가입이 완료되었습니다."}

    except Error as e:
        raise HTTPException(status_code=500, detail=f"회원가입 중 오류가 발생했습니다: {e}")

    finally:
        if cursor:
            cursor.close()
        if connection.is_connected():
            connection.close()
