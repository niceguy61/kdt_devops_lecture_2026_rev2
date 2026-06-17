# Week 2 Day 5: Docker Compose와 다중 컨테이너 실행 표준화

## Overview
Day 5는 Week 2에서 길게 실행했던 Docker 명령을 `compose.yaml`로 표준화하고, 제공 코드로 여러 유명 로컬 아키텍처를 직접 실행한다. 단순히 YAML 문법을 설명하는 날이 아니라 Web+DB, DB 관리 UI, cache, reverse proxy, queue+worker 같은 패턴을 `docker compose config`, `up`, `ps`, `logs`, `curl`, `exec`, `down`으로 검증한다.

오늘의 핵심 질문은 다음과 같다.

```text
유명한 다중 컨테이너 아키텍처를 compose.yaml로 제공하면 실행, 확인, 장애 분석, 인수인계가 어떻게 쉬워지는가?
```

Day 5는 Docker Compose 확정일이다. 강사는 각 아키텍처별 starter code와 `compose.yaml`을 제공하고, 학생은 명령을 실행해 진짜로 뜨는지 검증한다. 모든 실행 명령은 code block으로 제시하고, 각 architecture는 최소한 start, check, logs, cleanup 순서로 확인한다.

## Learning Goals
- Compose가 필요한 이유를 긴 `docker run` 명령의 반복성과 인수인계 문제로 설명한다.
- `compose.yaml`의 `services`, `image`, `ports`, `environment`, `volumes`, `networks`를 읽는다.
- Web+PostgreSQL two-tier 구조에서 service name, internal port, host port, connection string을 구분한다.
- Adminer/pgAdmin 같은 DB 관리 UI를 붙일 때 어떤 port를 host에 노출하는지 설명한다.
- Redis cache를 붙이고 cache hit/miss 또는 log 확인 지점을 확인한다.
- Nginx reverse proxy가 여러 web service로 routing하는 구조를 설명한다.
- queue+worker+database 구조에서 비동기 처리와 worker logs를 확인한다.
- `docker compose up`, `ps`, `logs`, `exec`, `down`, `down -v`의 차이를 설명한다.
- Compose volume cleanup이 database data 삭제로 이어질 수 있음을 설명한다.
- missing env, wrong service name, wrong port, stale volume을 Compose 장애로 분류한다.
- Week 2 확인 지점을 Compose 흐름으로 연결한다.

## Lesson Index
| 교시 | 주제 | 핵심 산출물 |
|---|---|---|
| 1교시 | Compose 기본과 검증 루프 | config/up/ps/logs/down 확인 지점 |
| 2교시 | Architecture 1: Web + PostgreSQL | two-tier app 확인 지점 |
| 3교시 | Architecture 2: Web + PostgreSQL + Adminer/pgAdmin | DB UI 확인 지점 |
| 4교시 | Architecture 3: Web + Redis cache | cache/log 확인 지점 |
| 5교시 | Architecture 4: Nginx reverse proxy + multiple web services | routing 확인 지점 |
| 6교시 | Architecture 5: Queue + worker + database | async worker 확인 지점 |
| 7교시 | Compose 장애 분석과 cleanup | missing env/wrong service/down-v RCA |
| 8교시 | 2주차 학습 흐름과 Week 3 MSA 연결 | service boundary readiness |

## Practice Files And Assets
| 자료 | 용도 |
|---|---|
| `assets/day5-compose-architecture-lab-overview.png` | Day 5 Compose architecture lab 전체 구조 인포그래픽 |
| `labs/compose-architectures/01-web-postgres/` | Web + PostgreSQL two-tier app |
| `labs/compose-architectures/02-web-postgres-admin/` | Web + DB + Adminer/pgAdmin |
| `labs/compose-architectures/03-web-redis/` | Web + Redis cache |
| `labs/compose-architectures/04-nginx-reverse-proxy/` | Nginx reverse proxy + multiple web services |
| `labs/compose-architectures/05-queue-worker-db/` | Queue + worker + database |
| 각 architecture의 `compose.yaml` | 실행 조건과 service 관계 |
| 각 architecture의 `README.md` | 실행/check/logs/cleanup 명령 |
| `hands-on-lab.md` | Day 5 전체 Compose 실행 흐름 |
| `academic-foundations.md` | 학술/현업 기준 mapping |
| `assets/lesson-01-docker-ops-model.png` | Docker 운영 모델 |
| `assets/lesson-02-good-dockerfile.png` | 좋은 Dockerfile 기준 |
| `assets/lesson-03-container-security.png` | 컨테이너 보안 기초 |
| `assets/lesson-04-image-flow.png` | image 배포 흐름 |
| `assets/lesson-05-integration-lab.png` | 통합 실습 확인 지점 |
| `assets/lesson-06-learning-summary-확인 지점.png` | 학습 정리 구조 |
| `assets/lesson-07-feedback-loop.png` | 학습 흐름 점검과 수정 흐름 |
| `assets/lesson-08-week3-bridge.png` | Week 3 MSA 연결 |

## 주의할 점
| 상황 | 실수를 줄이는 확인 지점 |
|---|---|
| Compose config 확인 지점 | `docker compose config` 성공 또는 error summary |
| Compose up 확인 지점 | `docker compose up -d`, `ps`, service status |
| PostgreSQL 확인 지점 | `exec` 또는 client query result |
| Volume 확인 지점 | Compose volume name, data persistence, cleanup decision |
| Web 확인 지점 | web service가 있으면 HTTP 200/body marker |
| Architecture 확인 지점 | 최소 2개 architecture의 실행/check/logs/cleanup |
| Logs 확인 지점 | `docker compose logs` 핵심 줄 |
| 실패 시 확인 지점 | missing env/wrong service name/wrong port/stale volume 중 하나 RCA |
| Handoff 확인 지점 | README compose up/check/exec/down/down-v warning |
| Week 3 readiness | service/network/dependency 질문 목록 |

## Preflight 확인 지점
현재 저장소 기준으로 다음 Compose architecture는 로컬 Docker에서 사전 검증했다.

| Architecture | 검증 명령 | 결과 |
|---|---|---|
| `01-web-postgres` | `docker compose up -d`, `curl -I http://localhost:18085`, `docker compose exec db psql ...`, `docker compose down` | HTTP 200, PostgreSQL `current_database = app`, cleanup 성공 |
| `04-nginx-reverse-proxy` | `docker compose up -d`, `curl http://localhost:18089/a/`, `curl http://localhost:18089/b/`, `docker compose down` | Web A/Web B 응답, proxy logs, cleanup 성공 |

`02`, `03`, `05`는 `docker compose config` 검증을 통과했다. 해당 예제는 `adminer:4`, `redis:7-alpine` image pull이 필요할 수 있으므로 수업 전 네트워크 상태에서 `docker compose pull`을 먼저 확인한다.

## Official References
| Topic | Reference | 확인할 키워드 |
|---|---|---|
| Docker Compose | https://docs.docker.com/compose/ | multi-container application |
| Compose file services | https://docs.docker.com/reference/compose-file/services/ | image, build, ports, environment, volumes |
| Compose networking | https://docs.docker.com/compose/how-tos/networking/ | service name, DNS |
| Compose volumes | https://docs.docker.com/reference/compose-file/volumes/ | named volumes |
| PostgreSQL official image | https://github.com/docker-library/docs/blob/master/postgres/README.md | env, data directory, tags |
| Twelve-Factor App | https://12factor.net/ | config, backing services |

## Academic/Workforce Standards Alignment
| 기준 | Day 5 적용 | 학생 확인 지점 |
|---|---|---|
| ABET problem analysis | 여러 service 실행 조건과 장애를 분류 | compose RCA |
| ABET communication | 실행 가능한 Compose README | handoff package |
| CS2023 Knowledge | service, network, volume, config 개념 | concept map |
| CS2023 Skill | compose config/up/ps/logs/exec/down 수행 | command 확인 지점 |
| CS2023 Disposition | secret 비노출과 volume cleanup 책임 | security/data note |
| Bloom Evaluate | `down -v`와 volume 삭제 위험 확인 | cleanup decision |
| SRE practice | failure drill, RCA, 확인 지점 summary | RCA note |

## Risk Register
| 위험 | 가능성 | 영향 | Severity | 완화 |
|---|---:|---:|---|---|
| `.env`/password 노출 | 중간 | 높음 | High | secret masking, `.env.example` |
| `down -v`로 DB data 삭제 | 중간 | 높음 | High | cleanup warning |
| wrong service name | 높음 | 중간 | Medium | Compose DNS 설명 |
| wrong host/container port | 높음 | 중간 | Medium | port mapping table |
| stale volume | 중간 | 중간 | Medium | volume inspect/cleanup decision |
| cleanup 누락 | 높음 | 낮음 | Medium | compose down audit |

## End-Of-Day Checklist
- [ ] Day 1~2의 긴 `docker run` 명령을 Compose service로 옮겼다.
- [ ] `docker compose config`를 실행했다.
- [ ] `docker compose up -d`와 `ps`로 service 상태를 확인했다.
- [ ] 최소 2개 architecture를 실행하고 검증했다.
- [ ] Web+DB architecture에서 DB query 또는 app response를 확인했다.
- [ ] DB UI, cache, reverse proxy, queue+worker 중 하나 이상을 추가로 실행했다.
- [ ] Compose volume이 data를 보존하는지 확인했다.
- [ ] `docker compose down`과 `down -v`의 차이를 설명했다.
- [ ] Compose 장애/RCA 확인 1개를 완성했다.
- [ ] README에 compose up/check/exec/logs/down/cleanup warning을 확인했다.
- [ ] Week 3 MSA readiness 질문을 작성했다.

## Completion Definition
Day 5는 다음 문장을 확인 지점과 함께 말할 수 있을 때 완료된다.

```text
제공된 Compose architecture는 compose.yaml 하나로 실행할 수 있고, services/ports/env/volumes/networks 조건이 파일에 남아 있으며, README는 다음 사람이 실행, 확인, 정리, 장애 대응을 재현할 수 있게 한다.
```

## Next Connection
Week 3는 MSA로 넘어간다. Day 5에서 정리한 Compose service, service name, network, volume, dependency 기준은 Week 3에서 frontend, api, database, worker 등 여러 service의 topology, dependency, health check, failure propagation을 다루는 기준이 된다.

## Final Submission Packet
| Artifact | 주의할 점 |
|---|---|
| compose.yaml | services/ports/env/volumes/networks |
| architecture folder | 제공 코드와 README |
| Compose 확인 지점 | config/up/ps/logs/exec/check |
| DB 확인 지점 | query result |
| volume 확인 지점 | persistence and cleanup decision |
| web 확인 지점 | HTTP 200/body marker if web service exists |
| RCA | symptom, fix, recheck, prevention |
| README | compose up/check/logs/exec/down/down-v warning |
| learning summary card | 확인 지점-centered study summary |
| Week 3 question | MSA readiness |

## Review Sequence
1. `compose.yaml`이 있는지 본다.
2. `docker compose config`가 되는지 본다.
3. `up`, `ps`, `logs`, `exec/check` 확인 지점가 있는지 본다.
4. volume과 cleanup 위험이 문서화됐는지 본다.
5. 실패 확인이 있는지 본다.
6. 다른 사람이 fresh clone 후 따라 할 수 있는지 본다.

## Day 5 Instructor Notes
- 새 기능 추가보다 Compose handoff와 확인 지점을 우선한다.
- Docker Hub push는 기본 요구하지 않는다.
- `down -v`는 데이터 삭제 명령으로 반복 강조한다.
- 학습 정리는 UI 시연보다 compose config/up/check/RCA/cleanup과 본인 인사이트 중심으로 유도한다.
- Week 3 preview는 MSA를 정답처럼 말하지 않고 운영 trade-off로 소개한다.
