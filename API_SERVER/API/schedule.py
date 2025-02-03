from datetime import datetime, date
from fastapi import APIRouter, Depends, HTTPException, Query
from pydantic import BaseModel
from sqlalchemy.orm import Session
from DataBase.conn import get_db
from DataBase.models import TB_SCHEDULE

router = APIRouter()

class Schedule(BaseModel):
    SCHE_IDX: str
    TOUR_NM: str
    TOUR_TYPE: str
    TOUR_DESC: str = None
    ST_DT: date
    ED_DT: date
    USER_ID: str
    CREATED_AT: datetime
    UPDATED_AT: datetime

    class Config:
        from_attributes = True

# ✅ 일정 추가
@router.post("/schedules")
async def create_schedule(schedule: Schedule, db: Session = Depends(get_db)):
    db_schedule = TB_SCHEDULE(**schedule.dict())
    db.add(db_schedule)
    db.commit()
    db.refresh(db_schedule)
    return db_schedule

# ✅ 전체 일정 조회
@router.get("/schedules")
async def get_all_schedules(db: Session = Depends(get_db)):
    return db.query(TB_SCHEDULE).all()

# ✅ 특정 일정 조회
@router.get("/schedules/{SCHE_IDX}")
async def get_schedule(SCHE_IDX: str, db: Session = Depends(get_db)):
    schedule = db.query(TB_SCHEDULE).filter(TB_SCHEDULE.SCHE_IDX == SCHE_IDX).first()
    if not schedule:
        raise HTTPException(status_code=404, detail="Schedule not found")
    return schedule

# ✅ 특정 사용자의 일정 조회
@router.get("/schedules/user/{USER_ID}")
async def get_schedules_by_user(USER_ID: str, db: Session = Depends(get_db)):
    schedules = db.query(TB_SCHEDULE).filter(TB_SCHEDULE.USER_ID == USER_ID).all()
    return schedules

# ✅ 특정 날짜 범위의 일정 조회
@router.get("/schedules/date-range")
async def get_schedules_by_date_range(
    start_date: date = Query(..., description="조회할 시작 날짜"),
    end_date: date = Query(..., description="조회할 종료 날짜"),
    db: Session = Depends(get_db)
):
    schedules = db.query(TB_SCHEDULE).filter(
        TB_SCHEDULE.ST_DT >= start_date,
        TB_SCHEDULE.ED_DT <= end_date
    ).all()
    return schedules

# ✅ 일정 수정
@router.put("/schedules/{SCHE_IDX}")
async def update_schedule(SCHE_IDX: str, schedule: Schedule, db: Session = Depends(get_db)):
    db_schedule = db.query(TB_SCHEDULE).filter(TB_SCHEDULE.SCHE_IDX == SCHE_IDX).first()
    if not db_schedule:
        raise HTTPException(status_code=404, detail="Schedule not found")

    for key, value in schedule.dict().items():
        setattr(db_schedule, key, value)

    db.commit()
    db.refresh(db_schedule)
    return db_schedule

# ✅ 일정 삭제
@router.delete("/schedules/{SCHE_IDX}")
async def delete_schedule(SCHE_IDX: str, db: Session = Depends(get_db)):
    db_schedule = db.query(TB_SCHEDULE).filter(TB_SCHEDULE.SCHE_IDX == SCHE_IDX).first()
    if not db_schedule:
        raise HTTPException(status_code=404, detail="Schedule not found")

    db.delete(db_schedule)
    db.commit()
    return {"detail": "Schedule deleted successfully"}
