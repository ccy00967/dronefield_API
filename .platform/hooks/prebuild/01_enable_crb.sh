#!/usr/bin/env bash
echo "===== Enabling codeready repo on AL2023 ====="
yum config-manager --set-enabled amazon-linux-2023-codeready
yum clean all && yum update -y
