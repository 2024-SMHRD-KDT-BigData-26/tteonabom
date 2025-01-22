import mysql.connector
from mysql.connector import Error

def get_db_connection():
    """DB 연결 설정 및 반환"""
    print("Attempting to connect to the database...")  # 디버깅 메시지

    try:
        connection = mysql.connector.connect(
            host="project-db-cgi.smhrd.com",  # DB 서버 주소
            port=3307,  # 포트 번호
            user="cgi_24K_bigdata26_p3_2",  # 사용자명
            password="smhrd2",  # 비밀번호
            database="cgi_24K_bigdata26_p3_2"  # 데이터베이스 이름
        )

        if connection.is_connected():
            print("Successfully connected to the database")  # 연결 성공 메시지
            cursor = connection.cursor()
            cursor.execute("SHOW TABLES;")  # 테이블 목록 조회
            tables = cursor.fetchall()
            print("Tables in the database:")
            for table in tables:
                print(table)  # 각 테이블 출력
            cursor.close()  # 커서 닫기
            return connection
        else:
            print("Failed to connect to the database")  # 연결 실패 메시지
            return None
    except Error as e:
        print(f"Error: {e}")  # MySQL 오류 메시지 출력
        return None
    finally:
        if connection and connection.is_connected():
            connection.close()
            print("Connection closed.")  # 연결 종료 메시지
        else:
            print("No connection to close.")  # 연결이 없을 경우 메시지 출력
