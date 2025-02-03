from datetime import datetime
from fastapi import APIRouter, Depends, HTTPException
from pydantic import BaseModel
from sqlalchemy.orm import Session
from DataBase.conn import get_db
from DataBase.models import TB_FESTIVAL

router = APIRouter()


class Festival(BaseModel):
    FEST_IDX: int
    FEST_NM: str
    FEST_DESC: str
    FEST_ADDR: str
    FEST_URL: str
    FEST_TEL: str
    FEST_PERIOD: str
    FEST_LOC: str
    LAT: float
    LON: float
    CREATED_AT: datetime
    UPDATED_AT: datetime

    class Config:
        from_attributes = True


# ✅ 축제 정보 추가 (등록)
@router.post("/festival")
async def create_festival(festival: Festival, db: Session = Depends(get_db)):
    db_festival = TB_FESTIVAL(**festival.dict())
    db.add(db_festival)
    db.commit()
    db.refresh(db_festival)
    return db_festival


# ✅ 전체 축제 조회
@router.get("/festival")
async def get_all_festivals(db: Session = Depends(get_db)):
    return db.query(TB_FESTIVAL).all()


# ✅ 특정 축제 조회
@router.get("/festival/{FEST_IDX}")
async def get_festival(FEST_IDX: int, db: Session = Depends(get_db)):
    festival = db.query(TB_FESTIVAL).filter(TB_FESTIVAL.FEST_IDX == FEST_IDX).first()
    if not festival:
        raise HTTPException(status_code=404, detail="Festival not found")
    return festival


# ✅ 특정 지역의 축제 조회
@router.get("/festival/region/{REGION}")
async def get_festivals_by_region(REGION: str, db: Session = Depends(get_db)):
    festivals = db.query(TB_FESTIVAL).filter(TB_FESTIVAL.FEST_LOC == REGION).all()
    return festivals


# ✅ 축제 정보 수정
@router.put("/festival/{FEST_IDX}")
async def update_festival(FEST_IDX: int, festival: Festival, db: Session = Depends(get_db)):
    db_festival = db.query(TB_FESTIVAL).filter(TB_FESTIVAL.FEST_IDX == FEST_IDX).first()
    if not db_festival:
        raise HTTPException(status_code=404, detail="Festival not found")

    for key, value in festival.dict().items():
        setattr(db_festival, key, value)

    db.commit()
    db.refresh(db_festival)
    return db_festival


# ✅ 축제 삭제
@router.delete("/festival/{FEST_IDX}")
async def delete_festival(FEST_IDX: int, db: Session = Depends(get_db)):
    db_festival = db.query(TB_FESTIVAL).filter(TB_FESTIVAL.FEST_IDX == FEST_IDX).first()
    if not db_festival:
        raise HTTPException(status_code=404, detail="Festival not found")

    db.delete(db_festival)
    db.commit()
    return {"detail": "Festival deleted successfully"}
