# Week 3 Day 3: 데이터 의존성, Worker, 장애 전파

## Overview
Day 3는 3주차 MSA 학습 흐름 중 `데이터 의존성, Worker, 장애 전파`를 다룬다. 오늘의 초점은 개발 코드 내부가 아니라 서비스를 실행하고 연결하고 관찰하고 복구하기 위해 인프라가 알아야 하는 정보다.

## Learning Goals
- 오늘 다루는 서비스 경계와 의존성을 운영 관점으로 설명한다.
- Docker Compose 상태, 로그, health, HTTP 응답 중 하나 이상으로 정상/비정상을 판단한다.
- 장애 증상을 숨기지 않고 재현 조건, 관찰 결과, 수정 또는 요청사항으로 기록한다.
- Week 4 Kubernetes에서 필요한 리소스와 설정으로 연결한다.

## Lesson Index
| 교시 | 주제 | 핵심 산출물 |
|---|---|---|
| 1교시 | 서비스 분리와 데이터 의존성 | DB 공유의 위험, 서비스별 데이터 책임, 장애 영향 범위 evidence |
| 2교시 | worker 서비스 운영 관점 | 비동기 처리, 배치 작업, 오래 걸리는 작업이 인프라에 주는 영향 evidence |
| 3교시 | queue 또는 redis 운영 개념 | 동기 호출과 비동기 처리의 차이, 병목과 적체 관찰 evidence |
| 4교시 | worker/queue 실습 | 요청 생성, 작업 처리, 로그와 상태로 처리 흐름 확인 evidence |
| 5교시 | 장애 전파와 부분 장애 | api, DB, worker 장애가 사용자 경험과 운영 대응에 미치는 영향 evidence |
| 6교시 | timeout과 retry 기본 | 무한 대기 방지, 재시도의 위험, 중복 처리 문제 evidence |
| 7교시 | 로그 분산 문제 | 여러 서비스 로그 보기, correlation id/request id 필요성 evidence |
| 8교시 | 관찰 가능성 기초 실습 | compose logs, 서비스별 로그 필터링, 요청 흐름 추적 evidence |

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
| 1교시 | 서비스 분리와 데이터 의존성 | ![Day 3 Lesson 1](./assets/lesson-01-data-dependency.png) |
| 2교시 | worker 서비스 운영 관점 | ![Day 3 Lesson 2](./assets/lesson-02-worker-operations.png) |
| 3교시 | queue 또는 redis 운영 개념 | ![Day 3 Lesson 3](./assets/lesson-03-queue-redis-concept.png) |
| 4교시 | worker/queue 실습 | ![Day 3 Lesson 4](./assets/lesson-04-worker-queue-lab.png) |
| 5교시 | 장애 전파와 부분 장애 | ![Day 3 Lesson 5](./assets/lesson-05-failure-propagation.png) |
| 6교시 | timeout과 retry 기본 | ![Day 3 Lesson 6](./assets/lesson-06-timeout-retry.png) |
| 7교시 | 로그 분산 문제 | ![Day 3 Lesson 7](./assets/lesson-07-distributed-logs.png) |
| 8교시 | 관찰 가능성 기초 실습 | ![Day 3 Lesson 8](./assets/lesson-08-observability-lab.png) |

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
