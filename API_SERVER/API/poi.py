from datetime import datetime
from fastapi import APIRouter, Depends, HTTPException
from pydantic import BaseModel
from sqlalchemy.orm import Session
from DataBase.conn import get_db
from DataBase.models import TB_POI, TB_REVIEW


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

class POIResponseWithCount(BaseModel):
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
    UPDATED_AT: datetime
    REVIEW_COUNT: int  # 여행지에 대한 리뷰 개수

    class Config:
        orm_mode = True


# ✅ 여행지 추가 (등록)
@router.post("/pois", response_model=POIResponse)
async def create_poi(poi: POICreate, db: Session = Depends(get_db)):
    db_poi = TB_POI(
        **poi.dict(),
        POI_LIKES=0,  # 좋아요 초기값 설정
        CREATED_AT=datetime.now(),
        UPDATED_AT=datetime.now()
    )
    db.add(db_poi)
    db.commit()
    db.refresh(db_poi)
    return db_poi


from sqlalchemy import func

# ✅ 전체 여행지 조회 (리뷰 수 포함)
@router.get("/pois", response_model=list[POIResponseWithCount])
async def get_all_pois(db: Session = Depends(get_db)):
    pois = (
        db.query(TB_POI, func.count(TB_REVIEW.REVIEW_IDX).label('review_count'))
        .outerjoin(TB_REVIEW, TB_POI.POI_IDX == TB_REVIEW.POI_IDX)
        .group_by(TB_POI.POI_IDX)
        .all()
    )

    # POI 정보와 리뷰 수를 포함한 리스트 반환
    poi_list = [
        {
            "POI_IDX": poi.TB_POI.POI_IDX,
            "POI_NM": poi.TB_POI.POI_NM,
            "POI_INFO": poi.TB_POI.POI_INFO,
            "POI_ADDR": poi.TB_POI.POI_ADDR,
            "POI_URL": poi.TB_POI.POI_URL,
            "POI_REGION": poi.TB_POI.POI_REGION,
            "POI_TEL": poi.TB_POI.POI_TEL,
            "POI_PERIOD": poi.TB_POI.POI_PERIOD,
            "LAT": poi.TB_POI.LAT,
            "LON": poi.TB_POI.LON,
            "POI_LIKES": poi.TB_POI.POI_LIKES,
            "CREATED_AT": poi.TB_POI.CREATED_AT,
            "UPDATED_AT": poi.TB_POI.UPDATED_AT,
            "REVIEW_COUNT": poi.review_count  # 여행지에 대한 리뷰 개수
        }
        for poi in pois
    ]

    return poi_list

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


# ✅ 여행지 좋아요 증가 (좋아요 누를 때 POI_LIKES 1 증가)
@router.put("/pois/{POI_IDX}/like", response_model=POIResponse)
async def like_poi(POI_IDX: int, db: Session = Depends(get_db)):
    poi = db.query(TB_POI).filter(TB_POI.POI_IDX == POI_IDX).first()
    if not poi:
        raise HTTPException(status_code=404, detail="POI not found")
    poi.POI_LIKES += 1
    db.commit()
    db.refresh(poi)
    return poi


# ✅ 여행지 좋아요 취소 (좋아요 취소 시 POI_LIKES 1 감소)
@router.put("/pois/{POI_IDX}/unlike", response_model=POIResponse)
async def unlike_poi(POI_IDX: int, db: Session = Depends(get_db)):
    poi = db.query(TB_POI).filter(TB_POI.POI_IDX == POI_IDX).first()
    if not poi:
        raise HTTPException(status_code=404, detail="POI not found")
    if poi.POI_LIKES > 0:
        poi.POI_LIKES -= 1
    db.commit()
    db.refresh(poi)
    return poi