import requests

url = "http://127.0.0.1:9000/prompt"  # FastAPI 서버의 /prompt 엔드포인트 URL
data = {"prompt": "서울에서 3박 4일, 친구랑 즉흥적인 여행을 하고싶어"}  # 서버로 보낼 JSON 데이터

# POST 요청 보내기
response = requests.post(url, json=data)

# 응답 상태와 JSON 출력
print(f"Status code: {response.status_code}")
print(f"Response JSON: {response.json()}")
