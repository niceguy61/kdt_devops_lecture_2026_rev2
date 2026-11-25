#!/bin/bash
# EC2가 처음 켜질 때 한 번 실행된다 (root 권한). Amazon Linux 2023용.
set -euxo pipefail
dnf install -y docker
systemctl enable --now docker
# 4주차 1일차의 podinfo — 화면에 '어느 서버가 답했는지'(hostname)를 보여 준다
docker run -d --name podinfo --restart always -p 9898:9898 \
  -e PODINFO_UI_MESSAGE="DevMart on EC2" \
  ghcr.io/stefanprodan/podinfo:6.14.0
