---
week: 2
day: 3
title: 이미지와 Dockerfile
subtitle: 이미지 레이어 · Dockerfile 문법 · DevMart 상품 API 첫 빌드 · 빌드 컨텍스트와 .dockerignore · 캐시 · 태그와 Docker Hub · 멀티 스테이지
hours: 8
---

# 2주차 3일차 — 이미지와 Dockerfile

## 오늘의 목표

어제까지는 남이 만든 이미지를 썼습니다. 오늘은 **내 앱을 이미지로 포장**합니다. 주인공은 DevMart의 **상품 API(catalog-api)**입니다. 내 노트북에 파이썬을 설치하지 않고도, Dockerfile 하나로 "파이썬 + 라이브러리 + 내 코드 + 실행 명령"을 묶어 어디서든 똑같이 실행되게 만듭니다. 1주차 4일차의 결론 **"Docker = 실행 조건을 이미지로 포장"**을 직접 해 보는 날입니다.

- 이미지가 **레이어**로 쌓인다는 것을 `docker image history`로 확인합니다.
- Dockerfile의 기본 명령(`FROM`, `WORKDIR`, `COPY`, `RUN`, `USER`, `ENV`, `EXPOSE`, `CMD`)을 읽고 씁니다.
- DevMart 상품 API를 빌드하고 실행해 `curl`로 확인합니다.
- `.dockerignore`로 비밀값이 이미지에 들어가는 사고를 막습니다.
- 명령의 **순서**가 빌드 시간을 좌우한다는 것을 캐시로 확인합니다.
- 이미지에 태그를 붙여 Docker Hub에 올리고, 다이제스트를 읽습니다.
- 멀티 스테이지 빌드로 이미지 크기를 100분의 1로 줄여 봅니다.

## 시간표

| 교시 | 주제 | 실습 결과물 |
|---|---|---|
| 1교시 | 어제 요약 + 이미지 레이어 | `docker image history` 읽기 |
| 2교시 | DevMart API와 Dockerfile 문법 | `devmart/catalog-api/Dockerfile` |
| 3교시 | 첫 빌드와 실행 | `curl /api/products` 성공 |
| 4교시 | 빌드 컨텍스트와 .dockerignore | 비밀값이 들어간 이미지 → 막기 |
| 5교시 | 빌드 캐시와 명령 순서 | `CACHED` 읽기, 순서 바꿔 비교 |
| 6교시 | 태그와 Docker Hub | 내 이미지를 Hub에 push |
| 7교시 | 멀티 스테이지와 이미지 크기·보안 | 약 1GB → 약 10MB |
| 8교시 | 배움일기 | |

## 교시별 자료

1. [이미지 레이어](lesson-01.md)
2. [DevMart API와 Dockerfile 문법](lesson-02.md)
3. [첫 빌드와 실행](lesson-03.md)
4. [빌드 컨텍스트와 .dockerignore](lesson-04.md)
5. [빌드 캐시와 명령 순서](lesson-05.md)
6. [태그와 Docker Hub](lesson-06.md)
7. [멀티 스테이지와 이미지 크기·보안](lesson-07.md)
