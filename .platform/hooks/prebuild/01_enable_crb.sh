#!/usr/bin/env bash

echo "===== Enabling CRB (CodeReady Builder) on Amazon Linux 2023 ====="

# yum 대신 dnf이 사용되지만, 현재 EB 환경에선 yum 명령을 래핑해서 사용 가능합니다.
yum config-manager --set-enabled crb || true

echo "===== Cleaning and updating yum repos ====="
yum clean all
yum update -y

echo "===== CRB has been enabled successfully. ====="
