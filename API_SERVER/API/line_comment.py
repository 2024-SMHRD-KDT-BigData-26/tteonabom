from datetime import datetime
from fastapi import APIRouter, Depends, HTTPException
from pydantic import BaseModel
from sqlalchemy.orm import Session
from typing import Optional
from DataBase.conn import get_db
from DataBase.models import TB_LINE_COMMENT

router = APIRouter()


# ✅ 한줄평 요청 모델 (입력 시 `LINE_IDX`, `CREATED_AT` 제외)
class LineCommentCreate(BaseModel):
    POI_IDX: int
    LINE_CONTENT: str
    USER_ID: str

    class Config:
        from_attributes = True


# ✅ 한줄평 응답 모델 (모든 필드 포함)
class LineCommentResponse(LineCommentCreate):
    LINE_IDX: int
    CREATED_AT: datetime


# ✅ 한줄평 추가
@router.post("/line_comment", response_model=LineCommentResponse)
async def create_line_comment(line_comment: LineCommentCreate, db: Session = Depends(get_db)):
    db_line_comment = TB_LINE_COMMENT(**line_comment.dict())
    db.add(db_line_comment)
    db.commit()
    db.refresh(db_line_comment)
    return db_line_comment


# ✅ 전체 한줄평 조회
@router.get("/line_comment", response_model=list[LineCommentResponse])
async def get_all_line_comments(db: Session = Depends(get_db)):
    return db.query(TB_LINE_COMMENT).all()


# ✅ 특정 여행지의 한줄평 조회
@router.get("/line_comment/{POI_IDX}", response_model=list[LineCommentResponse])
async def get_line_comments_by_poi(POI_IDX: int, db: Session = Depends(get_db)):
    line_comments = db.query(TB_LINE_COMMENT).filter(TB_LINE_COMMENT.POI_IDX == POI_IDX).all()
    return line_comments


# ✅ 특정 사용자의 한줄평 조회
@router.get("/line_comment/user/{USER_ID}", response_model=list[LineCommentResponse])
async def get_line_comments_by_user(USER_ID: str, db: Session = Depends(get_db)):
    line_comments = db.query(TB_LINE_COMMENT).filter(TB_LINE_COMMENT.USER_ID == USER_ID).all()
    return line_comments


# ✅ 한줄평 수정
@router.put("/line_comment/{LINE_IDX}", response_model=LineCommentResponse)
async def update_line_comment(LINE_IDX: int, line_comment: LineCommentCreate, db: Session = Depends(get_db)):
    db_line_comment = db.query(TB_LINE_COMMENT).filter(TB_LINE_COMMENT.LINE_IDX == LINE_IDX).first()
    if not db_line_comment:
        raise HTTPException(status_code=404, detail="Line comment not found")

    for key, value in line_comment.dict().items():
        setattr(db_line_comment, key, value)

    db.commit()
    db.refresh(db_line_comment)
    return db_line_comment


# ✅ 한줄평 삭제
@router.delete("/line_comment/{LINE_IDX}")
async def delete_line_comment(LINE_IDX: int, db: Session = Depends(get_db)):
    db_line_comment = db.query(TB_LINE_COMMENT).filter(TB_LINE_COMMENT.LINE_IDX == LINE_IDX).first()
    if not db_line_comment:
        raise HTTPException(status_code=404, detail="Line comment not found")

    db.delete(db_line_comment)
    db.commit()
    return {"detail": "Line comment deleted successfully"}
