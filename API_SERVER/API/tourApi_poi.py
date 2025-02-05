from fastapi import APIRouter, HTTPException
import requests
import os
from datetime import datetime

router = APIRouter()

# 한국관광공사 API 키
API_KEY = os.getenv("TOUR_API_KEY", "aFLxI2exO9pQCaigEWmOxEBI+mx2d4zmd+1rY/ef5vEe90JQVmoRuHAkt3OlNcFj7kyaMZo5XjwpWBm1LeQF8w==")

BASE_URL = "http://apis.data.go.kr/B551011/KorService1"

# ✅ 관광 데이터 조회 API (DB 없이 직접 반환)
@router.get("/poiData")
async def fetch_tour_data():
    params = {
        "serviceKey": API_KEY,
        "MobileOS": "ETC",
        "MobileApp": "TestApp",
        "arrange": "A",
        "contentTypeId": "12",  # 관광지
        "areaCode": "37",  # 지역코드
        "numOfRows": 10,  # 출력할 목록 수
        "_type": "json"
    }
    # 지역코드
    # 1 서울, 2 인천, 3 대전, 4 대구, 5 광주, 6 부산, 7 울산, 8 세종특별자치시
    # 31 경기도, 32 강원특별자치도, 33 충청북도, 34 충청남도
    # 35 경상북도, 36 경상남도, 37 전북특별자치도, 38 전남특별자치도, 39 제주특별자치도

    try:
        # ✅ 공동정보조회 API 호출
        response = requests.get(f"{BASE_URL}/areaBasedList1", params=params)
        response.raise_for_status()  # HTTP 오류 발생 시 예외를 발생시킴

        data = response.json()
        items = data.get("response", {}).get("body", {}).get("items", {}).get("item", [])

        result = []

        for item in items:
            content_id = item.get("contentid")
            addr1 = item.get("addr1", "-")
            area_code = str(item.get("areaCode", ""))  # areaCode를 문자열로 변환

            # ✅ POI_REGION: addr1에서 첫 2글자만 추출
            poi_region = addr1[:2] if addr1 != "-" else "-"

            # ✅ areaCode가 33, 34, 35, 36이면 첫 글자 + 세 번째 글자 추출
            if area_code in {"33", "34", "35", "36"} and len(addr1) >= 3:
                poi_region = addr1[0] + addr1[2]

            # ✅ 소개정보조회 API 호출 (상세정보)
            detail_params = {
                "serviceKey": API_KEY,
                "contentId": content_id,
                "MobileOS": "ETC",
                "MobileApp": "TestApp",
                "overviewYN": "Y",
                "_type": "json"
            }

            detail_response = requests.get(f"{BASE_URL}/detailCommon1", params=detail_params)
            detail_response.raise_for_status()  # HTTP 오류 발생 시 예외를 발생시킴

            detail_data = detail_response.json().get("response", {}).get("body", {}).get("items", {}).get("item", {})

            # 만약 detail_data가 리스트 형태라면 첫 번째 항목을 사용하도록 처리
            if isinstance(detail_data, list) and len(detail_data) > 0:
                detail_item = detail_data[0]
            else:
                detail_item = detail_data  # 빈 딕셔너리로 처리

            # ✅ 결과 데이터 구성
            tour_data = {
                "POI_IDX": content_id,
                "POI_NM": item.get("title", "-"),
                "POI_INFO": detail_item.get("overview", "-"),
                "POI_ADDR": addr1,
                "POI_URL": item.get("firstimage", ""),
                "POI_REGION": poi_region,  # 수정된 지역명
                "POI_TEL": item.get("tel", "-"),
                "POI_PERIOD": item.get("usetime", "-"),
                "LAT": item.get("mapy", 0.0),
                "LON": item.get("mapx", 0.0),
                "CREATED_AT": datetime.utcnow(),
                "UPDATED_AT": datetime.utcnow(),
            }

            result.append(tour_data)

        return result

    except requests.exceptions.RequestException as e:
        raise HTTPException(status_code=500, detail=f"API 호출 중 오류 발생: {str(e)}")
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"서버 내부 오류: {str(e)}")
