<sub>[🏠 과정 목차](../../README.md) › [3주차](../README.md) › [1일차](README.md)</sub>

<img src="../../v3/assets/readme/week3.png" alt="3주차 노선도" width="100%">

# 3주차 1일차 — MSA 개념과 실행

📕 3주차 이북 PDF: [보기](../../downloads/pdf/week3.pdf) · [내려받기](https://github.com/niceguy61/kdt_devops_lecture_2026_rev2/raw/main/downloads/pdf/week3.pdf) &nbsp;|&nbsp; 📊 1일차 슬라이드: [PPTX 내려받기](https://github.com/niceguy61/kdt_devops_lecture_2026_rev2/raw/main/downloads/pptx/week3-day1.pptx)

## 오늘의 목표

2주차의 DevMart는 웹 · API · DB 세 컨테이너였습니다. 오늘 DevMart에 **주문 기능**이 생깁니다. 그런데 주문 코드를 상품 API 안에 넣지 않고, **주문 서비스 · 주문 처리기 · 큐**를 따로 만듭니다. 하나의 앱을 여러 개의 작은 서비스로 나누는 **마이크로서비스 아키텍처(MSA)**입니다.

3주차부터는 난이도가 한 단계 올라갑니다. 대신 2주차에 익힌 Compose, 네트워크, 환경 변수, 로그 읽기가 그대로 쓰입니다. 오늘은 "MSA는 좋다/나쁘다"가 아니라, **인프라 엔지니어로서 여러 서비스를 실행하고, 연결을 확인하고, 끊긴 곳을 찾는 법**에 집중합니다.

- 모놀리식과 MSA를 배포 단위, 장애 범위, 운영 비용으로 비교합니다.
- 서비스 경계를 어떻게 나누는지, 왜 **데이터베이스까지 나누는지** 이해합니다.
- DevMart MSA의 여섯 서비스와 연결 방향을 `compose.yaml`에서 읽어 냅니다.
- 한 줄로 전체를 띄우고, 브라우저에서 주문을 넣어 봅니다.
- **요청 ID** 하나로 여러 서비스의 로그를 이어 읽습니다.
- 동기 호출과 비동기(큐) 처리의 차이를 눈으로 확인합니다.
- 주소 · DB 이름 · 큐 이름이 틀렸을 때의 증상을 구분합니다.

## 시간표

| 교시 | 주제 | 실습 결과물 |
|---|---|---|
| 1교시 | 2주차 요약 + 모놀리식과 MSA | 비교표 |
| 2교시 | 서비스 경계와 데이터 소유 | DevMart 서비스 경계 그리기 |
| 3교시 | DevMart MSA 구조 읽기 | 서비스 목록표 (포트 · 의존 · 설정 · 헬스) |
| 4교시 | 여섯 서비스 실행하기 | `docker compose up` + 브라우저 주문 |
| 5교시 | 요청 ID로 통신 추적하기 | 요청 하나의 여행 기록 |
| 6교시 | 동기와 비동기 — 큐와 처리기 | 처리기 3개로 늘리기 |
| 7교시 | 장애 시나리오 1 — 연결이 끊겼다 | 장애 3종 진단 기록 |
| 8교시 | 배움일기 | |

## 교시별 자료

1. [모놀리식과 MSA](lesson-01.md)
2. [서비스 경계와 데이터 소유](lesson-02.md)
3. [DevMart MSA 구조 읽기](lesson-03.md)
4. [여섯 서비스 실행하기](lesson-04.md)
5. [요청 ID로 통신 추적하기](lesson-05.md)
6. [동기와 비동기 — 큐와 처리기](lesson-06.md)
7. [장애 시나리오 1 — 연결이 끊겼다](lesson-07.md)

> [!IMPORTANT]
> **오늘 실습 전에 확인할 것**
>
> - 2주차 DevMart를 내려 둡니다: `cd ~/devops-lab/devmart && docker compose down` (8080 포트를 오늘 새 DevMart가 씁니다).
> - 오늘 처음 받는 이미지는 `redis:8-alpine`(수십 MB)입니다. 나머지는 2주차에 받은 `postgres:18`, `nginx:1.30-alpine`, `python:3.14-slim`을 그대로 씁니다.
> - 실습 파일은 강의 저장소의 `labs/week3/devmart-msa/`입니다. 4교시에 복사합니다.

---

| 이전 | 목차 | 다음 |
|:--|:--:|--:|
| ⬅️ [7교시 · 2주차 회고와 정리](../../week2/day5/lesson-07.md) | [⬆️ 3주차 목차](../README.md) | [1교시 · 모놀리식과 MSA](lesson-01.md) ➡️ |
