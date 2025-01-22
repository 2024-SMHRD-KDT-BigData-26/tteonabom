# models.py
from database import get_db_connection

def create_table():
    """DB 테이블 생성 예시"""
    connection = get_db_connection()
    if connection:
        cursor = connection.cursor()
        cursor.execute(''' 
            CREATE TABLE IF NOT EXISTS users (
                id INT AUTO_INCREMENT PRIMARY KEY,
                username VARCHAR(255) NOT NULL,
                email VARCHAR(255) NOT NULL
            )
        ''')
        connection.commit()  # 변경사항 커밋
        connection.close()  # 연결 종료
        print("Table 'users' created successfully!")
    else:
        print("Failed to connect to the database.")
