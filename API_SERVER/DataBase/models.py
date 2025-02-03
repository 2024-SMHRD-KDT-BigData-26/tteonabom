from sqlalchemy import (
    create_engine, Column, Integer, String, Text, TIMESTAMP, ForeignKey, BigInteger, Date, Time, DECIMAL
)
from sqlalchemy.sql import func
from sqlalchemy.orm import declarative_base, relationship

Base = declarative_base()
# 데이터베이스 연결 및 테이블 생성



class TB_USERS(Base):
    __tablename__ = "TB_USERS"

    USER_ID = Column(String(50), nullable=False, primary_key=True, comment="아이디")
    USER_PW = Column(String(255), comment="비밀번호")
    USER_NICK = Column(String(50), comment="닉네임")
    USER_PROFILE_IMG = Column(String(1000), comment="프로필 사진")
    KAKAO_ID = Column(BigInteger, comment="카카오 고유번호")
    AUTH_PROVIDER = Column(String(10), comment="인증 방식")
    CREATED_AT = Column(TIMESTAMP, server_default=func.current_timestamp(), comment="생성 일시")
    UPDATED_AT = Column(TIMESTAMP, comment="수정 일시")


class TB_POI(Base):
    __tablename__ = "TB_POI"

    POI_IDX = Column(Integer, primary_key=True, autoincrement=True, comment="여행지 고유번호")
    POI_NM = Column(String(255), comment="여행지 명")
    POI_INFO = Column(Text, comment="여행지 설명")
    POI_ADDR = Column(String(1000), comment="여행지 주소")
    POI_URL = Column(String(1000), comment="여행지 URL")
    POI_REGION = Column(String(100), comment="지역")
    POI_TEL = Column(String(20), comment="여행지 전화번호")
    POI_PERIOD = Column(String(1000), comment="이용 시간")
    LAT = Column(DECIMAL(17, 14), server_default="0.00000000000000", comment="위도")
    LON = Column(DECIMAL(17, 14), server_default="0.00000000000000", comment="경도")
    POI_LIKES = Column(Integer, server_default="0", comment="좋아요 수")
    CREATED_AT = Column(TIMESTAMP, server_default=func.current_timestamp(), comment="생성 일시")
    UPDATED_AT = Column(TIMESTAMP, comment="수정 일시")


class TB_POI_RECO(Base):
    __tablename__ = "TB_POI_RECO"

    RECO_IDX = Column(Integer, primary_key=True, autoincrement=True, comment="여추 고유번호")
    USER_ID = Column(String(50), comment="사용자 아이디")
    POI_IDX = Column(Integer, comment="여행지 고유번호")
    CREATED_AT = Column(TIMESTAMP, server_default=func.current_timestamp(), comment="추천 일시")
    RECO_REASON = Column(Text, comment="추천 사유")


class TB_SCHEDULE(Base):
    __tablename__ = "TB_SCHEDULE"

    SCHE_IDX = Column(String(60), primary_key=True, comment="일정 고유번호")
    TOUR_NM = Column(String(255), comment="여행 명")
    TOUR_TYPE = Column(String(50), comment="여행 형태")
    TOUR_DESC = Column(Text, comment="여행 소개")
    ST_DT = Column(Date, comment="시작 일자")
    ED_DT = Column(Date, comment="종료 일자")
    CREATED_AT = Column(TIMESTAMP, server_default=func.current_timestamp(), comment="생성 일시")
    UPDATED_AT = Column(TIMESTAMP, comment="수정 일시")
    USER_ID = Column(String(50), comment="사용자 아이디")


class TB_TIMETABLE(Base):
    __tablename__ = "TB_TIMETABLE"

    TT_IDX = Column(Integer, primary_key=True, autoincrement=True, comment="세부 고유번호")
    SCHE_IDX = Column(String(60), comment="일정 고유번호")
    TT_DATE = Column(Date, comment="여행 날짜")
    ST_TIME = Column(Time, comment="여행 시작 시간")
    POI_IDX = Column(Integer, comment="여행지 고유번호")
    TT_ORDER = Column(Integer, server_default="0", comment="세부 순번")
    CREATED_AT = Column(TIMESTAMP, server_default=func.current_timestamp(), comment="등록 일시")
    UPDATED_AT = Column(TIMESTAMP, comment="수정 일시")


class TB_REVIEW(Base):
    __tablename__ = "TB_REVIEW"

    REVIEW_IDX = Column(Integer, primary_key=True, autoincrement=True, comment="후기 식별자")
    POI_IDX = Column(Integer, comment="여행지 고유번호")
    USER_ID = Column(String(50), comment="사용자 아이디")
    REVIEW_CONTENT = Column(Text, comment="후기 내용")
    CREATED_AT = Column(TIMESTAMP, server_default=func.current_timestamp(), comment="생성 일시")
    UPDATED_AT = Column(TIMESTAMP, comment="수정 일시")


class TB_SHOPPING_MALL(Base):
    __tablename__ = "TB_SHOPPING_MALL"

    MALL_IDX = Column(Integer, primary_key=True, autoincrement=True, comment="몰 고유번호")
    CATEGORY = Column(String(100), comment="카테고리 명")
    MALL_NM = Column(String(255), comment="쇼핑몰 이름")
    MALL_URL = Column(String(1000), comment="쇼핑몰 URL")
    MALL_IMG = Column(String(1000), comment="쇼핑몰 이미지")
    MALL_LIKES = Column(Integer, server_default="0", comment="쇼핑몰 좋아요수")
    CREATED_AT = Column(TIMESTAMP, server_default=func.current_timestamp(), comment="생성 일시")
    UPDATED_AT = Column(TIMESTAMP, comment="수정 일시")


class TB_MALL_RECO(Base):
    __tablename__ = "TB_MALL_RECO"

    RECO_IDX = Column(Integer, primary_key=True, autoincrement=True, comment="쇼추 고유번호")
    CHAT_IDX = Column(Integer, comment="채팅 고유번호")
    MALL_IDX = Column(Integer, comment="몰 고유번호")
    CREATED_AT = Column(TIMESTAMP, server_default=func.current_timestamp(), comment="추천 일시")
    USER_ID = Column(String(50), comment="사용자 아이디")


class TB_FESTIVAL(Base):
    __tablename__ = "TB_FESTIVAL"

    FEST_IDX = Column(Integer, primary_key=True, autoincrement=True, comment="행사 식별자")
    FEST_NM = Column(String(100), comment="행사 이름")
    FEST_DESC = Column(Text, comment="행사 소개")
    FEST_ADDR = Column(String(1000), comment="행사 주소")
    FEST_URL = Column(String(1000), comment="행사 URL")
    FEST_TEL = Column(String(20), comment="행사 전화")
    FEST_PERIOD = Column(String(1000), comment="행사 공연시간")
    FEST_LOC = Column(String(255), comment="행사 장소")
    LAT = Column(DECIMAL(17, 14), comment="위도")
    LON = Column(DECIMAL(17, 14), comment="경도")
    CREATED_AT = Column(TIMESTAMP, server_default=func.current_timestamp(), comment="생성 일시")
    UPDATED_AT = Column(TIMESTAMP, server_default=func.current_timestamp(), comment="수정 일시")


class TB_CHATTING(Base):
    __tablename__ = "TB_CHATTING"

    CHAT_IDX = Column(Integer, primary_key=True, autoincrement=True, comment="채팅 고유번호")
    CROOM_IDX = Column(Integer, comment="방 고유번호")
    USER_ID = Column(String(50), comment="발화자")
    CHAT_CONTENT = Column(Text, comment="발화 내용")
    CHAT_FILE = Column(String(1000), comment="발화 첨부파일")
    CHAT_EMOTION = Column(String(1000), comment="발화 이모티콘")
    CREATED_AT = Column(TIMESTAMP, server_default=func.current_timestamp(), comment="발화 시간")
    USER_CONTENT = Column(Text)


class TB_CROOM(Base):
    __tablename__ = "TB_CROOM"

    CROOM_IDX = Column(Integer, primary_key=True, autoincrement=True, comment="방 고유번호")
    CROOM_TITLE = Column(String(1000), comment="방 제목")
    CROOM_INFO = Column(Text, comment="방 소개")
    USER_ID = Column(String(50), comment="방 개설자")
    CROOM_LIMIT = Column(Integer, server_default="0", comment="방 인원수")
    CREATED_AT = Column(TIMESTAMP, server_default=func.current_timestamp(), comment="방 개설일자")
    CROOM_STATUS = Column(String(10), comment="방 상태")


class TB_LINE_COMMENT(Base):
    __tablename__ = "TB_LINE_COMMENT"

    LINE_IDX = Column(Integer, primary_key=True, autoincrement=True, comment="한줄 고유번호")
    POI_IDX = Column(Integer, comment="여행지 고유번호")
    LINE_CONTENT = Column(String(300), comment="한줄 내용")
    CREATED_AT = Column(TIMESTAMP, server_default=func.current_timestamp(), comment="한줄 작성일자")
    USER_ID = Column(String(50), comment="한줄 작성자")


class TB_FILE(Base):
    __tablename__ = "TB_FILE"

    FILE_IDX = Column(Integer, primary_key=True, autoincrement=True, comment="파일 식별자")
    POI_IDX = Column(Integer, comment="여행지 고유번호")
    FILE_NM = Column(String(1000), comment="파일 명")
    FILE_SIZE = Column(Integer, server_default="0", comment="파일 사이즈")
    FILE_EXT = Column(String(10), comment="파일 확장자")
    CREATED_AT = Column(TIMESTAMP, server_default=func.current_timestamp(), comment="업로드 날짜")
    UPDATED_AT = Column(TIMESTAMP, server_default=func.current_timestamp(), comment="수정 날짜")
    USER_ID = Column(String(50), comment="작성자 아이디")
    DISP_ORDER = Column(Integer, server_default="0", comment="표시 순서")
    REVIEW_IDX = Column(Integer, comment="후기 식별자")


class TB_LIKE(Base):
    __tablename__ = "TB_LIKE"

    LIKE_IDX = Column(Integer, primary_key=True, autoincrement=True, comment="좋아요 식별자")
    USER_ID = Column(String(50), comment="사용자 아이디")
    MALL_IDX = Column(Integer, comment="몰 고유번호")
    POI_IDX = Column(Integer, comment="여행지 고유번호")
    CREATED_AT = Column(TIMESTAMP, server_default=func.current_timestamp(), comment="생성 일시")
