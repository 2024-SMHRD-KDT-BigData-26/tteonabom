from datetime import datetime
from fastapi import APIRouter, Depends, HTTPException
from pydantic import BaseModel
from sqlalchemy.orm import Session
from DataBase.conn import get_db
from DataBase.models import TB_POI_RECO

router = APIRouter()


class PoiReco(BaseModel):
    RECO_IDX: int
    USER_ID: str
    POI_IDX: int
    CREATED_AT: datetime
    RECO_REASON: str

    class Config:
        from_attributes = True


# ✅ 여행지 추천 추가
@router.post("/poi_reco")
async def create_poi_reco(poi_reco: PoiReco, db: Session = Depends(get_db)):
    db_poi_reco = TB_POI_RECO(**poi_reco.dict())
    db.add(db_poi_reco)
    db.commit()
    db.refresh(db_poi_reco)
    return db_poi_reco


# ✅ 전체 여행지 추천 조회
@router.get("/poi_reco")
async def get_all_poi_reco(db: Session = Depends(get_db)):
    return db.query(TB_POI_RECO).all()


# ✅ 특정 여행지에 대한 추천 조회
@router.get("/poi_reco/{POI_IDX}")
async def get_poi_reco_by_poi(POI_IDX: int, db: Session = Depends(get_db)):
    poi_recos = db.query(TB_POI_RECO).filter(TB_POI_RECO.POI_IDX == POI_IDX).all()
    return poi_recos


# ✅ 특정 사용자의 여행지 추천 조회
@router.get("/poi_reco/user/{USER_ID}")
async def get_poi_reco_by_user(USER_ID: str, db: Session = Depends(get_db)):
    poi_recos = db.query(TB_POI_RECO).filter(TB_POI_RECO.USER_ID == USER_ID).all()
    return poi_recos


# ✅ 여행지 추천 수정
@router.put("/poi_reco/{RECO_IDX}")
async def update_poi_reco(RECO_IDX: int, poi_reco: PoiReco, db: Session = Depends(get_db)):
    db_poi_reco = db.query(TB_POI_RECO).filter(TB_POI_RECO.RECO_IDX == RECO_IDX).first()
    if not db_poi_reco:
        raise HTTPException(status_code=404, detail="Poi recommendation not found")

    for key, value in poi_reco.dict().items():
        setattr(db_poi_reco, key, value)

    db.commit()
    db.refresh(db_poi_reco)
    return db_poi_reco


# ✅ 여행지 추천 삭제
@router.delete("/poi_reco/{RECO_IDX}")
async def delete_poi_reco(RECO_IDX: int, db: Session = Depends(get_db)):
    db_poi_reco = db.query(TB_POI_RECO).filter(TB_POI_RECO.RECO_IDX == RECO_IDX).first()
    if not db_poi_reco:
        raise HTTPException(status_code=404, detail="Poi recommendation not found")

    db.delete(db_poi_reco)
    db.commit()
    return {"detail": "Poi recommendation deleted successfully"}
