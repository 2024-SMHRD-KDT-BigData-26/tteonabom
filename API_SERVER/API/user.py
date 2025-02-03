from datetime import datetime
from fastapi import APIRouter, Depends, HTTPException
from pydantic import BaseModel
from sqlalchemy.orm import Session
from DataBase.conn import get_db
from DataBase.models import TB_USERS
import bcrypt

router = APIRouter()


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
    USER_PROFILE_IMG: str = None
    KAKAO_ID: int = None
    AUTH_PROVIDER: str = None
    CREATED_AT: datetime = None
    UPDATED_AT: datetime = None

    class Config:
        from_attributes = True


# ✅ 비밀번호 해싱 함수
def hash_password(password: str) -> str:
    salt = bcrypt.gensalt()
    hashed_pw = bcrypt.hashpw(password.encode("utf-8"), salt)
    return hashed_pw.decode("utf-8")


# ✅ 비밀번호 검증 함수
def verify_password(plain_password: str, hashed_password: str) -> bool:
    return bcrypt.checkpw(plain_password.encode("utf-8"), hashed_password.encode("utf-8"))


# ✅ 회원가입 API (비밀번호 해싱 적용)
@router.post("/api/join")
async def create_user(user: User, db: Session = Depends(get_db)):
    # 비밀번호 해싱
    hashed_pw = hash_password(user.USER_PW)

    db_user = TB_USERS(
        USER_ID=user.USER_ID,
        USER_PW=hashed_pw,  # 해싱된 비밀번호 저장
        USER_NICK=user.USER_NICK,
        USER_PROFILE_IMG=user.USER_PROFILE_IMG,
        KAKAO_ID=user.KAKAO_ID,
        AUTH_PROVIDER=user.AUTH_PROVIDER,
        CREATED_AT=datetime.utcnow(),
        UPDATED_AT=datetime.utcnow()
    )

    db.add(db_user)
    db.commit()
    db.refresh(db_user)
    return db_user


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
@router.put("/users/{USER_ID}")
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


# ✅ 로그인 API
@router.post("/login", response_model=LoginResponse)
async def login(user: LoginRequest, db: Session = Depends(get_db)):
    """ 사용자 로그인 검증 API """

    # 1️⃣ 해당 USER_ID가 존재하는지 확인
    db_user = db.query(TB_USERS).filter(TB_USERS.USER_ID == user.USER_ID).first()
    if not db_user:
        raise HTTPException(status_code=404, detail="User not found")

    # 2️⃣ 비밀번호 검증 (입력한 비밀번호 vs 저장된 해시된 비밀번호)
    if not verify_password(user.USER_PW, db_user.USER_PW):
        raise HTTPException(status_code=401, detail="Invalid password")

    # 3️⃣ 로그인 성공 → 사용자 정보 반환 (비밀번호 제외)
    return db_user
