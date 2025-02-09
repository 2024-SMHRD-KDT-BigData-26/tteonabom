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
    CROOM_LIMIT: int = 0  # 기본값 0 설정
    CROOM_STATUS: str
    GPT_RESPONSE: str = None  # ✅ GPT 추천 일정 기본값 None

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
    GPT_RESPONSE: str = None  # ✅ GPT 추천 일정 기본값 None

    class Config:
        from_attributes = True


# ✅ 채팅방 생성
@router.post("/crooms", response_model=CroomResponse)
async def create_croom(croom: CroomCreate, db: Session = Depends(get_db)):
    """ 새로운 채팅방을 생성하는 API """
    db_croom = TB_CROOM(
        **croom.model_dump(exclude_unset=True),
        CREATED_AT=datetime.utcnow()  # 생성 시간 자동 설정
    )
    db.add(db_croom)
    db.commit()
    db.refresh(db_croom)
    return db_croom


# ✅ 모든 채팅방 목록 조회
@router.get("/crooms", response_model=list[CroomResponse])
async def get_all_crooms(db: Session = Depends(get_db)):
    """ 모든 채팅방 리스트 조회 """
    return db.query(TB_CROOM).all()


# ✅ 특정 채팅방 조회
@router.get("/crooms/{CROOM_IDX}", response_model=CroomResponse)
async def get_croom(CROOM_IDX: int, db: Session = Depends(get_db)):
    """ 특정 채팅방 정보 조회 """
    croom = db.query(TB_CROOM).filter(TB_CROOM.CROOM_IDX == CROOM_IDX).first()
    if not croom:
        raise HTTPException(status_code=404, detail="채팅방을 찾을 수 없습니다.")
    return croom


# ✅ 특정 사용자가 만든 채팅방 목록 조회
@router.get("/crooms/user/{USER_ID}", response_model=list[CroomResponse])
async def get_crooms_by_user(USER_ID: str, db: Session = Depends(get_db)):
    """ 특정 사용자가 생성한 채팅방 리스트 조회 """
    crooms = db.query(TB_CROOM).filter(TB_CROOM.USER_ID == USER_ID).all()
    return crooms


# ✅ 특정 채팅방의 GPT 추천 일정 업데이트
@router.put("/crooms/{CROOM_IDX}/gpt", response_model=CroomResponse)
async def update_croom_gpt(CROOM_IDX: int, gpt_response: str, db: Session = Depends(get_db)):
    """ 특정 채팅방의 GPT 추천 일정(GPT_RESPONSE)만 업데이트하는 API """
    db_croom = db.query(TB_CROOM).filter(TB_CROOM.CROOM_IDX == CROOM_IDX).first()
    if not db_croom:
        raise HTTPException(status_code=404, detail="채팅방을 찾을 수 없습니다.")

    db_croom.GPT_RESPONSE = gpt_response
    db.commit()
    db.refresh(db_croom)
    return db_croom


# ✅ 채팅방 정보 수정
@router.put("/crooms/{CROOM_IDX}", response_model=CroomResponse)
async def update_croom(CROOM_IDX: int, croom: CroomCreate, db: Session = Depends(get_db)):
    """ 특정 채팅방의 정보를 수정하는 API """
    db_croom = db.query(TB_CROOM).filter(TB_CROOM.CROOM_IDX == CROOM_IDX).first()
    if not db_croom:
        raise HTTPException(status_code=404, detail="채팅방을 찾을 수 없습니다.")

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
        raise HTTPException(status_code=404, detail="채팅방을 찾을 수 없습니다.")

    db.delete(db_croom)
    db.commit()
    return {"detail": "채팅방이 삭제되었습니다."}
