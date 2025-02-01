from datetime import datetime
from fastapi import APIRouter, Depends, HTTPException
from pydantic import BaseModel
from sqlalchemy.orm import Session
from DataBase.conn import get_db
from DataBase.models import TB_FILE

router = APIRouter()


class File(BaseModel):
    file_idx: int
    poi_idx: int
    file_nm: str
    file_size: int
    file_ext: str
    created_at: datetime
    updated_at: datetime
    user_id: str
    disp_order: int
    review_idx: int

    class Config:
        from_attributes = True


# ✅ 파일 업로드 (등록)
@router.post("/file")
async def upload_file(file: File, db: Session = Depends(get_db)):
    db_file = TB_FILE(**file.dict())
    db.add(db_file)
    db.commit()
    db.refresh(db_file)
    return db_file


# ✅ 전체 파일 목록 조회
@router.get("/file")
async def get_all_files(db: Session = Depends(get_db)):
    return db.query(TB_FILE).all()


# ✅ 특정 파일 조회
@router.get("/file/{file_idx}")
async def get_file(file_idx: int, db: Session = Depends(get_db)):
    file = db.query(TB_FILE).filter(TB_FILE.file_idx == file_idx).first()
    if not file:
        raise HTTPException(status_code=404, detail="File not found")
    return file


# ✅ 특정 여행지 관련 파일 조회
@router.get("/file/poi/{poi_idx}")
async def get_files_by_poi(poi_idx: int, db: Session = Depends(get_db)):
    files = db.query(TB_FILE).filter(TB_FILE.poi_idx == poi_idx).all()
    return files


# ✅ 특정 리뷰 관련 파일 조회
@router.get("/file/review/{review_idx}")
async def get_files_by_review(review_idx: int, db: Session = Depends(get_db)):
    files = db.query(TB_FILE).filter(TB_FILE.review_idx == review_idx).all()
    return files


# ✅ 파일 정보 수정
@router.put("/file/{file_idx}")
async def update_file(file_idx: int, file: File, db: Session = Depends(get_db)):
    db_file = db.query(TB_FILE).filter(TB_FILE.file_idx == file_idx).first()
    if not db_file:
        raise HTTPException(status_code=404, detail="File not found")

    for key, value in file.dict().items():
        setattr(db_file, key, value)

    db.commit()
    db.refresh(db_file)
    return db_file


# ✅ 파일 삭제
@router.delete("/file/{file_idx}")
async def delete_file(file_idx: int, db: Session = Depends(get_db)):
    db_file = db.query(TB_FILE).filter(TB_FILE.file_idx == file_idx).first()
    if not db_file:
        raise HTTPException(status_code=404, detail="File not found")

    db.delete(db_file)
    db.commit()
    return {"detail": "File deleted successfully"}
