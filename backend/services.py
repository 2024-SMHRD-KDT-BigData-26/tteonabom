# services.py
from database import get_db_connection

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
