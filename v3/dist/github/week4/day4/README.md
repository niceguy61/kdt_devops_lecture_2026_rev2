# 4주차 4일차 — Service Mesh

## 오늘의 목표

어제 배움일기의 마지막 질문은 "서비스 사이의 호출(order-api → catalog-api)은 **아무 검사 없이** 오갔다. 누가 누구를 부를 수 있는지, 그 통신이 암호화되는지는 어떻게 정할까?"였습니다. 1일차의 Gateway는 **밖에서 안으로** 들어오는 요청을 다뤘습니다. 오늘은 **안에서 안으로** 오가는 요청을 다룹니다 — 코드를 한 줄도 고치지 않고.

- **남북(north-south)**과 **동서(east-west)** 트래픽, 그리고 서비스 메시가 하는 일을 구분합니다.
- **sidecar 모드**와 **ambient 모드**의 구조를 비교합니다.
- **Istio**(ambient)를 Helm으로 설치하고, DevMart를 **Git 커밋 하나로** 메시에 넣습니다.
- 서비스 사이 통신이 **mTLS**로 바뀐 것을 확인하고, **Kiali**로 메시 지도를 봅니다.
- **waypoint**를 두고, catalog-api 호출의 10%를 카나리로 보냅니다.
- **장애 주입**으로 catalog-api를 일부러 늦추고 실패시켜, 어제의 대시보드로 영향을 봅니다.
- **mTLS STRICT**와 **AuthorizationPolicy**로 "누가 누구를 부를 수 있나"를 정합니다.

## 시간표

| 교시 | 주제 | 실습 결과물 |
|---|---|---|
| 1교시 | 3일차 요약 + 서비스 메시 | 남북 · 동서 구분, sidecar vs ambient |
| 2교시 | Istio 설치와 메시 등록 | istiod · istio-cni · ztunnel, 라벨 커밋 하나 |
| 3교시 | mTLS 확인과 Kiali | 신원이 찍힌 로그, 메시 지도 |
| 4교시 | waypoint와 트래픽 나누기 | 메시 안 호출의 90/10 |
| 5교시 | 장애 주입 · 타임아웃 · 재시도 | 늦어진 catalog와 주문 오류 그래프 |
| 6교시 | mTLS STRICT와 호출 허가 | 메시 밖 · 허가 없는 손님 거절 |
| 7교시 | 메시 운영 판단 | 비용 · 대안 · 정리 |
| 8교시 | 배움일기 | |

## 교시별 자료

1. [3일차 요약 + 서비스 메시](lesson-01.md)
2. [Istio 설치와 메시 등록](lesson-02.md)
3. [mTLS 확인과 Kiali](lesson-03.md)
4. [waypoint와 트래픽 나누기](lesson-04.md)
5. [장애 주입 · 타임아웃 · 재시도](lesson-05.md)
6. [mTLS STRICT와 호출 허가](lesson-06.md)
7. [메시 운영 판단](lesson-07.md)

> [!IMPORTANT]
> **오늘 실습 전에 확인할 것**
>
> - Istio(ambient) + Kiali가 **약 0.6~1GB** 더 씁니다. 빠듯하면 1일차의 `podinfo` · `podinfo-canary`를 지웁니다(`helm uninstall … -n default`).
> - 어제의 Argo CD가 자동 동기화로 DevMart를 관리하고 있어야 합니다: `argocd app get devmart | grep -E "Sync Status|Health"` → `Synced` · `Healthy`.
> - **오늘 DevMart의 변경은 모두 배포 저장소(`devmart-deploy`)에 커밋**합니다. `kubectl apply`로 devmart에 직접 넣으면 selfHeal · prune과 엇갈립니다.
> - 실습 파일은 강의 저장소의 `labs/week4/day4/`입니다.

