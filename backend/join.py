import os
import bcrypt
import mysql.connector
from mysql.connector import Error
from flask import Flask, request, render_template, redirect, url_for, flash
from dotenv import load_dotenv

# 환경 변수 로드
load_dotenv()

# Flask 앱 초기화
app = Flask(__name__)
app.secret_key = os.getenv('SECRET_KEY', 'default_secret_key')  # 세션을 위한 비밀키

def get_db_connection():
    """데이터베이스 연결 함수"""
    try:
        connection = mysql.connector.connect(
            host=os.getenv('DB_HOST'),
            port=int(os.getenv('DB_PORT', 3306)),
            user=os.getenv('DB_USER'),
            password=os.getenv('DB_PASSWORD'),
            database=os.getenv('DB_NAME')
        )
        if connection.is_connected():
            return connection
    except Error as e:
        print(f"[ERROR] 데이터베이스 연결 오류: {e}")
        raise

def check_user_exists(cursor, user_id):
    """아이디 중복 확인"""
    query = "SELECT COUNT(*) FROM TB_USERS WHERE USER_ID = %s"
    cursor.execute(query, (user_id,))
    result = cursor.fetchone()
    return result[0] > 0 if result else False

@app.route('/join', methods=['GET', 'POST'])
def join():
    if request.method == 'POST':
        user_id = request.form['user_id']
        user_pw = request.form['user_pw']
        user_pw_confirm = request.form['user_pw_confirm']
        user_nick = request.form['user_nick']
        user_profile_img = request.form.get('user_profile_img', None)
        kakao_id = request.form.get('kakao_id', None)
        auth_provider = request.form.get('auth_provider', None)

        if user_pw != user_pw_confirm:
            flash("[오류] 비밀번호가 일치하지 않습니다.", "error")
            return redirect(url_for('join'))

        if not user_id or not user_pw or not user_nick:
            flash("[오류] 필수 정보를 모두 입력해주세요.", "error")
            return redirect(url_for('join'))

        try:
            connection = get_db_connection()
            cursor = connection.cursor()

            if check_user_exists(cursor, user_id):
                flash("[오류] 이미 존재하는 아이디입니다.", "error")
                return redirect(url_for('join'))

            hashed_pw = bcrypt.hashpw(user_pw.encode('utf-8'), bcrypt.gensalt()).decode('utf-8')

            query = """
                INSERT INTO TB_USERS 
                (USER_ID, USER_PW, USER_NICK, USER_PROFILE_IMG, KAKAO_ID, AUTH_PROVIDER, CREATED_AT)
                VALUES (%s, %s, %s, %s, %s, %s, CURRENT_TIMESTAMP)
            """
            cursor.execute(query, (
                user_id,
                hashed_pw,
                user_nick,
                user_profile_img if user_profile_img else None,
                int(kakao_id) if kakao_id and kakao_id.isdigit() else None,
                auth_provider if auth_provider else None
            ))
            connection.commit()

            flash("회원가입이 완료되었습니다. 로그인 해주세요.", "success")
            return redirect(url_for('login'))  # 로그인 페이지로 이동

        except Error as e:
            flash(f"[ERROR] 회원가입 중 오류가 발생했습니다: {e}", "error")
            return redirect(url_for('join'))
        finally:
            if cursor:
                cursor.close()
            if connection.is_connected():
                connection.close()

    return render_template('join.html')

if __name__ == '__main__':
    app.run(debug=True)
