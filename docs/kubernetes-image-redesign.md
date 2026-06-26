# Kubernetes Image Redesign Guide

## Goal
W3D4부터 W4D5까지의 Kubernetes 이미지는 강의 내용을 모두 담는 슬라이드가 아니라, 구조와 흐름을 빠르게 이해시키는 도식이어야 한다.

## Image Rules
| 항목 | 기준 |
|---|---|
| 텍스트 양 | 제목 1개, 노드명 4~7개, 짧은 상태 라벨 6~10개 이하 |
| 금지 | 긴 문장, 체크리스트, 비교표, 세부 주의사항, 작은 글씨 |
| 허용 | 구성요소 이름, 방향 라벨, 상태어, 짧은 edge label |
| 본문으로 내릴 것 | 장단점, 주의사항, 장애 원인, 운영 해석, 명령 예시 |
| 그림의 역할 | 구조, 경계, 흐름, 책임 분리, 통신 방향 |

## Visual Pattern
| 주제 | 이미지에 남길 것 | 본문 표로 내릴 것 |
|---|---|---|
| Control Plane | kubectl, API Server, etcd, Scheduler, Controller | 각 컴포넌트 상세 역할 |
| Node/Runtime | Node, kubelet, runtime, Pod | runtime 종류, 장애 원인 |
| Reconciliation | Desired, Current, Controller Loop | 장점/한계, 운영 해석 |
| Service/DNS/Ingress | Client, Ingress, Service, Endpoint, Pod | 404/503/timeout 원인표 |
| NetworkPolicy | frontend, api, db, DNS, allow/deny edge | selector 문법, CNI 주의 |
| Observability | App, Prometheus, Grafana, Alert | PromQL, metric 해석표 |
| RBAC/Kyverno | User/SA, API Server, RBAC, Admission, Policy | forbidden/deny 상세 비교 |
| Argo CD | Git, Argo CD, API Server, Cluster, Drift | prune/self-heal/rollback 주의 |
| Istio/Kiali | App, Envoy, istiod, Prometheus, Kiali graph | mTLS, traffic policy 상세 |

## Regeneration Priority
| 우선순위 | 범위 | 이유 |
|---|---|---|
| 1 | W3D4S2, W3D4S3, W3D4S4 | Kubernetes 기본 구조를 처음 잡는 그림 |
| 2 | W3D5S6, W4D2S2, W4D2S6 | Service/DNS/NetworkPolicy 통신 이해 |
| 3 | W4D5S1, W4D5S3, W4D5S7 | GitOps와 mesh 통신 구조 |
| 4 | W4D3S1~S5 | 관찰 흐름과 metric pipeline |
| 5 | 각 Day S8 | 요약 이미지는 evidence board로 단순화 |

## Prompt Template
```text
Professional Kubernetes architecture infographic, 16:9.
Keep the diagram simple and low-text.
Use only short labels for nodes and edges.
No paragraphs, no checklist blocks, no comparison table inside the image.
Move details to the lecture body.
Show structure, boundaries, and traffic/control flow clearly.
Small raccoon navigator character in one corner only.
```
