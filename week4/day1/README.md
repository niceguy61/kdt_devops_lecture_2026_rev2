[🏠 과정 목차](../../README.md) › [4주차](../README.md) › [1일차](README.md)

# 4주차 1일차 — Helm + Gateway API

📕 4주차 이북 PDF: [보기](../../downloads/pdf/week4.pdf) · [내려받기](https://github.com/niceguy61/kdt_devops_lecture_2026_rev2/raw/main/downloads/pdf/week4.pdf) &nbsp;|&nbsp; 📊 1일차 슬라이드: [PPTX 내려받기](https://github.com/niceguy61/kdt_devops_lecture_2026_rev2/raw/main/downloads/pptx/week4-day1.pptx)

## 오늘의 목표

3주차 금요일, DevMart 여섯 서비스가 `kubectl apply -k` 한 줄로 클러스터에 떴습니다. 매니페스트 여덟 개를 **직접** 썼습니다. 그런데 4주차에 설치할 도구들 — Envoy Gateway, Prometheus, Argo CD, Istio, Kyverno — 은 하나에 매니페스트가 **수십~수백 개**입니다. 이것을 손으로 쓰지 않습니다. **Helm**으로 설치합니다.

그리고 DevMart의 입구를 바꿉니다. 지금은 nginx Pod 하나가 NodePort 30080으로 손님을 받아 API로 나눠 보냅니다(3주차 1일차의 API 게이트웨이). 오늘은 이 역할을 Kubernetes의 **표준 입구 API — Gateway API**에 맡깁니다. 오랫동안 표준 노릇을 하던 ingress-nginx가 **2026년 3월 은퇴**했기 때문에, 이제 새로 배우는 사람은 Gateway API부터 배웁니다.

- **Helm**이 무엇이고 Kustomize와 무엇이 다른지 설명합니다.
- 연습용 앱 podinfo로 **설치 → 확인 → 바꾸기 → 되돌리기 → 지우기** 루프를 손에 붙입니다.
- Ingress가 왜 한계에 부딪혔는지, ingress-nginx 은퇴가 무엇을 뜻하는지 압니다.
- Gateway API의 **역할별 리소스** — GatewayClass · Gateway · HTTPRoute — 를 구분합니다.
- **Envoy Gateway**를 Helm으로 설치하고, DevMart의 문을 Gateway로 바꿉니다.
- HTTPRoute로 **경로 · Host · 가중치**에 따라 나눕니다.
- 라우트의 `status`를 읽어 **404와 500의 원인**을 찾습니다.

## 시간표

| 교시 | 주제 | 실습 결과물 |
|---|---|---|
| 1교시 | 3주차 요약 + Helm 개념 | Helm 4 설치 |
| 2교시 | Helm 설치 루프 | podinfo 설치 · 업그레이드 · 롤백 |
| 3교시 | Ingress의 역사와 ingress-nginx 은퇴 | 입구 방식 비교표 |
| 4교시 | Gateway API 구조 | 역할별 리소스 읽기 |
| 5교시 | Envoy Gateway 설치와 Gateway | NodePort 30080의 Gateway |
| 6교시 | HTTPRoute — 경로 · Host · 가중치 | DevMart를 Gateway 뒤로, 카나리 80:20 |
| 7교시 | 장애 분석 | 라우트 장애 4종 진단 기록 |
| 8교시 | 배움일기 | |

## 교시별 자료

1. [3주차 요약 + Helm 개념](lesson-01.md)
2. [Helm 설치 루프](lesson-02.md)
3. [Ingress의 역사와 ingress-nginx 은퇴](lesson-03.md)
4. [Gateway API 구조](lesson-04.md)
5. [Envoy Gateway 설치와 Gateway](lesson-05.md)
6. [HTTPRoute — 경로 · Host · 가중치](lesson-06.md)
7. [장애 분석](lesson-07.md)

> [!IMPORTANT]
> **오늘 실습 전에 확인할 것**
>
> - 3주차의 `devmart` 클러스터가 살아 있고, `devmart` 네임스페이스의 DevMart가 `localhost:30080`에서 열려야 합니다. 주말에 노트북을 껐다면 `docker start devmart-control-plane devmart-worker devmart-worker2` 후 40초 기다립니다.
> - 오늘 처음 받는 것: Helm 4 실행 파일, podinfo 이미지(수십 MB), Envoy Gateway 컨트롤러 · Envoy 프록시 이미지(합쳐 200MB 안팎).
> - 실습 파일은 강의 저장소의 `labs/week4/day1/`입니다.

> [!WARNING]
> **이번 주의 공통 주의 — values 파일이 원하는 상태다**
>
> 4주차에는 Helm으로 여러 도구를 설치합니다. 설정을 `--set`으로 명령줄에서 바꾸면 3주차 4일차의 `kubectl scale`처럼 **파일에 남지 않습니다.** 설정은 항상 **values 파일을 고치고** `helm upgrade -f`로 반영합니다. 이 주의는 교시마다 반복하지 않습니다.

---

⬅️ 이전: [7교시 · 3주차 회고](../../week3/day5/lesson-07.md) &nbsp;|&nbsp; 다음: [1교시 · 3주차 요약 + Helm 개념](lesson-01.md) ➡️
