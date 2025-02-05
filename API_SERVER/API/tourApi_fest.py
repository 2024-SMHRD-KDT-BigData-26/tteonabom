from fastapi import APIRouter, HTTPException
import requests
import os
from datetime import datetime

router = APIRouter()

# 한국관광공사 API 키
API_KEY = os.getenv("TOUR_API_KEY",
                    "aFLxI2exO9pQCaigEWmOxEBI+mx2d4zmd+1rY/ef5vEe90JQVmoRuHAkt3OlNcFj7kyaMZo5XjwpWBm1LeQF8w==")

BASE_URL = "http://apis.data.go.kr/B551011/KorService1"


# ✅ 요일을 포함한 날짜 포맷 변환 함수
def format_date_with_weekday(date_str):
    try:
        date_obj = datetime.strptime(date_str, "%Y%m%d")
        weekdays = ["월", "화", "수", "목", "금", "토", "일"]
        return date_obj.strftime(f"%Y.%m.%d({weekdays[date_obj.weekday()]})")
    except ValueError:
        return "-"


# ✅ 지역 코드 변환 함수
def extract_region_code(addr1):
    if not addr1 or len(addr1) < 2:
        return "-"  # 주소가 없거나 2글자 미만이면 '-'

    region_prefix = addr1[:2]  # 첫 2글자
    if region_prefix in ["충청", "경상"]:
        return f"{region_prefix[0]}{addr1[2]}" if len(addr1) > 2 else region_prefix[0]
    return region_prefix


# ✅ 행사 데이터 조회 API (DB 없이 직접 반환)
@router.get("/festData")
async def fetch_festival_data():
    params = {
        "serviceKey": API_KEY,
        "MobileOS": "ETC",
        "MobileApp": "AppTest",
        "arrange": "O",  # 대표 이미지가 있는 최신순 정렬
        "numOfRows": 100,  # 출력할 목록 수
        "pageNo": 1,  # 페이지 번호
        "listYN": "Y",  # 목록 출력 요청
        "eventStartDate": "20241225",  # 이벤트 시작 날짜
        "_type": "json"
    }

    try:
        response = requests.get(f"{BASE_URL}/searchFestival1", params=params)
        response.raise_for_status()

        data = response.json()
        items = data.get("response", {}).get("body", {}).get("items", {}).get("item", [])

        result = []
        for item in items:
            content_id = item.get("contentid")
            addr1 = item.get("addr1", "-")
            event_start = item.get("eventstartdate", "-")
            event_end = item.get("eventenddate", "-")

            # ✅ 날짜 변환 적용
            formatted_period = f"{format_date_with_weekday(event_start)} ~ {format_date_with_weekday(event_end)}"

            # ✅ 지역 코드 변환
            region_code = extract_region_code(addr1)

            # ✅ 축제 상세 정보 조회 API 호출 (overview 가져오기)
            detail_params = {
                "serviceKey": API_KEY,
                "contentId": content_id,
                "MobileOS": "ETC",
                "MobileApp": "AppTest",
                "overviewYN": "Y",
                "_type": "json"
            }

            detail_response = requests.get(f"{BASE_URL}/detailCommon1", params=detail_params, verify=False)
            detail_response.raise_for_status()

            detail_data = detail_response.json().get("response", {}).get("body", {}).get("items", {}).get("item", {})
            detail_item = detail_data[0] if isinstance(detail_data, list) and len(detail_data) > 0 else detail_data

            # ✅ 최종 데이터 구성
            festival_data = {
                "FEST_IDX": content_id,
                "FEST_NM": item.get("title", "-"),
                "FEST_DESC": detail_item.get("overview", "-"),
                "FEST_ADDR": addr1,
                "FEST_LOC": region_code,  # 지역 코드 추가
                "FEST_URL": item.get("firstimage", ""),
                "FEST_TEL": item.get("tel", "-"),
                "FEST_PERIOD": formatted_period,  # 변환된 날짜 적용
                "LAT": item.get("mapy", 0.0),
                "LON": item.get("mapx", 0.0),
                "CREATED_AT": datetime.utcnow(),
                "UPDATED_AT": datetime.utcnow(),
            }

            result.append(festival_data)

        return result

    except requests.exceptions.RequestException as e:
        raise HTTPException(status_code=500, detail=f"API 호출 중 오류 발생: {str(e)}")
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"서버 내부 오류: {str(e)}")
