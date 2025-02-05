from datetime import datetime, timedelta
from fastapi import APIRouter, Depends, HTTPException, UploadFile, File
from pydantic import BaseModel
from sqlalchemy.orm import Session
from sqlalchemy.exc import IntegrityError
from DataBase.conn import get_db
from DataBase.models import TB_USERS
import bcrypt
import shutil
import os
from typing import Optional

router = APIRouter()

UPLOAD_DIR = "uploads"  # 이미지 저장 경로
os.makedirs(UPLOAD_DIR, exist_ok=True)  # 폴더가 없으면 자동 생성

# ✅ 회원가입 & 사용자 정보 관련 요청 모델
class User(BaseModel):
    USER_ID: str
    USER_PW: str
    USER_NICK: str
    USER_PROFILE_IMG: str = None
    KAKAO_ID: int = None
    AUTH_PROVIDER: str = None
    CREATED_AT: datetime = None
    UPDATED_AT: datetime = None

    class Config:
        from_attributes = True



# ✅ 로그인 요청 모델
class LoginRequest(BaseModel):
    USER_ID: str
    USER_PW: str


# ✅ 로그인 응답 모델 (비밀번호 제외)
class LoginResponse(BaseModel):
    USER_ID: str
    USER_NICK: str
    USER_PROFILE_IMG: Optional[str] = None
    KAKAO_ID: int = 0  # ✅ 기본값 설정
    AUTH_PROVIDER: str = "LOCAL"  # ✅ 기본값 설정
    CREATED_AT: datetime
    UPDATED_AT: datetime = datetime.utcnow()  # ✅ 기본값 설정

    class Config:
        from_attributes = True

# ✅ 프로필 이미지 업로드 API (이미지 경로 반환)
@router.post("/api/upload")
async def upload_file(file: UploadFile = File(...)):
    try:
        file_path = os.path.join(UPLOAD_DIR, file.filename)

        # 파일 저장
        with open(file_path, "wb") as buffer:
            shutil.copyfileobj(file.file, buffer)

        print(f"📷 업로드된 이미지 경로: {file_path}")
        return {"fileUrl": file_path}

    except Exception as e:
        print(f"❌ 이미지 업로드 오류: {e}")
        raise HTTPException(status_code=500, detail="파일 업로드 실패")

# ✅ 비밀번호 해싱 함수
def hash_password(password: str) -> str:
    salt = bcrypt.gensalt()
    hashed_pw = bcrypt.hashpw(password.encode("utf-8"), salt)
    return hashed_pw.decode("utf-8")


# ✅ 비밀번호 검증 함수
def verify_password(plain_password: str, hashed_password: str) -> bool:
    return bcrypt.checkpw(plain_password.encode("utf-8"), hashed_password.encode("utf-8"))


# ✅ 회원가입 API (JSON 요청 처리)
@router.post("/api/join")
async def create_user(user: User, db: Session = Depends(get_db)):
    try:
        print("🔍 회원가입 요청 데이터:", user.dict())


         # 비밀번호 해싱
        hashed_pw = hash_password(user.USER_PW)

        db_user = TB_USERS(
        USER_ID=user.USER_ID,
        USER_PW=hashed_pw,  # 해싱된 비밀번호 저장
        USER_NICK=user.USER_NICK
        )


        # DB 저장
        db_user = TB_USERS(
            USER_ID=user.USER_ID,
            USER_PW=hashed_pw,
            USER_NICK=user.USER_NICK,
            USER_PROFILE_IMG=user.USER_PROFILE_IMG if user.USER_PROFILE_IMG else None,  # 빈 문자열 처리
            KAKAO_ID=user.KAKAO_ID,
            AUTH_PROVIDER=user.AUTH_PROVIDER,
            CREATED_AT=user.CREATED_AT,
            UPDATED_AT=user.UPDATED_AT
        )

        db.add(db_user)
        db.commit()
        db.refresh(db_user)

        print("✅ 회원가입 성공:", db_user.USER_ID)
        return {"message": "회원가입 성공", "USER_ID": db_user.USER_ID, "PROFILE_IMG": db_user.USER_PROFILE_IMG}

    except IntegrityError:
        db.rollback()
        print("❌ USER_ID 중복 오류:", user.USER_ID)
        raise HTTPException(status_code=400, detail="이미 존재하는 USER_ID입니다.")

    except Exception as e:
        db.rollback()
        print(f"❌ 회원가입 중 오류: {e}")
        raise HTTPException(status_code=500, detail="회원가입 처리 중 오류 발생")


# ✅ 사용자 조회 API (단일 사용자)
@router.get("/users/{USER_ID}")
async def get_user(USER_ID: str, db: Session = Depends(get_db)):
    user = db.query(TB_USERS).filter(TB_USERS.USER_ID == USER_ID).first()
    if not user:
        raise HTTPException(status_code=404, detail="User not found")
    return user


# ✅ 사용자 전체 조회 API
@router.get("/users")
async def get_all_users(db: Session = Depends(get_db)):
    users = db.query(TB_USERS).all()
    return users


# ✅ 사용자 정보 수정 API
@router.put("/api/myinfo")
async def update_user(USER_ID: str, user: User, db: Session = Depends(get_db)):
    db_user = db.query(TB_USERS).filter(TB_USERS.USER_ID == USER_ID).first()
    if not db_user:
        raise HTTPException(status_code=404, detail="User not found")

    for key, value in user.dict(exclude_unset=True).items():
        setattr(db_user, key, value)

    db_user.UPDATED_AT = datetime.utcnow()  # 수정 시간 업데이트

    db.commit()
    db.refresh(db_user)
    return db_user


# ✅ 사용자 삭제 API
@router.delete("/users/{USER_ID}")
async def delete_user(USER_ID: str, db: Session = Depends(get_db)):
    db_user = db.query(TB_USERS).filter(TB_USERS.USER_ID == USER_ID).first()
    if not db_user:
        raise HTTPException(status_code=404, detail="User not found")

    db.delete(db_user)
    db.commit()
    return {"detail": "User deleted successfully"}


# ✅ 로그인 API (JSON 응답)
@router.post("/api/login", response_model=LoginResponse)
async def login(user: LoginRequest, db: Session = Depends(get_db)):
    """ 사용자 로그인 검증 API """

    # 1️⃣ 해당 USER_ID가 존재하는지 확인
    db_user = db.query(TB_USERS).filter(TB_USERS.USER_ID == user.USER_ID).first()
    if not db_user:
        raise HTTPException(status_code=404, detail={"error": "존재하지 않는 사용자입니다."})

    # 2️⃣ 비밀번호 검증 (입력한 비밀번호 vs 저장된 해시된 비밀번호)
    if not verify_password(user.USER_PW, db_user.USER_PW):
        raise HTTPException(status_code=401, detail={"error": "비밀번호가 일치하지 않습니다."})

    # 3️⃣ 로그인 성공 → JSON 응답 반환
    return {
        "USER_ID": db_user.USER_ID,
        "USER_NICK": db_user.USER_NICK,
        "USER_PROFILE_IMG": db_user.USER_PROFILE_IMG if db_user.USER_PROFILE_IMG is not None else None,
        "KAKAO_ID": db_user.KAKAO_ID if db_user.KAKAO_ID is not None else 0,  # 기본값 설정
        "AUTH_PROVIDER": db_user.AUTH_PROVIDER if db_user.AUTH_PROVIDER is not None else "LOCAL",  # 기본값 설정
        "CREATED_AT": db_user.CREATED_AT,
        "UPDATED_AT": db_user.UPDATED_AT if db_user.UPDATED_AT is not None else datetime.utcnow(),  # 기본값 설정
    }
