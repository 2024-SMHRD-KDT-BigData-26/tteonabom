from datetime import datetime
from fastapi import APIRouter, Depends, HTTPException
from pydantic import BaseModel
from sqlalchemy.orm import Session
from DataBase.conn import get_db
from DataBase.models import TB_POI

router = APIRouter()


class POICreate(BaseModel):
    POI_NM: str
    POI_INFO: str
    POI_ADDR: str
    POI_URL: str
    POI_REGION: str
    POI_TEL: str
    POI_PERIOD: str
    LAT: float = 0.0  # 기본값 설정
    LON: float = 0.0  # 기본값 설정

    class Config:
        from_attributes = True


class POIResponse(BaseModel):
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
    POI_LIKES: int
    CREATED_AT: datetime
    UPDATED_AT: datetime = None

    class Config:
        from_attributes = True


# ✅ 여행지 추가 (등록)
@router.post("/pois", response_model=POIResponse)
async def create_poi(poi: POICreate, db: Session = Depends(get_db)):
    db_poi = TB_POI(
        **poi.dict(),
        POI_LIKES=0,  # 좋아요 초기값 설정
        CREATED_AT=datetime.utcnow(),
        UPDATED_AT=datetime.utcnow()
    )
    db.add(db_poi)
    db.commit()
    db.refresh(db_poi)
    return db_poi


# ✅ 전체 여행지 조회
@router.get("/pois", response_model=list[POIResponse])
async def get_all_pois(db: Session = Depends(get_db)):
    return db.query(TB_POI).all()


# ✅ 특정 여행지 조회
@router.get("/pois/{POI_IDX}", response_model=POIResponse)
async def get_poi(POI_IDX: int, db: Session = Depends(get_db)):
    poi = db.query(TB_POI).filter(TB_POI.POI_IDX == POI_IDX).first()
    if not poi:
        raise HTTPException(status_code=404, detail="POI not found")
    return poi


# ✅ 특정 지역의 여행지 조회
@router.get("/pois/region/{POI_REGION}", response_model=list[POIResponse])
async def get_pois_by_region(POI_REGION: str, db: Session = Depends(get_db)):
    pois = db.query(TB_POI).filter(TB_POI.POI_REGION == POI_REGION).all()
    return pois


# ✅ 여행지 수정
@router.put("/pois/{POI_IDX}", response_model=POIResponse)
async def update_poi(POI_IDX: int, poi: POICreate, db: Session = Depends(get_db)):
    db_poi = db.query(TB_POI).filter(TB_POI.POI_IDX == POI_IDX).first()
    if not db_poi:
        raise HTTPException(status_code=404, detail="POI not found")

    for key, value in poi.dict().items():
        setattr(db_poi, key, value)

    db_poi.UPDATED_AT = datetime.utcnow()  # 수정 시간 갱신

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

    db_poi.POI_LIKES += 1  # 좋아요 증가
    db.commit()
    db.refresh(db_poi)
    return {"detail": "POI liked successfully", "POI_LIKES": db_poi.POI_LIKES}
