#!/bin/bash

# 스크립트 에러 발생 시 종료
set -e

# 데이터베이스 마이그레이션
echo "Running migrations..."
python manage.py migrate

# 정적 파일 수집
echo "Collecting static files..."
python manage.py collectstatic --noinput

# Gunicorn 실행 (프로젝트 루트에 application.py 필요)
echo "Starting Gunicorn..."
exec gunicorn application:application --bind 0.0.0.0:8000
