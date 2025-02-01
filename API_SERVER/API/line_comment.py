from datetime import datetime
from fastapi import APIRouter, Depends, HTTPException
from pydantic import BaseModel
from sqlalchemy.orm import Session
from DataBase.conn import get_db
from DataBase.models import TB_LINE_COMMENT

router = APIRouter()


class LineComment(BaseModel):
    line_idx: int
    poi_idx: int
    line_content: str
    created_at: datetime
    user_id: str

    class Config:
        from_attributes = True


# ✅ 한줄평 추가
@router.post("/line_comment")
async def create_line_comment(line_comment: LineComment, db: Session = Depends(get_db)):
    db_line_comment = TB_LINE_COMMENT(**line_comment.dict())
    db.add(db_line_comment)
    db.commit()
    db.refresh(db_line_comment)
    return db_line_comment


# ✅ 전체 한줄평 조회
@router.get("/line_comment")
async def get_all_line_comments(db: Session = Depends(get_db)):
    return db.query(TB_LINE_COMMENT).all()


# ✅ 특정 여행지의 한줄평 조회
@router.get("/line_comment/{poi_idx}")
async def get_line_comments_by_poi(poi_idx: int, db: Session = Depends(get_db)):
    line_comments = db.query(TB_LINE_COMMENT).filter(TB_LINE_COMMENT.poi_idx == poi_idx).all()
    return line_comments


# ✅ 특정 사용자의 한줄평 조회
@router.get("/line_comment/user/{user_id}")
async def get_line_comments_by_user(user_id: str, db: Session = Depends(get_db)):
    line_comments = db.query(TB_LINE_COMMENT).filter(TB_LINE_COMMENT.user_id == user_id).all()
    return line_comments


# ✅ 한줄평 수정
@router.put("/line_comment/{line_idx}")
async def update_line_comment(line_idx: int, line_comment: LineComment, db: Session = Depends(get_db)):
    db_line_comment = db.query(TB_LINE_COMMENT).filter(TB_LINE_COMMENT.line_idx == line_idx).first()
    if not db_line_comment:
        raise HTTPException(status_code=404, detail="Line comment not found")

    for key, value in line_comment.dict().items():
        setattr(db_line_comment, key, value)

    db.commit()
    db.refresh(db_line_comment)
    return db_line_comment


# ✅ 한줄평 삭제
@router.delete("/line_comment/{line_idx}")
async def delete_line_comment(line_idx: int, db: Session = Depends(get_db)):
    db_line_comment = db.query(TB_LINE_COMMENT).filter(TB_LINE_COMMENT.line_idx == line_idx).first()
    if not db_line_comment:
        raise HTTPException(status_code=404, detail="Line comment not found")

    db.delete(db_line_comment)
    db.commit()
    return {"detail": "Line comment deleted successfully"}
