# Week 2 Day 5 Academic Foundations

Day 5는 Docker Compose로 Week1 Day4의 회사형 서비스 아키텍처를 로컬에서 재현하는 통합 실습이다. 목표는 Compose 문법을 외우는 것이 아니라, frontend, gateway, API, database, cache, queue, worker를 하나의 application model로 묶고 검증 루프를 표준화하는 것이다.

| 근거 | Day 5 연결 |
|---|---|
| Docker Compose docs | multi-container application stack 정의와 lifecycle |
| Compose Specification | services, networks, volumes, configs, secrets의 application model |
| Compose services reference | image, build, ports, environment, volumes, depends_on |
| Compose networking docs | service name 기반 discovery와 project network |
| Compose volumes reference | named volume과 stateful service persistence |
| PostgreSQL official image | database service 초기화와 data directory |
| SRE/DevOps handoff | architecture별 run/check/logs/cleanup 문서화 |

## Conceptual Rationale

Compose는 `docker run` 명령을 길게 적는 편의 도구가 아니다. application을 구성하는 service, network, volume, environment를 파일로 남겨 다른 사람이 같은 구조를 재현하게 만드는 도구다. Day 5에서는 커머스 카탈로그, 백엔드 서비스 경계, 프론트엔드 설정 API, cache, gateway, queue/worker, API+DB, MSA preview 같은 구조를 짧은 코드와 함께 제공하고 학생이 직접 실행, 확인, 실패 정리를 하게 한다.

각 architecture는 Week 3 MSA로 이어지는 전 단계다. service name으로 DB에 붙는 경험은 internal API host 이해로 이어지고, reverse proxy 실습은 ingress 개념의 준비가 된다. queue/worker 구조는 동기 HTTP 호출만으로 서비스를 설계하지 않는 이유를 보여준다. 마지막 frontend+gateway+API+DB template은 여러 service가 하나의 사용자 요청을 처리할 때 dependency와 장애 전파를 어떻게 읽어야 하는지 보여준다.

## Architecture Coverage

| Template | 회사형 시나리오 | 확인 증거 |
|---|---|---|
| Commerce catalog | frontend, catalog API, products DB | HTTP 200, `/products`, DB query |
| Backend boundary | gateway, identity API, payment API, DB UI | `/identity/users`, `/payment/payments`, Adminer server `db` |
| Frontend platform | config API, feature flag, cache backing service | `/config`, Redis `GET`, cache writer logs |
| Nginx reverse proxy | gateway, upstream routing | `/a/`, `/b/`, proxy logs |
| Messaging worker | HTTP producer, Redis queue, worker | `/publish`, worker logs, DB query |
| API + PostgreSQL | API layer, DB schema/role | `/tasks` JSON response |
| Frontend + gateway + API + DB | MSA preview | frontend marker, `/api/services` response |

## Official Links

- Docker Compose: https://docs.docker.com/compose/
- Compose application model: https://docs.docker.com/compose/intro/compose-application-model/
- Compose file reference: https://docs.docker.com/compose/compose-file/
- Compose services reference: https://docs.docker.com/reference/compose-file/services/
- Compose networking: https://docs.docker.com/compose/how-tos/networking/
- Compose volumes reference: https://docs.docker.com/reference/compose-file/volumes/
- PostgreSQL Docker Official Image: https://hub.docker.com/_/postgres

## Standards Crosswalk

| 기준 | 학생 행동 |
|---|---|
| Bloom create/evaluate | architecture별 Compose file을 실행하고 적합성을 확인 |
| ABET-style solution design | service, network, volume, port, env를 하나의 model로 구성 |
| Professional responsibility | `.env.example`, secret 비노출, `down -v` 위험을 문서화 |
| SRE/DevOps 확인 지점 | `docker compose config`, `up`, `ps`, `logs`, HTTP/DB query 결과 확인 |

## 완료 전 주의할 점

학생은 Day 5 종료 시점에 다음을 설명할 수 있어야 한다.

- 최소 4개 이상 Compose architecture 실행 확인 지점
- `docker compose config --quiet` 통과 확인
- web endpoint, DB query, reverse proxy route, cache 또는 worker log 중 architecture별 검증 결과
- `docker compose down`과 `down -v`의 차이를 설명한 cleanup 확인
- Week 3 MSA로 넘어갈 때 남는 질문: service discovery, readiness, config, scaling, deployment
