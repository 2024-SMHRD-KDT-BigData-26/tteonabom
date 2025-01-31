from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker

# MySQL에 연결할 URL
DATABASE_URL = "mysql+pymysql://cgi_24K_bigdata26_p3_2:smhrd2@project-db-cgi.smhrd.com:3307/cgi_24K_bigdata26_p3_2"

# SQLAlchemy 엔진 생성
engine = create_engine(DATABASE_URL, connect_args={"charset": "utf8mb4"})

# 세션을 위한 세션메이커 생성
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)


# DB 세션을 가져오는 함수
def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()