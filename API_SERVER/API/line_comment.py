# line_comment.py
from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session
from DataBase.conn import get_db
from DataBase.models import TB_LINE_COMMENT
from pydantic import BaseModel
from datetime import datetime

router = APIRouter()

class LineComment(BaseModel):
    line_idx: int
    poi_idx: int
    line_content: str
    created_at: datetime
    user_id: str

    class Config:
        orm_mode = True

@router.post("/line_comment")
async def create_line_comment(line_comment: LineComment, db: Session = Depends(get_db)):
    line_comment_dict = {
        "line_idx": line_comment.line_idx,
        "poi_idx": line_comment.poi_idx,
        "line_content": line_comment.line_content,
        "created_at": line_comment.created_at,
        "user_id": line_comment.user_id
    }
    return line_comment_dict
