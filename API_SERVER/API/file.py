from datetime import datetime
from fastapi import APIRouter, Depends, HTTPException
from pydantic import BaseModel
from sqlalchemy.orm import Session
from typing import Optional
from DataBase.conn import get_db
from DataBase.models import TB_FILE

router = APIRouter()


# ✅ 파일 업로드 요청 모델 (입력 시 `FILE_IDX`, `CREATED_AT`, `UPDATED_AT` 제외)
class FileCreate(BaseModel):
    POI_IDX: int
    FILE_NM: str
    FILE_SIZE: int
    FILE_EXT: str
    USER_ID: str
    DISP_ORDER: Optional[int] = None
    REVIEW_IDX: Optional[int] = None

    class Config:
        from_attributes = True


# ✅ 파일 응답 모델 (모든 필드 포함)
class FileResponse(FileCreate):
    FILE_IDX: int
    CREATED_AT: datetime
    UPDATED_AT: Optional[datetime]


# ✅ 파일 업로드 (등록)
@router.post("/file", response_model=FileResponse)
async def upload_file(file: FileCreate, db: Session = Depends(get_db)):
    db_file = TB_FILE(**file.dict())
    db.add(db_file)
    db.commit()
    db.refresh(db_file)
    return db_file


# ✅ 전체 파일 목록 조회
@router.get("/file", response_model=list[FileResponse])
async def get_all_files(db: Session = Depends(get_db)):
    return db.query(TB_FILE).all()


# ✅ 특정 파일 조회
@router.get("/file/{FILE_IDX}", response_model=FileResponse)
async def get_file(FILE_IDX: int, db: Session = Depends(get_db)):
    file = db.query(TB_FILE).filter(TB_FILE.FILE_IDX == FILE_IDX).first()
    if not file:
        raise HTTPException(status_code=404, detail="File not found")
    return file


# ✅ 특정 여행지 관련 파일 조회
@router.get("/file/poi/{POI_IDX}", response_model=list[FileResponse])
async def get_files_by_poi(POI_IDX: int, db: Session = Depends(get_db)):
    files = db.query(TB_FILE).filter(TB_FILE.POI_IDX == POI_IDX).all()
    return files


# ✅ 특정 리뷰 관련 파일 조회
@router.get("/file/review/{REVIEW_IDX}", response_model=list[FileResponse])
async def get_files_by_review(REVIEW_IDX: int, db: Session = Depends(get_db)):
    files = db.query(TB_FILE).filter(TB_FILE.REVIEW_IDX == REVIEW_IDX).all()
    return files


# ✅ 파일 정보 수정
@router.put("/file/{FILE_IDX}", response_model=FileResponse)
async def update_file(FILE_IDX: int, file: FileCreate, db: Session = Depends(get_db)):
    db_file = db.query(TB_FILE).filter(TB_FILE.FILE_IDX == FILE_IDX).first()
    if not db_file:
        raise HTTPException(status_code=404, detail="File not found")

    for key, value in file.dict().items():
        setattr(db_file, key, value)

    db.commit()
    db.refresh(db_file)
    return db_file


# ✅ 파일 삭제
@router.delete("/file/{FILE_IDX}")
async def delete_file(FILE_IDX: int, db: Session = Depends(get_db)):
    db_file = db.query(TB_FILE).filter(TB_FILE.FILE_IDX == FILE_IDX).first()
    if not db_file:
        raise HTTPException(status_code=404, detail="File not found")

    db.delete(db_file)
    db.commit()
    return {"detail": "File deleted successfully"}
