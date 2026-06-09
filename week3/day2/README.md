# Week 3 Day 2: 서비스 간 통신과 연결 실패 분석

## Overview
Day 2는 3주차 MSA 학습 흐름 중 `서비스 간 통신과 연결 실패 분석`를 다룬다. 오늘의 초점은 개발 코드 내부가 아니라 서비스를 실행하고 연결하고 관찰하고 복구하기 위해 인프라가 알아야 하는 정보다.

## Learning Goals
- 오늘 다루는 서비스 경계와 의존성을 운영 관점으로 설명한다.
- Docker Compose 상태, 로그, health, HTTP 응답 중 하나 이상으로 정상/비정상을 판단한다.
- 장애 증상을 숨기지 않고 재현 조건, 관찰 결과, 수정 또는 요청사항으로 기록한다.
- Week 4 Kubernetes에서 필요한 리소스와 설정으로 연결한다.

## Lesson Index
| 교시 | 주제 | 핵심 산출물 |
|---|---|---|
| 1교시 | 서비스 간 통신을 보는 법 | endpoint, protocol, status code, latency, dependency map evidence |
| 2교시 | frontend와 api 연결 운영 관점 | API URL, reverse proxy, CORS 협업 기준 evidence |
| 3교시 | 컨테이너 네트워크 복습 | localhost 오해, service name DNS, 내부 포트와 외부 포트 evidence |
| 4교시 | api와 database 연결 운영 관점 | connection string, credential, migration, 초기 데이터, 접근 권한 evidence |
| 5교시 | 서비스 실행 순서 문제 | depends_on의 의미와 한계, DB readiness, 재시도 필요성 evidence |
| 6교시 | health check 기본 | /health endpoint, liveness/readiness 차이, 장애 감지 기준 evidence |
| 7교시 | 연결 실패 장애 분석 | 잘못된 API URL, DB host 오류, 포트 오류, 환경변수 누락 찾기 evidence |
| 8교시 | 개발팀에 전달할 장애 리포트 작성 | 재현 조건, 관찰 결과, 의심 지점, 필요한 수정 요청 evidence |

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
| 1교시 | 서비스 간 통신을 보는 법 | ![Day 2 Lesson 1](./assets/lesson-01-service-communication.png) |
| 2교시 | frontend와 api 연결 운영 관점 | ![Day 2 Lesson 2](./assets/lesson-02-frontend-api-link.png) |
| 3교시 | 컨테이너 네트워크 복습 | ![Day 2 Lesson 3](./assets/lesson-03-container-network-dns.png) |
| 4교시 | api와 database 연결 운영 관점 | ![Day 2 Lesson 4](./assets/lesson-04-api-database-link.png) |
| 5교시 | 서비스 실행 순서 문제 | ![Day 2 Lesson 5](./assets/lesson-05-startup-order-readiness.png) |
| 6교시 | health check 기본 | ![Day 2 Lesson 6](./assets/lesson-06-health-check-basics.png) |
| 7교시 | 연결 실패 장애 분석 | ![Day 2 Lesson 7](./assets/lesson-07-connection-failure-analysis.png) |
| 8교시 | 개발팀에 전달할 장애 리포트 작성 | ![Day 2 Lesson 8](./assets/lesson-08-developer-incident-report.png) |

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
