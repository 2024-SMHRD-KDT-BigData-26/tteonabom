import openai
from fastapi import FastAPI, HTTPException
from pydantic import BaseModel
from dotenv import load_dotenv
import os
from services import generate_answer  # 수정된 services.py에서 import

# 환경 변수 로드
load_dotenv()

# API_KEY를 환경 변수에서 가져오기
API_KEY = os.getenv('OPENAI_API_KEY')
if not API_KEY:
    raise ValueError("API_KEY is not set in the environment variables")

openai.api_key = API_KEY  # OpenAI API 키 설정

app = FastAPI()  # FastAPI 앱 객체 생성

# Pydantic 모델 정의
class PromptRequest(BaseModel):
    prompt: str  # 'prompt' 값을 반드시 받아오도록 설정


# 기본 홈 엔드포인트
@app.get("/")
def read_root():
    return {"message": "Welcome to the homepage!"}


# GPT API를 호출하는 엔드포인트 (POST 요청을 통해 챗봇 응답 받기)
@app.post("/prompt")
async def generate_answer_from_prompt(request: PromptRequest):
    try:
        prompt = request.prompt.strip()  # 공백 제거
        print(f"Received prompt: {prompt}")  # 디버깅을 위해 prompt 출력

        # Prompt가 비어있으면 오류 반환
        if not prompt:
            raise HTTPException(status_code=400, detail="Prompt cannot be empty")

        # GPT-4 모델을 이용한 답변 생성
        answer = await generate_answer(prompt)

        return {"answer": answer}

    except HTTPException as e:
        # HTTPException 발생 시 처리
        raise e
    except Exception as e:
        # 그 외의 예외 처리
        print(f"Unexpected error: {e}")
        raise HTTPException(status_code=500, detail="Internal Server Error")

# 서버 실행 (포트 9000번에서 실행)
if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="127.0.0.1", port=9000)  # 9000번 포트에서 FastAPI 서버 실행
