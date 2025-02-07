from datetime import datetime
from fastapi import APIRouter, Depends, HTTPException, UploadFile, File, Form
from pydantic import BaseModel
from sqlalchemy.orm import Session
from DataBase.conn import get_db
from DataBase.models import TB_REVIEW, TB_FILE, TB_USERS, TB_POI
from fastapi.responses import FileResponse
from typing import Optional
import logging
import os
import shutil
import uuid

router = APIRouter()

UPLOAD_DIR = "uploads"
os.makedirs(UPLOAD_DIR, exist_ok=True)  # 업로드 폴더 없으면 생성

class ReviewCreate(BaseModel):
    POI_IDX: int
    USER_ID: str
    REVIEW_CONTENT: str

    class Config:
        from_attributes = True


class ReviewResponse(BaseModel):
    REVIEW_IDX: int
    USER_ID: str
    REVIEW_CONTENT: str
    CREATED_AT: datetime
    USER_NICK: Optional[str] = None  # 선택적 필드로 변경
    USER_PROFILE_IMG: Optional[str] = None
    FILE_URL: Optional[str] = None  # 선택적 필드로 변경
    POI_IDX: Optional[int] = None  # 선택적 필드로 변경
    UPDATED_AT: Optional[datetime] = None  # 선택적 필드로 변경
    POI_NM: Optional[str] = None  # 선택적 필드로 변경

    class Config:
        from_attributes = True

# 유틸리티 함수 추가
def generate_unique_filename(filename: str) -> str:
    file_extension = os.path.splitext(filename)[1]  # 확장자 추출
    unique_filename = f"{uuid.uuid4().hex}{file_extension}"  # 고유 파일명 생성
    return unique_filename


# ✅ 리뷰 생성 + 파일 업로드 추가
@router.post("/reviews", response_model=ReviewResponse)
async def create_review(
    POI_IDX: int = Form(None),
    USER_ID: str = Form(...),
    REVIEW_CONTENT: str = Form(...),
    review_file: UploadFile = File(None),
    db: Session = Depends(get_db)
):
    # 1️⃣ 리뷰 저장
    db_review = TB_REVIEW(
        POI_IDX=POI_IDX,
        USER_ID=USER_ID,
        REVIEW_CONTENT=REVIEW_CONTENT,
        CREATED_AT=datetime.now(),
        UPDATED_AT=None
    )
    db.add(db_review)
    db.commit()
    db.refresh(db_review)  # 저장된 리뷰 가져오기

    # 2️⃣ 파일 저장 (리뷰와 연결)
    if review_file:
        file_ext = os.path.splitext(review_file.filename)[1]
        filename = f"{datetime.now().strftime('%Y%m%d%H%M%S')}_{review_file.filename}"
        file_path = os.path.join(UPLOAD_DIR, filename)

        # 파일을 실제로 저장
        with open(file_path, "wb") as buffer:
            shutil.copyfileobj(review_file.file, buffer)

        # DB에 파일 정보 저장
        db_file = TB_FILE(
            POI_IDX=POI_IDX,
            REVIEW_IDX=db_review.REVIEW_IDX,  # 새로 생성된 리뷰 ID와 연결
            FILE_NM=filename,
            FILE_SIZE=len(await review_file.read()),  # 파일 크기
            FILE_EXT=file_ext,
            USER_ID=USER_ID,
            CREATED_AT=datetime.now(),
            UPDATED_AT=datetime.now()
        )
        db.add(db_file)
        db.commit()
        db.refresh(db_file)

    return db_review


# ✅ 전체 리뷰 조회 (파일 URL + 사용자 정보 포함, 최신 순 정렬)
@router.get("/reviews", response_model=list[ReviewResponse])
async def get_all_reviews(db: Session = Depends(get_db)):
    reviews = (
        db.query(TB_REVIEW)
        .outerjoin(TB_USERS, TB_REVIEW.USER_ID == TB_USERS.USER_ID)
        .outerjoin(TB_FILE, TB_REVIEW.REVIEW_IDX == TB_FILE.REVIEW_IDX)
        .add_columns(
            TB_USERS.USER_NICK,
            TB_USERS.USER_PROFILE_IMG,
            TB_FILE.FILE_NM.label("FILE_URL"),
            TB_REVIEW.POI_IDX  # 추가된 부분: POI_IDX
        )
        .order_by(TB_REVIEW.REVIEW_IDX.desc())
        .all()
    )

    # ✅ 결과를 Pydantic 모델에 맞게 변환
    review_list = [
        {
            "REVIEW_IDX": review.TB_REVIEW.REVIEW_IDX,
            "USER_ID": review.TB_REVIEW.USER_ID,
            "REVIEW_CONTENT": review.TB_REVIEW.REVIEW_CONTENT,
            "CREATED_AT": review.TB_REVIEW.CREATED_AT,
            "USER_NICK": review.USER_NICK if review.USER_NICK else "익명",
            "USER_PROFILE_IMG": review.USER_PROFILE_IMG,
            "FILE_URL": review.FILE_URL,
            "POI_IDX": review.TB_REVIEW.POI_IDX,  # POI_IDX 추가
        }
        for review in reviews
    ]

    return review_list


# ✅ 특정 리뷰 조회 (파일 URL 포함 + 사용자 정보 포함 + POI 정보 포함)
@router.get("/reviews/{REVIEW_IDX}", response_model=ReviewResponse)
async def get_review(REVIEW_IDX: int, db: Session = Depends(get_db)):
    logging.info(f"리뷰 조회 요청: REVIEW_IDX = {REVIEW_IDX}")

    try:
        # 데이터베이스에서 리뷰 정보 조회 (POI 정보를 TB_POI에서 가져옴)
        review = (
            db.query(TB_REVIEW)
            .outerjoin(TB_USERS, TB_REVIEW.USER_ID == TB_USERS.USER_ID)  # 사용자 정보와 조인
            .outerjoin(TB_FILE, TB_REVIEW.REVIEW_IDX == TB_FILE.REVIEW_IDX)  # 파일 정보와 조인
            .outerjoin(TB_POI, TB_REVIEW.POI_IDX == TB_POI.POI_IDX)  # POI 정보를 TB_POI와 조인
            .add_columns(
                TB_USERS.USER_NICK,  # 사용자 닉네임
                TB_USERS.USER_PROFILE_IMG,  # 사용자 프로필 이미지
                TB_FILE.FILE_NM.label("FILE_URL"),  # 파일 URL
                TB_POI.POI_IDX,  # POI_IDX
                TB_POI.POI_NM  # POI 이름
            )
            .filter(TB_REVIEW.REVIEW_IDX == REVIEW_IDX)  # 특정 리뷰 ID로 필터링
            .first()  # 첫 번째 결과만 가져옴
        )

        # 리뷰가 존재하지 않는 경우
        if not review:
            logging.error(f"리뷰를 찾을 수 없습니다: REVIEW_IDX = {REVIEW_IDX}")
            raise HTTPException(status_code=404, detail="Review not found")

        logging.info(f"리뷰 조회 성공: {review}")

        # Pydantic 모델에 맞게 반환할 데이터 준비
        review_data = {
            "REVIEW_IDX": review.TB_REVIEW.REVIEW_IDX,  # 리뷰 ID
            "USER_ID": review.TB_REVIEW.USER_ID,  # 사용자 ID
            "REVIEW_CONTENT": review.TB_REVIEW.REVIEW_CONTENT,  # 리뷰 내용
            "CREATED_AT": review.TB_REVIEW.CREATED_AT,  # 리뷰 작성 시간
            "USER_NICK": review.USER_NICK if review.USER_NICK else "익명",  # 사용자 닉네임 (없으면 '익명'으로 표시)
            "USER_PROFILE_IMG": review.USER_PROFILE_IMG,  # 사용자 프로필 이미지
            "FILE_URL": review.FILE_URL,  # 파일 URL
            "POI_IDX": review.POI_IDX,  # POI IDX
            "POI_NM": review.POI_NM if review.POI_NM else "Unknown",  # POI 이름이 없으면 "Unknown"으로 표시
        }

        return review_data  # 조회된 리뷰 데이터를 반환

    except Exception as e:
        # 예외 발생 시 로그 기록
        logging.error(f"리뷰 조회 중 오류 발생: {str(e)}")
        raise HTTPException(status_code=500, detail="Internal Server Error")


# ✅ 특정 여행지의 리뷰 조회
@router.get("/reviews/poi/{POI_IDX}", response_model=list[ReviewResponse])
async def get_reviews_by_poi(POI_IDX: int, db: Session = Depends(get_db)):
    reviews = db.query(TB_REVIEW).filter(TB_REVIEW.POI_IDX == POI_IDX).all()
    return reviews


# 로그 설정
logging.basicConfig(level=logging.DEBUG)

# ✅ 리뷰 수정 + 파일 업로드 (리뷰 내용 수정 및 파일 교체)
@router.put("/reviews/{REVIEW_IDX}", response_model=ReviewResponse)
async def update_review(
        REVIEW_IDX: int,
        review_content: str = Form(...),
        poi_nm: str = Form(...),
        poi_idx: int = Form(...),
        review_file: UploadFile = File(None),
        db: Session = Depends(get_db)
):
    # 로그 추가: 전달된 값 확인
    print(f"리뷰 수정 요청: REVIEW_IDX = {REVIEW_IDX}, review_content = {review_content}, poi_nm = {poi_nm}, poi_idx = {poi_idx}")

    # 기존 리뷰 조회
    db_review = db.query(TB_REVIEW).filter(TB_REVIEW.REVIEW_IDX == REVIEW_IDX).first()
    if not db_review:
        raise HTTPException(status_code=404, detail="Review not found")

    # 필수 데이터 업데이트
    db_review.REVIEW_CONTENT = review_content
    db_review.POI_NM = poi_nm
    db_review.POI_IDX = poi_idx
    db_review.UPDATED_AT = datetime.now()

    # 파일 처리
    if review_file:
        # 고유한 파일명 생성
        unique_filename = generate_unique_filename(review_file.filename)
        file_path = os.path.join(UPLOAD_DIR, unique_filename)

        # 파일 저장
        try:
            with open(file_path, "wb") as buffer:
                shutil.copyfileobj(review_file.file, buffer)
        except Exception as e:
            raise HTTPException(status_code=500, detail=f"파일 저장 실패: {str(e)}")

        # 기존 파일 삭제
        db_file = db.query(TB_FILE).filter(TB_FILE.REVIEW_IDX == REVIEW_IDX).first()
        if db_file:
            try:
                os.remove(os.path.join(UPLOAD_DIR, db_file.FILE_NM))  # 기존 파일 삭제
                db.delete(db_file)
                db.commit()  # 파일 삭제 후 커밋
            except Exception as e:
                db.rollback()
                raise HTTPException(status_code=500, detail=f"기존 파일 삭제 실패: {str(e)}")

        # 새 파일 정보 저장
        file_size = os.path.getsize(file_path)
        db_file = TB_FILE(
            POI_IDX=db_review.POI_IDX,
            REVIEW_IDX=db_review.REVIEW_IDX,
            FILE_NM=unique_filename,
            FILE_SIZE=file_size,
            FILE_EXT=os.path.splitext(review_file.filename)[1],
            USER_ID=db_review.USER_ID,
            CREATED_AT=datetime.now(),
            UPDATED_AT=datetime.now()
        )
        db.add(db_file)

    # 변경 사항 저장 및 반환
    try:
        db.commit()
        db.refresh(db_review)
    except Exception as e:
        db.rollback()
        raise HTTPException(status_code=500, detail=f"리뷰 업데이트 실패: {str(e)}")

    return db_review


# ✅ 리뷰 삭제
@router.delete("/reviews/{REVIEW_IDX}")
async def delete_review(REVIEW_IDX: int, db: Session = Depends(get_db)):
    db_review = db.query(TB_REVIEW).filter(TB_REVIEW.REVIEW_IDX == REVIEW_IDX).first()
    if not db_review:
        raise HTTPException(status_code=404, detail="Review not found")

    db.delete(db_review)
    db.commit()
    return {"detail": "Review deleted successfully"}

BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
IMG_DIR = os.path.join(BASE_DIR,'uploads/')
SERVER_IMG_DIR = os.path.join('http://localhost:9000/','uploads/')

# ✅ 이미지 불러오기
@router.get('/images/{file_name}')
def get_image(file_name: str):
    file_path = os.path.join(IMG_DIR, file_name)
    if os.path.exists(file_path):
        return FileResponse(file_path)
    return {"error": "File not found"}
