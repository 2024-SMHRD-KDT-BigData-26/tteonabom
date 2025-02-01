from sqlalchemy import (
    create_engine, Column, Integer, String, Text, TIMESTAMP, ForeignKey, BigInteger, Date, Time, DECIMAL
)
from sqlalchemy.sql import func
from sqlalchemy.orm import declarative_base, relationship

Base = declarative_base()
# 데이터베이스 연결 및 테이블 생성


class TB_USERS(Base):
    __tablename__ = "TB_USERS"

    user_id = Column(String(50), primary_key=True, comment="아이디")
    user_pw = Column(String(255), comment="비밀번호")
    user_nick = Column(String(50), comment="닉네임")
    user_profile_img = Column(String(1000), comment="프로필 사진")
    kakao_id = Column(BigInteger, comment="카카오 고유번호")
    auth_provider = Column(String(10), comment="인증 방식")
    created_at = Column(TIMESTAMP, server_default=func.current_timestamp(), comment="생성 일시")
    updated_at = Column(TIMESTAMP, comment="수정 일시")


class TB_CROOM(Base):
    __tablename__ = "TB_CROOM"

    croom_idx = Column(Integer, primary_key=True, autoincrement=True, comment="방 고유번호")
    croom_title = Column(String(1000), comment="방 제목")
    croom_info = Column(Text, comment="방 소개")
    user_id = Column(String(50), comment="방 개설자")
    croom_limit = Column(Integer, default=0, comment="방 인원수")
    created_at = Column(TIMESTAMP, server_default=func.current_timestamp(), comment="방 개설일자")
    croom_status = Column(String(10), comment="방 상태")


class TB_POI(Base):
    __tablename__ = "TB_POI"

    poi_idx = Column(Integer, primary_key=True, autoincrement=True, comment="여행지 고유번호")
    poi_nm = Column(String(255), comment="여행지 명")
    poi_info = Column(Text, comment="여행지 설명")
    poi_addr = Column(String(1000), comment="여행지 주소")
    poi_url = Column(String(1000), comment="여행지 URL")
    poi_region = Column(String(100), comment="지역")
    poi_tel = Column(String(20), comment="여행지 전화번호")
    poi_period = Column(String(1000), comment="이용 시간")
    lat = Column(DECIMAL(17, 14), default=0.0, comment="위도")
    lon = Column(DECIMAL(17, 14), default=0.0, comment="경도")
    poi_likes = Column(Integer, default=0, comment="좋아요 수")
    created_at = Column(TIMESTAMP, server_default=func.current_timestamp(), comment="생성 일시")
    updated_at = Column(TIMESTAMP, comment="수정 일시")


class TB_SHOPPING_MALL(Base):
    __tablename__ = "TB_SHOPPING_MALL"

    mall_idx = Column(Integer, primary_key=True, autoincrement=True, comment="몰 고유번호")
    category = Column(String(100), comment="카테고리 명")
    mall_nm = Column(String(255), comment="쇼핑몰 이름")
    mall_url = Column(String(1000), comment="쇼핑몰 URL")
    mall_img = Column(String(1000), comment="쇼핑몰 이미지")
    mall_likes = Column(Integer, default=0, comment="쇼핑몰 좋아요수")
    created_at = Column(TIMESTAMP, server_default=func.current_timestamp(), comment="생성 일시")
    updated_at = Column(TIMESTAMP, comment="수정 일시")


class TB_CHATTING(Base):
    __tablename__ = "TB_CHATTING"

    chat_idx = Column(Integer, primary_key=True, autoincrement=True, comment="채팅 고유번호")
    croom_idx = Column(Integer, comment="방 고유번호")
    chatter = Column(String(50), comment="발화자")
    chat_content = Column(Text, comment="발화 내용")
    chat_file = Column(String(1000), comment="발화 첨부파일")
    chat_emotion = Column(String(1000), comment="발화 이모티콘")
    created_at = Column(TIMESTAMP, server_default=func.current_timestamp(), comment="발화 시간")


class TB_REVIEW(Base):
    __tablename__ = "TB_REVIEW"

    review_idx = Column(Integer, primary_key=True, autoincrement=True, comment="후기 식별자")
    poi_idx = Column(Integer, comment="여행지 고유번호")
    user_id = Column(String(50), comment="사용자 아이디")
    review_content = Column(Text, comment="후기 내용")
    created_at = Column(TIMESTAMP, server_default=func.current_timestamp(), comment="생성 일시")
    updated_at = Column(TIMESTAMP, comment="수정 일시")


class TB_SCHEDULE(Base):
    __tablename__ = "TB_SCHEDULE"

    sche_idx = Column(String(60), primary_key=True, comment="일정 고유번호")
    tour_nm = Column(String(255), comment="여행 명")
    tour_type = Column(String(50), comment="여행 형태")
    tour_desc = Column(Text, comment="여행 소개")
    st_dt = Column(Date, comment="시작 일자")
    ed_dt = Column(Date, comment="종료 일자")
    created_at = Column(TIMESTAMP, server_default=func.current_timestamp(), comment="생성 일시")
    updated_at = Column(TIMESTAMP, comment="수정 일시")
    user_id = Column(String(50), comment="사용자 아이디")


class TB_TIMETABLE(Base):
    __tablename__ = "TB_TIMETABLE"

    tt_idx = Column(Integer, primary_key=True, autoincrement=True, comment="세부 고유번호")
    sche_idx = Column(String(60), comment="일정 고유번호")
    tt_date = Column(Date, comment="여행 날짜")
    st_time = Column(Time, comment="여행 시작 시간")
    poi_idx = Column(Integer, comment="여행지 고유번호")
    tt_order = Column(Integer, default=0, comment="세부 순번")
    created_at = Column(TIMESTAMP, server_default=func.current_timestamp(), comment="등록 일시")
    updated_at = Column(TIMESTAMP, comment="수정 일시")


class TB_POI_RECO(Base):
    __tablename__ = "TB_POI_RECO"

    reco_idx = Column(Integer, primary_key=True, autoincrement=True, comment="여추 고유번호")
    user_id = Column(String(50), comment="사용자 아이디")
    poi_idx = Column(Integer, comment="여행지 고유번호")
    created_at = Column(TIMESTAMP, server_default=func.current_timestamp(), comment="추천 일시")
    reco_reason = Column(Text, comment="추천 사유")


class TB_MALL_RECO(Base):
    __tablename__ = "TB_MALL_RECO"

    reco_idx = Column(Integer, primary_key=True, autoincrement=True, comment="쇼추 고유번호")
    chat_idx = Column(Integer, comment="채팅 고유번호")
    mall_idx = Column(Integer, comment="몰 고유번호")
    created_at = Column(TIMESTAMP, server_default=func.current_timestamp(), comment="추천 일시")
    user_id = Column(String(50), comment="사용자 아이디")


class TB_LINE_COMMENT(Base):
    __tablename__ = "TB_LINE_COMMENT"

    line_idx = Column(Integer, primary_key=True, autoincrement=True, comment="한줄 고유번호")
    poi_idx = Column(Integer, comment="여행지 고유번호")
    line_content = Column(String(300), comment="한줄 내용")
    created_at = Column(TIMESTAMP, server_default=func.current_timestamp(), comment="한줄 작성일자")
    user_id = Column(String(50), comment="한줄 작성자")


class TB_FILE(Base):
    __tablename__ = "TB_FILE"

    file_idx = Column(Integer, primary_key=True, autoincrement=True, comment="파일 식별자")
    poi_idx = Column(Integer, comment="여행지 고유번호")
    file_nm = Column(String(1000), comment="파일 명")
    file_size = Column(Integer, default=0, comment="파일 사이즈")
    file_ext = Column(String(10), comment="파일 확장자")
    created_at = Column(TIMESTAMP, server_default=func.current_timestamp(), comment="업로드 날짜")
    updated_at = Column(TIMESTAMP, server_default=func.current_timestamp(), comment="수정 날짜")
    user_id = Column(String(50), comment="작성자 아이디")
    disp_order = Column(Integer, default=0, comment="표시 순서")
    review_idx = Column(Integer, comment="후기 식별자")



class TB_FESTIVAL(Base):
    __tablename__ = "TB_FESTIVAL"

    fest_idx = Column(Integer, primary_key=True, autoincrement=True, comment="행사 식별자")
    fest_nm = Column(String(100), comment="행사 이름")
    fest_desc = Column(Text, comment="행사 소개")
    fest_addr = Column(String(1000), comment="행사 주소")
    fest_url = Column(String(1000), comment="행사 URL")
    fest_tel = Column(String(20), comment="행사 전화")
    fest_period = Column(String(1000), comment="행사 공연시간")
    fest_loc = Column(String(255), comment="행사 장소")
    lat = Column(DECIMAL(17, 14), comment="위도")
    lon = Column(DECIMAL(17, 14), comment="경도")
    created_at = Column(TIMESTAMP, server_default=func.current_timestamp(), comment="생성 일시")
    updated_at = Column(TIMESTAMP, server_default=func.current_timestamp(), comment="수정 일시")



class TB_LIKE(Base) :
    __tavlename__ = "TB_LIKE"

    like_idx = Column(Integer, primary_key=True, autoincrement=True, comment="좋아요 식별자")
    user_id = Column(String(50), comment="사용자 아이디")
    mall_idx = Column(Integer, comment="몰 고유번호")
    poi_idx = Column(Integer, comment="여행지 고유번호")
    created_at = Column(TIMESTAMP, server_default=func.current_timestamp(), comment="생성 일시")