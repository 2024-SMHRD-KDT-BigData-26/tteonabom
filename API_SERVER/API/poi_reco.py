from datetime import datetime
from fastapi import APIRouter, Depends, HTTPException
from pydantic import BaseModel
from sqlalchemy.orm import Session
from DataBase.conn import get_db
from DataBase.models import TB_POI_RECO

router = APIRouter()


class PoiReco(BaseModel):
    reco_idx: int
    user_id: str
    poi_idx: int
    created_at: datetime
    reco_reason: str

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
@router.get("/poi_reco/{poi_idx}")
async def get_poi_reco_by_poi(poi_idx: int, db: Session = Depends(get_db)):
    poi_recos = db.query(TB_POI_RECO).filter(TB_POI_RECO.poi_idx == poi_idx).all()
    return poi_recos


# ✅ 특정 사용자의 여행지 추천 조회
@router.get("/poi_reco/user/{user_id}")
async def get_poi_reco_by_user(user_id: str, db: Session = Depends(get_db)):
    poi_recos = db.query(TB_POI_RECO).filter(TB_POI_RECO.user_id == user_id).all()
    return poi_recos


# ✅ 여행지 추천 수정
@router.put("/poi_reco/{reco_idx}")
async def update_poi_reco(reco_idx: int, poi_reco: PoiReco, db: Session = Depends(get_db)):
    db_poi_reco = db.query(TB_POI_RECO).filter(TB_POI_RECO.reco_idx == reco_idx).first()
    if not db_poi_reco:
        raise HTTPException(status_code=404, detail="Poi recommendation not found")

    for key, value in poi_reco.dict().items():
        setattr(db_poi_reco, key, value)

    db.commit()
    db.refresh(db_poi_reco)
    return db_poi_reco


# ✅ 여행지 추천 삭제
@router.delete("/poi_reco/{reco_idx}")
async def delete_poi_reco(reco_idx: int, db: Session = Depends(get_db)):
    db_poi_reco = db.query(TB_POI_RECO).filter(TB_POI_RECO.reco_idx == reco_idx).first()
    if not db_poi_reco:
        raise HTTPException(status_code=404, detail="Poi recommendation not found")

    db.delete(db_poi_reco)
    db.commit()
    return {"detail": "Poi recommendation deleted successfully"}
