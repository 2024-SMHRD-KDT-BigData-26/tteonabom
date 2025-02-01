from datetime import datetime, date
from fastapi import APIRouter, Depends, HTTPException, Query
from pydantic import BaseModel
from sqlalchemy.orm import Session
from DataBase.conn import get_db
from DataBase.models import TB_SCHEDULE

router = APIRouter()

class Schedule(BaseModel):
    sche_idx: str
    tour_nm: str
    tour_type: str
    tour_desc: str = None
    st_dt: date
    ed_dt: date
    user_id: str
    created_at: datetime
    updated_at: datetime

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
@router.get("/schedules/{sche_idx}")
async def get_schedule(sche_idx: str, db: Session = Depends(get_db)):
    schedule = db.query(TB_SCHEDULE).filter(TB_SCHEDULE.sche_idx == sche_idx).first()
    if not schedule:
        raise HTTPException(status_code=404, detail="Schedule not found")
    return schedule

# ✅ 특정 사용자의 일정 조회
@router.get("/schedules/user/{user_id}")
async def get_schedules_by_user(user_id: str, db: Session = Depends(get_db)):
    schedules = db.query(TB_SCHEDULE).filter(TB_SCHEDULE.user_id == user_id).all()
    return schedules

# ✅ 특정 날짜 범위의 일정 조회
@router.get("/schedules/date-range")
async def get_schedules_by_date_range(
    start_date: date = Query(..., description="조회할 시작 날짜"),
    end_date: date = Query(..., description="조회할 종료 날짜"),
    db: Session = Depends(get_db)
):
    schedules = db.query(TB_SCHEDULE).filter(
        TB_SCHEDULE.st_dt >= start_date,
        TB_SCHEDULE.ed_dt <= end_date
    ).all()
    return schedules

# ✅ 일정 수정
@router.put("/schedules/{sche_idx}")
async def update_schedule(sche_idx: str, schedule: Schedule, db: Session = Depends(get_db)):
    db_schedule = db.query(TB_SCHEDULE).filter(TB_SCHEDULE.sche_idx == sche_idx).first()
    if not db_schedule:
        raise HTTPException(status_code=404, detail="Schedule not found")

    for key, value in schedule.dict().items():
        setattr(db_schedule, key, value)

    db.commit()
    db.refresh(db_schedule)
    return db_schedule

# ✅ 일정 삭제
@router.delete("/schedules/{sche_idx}")
async def delete_schedule(sche_idx: str, db: Session = Depends(get_db)):
    db_schedule = db.query(TB_SCHEDULE).filter(TB_SCHEDULE.sche_idx == sche_idx).first()
    if not db_schedule:
        raise HTTPException(status_code=404, detail="Schedule not found")

    db.delete(db_schedule)
    db.commit()
    return {"detail": "Schedule deleted successfully"}
