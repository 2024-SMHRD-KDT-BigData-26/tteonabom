import os
import bcrypt
import mysql.connector
from mysql.connector import Error
from flask import Flask, request, render_template, redirect, url_for, session, flash
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

def get_user_password(cursor, user_id):
    """특정 아이디의 비밀번호 가져오기"""
    query = "SELECT USER_PW FROM TB_USERS WHERE USER_ID = %s"
    cursor.execute(query, (user_id,))
    result = cursor.fetchone()
    return result[0] if result else None

@app.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        user_id = request.form['user_id']
        user_pw = request.form['user_pw']

        if not user_id or not user_pw:
            flash("[오류] 아이디와 비밀번호를 모두 입력해주세요.", "error")
            return redirect(url_for('login'))

        try:
            connection = get_db_connection()
            cursor = connection.cursor()

            hashed_pw = get_user_password(cursor, user_id)
            if not hashed_pw:
                flash("[오류] 존재하지 않는 아이디입니다.", "error")
                return redirect(url_for('login'))

            if bcrypt.checkpw(user_pw.encode('utf-8'), hashed_pw.encode('utf-8')):
                session['user_id'] = user_id
                flash(f"[성공] 로그인에 성공했습니다. 환영합니다, {user_id}님!", "success")
                return redirect(url_for('dashboard'))
            else:
                flash("[오류] 비밀번호가 일치하지 않습니다.", "error")
                return redirect(url_for('login'))

        except Error as e:
            flash(f"[ERROR] 로그인 중 오류가 발생했습니다: {e}", "error")
            return redirect(url_for('login'))
        finally:
            if cursor:
                cursor.close()
            if connection.is_connected():
                connection.close()

    return render_template('login.html')

@app.route('/dashboard')
def dashboard():
    if 'user_id' not in session:
        flash("[오류] 로그인이 필요합니다.", "error")
        return redirect(url_for('login'))
    return f"<h1>안녕하세요, {session['user_id']}님! 이것은 대시보드입니다.</h1>"

@app.route('/logout')
def logout():
    session.pop('user_id', None)
    flash("[성공] 로그아웃되었습니다.", "success")
    return redirect(url_for('login'))

if __name__ == '__main__':
    app.run(debug=True)
