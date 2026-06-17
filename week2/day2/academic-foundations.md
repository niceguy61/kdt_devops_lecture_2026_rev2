# Week 2 Day 2 Academic And Professional Foundations

Day 2는 Docker container의 실행 상태가 어디에 남고, container들이 어떤 이름과 network boundary로 서로를 찾는지 다룬다. 핵심은 volume과 network를 옵션 암기가 아니라 운영 계약으로 읽는 것이다.

| 기준 | Day 2 연결 |
|---|---|
| Docker storage docs | container writable layer, named volume, bind mount의 lifecycle 구분 |
| Docker volumes docs | database data persistence와 volume 재사용 실습 |
| Docker bind mounts docs | host path 의존성과 개발 편의, 권한 위험 설명 |
| Docker networking docs | bridge network, user-defined network, container DNS 구분 |
| Docker run reference | `-v`, `--mount`, `--network`, `-p` 실행 옵션의 공식 기준 |
| PostgreSQL official image | data directory, initialization, password env 기준 |
| SRE/DevOps 운영 점검 culture | 데이터 생존 여부와 연결 경로를 query/log로 확인 |

## Conceptual Rationale

Container는 지우고 다시 만들 수 있어야 하지만, 모든 데이터가 같이 사라져야 하는 것은 아니다. Day 2의 첫 실험은 volume 없이 PostgreSQL container를 띄우고 데이터를 넣은 뒤 container를 삭제했을 때 데이터가 사라지는지 확인한다. 이 실패를 먼저 보여주면 volume이 "편의 기능"이 아니라 stateful workload의 필수 경계라는 점이 명확해진다.

Network도 같은 방식으로 다룬다. host에서 `localhost:15432`로 붙는 것과 같은 Docker network 안의 container가 `postgres16:5432`로 붙는 것은 다른 경로다. 학생은 port publishing과 service discovery를 분리해서 설명해야 한다.

## Official Links

- Docker storage: https://docs.docker.com/engine/storage/
- Docker volumes: https://docs.docker.com/engine/storage/volumes/
- Docker bind mounts: https://docs.docker.com/engine/storage/bind-mounts/
- Docker networking: https://docs.docker.com/engine/network/
- Docker bridge network driver: https://docs.docker.com/engine/network/drivers/bridge/
- Docker run reference: https://docs.docker.com/reference/cli/docker/container/run/
- Docker volume CLI: https://docs.docker.com/reference/cli/docker/volume/
- Docker network CLI: https://docs.docker.com/reference/cli/docker/network/
- PostgreSQL Docker Official Image: https://hub.docker.com/_/postgres

## Standards Crosswalk

| 기준 | 학생 행동 |
|---|---|
| Bloom apply/analyze | volume 없는 DB와 named volume DB의 데이터 생존 결과를 비교 |
| ABET-style problem solving | 접속 실패를 port, network, DNS, container 상태로 분류 |
| Professional responsibility | `docker volume rm`과 `down -v`류 삭제 위험을 설명 |
| SRE/DevOps 운영 점검 | query, `docker volume ls`, `docker network inspect`로 상태 확인 |

## 완료 전 주의할 점

- Volume 없이 만든 DB data는 container 삭제와 함께 사라질 수 있다. 이를 PostgreSQL 문제나 Docker 오류로 해석하지 않는다.
- Named volume은 container보다 오래 남는다. cleanup에서 container 삭제와 volume 삭제를 같은 의미로 다루면 안 된다.
- bind mount는 host filesystem을 직접 노출한다. host 경로, 권한, read-only 여부가 바뀌면 container 동작도 달라진다.
- User-defined network에서는 container name이 service discovery 역할을 한다. 같은 network에 붙어 있지 않으면 이름이 맞아도 통신되지 않는다.
- Host port publish는 host에서 들어오는 경로이고, container DNS는 container끼리 통신하는 경로다. `localhost`, published port, container port를 섞지 않는다.
