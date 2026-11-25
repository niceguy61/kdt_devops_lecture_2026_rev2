#!/usr/bin/env bash
# 2주차 설치 점검 스크립트 — 각 도구가 설치되어 있는지 확인한다.
# 사용법: bash check-env.sh

check() {
  local name="$1"; shift
  if out=$("$@" 2>/dev/null | head -n 1) && [ -n "$out" ]; then
    printf "  [ OK ] %-16s %s\n" "$name" "$out"
  else
    printf "  [FAIL] %-16s 설치 또는 실행 상태를 확인하세요\n" "$name"
    FAILED=$((FAILED + 1))
  fi
}

FAILED=0
echo "== 2주차 설치 점검 ($(date '+%Y-%m-%d %H:%M')) =="
check "OS"             uname -sr
check "git"            git --version
check "git user.name"  git config --global user.name
check "gh"             gh --version
check "gh login"       bash -c 'gh auth status >/dev/null 2>&1 && echo "logged in"'
check "docker client"  docker version --format 'client {{.Client.Version}}'
check "docker server"  docker version --format 'server {{.Server.Version}}'
check "docker compose" docker compose version
echo "== 결과: 실패 ${FAILED}개 =="
exit "$FAILED"
