import openai
from database import get_db_connection
import os

# 환경 변수에서 API 키 로드
API_KEY = os.getenv('API_KEY')
openai.api_key = API_KEY  # OpenAI API 키 설정


def get_all_users():
    """DB에서 모든 사용자 조회"""
    connection = get_db_connection()
    if connection:
        cursor = connection.cursor(dictionary=True)  # dictionary=True로 딕셔너리 형태로 결과 반환
        cursor.execute("SELECT * FROM users")  # 'users' 테이블에서 데이터 조회
        result = cursor.fetchall()  # 모든 데이터 가져오기
        connection.close()  # 연결 종료
        return result
    else:
        print("Failed to connect to the database.")
        return None


async def generate_answer(prompt: str):
    """GPT-4 모델을 이용한 답변 생성"""
    try:
        # GPT-4 모델에 prompt를 보내고 응답을 받음
        completion = openai.Completion.create(
            model="gpt-4",  # GPT-4 모델로 설정
            messages=[
                {"role": "system", "content": "You are a helpful assistant."},
                {"role": "user", "content": prompt}
            ],
            max_tokens=150  # 최대 토큰 수를 설정하여 응답 길이를 제한
        )

        # 응답에서 첫 번째 선택의 내용 반환
        return completion.choices[0].message['content']

    except openai.Error as e:
        # API 호출 중 오류가 발생하면 오류 메시지 반환
        print(f"Error during OpenAI API call: {e}")
        return "Sorry, I couldn't generate a response at the moment."
