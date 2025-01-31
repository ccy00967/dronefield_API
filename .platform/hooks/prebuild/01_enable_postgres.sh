#!/usr/bin/env bash
echo "===== Installing PostgreSQL 15 dev libraries on AL2023 ====="

# 필요하다면 clean/update
dnf clean all
dnf update -y

# 여기서 'server-devel' 패키지를 설치
dnf install -y postgresql15-server-devel
dnf install -y libjpeg-devel zlib-devel

echo "===== postgresql15-server-devel installed successfully ====="
