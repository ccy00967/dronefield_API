# 베이스 이미지 설정
FROM python:3.12-slim

# 작업 디렉터리 설정
WORKDIR /app

# 시스템 의존성 설치
RUN apt-get update && apt-get install -y \
    postgresql-client gcc python3-dev musl-dev libpq-dev \
    && apt-get clean

# 종속성 설치
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

# 애플리케이션 코드 복사
COPY . .

# 환경 변수 설정
ENV PYTHONUNBUFFERED=1
ENV DJANGO_SETTINGS_MODULE=core.settings

# 포트 노출
EXPOSE 8000

# 엔트리포인트 설정
ENTRYPOINT ["/app/entrypoint.sh"]
