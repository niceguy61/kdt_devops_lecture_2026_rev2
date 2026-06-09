# Week 3 Day 1: MSA 첫 실행과 서비스 토폴로지

## Overview
Day 1는 3주차 MSA 학습 흐름 중 `MSA 첫 실행과 서비스 토폴로지`를 다룬다. 오늘의 초점은 개발 코드 내부가 아니라 서비스를 실행하고 연결하고 관찰하고 복구하기 위해 인프라가 알아야 하는 정보다.

## Learning Goals
- 오늘 다루는 서비스 경계와 의존성을 운영 관점으로 설명한다.
- Docker Compose 상태, 로그, health, HTTP 응답 중 하나 이상으로 정상/비정상을 판단한다.
- 장애 증상을 숨기지 않고 재현 조건, 관찰 결과, 수정 또는 요청사항으로 기록한다.
- Week 4 Kubernetes에서 필요한 리소스와 설정으로 연결한다.

## Lesson Index
| 교시 | 주제 | 핵심 산출물 |
|---|---|---|
| 1교시 | 2주차 복습 및 3주차 학습 목표 | 단일 컨테이너 앱에서 여러 서비스 앱으로 확장되는 흐름 evidence |
| 2교시 | Monolith vs MSA | 배포 단위, 장애 영향 범위, 네트워크 의존성, 운영 복잡도 비교 evidence |
| 3교시 | 인프라 엔지니어가 MSA에서 알아야 할 것 | 서비스 목록, 포트, 프로토콜, 의존성, 설정, 헬스체크, 로그 위치 evidence |
| 4교시 | 표준 MSA 실습 앱 토폴로지 소개 | frontend, api, worker, database 역할과 요청 흐름 evidence |
| 5교시 | 실습 앱 다운로드 및 실행 준비 | 폴더 구조, 운영 문서, 환경변수 예시 확인 evidence |
| 6교시 | Docker Compose로 전체 서비스 실행 | compose up, ps, logs, 브라우저 접속, 서비스 상태 확인 evidence |
| 7교시 | 개인 면담 및 환경 점검 | Compose 실행, 포트 충돌, 이미지 pull/build 문제 해결 evidence |
| 8교시 | 보충 실습 | 전체 서비스 실행 실패 학생 진도 회복 evidence |

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
| 1교시 | 2주차 복습 및 3주차 학습 목표 | ![Day 1 Lesson 1](./assets/lesson-01-week2-to-msa-goals.png) |
| 2교시 | Monolith vs MSA | ![Day 1 Lesson 2](./assets/lesson-02-monolith-vs-msa.png) |
| 3교시 | 인프라 엔지니어가 MSA에서 알아야 할 것 | ![Day 1 Lesson 3](./assets/lesson-03-msa-ops-contract.png) |
| 4교시 | 표준 MSA 실습 앱 토폴로지 소개 | ![Day 1 Lesson 4](./assets/lesson-04-standard-msa-topology.png) |
| 5교시 | 실습 앱 다운로드 및 실행 준비 | ![Day 1 Lesson 5](./assets/lesson-05-app-download-setup.png) |
| 6교시 | Docker Compose로 전체 서비스 실행 | ![Day 1 Lesson 6](./assets/lesson-06-compose-full-run.png) |
| 7교시 | 개인 면담 및 환경 점검 | ![Day 1 Lesson 7](./assets/lesson-07-environment-check.png) |
| 8교시 | 보충 실습 | ![Day 1 Lesson 8](./assets/lesson-08-recovery-practice.png) |

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
