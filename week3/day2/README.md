<sub>[🏠 과정 목차](../../README.md) › [3주차](../README.md) › [2일차](README.md)</sub>

<img src="../../v3/assets/readme/week3.png" alt="3주차 노선도" width="100%">

# 3주차 2일차 — MSA 장애와 CI

📕 3주차 이북 PDF: [보기](../../downloads/pdf/week3.pdf) · [내려받기](https://github.com/niceguy61/kdt_devops_lecture_2026_rev2/raw/main/downloads/pdf/week3.pdf) &nbsp;|&nbsp; 📊 2일차 슬라이드: [PPTX 내려받기](https://github.com/niceguy61/kdt_devops_lecture_2026_rev2/raw/main/downloads/pptx/week3-day2.pptx)

## 오늘의 목표

어제 DevMart MSA의 **연결이 끊기는** 장애를 봤습니다. 오늘은 더 까다로운 장애를 봅니다. 서비스가 **죽은 것이 아니라 느려질 때**, 그 느림이 다른 서비스로 **번지는** 장애입니다. 그리고 그 장애를 막는 기본 장치 — 타임아웃, 재시도, 헬스 체크, 재시작 정책 — 를 하나씩 켜 봅니다.

오후에는 방향을 바꿉니다. 서비스가 셋이면 이미지도 셋이고, 누군가 코드를 고칠 때마다 테스트하고 빌드하는 일이 세 배가 됩니다. 이 일을 **GitHub Actions**에 맡깁니다. PR을 열면 자동으로 테스트하고, `main`에 합쳐지면 자동으로 이미지를 만들어 **GHCR**에 올리는 **CI**를 오늘 완성합니다. 1주차 5일차 2교시에 그림으로만 본 파이프라인의 ①~⑤를 직접 만드는 날입니다.

- 상품 서비스를 멈춰 세워(pause) 주문 서비스까지 느려지는 **장애 전파**를 봅니다.
- 타임아웃 길이와 재시도 횟수에 따라 결과가 어떻게 달라지는지 비교합니다.
- 헬스 체크와 재시작 정책을 `compose.yaml`에 넣고, 크래시 루프를 관찰합니다.
- 처리기가 멈췄을 때 큐가 쌓이는 것, 처리 중에 죽었을 때 **주문이 사라지는 것**을 봅니다.
- GitHub Actions의 구성 요소를 이해하고 첫 워크플로를 실행합니다.
- PR마다 자동 테스트, `main`마다 이미지 자동 빌드 · push를 만듭니다.

## 시간표

| 교시 | 주제 | 실습 결과물 |
|---|---|---|
| 1교시 | 1일차 요약 + 장애 전파 | 느림이 번지는 것 측정 |
| 2교시 | 타임아웃 · 재시도 · 헬스 체크 | 재시도 실험, 헬스 체크와 재시작 정책 |
| 3교시 | 큐 적체와 메시지 유실 + 장애 보고서 | 유령 주문 찾기, 장애 보고서 |
| 4교시 | GitHub Actions 개념과 첫 워크플로 | `hello.yml` 실행 |
| 5교시 | PR마다 자동 테스트 | 테스트 실패로 빨간 X 보기 |
| 6교시 | 이미지 자동 빌드와 GHCR | 내 이미지 세 개가 GHCR에 |
| 7교시 | CI 실패 읽기와 main 보호 | 필수 검사 규칙 + 배움일기 |
| 8교시 | 배움일기 | |

## 교시별 자료

1. [장애 전파](lesson-01.md)
2. [타임아웃 · 재시도 · 헬스 체크](lesson-02.md)
3. [큐 적체와 메시지 유실](lesson-03.md)
4. [GitHub Actions 개념과 첫 워크플로](lesson-04.md)
5. [PR마다 자동 테스트](lesson-05.md)
6. [이미지 자동 빌드와 GHCR](lesson-06.md)
7. [CI 실패 읽기와 main 보호](lesson-07.md)

> [!IMPORTANT]
> **오늘 실습 전에 확인할 것**
>
> - 어제의 `~/devops-lab/devmart-msa`를 그대로 씁니다. `docker compose up -d`로 띄워 두고, 주문이 completed까지 가는지 확인합니다.
> - 강의 저장소를 최신으로 받습니다: `cd ~/course && git pull`. 오늘 쓰는 파일(테스트, 워크플로)이 `labs/week3/`에 추가되었습니다.
> - 오후 실습은 GitHub에서 합니다. `gh auth status`로 로그인 상태를 확인합니다.

---

| 이전 | 목차 | 다음 |
|:--|:--:|--:|
| ⬅️ [7교시 · 장애 시나리오 1 — 연결이 끊겼다](../day1/lesson-07.md) | [⬆️ 3주차 목차](../README.md) | [1교시 · 장애 전파](lesson-01.md) ➡️ |
