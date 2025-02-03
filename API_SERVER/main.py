from fastapi import FastAPI
import uvicorn
from API import user, chatting, croom, festival, file, mall_reco, poi, review, schedule, shopping_mall, timetable, poi_reco, line_comment, like
from fastapi.middleware.cors import CORSMiddleware

# FastAPI 애플리케이션 생성
app = FastAPI()

# CORS 설정 (프론트엔드 연결용)
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # 특정 도메인만 허용할 수도 있음
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# API 라우팅
app.include_router(user.router)
app.include_router(chatting.router)
app.include_router(croom.router)
app.include_router(festival.router)
app.include_router(file.router)
app.include_router(mall_reco.router)
app.include_router(poi.router)
app.include_router(review.router)
app.include_router(schedule.router)
app.include_router(shopping_mall.router)
app.include_router(timetable.router)
app.include_router(poi_reco.router)
app.include_router(line_comment.router)
app.include_router(like.router)

if __name__ == "__main__":
    uvicorn.run(
        app,
        host="0.0.0.0",
        port=9000
    )  # 9000번 포트에서 FastAPI 서버 실행
