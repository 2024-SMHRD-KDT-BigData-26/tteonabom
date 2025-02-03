from datetime import datetime, date, time
from fastapi import APIRouter, Depends, HTTPException
from pydantic import BaseModel
from sqlalchemy.orm import Session
from DataBase.conn import get_db
from DataBase.models import TB_TIMETABLE

router = APIRouter()


class TimetableCreate(BaseModel):
    SCHE_IDX: str
    TT_DATE: date
    ST_TIME: time
    POI_IDX: int
    TT_ORDER: int = 0  # 기본값 0 설정

    class Config:
        from_attributes = True


class TimetableResponse(TimetableCreate):
    TT_IDX: int
    CREATED_AT: datetime
    UPDATED_AT: datetime | None  # 수정되지 않았을 경우 None 허용


# ✅ 일정 세부 정보 생성
@router.post("/timetables", response_model=TimetableResponse)
async def create_timetable(timetable: TimetableCreate, db: Session = Depends(get_db)):
    db_timetable = TB_TIMETABLE(
        **timetable.dict(),
        CREATED_AT=datetime.utcnow(),
        UPDATED_AT=None
    )
    db.add(db_timetable)
    db.commit()
    db.refresh(db_timetable)
    return db_timetable


# ✅ 전체 일정 세부 정보 조회
@router.get("/timetables", response_model=list[TimetableResponse])
async def get_all_timetables(db: Session = Depends(get_db)):
    return db.query(TB_TIMETABLE).all()


# ✅ 특정 일정 세부 정보 조회
@router.get("/timetables/{TT_IDX}", response_model=TimetableResponse)
async def get_timetable(TT_IDX: int, db: Session = Depends(get_db)):
    timetable = db.query(TB_TIMETABLE).filter(TB_TIMETABLE.TT_IDX == TT_IDX).first()
    if not timetable:
        raise HTTPException(status_code=404, detail="Timetable not found")
    return timetable


# ✅ 특정 일정(`SCHE_IDX`)에 속한 세부 일정 조회
@router.get("/timetables/schedule/{SCHE_IDX}", response_model=list[TimetableResponse])
async def get_timetables_by_schedule(SCHE_IDX: str, db: Session = Depends(get_db)):
    timetables = db.query(TB_TIMETABLE).filter(TB_TIMETABLE.SCHE_IDX == SCHE_IDX).all()
    return timetables


# ✅ 일정 세부 정보 수정
@router.put("/timetables/{TT_IDX}", response_model=TimetableResponse)
async def update_timetable(TT_IDX: int, timetable: TimetableCreate, db: Session = Depends(get_db)):
    db_timetable = db.query(TB_TIMETABLE).filter(TB_TIMETABLE.TT_IDX == TT_IDX).first()
    if not db_timetable:
        raise HTTPException(status_code=404, detail="Timetable not found")

    for key, value in timetable.dict().items():
        setattr(db_timetable, key, value)

    db_timetable.UPDATED_AT = datetime.utcnow()  # 수정 시간 업데이트
    db.commit()
    db.refresh(db_timetable)
    return db_timetable


# ✅ 일정 세부 정보 삭제
@router.delete("/timetables/{TT_IDX}")
async def delete_timetable(TT_IDX: int, db: Session = Depends(get_db)):
    db_timetable = db.query(TB_TIMETABLE).filter(TB_TIMETABLE.TT_IDX == TT_IDX).first()
    if not db_timetable:
        raise HTTPException(status_code=404, detail="Timetable not found")

    db.delete(db_timetable)
    db.commit()
    return {"detail": "Timetable deleted successfully"}
