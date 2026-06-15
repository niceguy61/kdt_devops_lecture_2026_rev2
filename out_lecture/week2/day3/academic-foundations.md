# Week 2 Day 3 Academic Foundations

## 핵심 근거
| 근거 | Day 3 연결 |
|---|---|
| Docker run reference | port, env, mount, network 실행 옵션의 공식 기준 |
| Docker networking docs | bridge network, container DNS, port publishing 구분 |
| Docker storage docs | bind mount와 volume의 lifecycle 차이 |
| PostgreSQL official image docs | `POSTGRES_PASSWORD`, data directory, initialization behavior |
| Twelve-Factor App config principle | 설정은 code/image에 굳히지 않고 environment로 분리 |

## 시스템 관점
Container runtime은 image를 실행 가능한 instance로 바꾸는 단계다. image는 read-only filesystem layer와 metadata를 제공하지만, 외부에서 접근할 port, runtime config, persistent storage, network membership은 실행 시점에 결정된다.

Port publishing은 namespace boundary를 넘는 작업이다. container 내부 process가 80번 port에서 listen하더라도 host가 자동으로 접근할 수 있는 것은 아니다. `-p 18083:80`은 host namespace의 18083번 port로 들어온 요청을 container namespace의 80번 port로 전달한다.

Environment variable은 build artifact가 아니라 runtime configuration으로 다룬다. 같은 image라도 `APP_ENV=practice`와 `APP_ENV=prod`로 실행하면 동작 조건이 달라질 수 있다. 단, secret을 environment variable로 주입하는 것은 실습에서는 편리하지만 운영에서는 노출 경로를 함께 고려해야 한다.

Bind mount와 named volume은 모두 container filesystem 바깥에 데이터를 둔다. bind mount는 host path에 직접 의존하고, named volume은 Docker가 관리하는 storage object에 의존한다. 개발 중 file sync에는 bind mount가 직관적이고, DB data persistence에는 named volume이 더 표준적이다.

## 교육적 초점
Day 3의 난이도는 명령어 자체보다 분류에 있다. 학생은 실패를 보면 먼저 "build 문제인가 runtime 문제인가"를 나누고, runtime 문제 안에서 port, network, env, volume, process/log 중 어디에 가까운지 분류한다.

## 평가 관점
| 수준 | 기대 행동 |
|---|---|
| 기억 | `-p`, `-e`, `-v`, `--network` 옵션 이름을 말한다 |
| 이해 | host port와 container port를 구분한다 |
| 적용 | 같은 image를 다른 port/env/volume 조건으로 실행한다 |
| 분석 | HTTP 실패, env 누락, DB readiness 실패를 evidence로 분류한다 |
| 종합 | README에 실행 조건과 cleanup을 재현 가능하게 남긴다 |

## 공식 링크
- Docker run reference: https://docs.docker.com/reference/cli/docker/container/run/
- Docker networking: https://docs.docker.com/engine/network/
- Docker storage: https://docs.docker.com/engine/storage/
- Docker volumes: https://docs.docker.com/engine/storage/volumes/
- Docker bind mounts: https://docs.docker.com/engine/storage/bind-mounts/
- PostgreSQL Docker Official Image: https://hub.docker.com/_/postgres
- Twelve-Factor App Config: https://12factor.net/config
