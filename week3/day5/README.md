<sub>[🏠 과정 목차](../../README.md) › [3주차](../README.md) › [5일차](README.md)</sub>

<img src="../../v3/assets/readme/week3.png" alt="3주차 노선도" width="100%">

# 3주차 5일차 — 운영 가능한 워크로드

📕 3주차 이북 PDF: [보기](../../downloads/pdf/week3.pdf) · [내려받기](https://github.com/niceguy61/kdt_devops_lecture_2026_rev2/raw/main/downloads/pdf/week3.pdf) &nbsp;|&nbsp; 📊 5일차 슬라이드: [PPTX 내려받기](https://github.com/niceguy61/kdt_devops_lecture_2026_rev2/raw/main/downloads/pptx/week3-day5.pptx)

## 오늘의 목표

어제 catalog-api를 Kubernetes에 올렸지만, 운영하기에는 모자란 곳이 많았습니다. DB가 없어 상품 목록은 503이었고, 설정은 매니페스트에 박혀 있었고, 롤링 업데이트 중에 요청이 실패했고, Pod가 메모리를 얼마나 써도 되는지 아무도 정하지 않았습니다.

오늘은 그 빈칸을 하나씩 채운 뒤, **DevMart MSA 여섯 서비스 전체**를 Kubernetes 위에 올립니다. 1일차에 `docker compose up` 한 줄로 띄우던 그 앱이, 금요일 오후에는 `kubectl apply -k` 한 줄로 클러스터에 뜹니다. 마지막으로 짝끼리 서로의 DevMart를 망가뜨리고 고치며 한 주를 마무리합니다.

- **Namespace**로 DevMart만의 공간을 만듭니다.
- 설정은 **ConfigMap**, 비밀번호는 **Secret**으로 이미지 밖에서 넣습니다.
- **readiness · liveness probe**로 "준비됐나 · 살아 있나"를 Kubernetes가 직접 묻게 합니다. 어제의 FAIL이 사라지는 것을 확인합니다.
- **requests · limits**로 자원을 예약하고 상한을 정합니다. 메모리 상한을 넘은 Pod가 죽는 것을 봅니다.
- DevMart MSA 전체를 배포하고, 브라우저 `localhost:30080`에서 주문합니다.
- 짝이 넣은 장애를 **바깥에서 안으로** 진단하고 장애 보고서를 씁니다.
- 3주차를 회고합니다.

## 시간표

| 교시 | 주제 | 실습 결과물 |
|---|---|---|
| 1교시 | 4일차 요약 + Namespace | `devmart` 네임스페이스 |
| 2교시 | ConfigMap과 Secret | DB + catalog-api, 상품 목록 200 |
| 3교시 | probe — 준비됐나, 살아 있나 | FAIL 없는 롤링 업데이트 |
| 4교시 | requests와 limits | 노드 예약량 확인, OOMKilled 관찰 |
| 5교시 | DevMart MSA를 Kubernetes에 | 브라우저 주문 → completed |
| 6교시 | 장애 연습 | 장애 보고서 |
| 7교시 | HPA — 부하에 따라 늘어나고 줄어들기 | 부하에 2 → 6 → 2 |
| 8교시 | 3주차 회고 | KPT + Compose ↔ Kubernetes 대응표 |

배움일기는 수업이 끝난 뒤 각자 씁니다(마지막 교시 끝의 질문).

## 교시별 자료

1. [4일차 요약 + Namespace](lesson-01.md)
2. [ConfigMap과 Secret](lesson-02.md)
3. [probe — 준비됐나, 살아 있나](lesson-03.md)
4. [requests와 limits](lesson-04.md)
5. [DevMart MSA를 Kubernetes에](lesson-05.md)
6. [장애 연습](lesson-06.md)
7. [HPA — 자동으로 늘고 줄기](lesson-07.md)
8. [3주차 회고](lesson-08.md)

> [!IMPORTANT]
> **오늘 실습 전에 확인할 것**
>
> - `kubectl get nodes`에서 세 노드가 `Ready`.
> - 2일차 CI가 만든 **세 이미지**(catalog-api · order-api · order-worker)가 GHCR에 **같은 SHA 태그**로 있어야 합니다. 1교시에 확인합니다.
> - 오늘 처음 클러스터가 받는 이미지: `postgres:18`(약 150MB), `redis:8-alpine`, `nginx:1.30-alpine`, `python:3.14-slim`. 노트북에는 2주차에 받아 두었지만 **kind 노드는 따로 받습니다**(노드는 별도의 컨테이너 런타임을 쓰기 때문, 3일차 3교시).
> - 실습 파일은 강의 저장소의 `labs/week3/day5/`입니다.

> [!WARNING]
> **오늘의 공통 주의 — 네임스페이스를 빠뜨리지 않는다**
>
> 오늘은 대부분의 명령에 `-n devmart`가 붙습니다. 빠뜨리면 `default` 네임스페이스를 보게 되어 "아무것도 없다"거나 어제의 catalog-api가 보입니다. 1교시 실습 2에서 기본 네임스페이스를 `devmart`로 바꾸는 방법도 배웁니다.

---

| 이전 | 목차 | 다음 |
|:--|:--:|--:|
| ⬅️ [8교시 · Pod 디버깅 종합 — 안 닿을 때 · `kubectl debug`](../day4/lesson-08.md) | [⬆️ 3주차 목차](../README.md) | [1교시 · 4일차 요약 + Namespace](lesson-01.md) ➡️ |
