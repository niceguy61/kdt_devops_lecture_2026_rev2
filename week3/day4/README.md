# Week 3 Day 4: 설정, API 계약, 배포 협업, Kubernetes 필요성

## Overview
Day 4는 3주차 MSA 학습 흐름 중 `설정, API 계약, 배포 협업, Kubernetes 필요성`를 다룬다. 오늘의 초점은 개발 코드 내부가 아니라 서비스를 실행하고 연결하고 관찰하고 복구하기 위해 인프라가 알아야 하는 정보다.

## Learning Goals
- 오늘 다루는 서비스 경계와 의존성을 운영 관점으로 설명한다.
- Docker Compose 상태, 로그, health, HTTP 응답 중 하나 이상으로 정상/비정상을 판단한다.
- 장애 증상을 숨기지 않고 재현 조건, 관찰 결과, 수정 또는 요청사항으로 기록한다.
- Week 4 Kubernetes에서 필요한 리소스와 설정으로 연결한다.

## Lesson Index
| 교시 | 주제 | 핵심 산출물 |
|---|---|---|
| 1교시 | MSA 설정 관리 | 환경변수, .env, config 분리, secret 비노출 evidence |
| 2교시 | MSA 로컬 개발 환경 | hot reload, bind mount, dev/prod compose 분리 개념 evidence |
| 3교시 | API 계약과 운영 문서 | OpenAPI/Swagger 개념, endpoint, health, dependency 정보 evidence |
| 4교시 | 버전 관리와 배포 협업 | 이미지 태그, 하위 호환, 배포 순서, rollback 가능성 evidence |
| 5교시 | MSA 운영 비용 정리 | 배포 단위 증가, 로그 증가, 네트워크 장애, 알림 복잡도 evidence |
| 6교시 | Kubernetes가 필요한 이유 | 수동 Compose 운영의 한계와 선언적 운영 필요성 evidence |
| 7교시 | 개인 면담 및 환경 점검 | MSA 앱 실행 상태, Compose 설정, 로그 분석 기록 확인 evidence |
| 8교시 | 보충 실습 | 서비스 연결 문제, DB 초기화 문제, worker 실행 문제 해결 evidence |

## Practice Files And Assets
| 자료 | 용도 |
|---|---|
| `../day1/labs/msa-demo/compose.yaml` | 표준 MSA 실습 앱 실행 |
| `../day1/labs/msa-demo/README.md` | run/check/failure/cleanup 기준 |
| `hands-on-lab.md` | 오늘 실습 흐름이 있는 경우 실행 가이드 |
| `academic-foundations.md` | 공식/학술/현업 기준 mapping |
| `assets/` | 각 교시 보조 시각 자료 위치 |

## Session Visual Index
| 교시 | 주제 | 세션별 이미지 |
|---|---|---|
| 1교시 | MSA 설정 관리 | ![Day 4 Lesson 1](./assets/lesson-01-config-management.png) |
| 2교시 | MSA 로컬 개발 환경 | ![Day 4 Lesson 2](./assets/lesson-02-local-dev-environment.png) |
| 3교시 | API 계약과 운영 문서 | ![Day 4 Lesson 3](./assets/lesson-03-api-contract-docs.png) |
| 4교시 | 버전 관리와 배포 협업 | ![Day 4 Lesson 4](./assets/lesson-04-version-deploy-collaboration.png) |
| 5교시 | MSA 운영 비용 정리 | ![Day 4 Lesson 5](./assets/lesson-05-msa-operating-cost.png) |
| 6교시 | Kubernetes가 필요한 이유 | ![Day 4 Lesson 6](./assets/lesson-06-why-kubernetes.png) |
| 7교시 | 개인 면담 및 환경 점검 | ![Day 4 Lesson 7](./assets/lesson-07-msa-environment-check.png) |
| 8교시 | 보충 실습 | ![Day 4 Lesson 8](./assets/lesson-08-supplemental-troubleshooting.png) |

## Today Evidence
| Evidence | 제출 기준 |
|---|---|
| topology note | 서비스별 역할과 의존성 설명 |
| command evidence | 실행/확인/로그/정리 명령 |
| failure note | 장애 재현, 관찰, 복구, 예방 |
| handoff note | 개발팀 또는 다음 운영자에게 전달할 정보 |

## Official References
| Topic | Reference | 확인할 키워드 |
|---|---|---|
| Microservices on AWS | https://docs.aws.amazon.com/whitepapers/latest/microservices-on-aws/microservices.html | service, API, database, deployment |
| AWS Microservices | https://aws.amazon.com/microservices/ | independent component, business capability |
| Martin Fowler Microservices Guide | https://martinfowler.com/microservices/ | independently deployable, lightweight communication |
| Docker Compose | https://docs.docker.com/compose/ | services, networks, depends_on, healthcheck |
| Compose services reference | https://docs.docker.com/reference/compose-file/services/ | healthcheck, depends_on, environment |
| Google SRE Cascading Failures | https://sre.google/sre-book/addressing-cascading-failures/ | failure propagation, overload, mitigation |
| OpenTelemetry Concepts | https://opentelemetry.io/docs/concepts/ | traces, metrics, logs, observability |
| Twelve-Factor App | https://12factor.net/ | config, backing services, logs |


## End-Of-Day Checklist
- [ ] 오늘 다룬 서비스와 의존성을 다이어그램으로 설명했다.
- [ ] `docker compose ps`와 `docker compose logs`를 사용했다.
- [ ] 정상 상태와 장애 상태를 증거로 구분했다.
- [ ] 설정, health, logs, cleanup 기준을 문서에 남겼다.
- [ ] Kubernetes로 넘어갈 때 필요한 리소스 후보를 적었다.
