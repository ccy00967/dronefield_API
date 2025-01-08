#!/usr/bin/env bash
echo "===== Checking for PostgreSQL 15 on AL2023 ====="
dnf clean all
dnf update -y

# (예시 1) 단일 패키지가 기본 리포지토리에 존재한다면:
dnf install -y postgresql15-devel

# (예시 2) 만약 모듈 활성화가 필요하다면:
# dnf module enable postgresql:15
# dnf install -y postgresql-devel
