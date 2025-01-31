import openai
from openai import OpenAIError
from dotenv import load_dotenv
import os

# 환경 변수 로드
load_dotenv()

# API_KEY를 환경 변수에서 가져오기
API_KEY = os.getenv('OPENAI_API_KEY')
if not API_KEY:
    raise ValueError("API_KEY is not set in the environment variables")

openai.api_key = API_KEY  # OpenAI API 키 설정


async def generate_answer(prompt: str):
    """GPT-4 모델을 이용한 답변 생성"""
    try:
        # 프리프롬프트와 함께 GPT-4 모델에 prompt를 보내고 응답을 받음
        completion = openai.ChatCompletion.create(
            model="gpt-4",  # GPT-4 모델로 설정
            messages=[  # GPT-4 메시지 형식에 맞게 데이터 전달
                {"role": "system", "content": """
                    당신은 전문 여행 플래너 AI입니다. 사용자가 제공한 정보를 바탕으로 아래의 세부 사항을 모두 반영하여 답변하세요.
                    항상 **일관된 형식**으로 작성하며, 아래 답변 형식에 따라 사용자의 요구를 충족하세요.

                    ---

                    [답변 형식]

                    ### :one: **여행 개요**
                    - **여행지**: [사용자가 입력한 목적지]
                    - **여행 기간**: [사용자가 입력한 여행 기간에 따른 일정 개요]
                    - **동행자 유형**: [동행자 유형에 따른 여행지와 활동 추천]
                    - **일정 스타일**: [여유로운 일정/빡빡한 일정에 맞춘 추천]

                    ### :two: **추천 일정**
                    - **일정 Day 1**:
                      - 오전: [첫날의 주요 명소 및 활동 추천]
                      - 오후: [첫날 오후의 활동 및 방문 명소]
                      - 저녁: [저녁 시간대의 추천 활동]

                    ### :three: **교통 정보**
                    - **출발지**: [사용자가 입력한 현재 위치]
                    - **이동 수단**: [추천 교통수단]
                    - **예상 교통비**: [교통비와 시간 정보]
                    - **소요 시간**: [소요 시간]

                    ### :four: **예산 및 준비물**
                    - **총 예상 예산 **: [총 예산 요약]
                    - **항목별 예산**: 교통비, 숙박비 등
                    - **준비물**: [여행에 필요한 물품]

                    ### :five: **여행 팁**
                    - **맞춤 팁**: [여행 스타일 및 동행자 유형에 따른 팁]
                    - **축제 및 행사**: [여행 기간에 맞는 행사 정보]
                """},

                {"role": "user", "content": prompt}  # 사용자 입력
            ],
            max_tokens=1000  # 최대 토큰 수를 설정하여 응답 길이를 제한
        )

        # 응답에서 첫 번째 선택의 내용 반환
        return completion.choices[0].message['content']

    except OpenAIError as e:
        # API 호출 중 오류가 발생하면 오류 메시지 반환
        print(f"Error during OpenAI API call: {e}")
        return f"Error during OpenAI API call: {e}"
