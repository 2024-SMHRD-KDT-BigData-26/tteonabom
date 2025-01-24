import os
import bcrypt
import mysql.connector
from mysql.connector import Error
from fastapi import FastAPI, Form, HTTPException, Request
from fastapi.responses import HTMLResponse, RedirectResponse
from fastapi.templating import Jinja2Templates
from starlette.middleware.sessions import SessionMiddleware  # 올바른 SessionMiddleware
from dotenv import load_dotenv

# 환경 변수 로드
load_dotenv()

# FastAPI 앱 초기화
app = FastAPI()

# 세션 미들웨어 추가
app.add_middleware(SessionMiddleware, secret_key=os.getenv('SECRET_KEY', 'default_secret_key'))

# 템플릿 설정
templates = Jinja2Templates(directory="templates")

# 데이터베이스 연결 함수
def get_db_connection():
    """데이터베이스
        connection = mysql.connector.connect(
            host=os.getenv('DB_HOST'),
            port=int(os.getenv('DB_PORT', 3306)),
            user=os.getenv('DB_USER'),
            password=os.getenv('DB_PASSWORD'),
            database=os.getenv('DB_NAME')연결 함수"""
    try:
        )
        if connection.is_connected():
            return connection
    except Error as e:
        print(f"[ERROR] 데이터베이스 연결 오류: {e}")
        raise

# 특정 아이디의 비밀번호 가져오기
def get_user_password(cursor, user_id):
    query = "SELECT USER_PW FROM TB_USERS WHERE USER_ID = %s"
    cursor.execute(query, (user_id,))
    result = cursor.fetchone()
    return result[0] if result else None

@app.get("/login", response_class=HTMLResponse)
async def login_form(request: Request):
    """로그인 폼 페이지"""
    return templates.TemplateResponse("Login.html", {"request": request})

@app.post("/login")
async def login(user_id: str = Form(...), user_pw: str = Form(...), request: Request = None):
    """로그인 처리"""
    if not user_id or not user_pw:
        raise HTTPException(status_code=400, detail="[오류] 아이디와 비밀번호를 모두 입력해주세요.")

    try:
        connection = get_db_connection()
        cursor = connection.cursor()

        hashed_pw = get_user_password(cursor, user_id)
        if not hashed_pw:
            raise HTTPException(status_code=404, detail="[오류] 존재하지 않는 아이디입니다.")

        if bcrypt.checkpw(user_pw.encode('utf-8'), hashed_pw.encode('utf-8')):
            # 세션에 유저 아이디 저장
            request.session['user_id'] = user_id
            return RedirectResponse(url="/dashboard", status_code=302)
        else:
            raise HTTPException(status_code=401, detail="[오류] 비밀번호가 일치하지 않습니다.")

    except Error as e:
        raise HTTPException(status_code=500, detail=f"[ERROR] 로그인 중 오류가 발생했습니다: {e}")

    finally:
        if cursor:
            cursor.close()
        if connection.is_connected():
            connection.close()

@app.get("/dashboard", response_class=HTMLResponse)
async def dashboard(request: Request):
    """대시보드"""
    user_id = request.session.get('user_id')
    if not user_id:
        return RedirectResponse(url="/login", status_code=302)
    return f"<h1>안녕하세요, {user_id}님! 이것은 대시보드입니다.</h1>"

@app.get("/logout")
async def logout(request: Request):
    """로그아웃"""
    request.session.clear()
    return RedirectResponse(url="/login", status_code=302)
