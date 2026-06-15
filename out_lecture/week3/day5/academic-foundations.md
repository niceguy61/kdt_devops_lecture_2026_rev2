# Week 3 Day 5 Academic And Workforce Foundations

## 기준 연결
| 기준 | Day 5 적용 | 학생 evidence |
|---|---|---|
| ABET problem analysis | 서비스 의존성과 장애 원인 분류 | topology/failure table |
| ABET communication | 개발팀과 운영팀이 공유할 장애 리포트 작성 | handoff note |
| CS2023 Knowledge | distributed systems, networking, reliability 개념 | service map |
| CS2023 Skill | Compose 실행, 로그 확인, 설정 변경 | command evidence |
| NIST NICE | credential hygiene, least privilege, operational monitoring | config/security note |
| SRE practice | cascading failure, postmortem, health check | RCA note |

## 핵심 판단
MSA 학습의 핵심은 서비스를 많이 쪼개는 것이 아니라, 쪼갠 서비스의 실행 조건과 장애 영향을 설명할 수 있는가이다. 배포 단위가 늘면 팀 독립성과 확장성의 가능성이 생기지만, 네트워크 실패와 로그 분산, 설정 관리 비용도 늘어난다.

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
