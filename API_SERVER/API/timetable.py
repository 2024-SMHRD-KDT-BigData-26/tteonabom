from datetime import datetime, date, time
from fastapi import APIRouter, Depends, HTTPException
from pydantic import BaseModel
from sqlalchemy.orm import Session
from DataBase.conn import get_db
from DataBase.models import TB_TIMETABLE

router = APIRouter()


class Timetable(BaseModel):
    tt_idx: int
    sche_idx: str
    tt_date: date
    st_time: time
    poi_idx: int
    tt_order: int
    created_at: datetime
    updated_at: datetime

    class Config:
        from_attributes = True


# ✅ 일정 세부 정보 생성
@router.post("/timetables")
async def create_timetable(timetable: Timetable, db: Session = Depends(get_db)):
    db_timetable = TB_TIMETABLE(**timetable.dict())
    db.add(db_timetable)
    db.commit()
    db.refresh(db_timetable)
    return db_timetable


# ✅ 전체 일정 세부 정보 조회
@router.get("/timetables")
async def get_all_timetables(db: Session = Depends(get_db)):
    return db.query(TB_TIMETABLE).all()


# ✅ 특정 일정 세부 정보 조회
@router.get("/timetables/{tt_idx}")
async def get_timetable(tt_idx: int, db: Session = Depends(get_db)):
    timetable = db.query(TB_TIMETABLE).filter(TB_TIMETABLE.tt_idx == tt_idx).first()
    if not timetable:
        raise HTTPException(status_code=404, detail="Timetable not found")
    return timetable


# ✅ 특정 일정(`sche_idx`)에 속한 세부 일정 조회
@router.get("/timetables/schedule/{sche_idx}")
async def get_timetables_by_schedule(sche_idx: str, db: Session = Depends(get_db)):
    timetables = db.query(TB_TIMETABLE).filter(TB_TIMETABLE.sche_idx == sche_idx).all()
    return timetables


# ✅ 일정 세부 정보 수정
@router.put("/timetables/{tt_idx}")
async def update_timetable(tt_idx: int, timetable: Timetable, db: Session = Depends(get_db)):
    db_timetable = db.query(TB_TIMETABLE).filter(TB_TIMETABLE.tt_idx == tt_idx).first()
    if not db_timetable:
        raise HTTPException(status_code=404, detail="Timetable not found")

    for key, value in timetable.dict().items():
        setattr(db_timetable, key, value)

    db.commit()
    db.refresh(db_timetable)
    return db_timetable


# ✅ 일정 세부 정보 삭제
@router.delete("/timetables/{tt_idx}")
async def delete_timetable(tt_idx: int, db: Session = Depends(get_db)):
    db_timetable = db.query(TB_TIMETABLE).filter(TB_TIMETABLE.tt_idx == tt_idx).first()
    if not db_timetable:
        raise HTTPException(status_code=404, detail="Timetable not found")

    db.delete(db_timetable)
    db.commit()
    return {"detail": "Timetable deleted successfully"}
