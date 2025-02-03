from datetime import datetime
from fastapi import APIRouter, Depends, HTTPException
from pydantic import BaseModel
from sqlalchemy.orm import Session
from DataBase.conn import get_db
from DataBase.models import TB_POI

router = APIRouter()


class POI(BaseModel):
    POI_IDX: int
    POI_NM: str
    POI_INFO: str
    POI_ADDR: str
    POI_URL: str
    POI_REGION: str
    POI_TEL: str
    POI_PERIOD: str
    LAT: float
    LON: float
    POI_LIKES: int = 0
    CREATED_AT: datetime
    UPDATED_AT: datetime

    class Config:
        from_attributes = True


# ✅ 여행지 추가
@router.post("/pois")
async def create_poi(poi: POI, db: Session = Depends(get_db)):
    db_poi = TB_POI(**poi.dict())
    db.add(db_poi)
    db.commit()
    db.refresh(db_poi)
    return db_poi


# ✅ 전체 여행지 조회
@router.get("/pois")
async def get_all_pois(db: Session = Depends(get_db)):
    return db.query(TB_POI).all()


# ✅ 특정 여행지 조회
@router.get("/pois/{POI_IDX}")
async def get_poi(POI_IDX: int, db: Session = Depends(get_db)):
    poi = db.query(TB_POI).filter(TB_POI.POI_IDX == POI_IDX).first()
    if not poi:
        raise HTTPException(status_code=404, detail="POI not found")
    return poi


# ✅ 특정 지역의 여행지 조회
@router.get("/pois/region/{POI_REGION}")
async def get_pois_by_region(POI_REGION: str, db: Session = Depends(get_db)):
    pois = db.query(TB_POI).filter(TB_POI.POI_REGION == POI_REGION).all()
    return pois


# ✅ 여행지 수정
@router.put("/pois/{POI_IDX}")
async def update_poi(POI_IDX: int, poi: POI, db: Session = Depends(get_db)):
    db_poi = db.query(TB_POI).filter(TB_POI.POI_IDX == POI_IDX).first()
    if not db_poi:
        raise HTTPException(status_code=404, detail="POI not found")

    for key, value in poi.dict().items():
        setattr(db_poi, key, value)

    db.commit()
    db.refresh(db_poi)
    return db_poi


# ✅ 여행지 삭제
@router.delete("/pois/{POI_IDX}")
async def delete_poi(POI_IDX: int, db: Session = Depends(get_db)):
    db_poi = db.query(TB_POI).filter(TB_POI.POI_IDX == POI_IDX).first()
    if not db_poi:
        raise HTTPException(status_code=404, detail="POI not found")

    db.delete(db_poi)
    db.commit()
    return {"detail": "POI deleted successfully"}


# ✅ 여행지 좋아요 증가
@router.put("/pois/{POI_IDX}/like")
async def like_poi(POI_IDX: int, db: Session = Depends(get_db)):
    db_poi = db.query(TB_POI).filter(TB_POI.POI_IDX == POI_IDX).first()
    if not db_poi:
        raise HTTPException(status_code=404, detail="POI not found")

    db_poi.POI_LIKES += 1  # 좋아요 수 증가
    db.commit()
    db.refresh(db_poi)
    return {"detail": "POI liked successfully", "POI_LIKES": db_poi.POI_LIKES}
