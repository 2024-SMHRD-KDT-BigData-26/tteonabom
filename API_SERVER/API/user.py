from datetime import datetime, timedelta
from fastapi import FastAPI, APIRouter, Depends, HTTPException, UploadFile, File, Query, Body
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel, Field
from sqlalchemy.orm import Session
from sqlalchemy.exc import IntegrityError
from DataBase.conn import get_db
from DataBase.models import TB_USERS
import bcrypt
import shutil
import os
from typing import Optional

app = FastAPI()
router = APIRouter()

UPLOAD_DIR = "uploads"
os.makedirs(UPLOAD_DIR, exist_ok=True)

# ✅ CORS 설정 (프론트엔드 9001과 연동)
app.add_middleware(
    CORSMiddleware,
    allow_origins=["http://localhost:9001"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


# ✅ 사용자 모델
class User(BaseModel):
    USER_ID: str
    USER_PW: str
    USER_NICK: str
    USER_PROFILE_IMG: Optional[str] = None


# ✅ 로그인 요청 모델
class LoginRequest(BaseModel):
    USER_ID: str
    USER_PW: str


# ✅ 비밀번호 해싱 및 검증
def hash_password(password: str) -> str:
    salt = bcrypt.gensalt()
    return bcrypt.hashpw(password.encode("utf-8"), salt).decode("utf-8")


def verify_password(plain_password: str, hashed_password: str) -> bool:
    return bcrypt.checkpw(plain_password.encode("utf-8"), hashed_password.encode("utf-8"))


# ✅ 프로필 이미지 업로드 API 수정
@router.post("/api/upload")
async def upload_file(file: UploadFile = File(...)):
    try:
        file_location = os.path.join(UPLOAD_DIR, file.filename)

        # 파일 저장
        with open(file_location, "wb") as buffer:
            shutil.copyfileobj(file.file, buffer)

        return {"fileUrl": f"/uploads/{file.filename}"}  # ✅ 상대 경로 반환

    except Exception as e:
        raise HTTPException(status_code=500, detail=f"파일 업로드 실패: {str(e)}")


app.include_router(router)

if __name__ == "__main__":
    import uvicorn

    uvicorn.run(app, host="127.0.0.1", port=9000)  # ✅ 백엔드 9000번 포트에서 실행

# ✅ 아이디 중복 확인 API
@router.get("/api/check-id")
async def check_user_id(USER_ID: str = Query(...), db: Session = Depends(get_db)):
    exists = db.query(TB_USERS).filter(TB_USERS.USER_ID == USER_ID).first()
    return {"available": not bool(exists)}


# ✅ 닉네임 중복 확인 API
@router.get("/api/check-nick")
async def check_nickname(USER_NICK: str = Query(...), db: Session = Depends(get_db)):
    exists = db.query(TB_USERS).filter(TB_USERS.USER_NICK == USER_NICK).first()
    return {"available": not bool(exists)}


# ✅ 회원가입 API
@router.post("/api/join")
async def create_user(user: User, db: Session = Depends(get_db)):
    if not user.USER_ID.isalnum() or not (5 <= len(user.USER_ID) <= 10):
        raise HTTPException(status_code=400, detail="아이디는 5~10자의 영문 소문자와 숫자만 가능합니다.")

    if not (8 <= len(user.USER_PW) <= 16) or not any(c.islower() for c in user.USER_PW) or not any(
            c.isupper() for c in user.USER_PW) or not any(c.isdigit() for c in user.USER_PW):
        raise HTTPException(status_code=400, detail="비밀번호는 8~16자의 영문 대/소문자와 숫자를 포함해야 합니다.")

    try:
        user.USER_PW = hash_password(user.USER_PW)
        db_user = TB_USERS(**user.dict())
        db.add(db_user)
        db.commit()
        db.refresh(db_user)
        return {"message": "회원가입 성공", "USER_ID": db_user.USER_ID, "USER_PROFILE_IMG": db_user.USER_PROFILE_IMG}
    except IntegrityError:
        db.rollback()
        raise HTTPException(status_code=400, detail="이미 존재하는 USER_ID입니다.")


# ✅ 로그인 API
@router.post("/api/login")
async def login(user: LoginRequest, db: Session = Depends(get_db)):
    db_user = db.query(TB_USERS).filter(TB_USERS.USER_ID == user.USER_ID).first()
    if not db_user or not verify_password(user.USER_PW, db_user.USER_PW):
        raise HTTPException(status_code=401, detail="아이디 또는 비밀번호가 올바르지 않습니다.")
    return {"USER_ID": db_user.USER_ID, "USER_NICK": db_user.USER_NICK, "USER_PROFILE_IMG": db_user.USER_PROFILE_IMG}


# ✅ 사용자 정보 수정 API
@router.put("/api/myinfo")
async def update_user(USER_ID: str = Query(...), user: User = Body(...), db: Session = Depends(get_db)):
    db_user = db.query(TB_USERS).filter(TB_USERS.USER_ID == USER_ID).first()
    if not db_user:
        raise HTTPException(status_code=404, detail="User not found")
    update_data = user.dict(exclude_unset=True)
    if "USER_PW" in update_data:
        update_data["USER_PW"] = hash_password(update_data["USER_PW"])
    for key, value in update_data.items():
        setattr(db_user, key, value)
    db_user.UPDATED_AT = datetime.utcnow()
    db.commit()
    db.refresh(db_user)
    return {"message": "회원정보가 수정되었습니다.", "updated_data": db_user}


# ✅ 사용자 삭제 API
@router.delete("/users/{USER_ID}")
async def delete_user(USER_ID: str, db: Session = Depends(get_db)):
    db_user = db.query(TB_USERS).filter(TB_USERS.USER_ID == USER_ID).first()
    if not db_user:
        raise HTTPException(status_code=404, detail="User not found")
    db.delete(db_user)
    db.commit()
    return {"detail": "User deleted successfully"}


app.include_router(router)
