@echo off
:: 배치 파일 시작
echo Setting up FastAPI environment...

:: 가상환경 생성
python -m venv .venv
if %ERRORLEVEL% neq 0 (
    echo Failed to create virtual environment. Make sure Python is installed and in PATH.
    pause
    exit /b
)

:: 가상환경 활성화
call .venv\Scripts\activate
if %ERRORLEVEL% neq 0 (
    echo Failed to activate virtual environment.
    pause
    exit /b
)

:: FastAPI와 Uvicorn 설치
echo Installing FastAPI and Uvicorn...
pip install --upgrade pip
pip install fastapi uvicorn
if %ERRORLEVEL% neq 0 (
    echo Failed to install FastAPI or Uvicorn.
    pause
    exit /b
)

:: requirements.txt 생성
echo Generating requirements.txt...
pip freeze > requirements.txt

:: 완료 메시지
echo FastAPI environment setup is complete!
pause
