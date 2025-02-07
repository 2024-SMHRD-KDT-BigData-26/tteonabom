from datetime import datetime
from fastapi import APIRouter, Depends, HTTPException
from pydantic import BaseModel
from sqlalchemy.orm import Session
from DataBase.conn import get_db
from DataBase.models import TB_CROOM

router = APIRouter()

class CroomCreate(BaseModel):
    CROOM_TITLE: str
    CROOM_INFO: str
    USER_ID: str
    CROOM_LIMIT: int = 0  # 🟢 기본값 0 설정
    CROOM_STATUS: str
    GPT_RESPONSE: str = ""  # ✅ GPT 추천 일정 추가 (기본값 빈 문자열)

    class Config:
        from_attributes = True


class CroomResponse(BaseModel):
    CROOM_IDX: int
    CROOM_TITLE: str
    CROOM_INFO: str
    USER_ID: str
    CROOM_LIMIT: int
    CREATED_AT: datetime
    CROOM_STATUS: str
    GPT_RESPONSE: str  # ✅ GPT 추천 일정 추가

    class Config:
        from_attributes = True


# ✅ 채팅방 생성
@router.post("/crooms", response_model=CroomResponse)
async def create_croom(croom: CroomCreate, db: Session = Depends(get_db)):
    """ 새로운 채팅방을 생성하는 API (GPT 추천 일정 포함) """
    db_croom = TB_CROOM(
        **croom.model_dump(exclude_unset=True),  # 기본값 유지
        CREATED_AT=datetime.utcnow()  # 생성 시간 자동 설정
    )
    db.add(db_croom)
    db.commit()
    db.refresh(db_croom)
    return db_croom


# ✅ 모든 채팅방 목록 조회 (GPT 추천 일정 포함)
@router.get("/crooms", response_model=list[CroomResponse])
async def get_all_crooms(db: Session = Depends(get_db)):
    """ 모든 채팅방 리스트 조회 (GPT 추천 일정 포함) """
    return db.query(TB_CROOM).all()


# ✅ 특정 채팅방 조회 (GPT 추천 일정 포함)
@router.get("/crooms/{CROOM_IDX}", response_model=CroomResponse)
async def get_croom(CROOM_IDX: int, db: Session = Depends(get_db)):
    """ 특정 채팅방 정보 조회 (GPT 추천 일정 포함) """
    croom = db.query(TB_CROOM).filter(TB_CROOM.CROOM_IDX == CROOM_IDX).first()
    if not croom:
        raise HTTPException(status_code=404, detail="Croom not found")
    return {
        "CROOM_IDX": croom.CROOM_IDX,
        "CROOM_TITLE": croom.CROOM_TITLE,
        "CROOM_INFO": croom.CROOM_INFO,
        "USER_ID": croom.USER_ID,
        "CROOM_LIMIT": croom.CROOM_LIMIT,
        "CREATED_AT": croom.CREATED_AT,
        "CROOM_STATUS": croom.CROOM_STATUS,
        "GPT_RESPONSE": croom.GPT_RESPONSE  # ✅ GPT 추천 일정 포함
    }


# ✅ 특정 사용자가 만든 채팅방 목록 조회 (GPT 추천 일정 포함)
@router.get("/crooms/user/{USER_ID}", response_model=list[CroomResponse])
async def get_crooms_by_user(USER_ID: str, db: Session = Depends(get_db)):
    """ 특정 사용자가 생성한 채팅방 리스트 조회 (GPT 추천 일정 포함) """
    crooms = db.query(TB_CROOM).filter(TB_CROOM.USER_ID == USER_ID).all()
    return [
        {
            "CROOM_IDX": croom.CROOM_IDX,
            "CROOM_TITLE": croom.CROOM_TITLE,
            "CROOM_INFO": croom.CROOM_INFO,
            "USER_ID": croom.USER_ID,
            "CROOM_LIMIT": croom.CROOM_LIMIT,
            "CREATED_AT": croom.CREATED_AT,
            "CROOM_STATUS": croom.CROOM_STATUS,
            "GPT_RESPONSE": croom.GPT_RESPONSE  # ✅ GPT 추천 일정 포함
        }
        for croom in crooms
    ]


# ✅ 채팅방 정보 수정 (GPT 추천 일정 포함)
@router.put("/crooms/{CROOM_IDX}", response_model=CroomResponse)
async def update_croom(CROOM_IDX: int, croom: CroomCreate, db: Session = Depends(get_db)):
    """ 특정 채팅방의 정보를 수정하는 API (GPT 추천 일정 포함) """
    db_croom = db.query(TB_CROOM).filter(TB_CROOM.CROOM_IDX == CROOM_IDX).first()
    if not db_croom:
        raise HTTPException(status_code=404, detail="Croom not found")

    for key, value in croom.dict().items():
        setattr(db_croom, key, value)

    db.commit()
    db.refresh(db_croom)
    return db_croom


# ✅ 채팅방 삭제
@router.delete("/crooms/{CROOM_IDX}")
async def delete_croom(CROOM_IDX: int, db: Session = Depends(get_db)):
    """ 특정 채팅방을 삭제하는 API """
    db_croom = db.query(TB_CROOM).filter(TB_CROOM.CROOM_IDX == CROOM_IDX).first()
    if not db_croom:
        raise HTTPException(status_code=404, detail="Croom not found")

    db.delete(db_croom)
    db.commit()
    return {"detail": "Croom deleted successfully"}
