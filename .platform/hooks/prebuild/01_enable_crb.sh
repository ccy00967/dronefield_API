#!/usr/bin/env bash
# 꼭 chmod +x 해주세요 (실행 권한 필수)

echo "===== Enabling CRB on Amazon Linux 2023 ====="
yum config-manager --set-enabled crb || true
yum clean all
yum update -y

echo "===== CRB enabled successfully ====="
