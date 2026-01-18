# 파이썬 3.12-slim 이미지 사용
FROM python:3.12-slim

# 도커 작업 디렉토리 설정
WORKDIR /code

# 빌드 콘텍스트 디렉토리에서 도커 작업 디렉토리로 복사
COPY src/requirements.txt /code/

# requirements에 따라 파이썬 라이브러리 설치
RUN pip3 install --no-cache-dir --upgrade -r requirements.txt

# 코드 파일과 데이터베이스를 빌드 콘텍스트 디렉토리에서 복사
COPY src/*.py /code/
COPY src/*.db /code/

# Uvicorm 웹 서버를 시작하고 애플리케이션을 실행
CMD [ "uvicorn", "main:app", "--host", "0.0.0.0", "--port", "80" ]