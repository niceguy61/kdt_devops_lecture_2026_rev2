[🏠 과정 목차](../../README.md) › [4주차](../README.md) › [2일차](README.md)

# 4주차 2일차 — Observability

📕 4주차 이북 PDF: [보기](../../downloads/pdf/week4.pdf) · [내려받기](https://github.com/niceguy61/kdt_devops_lecture_2026_rev2/raw/main/downloads/pdf/week4.pdf) &nbsp;|&nbsp; 📊 2일차 슬라이드: [PPTX 내려받기](https://github.com/niceguy61/kdt_devops_lecture_2026_rev2/raw/main/downloads/pptx/week4-day2.pptx)

## 오늘의 목표

어제 배움일기의 마지막 질문은 "하루 100만 요청의 카나리는 누가 세나? 오류가 늘었는지 어떻게 알까?"였습니다. 3주차까지 우리는 장애를 **사람이** 찾았습니다 — curl로 두드리고, `kubectl get`으로 보고, 로그를 grep했습니다. 그것은 **이미 장애가 났다는 것을 안 뒤**의 일입니다. 오늘은 장애를 **먼저 알아채는** 방법을 만듭니다.

- **로그 · 메트릭 · 트레이스**가 각각 무엇에 답하는지 구분합니다.
- **kube-prometheus-stack**을 Helm으로 설치합니다 — Prometheus · Grafana · Alertmanager와 그 운영자(operator).
- Prometheus가 무엇을 **긁어 가는지**(target) 확인하고, Gateway(Envoy)의 지표를 더합니다.
- **PromQL**로 DevMart의 요청 수 · 오류율 · 응답 시간(RED)을 계산합니다.
- **Grafana** 대시보드를 만들고, 그것을 **코드(ConfigMap)**로 관리합니다.
- **k6**로 부하를 걸고, 일부러 장애를 넣어 그래프가 어떻게 변하는지 봅니다.
- **알림 규칙**을 만들어 장애를 사람보다 먼저 알아채게 하고, 알림에 붙일 **런북**을 씁니다.

## 시간표

| 교시 | 주제 | 실습 결과물 |
|---|---|---|
| 1교시 | 1일차 요약 + 관찰 가능성 | DevMart에 던질 질문 목록 |
| 2교시 | kube-prometheus-stack 설치 | Prometheus · Grafana · Alertmanager |
| 3교시 | 타깃과 PromQL | Envoy 지표 수집, RED 쿼리 셋 |
| 4교시 | Grafana 대시보드 | 코드로 관리하는 DevMart 대시보드 |
| 5교시 | k6 부하 테스트 | 부하 + 장애 중의 그래프 |
| 6교시 | 알림 | DevMartHighErrorRate 발생 · 잠재우기 |
| 7교시 | 관찰 런북과 SLO | 런북 한 장 |
| 8교시 | 배움일기 | |

## 교시별 자료

1. [1일차 요약 + 관찰 가능성](lesson-01.md)
2. [kube-prometheus-stack 설치](lesson-02.md)
3. [타깃과 PromQL](lesson-03.md)
4. [Grafana 대시보드](lesson-04.md)
5. [k6 부하 테스트](lesson-05.md)
6. [알림](lesson-06.md)
7. [관찰 런북과 SLO](lesson-07.md)

> [!IMPORTANT]
> **오늘 실습 전에 확인할 것**
>
> - 오늘 설치하는 도구들이 메모리를 **1.5~2GB** 더 씁니다. Docker Desktop 메모리를 **6GB 이상**으로 권합니다(3주차 3일차 6교시). 4GB라면 2교시 values의 Prometheus 메모리 한도를 그대로 두고, podinfo-canary를 지워 자리를 만듭니다(`helm uninstall podinfo-canary`).
> - 어제의 Gateway가 살아 있어야 합니다: `curl -s -o /dev/null -w '%{http_code}\n' localhost:30080/api/products` → `200`.
> - 오늘 처음 받는 이미지: Prometheus · Grafana · Alertmanager · node-exporter · kube-state-metrics · 운영자(합쳐 약 1GB), `grafana/k6`.
> - 실습 파일은 강의 저장소의 `labs/week4/day2/`입니다.

---

⬅️ 이전: [7교시 · 장애 분석](../day1/lesson-07.md) &nbsp;|&nbsp; 다음: [1교시 · 1일차 요약 + 관찰 가능성](lesson-01.md) ➡️
