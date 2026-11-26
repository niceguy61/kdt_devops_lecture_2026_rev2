---
week: 2
day: 5
title: Docker Compose와 GitHub 협업
subtitle: compose.yaml 읽고 쓰기 · up/ps/logs/down · 헬스 체크와 의존 순서 · 일상 작업과 확장 · 브랜치 · Pull Request와 코드 리뷰 · 충돌 해결 · 2주차 회고
hours: 8
---

# 2주차 5일차 — Docker Compose와 GitHub 협업

## 오늘의 목표

어제는 세 컨테이너를 띄우려고 긴 명령 여섯 개를 순서대로 쳤습니다. 오늘 오전에는 그것을 **`compose.yaml` 파일 하나**에 적고 **`docker compose up` 한 줄**로 바꿉니다. "이 순서로 실행하라"가 아니라 **"이런 상태여야 한다"**고 적는 선언형 방식의 첫 경험입니다.

오후에는 그 파일을 **동료와 함께** 고칩니다. 혼자 `main`에 바로 커밋하던 방식에서 벗어나, **브랜치 → Pull Request → 코드 리뷰 → 병합**의 흐름을 짝과 함께 해 보고, 두 사람이 같은 줄을 고쳤을 때 생기는 **충돌**을 직접 풉니다. 마지막으로 2주차 전체를 회고합니다.

- 어제의 명령들을 `compose.yaml`로 옮겨 읽고 씁니다.
- `up` · `ps` · `logs` · `exec` · `down` · `down -v`로 DevMart를 다룹니다.
- 헬스 체크와 `depends_on`으로 시작 순서를 도구에 맡깁니다.
- 코드를 고치고 다시 빌드하는 일, API를 3개로 늘리는 일을 한 줄로 합니다.
- 브랜치를 만들어 작업하고, PR을 열어 짝에게 리뷰를 받고 병합합니다.
- 일부러 충돌을 만들고 VS Code에서 해결합니다.

## 시간표

| 교시 | 주제 | 실습 결과물 |
|---|---|---|
| 1교시 | 어제 요약 + `compose.yaml` 읽기 | `devmart/compose.yaml` |
| 2교시 | `up` · `ps` · `logs` · `down`과 헬스 체크 | 한 줄로 DevMart 띄우기 |
| 3교시 | Compose로 하는 일상 작업 | 코드 수정 → 재빌드, API 3개로 늘리기 |
| 4교시 | Git 브랜치 | 브랜치에서 작업하고 병합 |
| 5교시 | Pull Request와 코드 리뷰 | 짝의 PR 리뷰 · 승인 · 병합 |
| 6교시 | 충돌 해결 | 충돌 표시 읽고 풀기 |
| 7교시 | Compose 심화 — 덧씌우기 파일과 환경별 설정 | 개발 · 운영 덧씌우기 파일, 한 노트북에 두 벌 |
| 8교시 | 2주차 회고 + 정리 | KPT 회고, 디스크 정리 |

배움일기는 수업이 끝난 뒤 각자 씁니다(마지막 교시 끝의 질문).

## 교시별 자료

1. [compose.yaml 읽기](lesson-01.md)
2. [up · ps · logs · down과 헬스 체크](lesson-02.md)
3. [Compose로 하는 일상 작업](lesson-03.md)
4. [Git 브랜치](lesson-04.md)
5. [Pull Request와 코드 리뷰](lesson-05.md)
6. [충돌 해결](lesson-06.md)
7. [Compose 심화](lesson-07.md)
8. [2주차 회고와 정리](lesson-08.md)

!!! key "오늘 실습 전에 확인할 것"
    - 어제 띄운 컨테이너가 남아 있다면 `bash ../day4/devmart-down.sh`로 지웁니다 (볼륨 `devmart-db`는 남겨 둡니다).
    - `docker compose version`이 나와야 합니다. Docker Desktop과 2주차 1일차의 Linux 설치에는 이미 들어 있습니다.
    - 4교시부터는 **짝 실습**입니다. 짝의 GitHub 아이디를 미리 알아 두세요.
