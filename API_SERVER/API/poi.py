from datetime import datetime
from fastapi import APIRouter, Depends, HTTPException
from pydantic import BaseModel
from sqlalchemy.orm import Session
from DataBase.conn import get_db
from DataBase.models import TB_POI

router = APIRouter()

class POI(BaseModel):
    poi_idx: int
    poi_nm: str
    poi_info: str
    poi_addr: str
    poi_url: str
    poi_region: str
    poi_tel: str
    poi_period: str
    lat: float
    lon: float
    poi_likes: int = 0
    created_at: datetime
    updated_at: datetime

    class Config:
        orm_mode = True

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
@router.get("/pois/{poi_idx}")
async def get_poi(poi_idx: int, db: Session = Depends(get_db)):
    poi = db.query(TB_POI).filter(TB_POI.poi_idx == poi_idx).first()
    if not poi:
        raise HTTPException(status_code=404, detail="POI not found")
    return poi

# ✅ 특정 지역의 여행지 조회
@router.get("/pois/region/{poi_region}")
async def get_pois_by_region(poi_region: str, db: Session = Depends(get_db)):
    pois = db.query(TB_POI).filter(TB_POI.poi_region == poi_region).all()
    return pois

# ✅ 여행지 수정
@router.put("/pois/{poi_idx}")
async def update_poi(poi_idx: int, poi: POI, db: Session = Depends(get_db)):
    db_poi = db.query(TB_POI).filter(TB_POI.poi_idx == poi_idx).first()
    if not db_poi:
        raise HTTPException(status_code=404, detail="POI not found")

    for key, value in poi.dict().items():
        setattr(db_poi, key, value)

    db.commit()
    db.refresh(db_poi)
    return db_poi

# ✅ 여행지 삭제
@router.delete("/pois/{poi_idx}")
async def delete_poi(poi_idx: int, db: Session = Depends(get_db)):
    db_poi = db.query(TB_POI).filter(TB_POI.poi_idx == poi_idx).first()
    if not db_poi:
        raise HTTPException(status_code=404, detail="POI not found")

    db.delete(db_poi)
    db.commit()
    return {"detail": "POI deleted successfully"}

# ✅ 여행지 좋아요 증가
@router.put("/pois/{poi_idx}/like")
async def like_poi(poi_idx: int, db: Session = Depends(get_db)):
    db_poi = db.query(TB_POI).filter(TB_POI.poi_idx == poi_idx).first()
    if not db_poi:
        raise HTTPException(status_code=404, detail="POI not found")

    db_poi.poi_likes += 1  # 좋아요 수 증가
    db.commit()
    db.refresh(db_poi)
    return {"detail": "POI liked successfully", "poi_likes": db_poi.poi_likes}
