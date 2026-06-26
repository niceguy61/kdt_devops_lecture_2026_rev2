# Week 4 Day2: Service, DNS, Ingress, 외부 Traffic

## Overview
W4D2는 W4D1에서 만든 운영형 workload 기준을 외부 traffic 흐름으로 확장한다. Kubernetes 안에서는 Service DNS와 Endpoint가 traffic을 연결하고, cluster 밖 사용자는 Ingress Controller와 Ingress rule을 통해 Service에 도달한다.

오늘의 add-on은 `ingress-nginx`다. 설치는 W4 공통 원칙에 따라 Helm으로 진행하고, values file, release name, namespace, 검증 명령, uninstall 명령을 함께 남긴다.

## Learning Goals
- Pod IP, Service, Endpoint, DNS, selector 관계를 출력으로 설명한다.
- frontend, api, database 성격의 MSA 앱을 Kubernetes Service로 연결한다.
- ingress-nginx를 Helm으로 설치하고 controller Pod/Service/admission job을 확인한다.
- Ingress `host`, `path`, `pathType`, `ingressClassName`, backend service/port를 구분한다.
- `/`는 frontend, `/api`는 api로 routing되는 것을 curl과 browser 기준으로 확인한다.
- className 누락, selector 오류, backend port 오류, readiness 실패를 404/503/connection refused와 연결해 분석한다.
- NetworkPolicy preview로 frontend -> api, api -> db만 허용하는 사고방식을 익힌다.
- rollout이 외부 traffic에 미치는 영향을 Ingress 경로로 확인한다.

## Lesson Index
| 교시 | 주제 | 핵심 확인 |
|---|---|---|
| 1교시 | Day1 요약 + Kubernetes networking 다시 잡기 | Pod IP, Service, Endpoint, DNS, selector |
| 2교시 | MSA 앱 내부 통신 | frontend/api/db Service DNS와 targetPort |
| 3교시 | ingress-nginx 설치 | Helm release, controller Pod/Service, admission |
| 4교시 | Ingress rule 작성 | host/path routing, `/`, `/api`, curl/browser |
| 5교시 | Ingress 장애 분석 | className, selector, backend port, endpoint |
| 6교시 | NetworkPolicy preview | traffic 허용선, DNS egress, CNI 주의 |
| 7교시 | rollout과 external traffic | image/tag 변경, rollout status/history/undo |
| 8교시 | 구름 EXP 배움일기 | Service/Ingress/DNS 증거와 장애 메모 |

## Practice Files
| 자료 | 용도 |
|---|---|
| `hands-on-lab.md` | 당일 실습 명령과 예상 출력 |
| `academic-foundations.md` | Service, DNS, Ingress, NetworkPolicy 개념 |
| `labs/traffic-routing/` | frontend/api/db, Service, Ingress, 장애/NetworkPolicy manifest |
| `labs/ingress-nginx/values.yaml` | ingress-nginx Helm values |

## Official References
| Topic | Reference |
|---|---|
| Kubernetes Service | https://kubernetes.io/docs/concepts/services-networking/service/ |
| Kubernetes Ingress | https://kubernetes.io/docs/concepts/services-networking/ingress/ |
| Kubernetes NetworkPolicy | https://kubernetes.io/docs/concepts/services-networking/network-policies/ |
| kind Ingress guide | https://kind.sigs.k8s.io/docs/user/ingress/ |
| ingress-nginx Helm chart | https://artifacthub.io/packages/helm/ingress-nginx/ingress-nginx |

## End-Of-Day Checklist
- [ ] Service selector와 Endpoint가 연결되는 것을 확인했다.
- [ ] Service DNS 이름으로 frontend -> api 통신을 확인했다.
- [ ] ingress-nginx를 Helm으로 설치하고 release와 Pod 상태를 확인했다.
- [ ] `/`와 `/api`가 서로 다른 Service로 routing되는 것을 확인했다.
- [ ] Ingress 장애에서 className, selector, backend port, endpoint를 구분했다.
- [ ] NetworkPolicy가 필요한 이유와 kind 기본 CNI 주의점을 설명했다.
- [ ] rollout이 외부 경로에 어떤 영향을 주는지 확인했다.

