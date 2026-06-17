# Week 2 Day 4: Runtime Config, Observability, Failure Drill

## Overview
Day 4는 Day 3에서 만든 image와 Day 2에서 배운 storage/network를 바탕으로 runtime config와 관찰 방법을 깊게 다룬다. 같은 image라도 environment variable, env file, port, network, volume 조건이 달라지면 정상/장애 상태가 달라진다.

오늘의 핵심 질문은 다음과 같다.

```text
container가 정상인지, 왜 실패했는지, 무엇을 지워도 되는지는 어떤 명령과 확인 지점으로 판단하는가?
```

Day 4는 Compose 전 마지막 `docker run` 심화일이다. Compose로 넘어가기 전에 `-e`, `--env-file`, `logs`, `inspect`, `exec`, `stats`, restart policy, cleanup audit을 익힌다. 실습은 성공만 확인하지 않고 missing env, wrong port, wrong network, stale volume, bad image tag를 일부러 만들어 장애 흐름으로 구분한다.

## Learning Goals
- `-e`, `--env-file`, `.env.example`로 runtime config를 주입한다.
- secret을 image, README, screenshot, terminal history에 남기지 않는 기준을 설명한다.
- `docker logs`로 stdout/stderr와 readiness message를 확인한다.
- `docker inspect`로 env, network, mount, port mapping을 확인한다.
- `docker exec`로 container 내부 process/filesystem/network를 확인한다.
- `docker stats`와 restart policy로 resource/crash 상태를 관찰한다.
- missing env, wrong port, wrong network, stale volume, bad image tag를 RCA로 분류한다.
- Day 2~4의 긴 명령을 Compose로 옮길 mapping을 만든다.

## Lesson Index
- 1교시: environment variable과 runtime config - `-e`, `--env-file`, `.env.example`, image 밖 config
- 2교시: secret 비노출과 설정 파일 위험 - README/screenshot/history에 password/token을 남기지 않는 기준
- 3교시: logs 기반 정상/장애 확인 - `docker logs`, app stdout/stderr, DB readiness log
- 4교시: inspect/exec 기반 내부 확인 - filesystem, env, network, mount, process 확인
- 5교시: stats/resource/restart policy - CPU/memory 관찰, restart 옵션, crash loop 맛보기
- 6교시: 통합 failure drill - missing env, wrong port, wrong network, stale volume, bad image tag
- 7교시: cleanup/security audit - container/image/network/volume 정리, 삭제하면 안 되는 data 구분
- 8교시: Compose 준비 handoff - Day 2~4 긴 명령을 compose.yaml로 옮길 mapping 작성

## Practice Files And Assets
| 자료 | 용도 |
|---|---|
| `assets/day4-runtime-observability-overview.png` | Day 4 runtime config/observability 전체 구조 인포그래픽 |
| `labs/env-report/report.sh` | environment variable 출력 실습 |
| `labs/env-report/.env.example` | env file 형식과 secret masking 기준 |
| Day 3 built image | runtime config와 logs/inspect/exec 실습 대상 |
| Day 2 PostgreSQL network/volume | stale volume, wrong network failure drill |
| `hands-on-lab.md` | Day 4 전체 실행 흐름 |
| `assets/lesson-01-runtime-env-vars.png` | runtime env var |
| `assets/lesson-02-secret-risk.png` | secret 비노출 기준 |
| `assets/lesson-03-docker-logs-readiness.png` | logs/readiness |
| `assets/lesson-04-inspect-exec-map.png` | inspect/exec |
| `assets/lesson-05-stats-restart-policy.png` | stats/restart |
| `assets/lesson-06-runtime-failure-drill.png` | failure drill |
| `assets/lesson-07-cleanup-security-audit.png` | cleanup/security audit |
| `assets/lesson-08-compose-mapping.png` | docker run to Compose mapping |

## 주의할 점
| 상황 | 실수를 줄이는 확인 지점 |
|---|---|
| Env 확인 지점 | `-e` 또는 `--env-file`로 주입한 config와 secret masking |
| Log 확인 지점 | 정상 startup log 또는 failure log 핵심 줄 |
| Inspect 확인 지점 | env/network/mount/port 중 2개 이상 |
| Exec 확인 지점 | container 내부 command 결과 |
| Stats/restart 확인 지점 | resource 관찰 또는 restart policy 결과 |
| 실패 시 확인 지점 | missing env, wrong port, wrong network, stale volume, bad image tag 중 하나 RCA |
| cleanup 주의점 | container/image/network/volume 정리 결과와 data 보존 판단 |
| Compose mapping 확인 지점 | 긴 `docker run` 옵션을 compose 항목으로 옮긴 표 |

## Official References
| Topic | Reference | 확인할 키워드 |
|---|---|---|
| Docker run reference | https://docs.docker.com/reference/cli/docker/container/run/ | env, ports, volumes, restart |
| Docker logs | https://docs.docker.com/reference/cli/docker/container/logs/ | stdout/stderr |
| Docker inspect | https://docs.docker.com/reference/cli/docker/inspect/ | low-level metadata |
| Docker exec | https://docs.docker.com/reference/cli/docker/container/exec/ | inside container command |
| Docker stats | https://docs.docker.com/reference/cli/docker/container/stats/ | resource usage |
| OWASP Secrets Management | https://cheatsheetseries.owasp.org/cheatsheets/Secrets_Management_Cheat_Sheet.html | credential hygiene |

## Readiness And Cost Notes
- Day 4는 로컬 Docker runtime 실습이다. cloud resource, 유료 DB, Kubernetes cluster를 만들지 않는다.
- `.env`는 실습자의 로컬 파일로 두고, 공개 repository에는 실제 secret 값을 올리지 않는다.
- screenshot, README, terminal output에 password/token/MFA가 남지 않도록 마스킹한다.
- cleanup 명령은 container/image/network/volume을 구분하고, data 삭제 여부를 확인한 뒤 실행한다.

## End-Of-Day Checklist
- [ ] `-e` 또는 `--env-file`로 runtime config를 주입했다.
- [ ] secret 값을 README/screenshot/history에 남기지 않았다.
- [ ] `docker logs`로 정상 또는 장애 로그를 확인했다.
- [ ] `docker inspect`로 env/network/mount/port 중 2개 이상을 확인했다.
- [ ] `docker exec`로 container 내부 상태를 확인했다.
- [ ] `docker stats` 또는 restart policy로 resource/crash 상태를 관찰했다.
- [ ] missing env, wrong port, wrong network, stale volume, bad image tag 중 하나를 RCA로 확인했다.
- [ ] container/image/network/volume cleanup audit을 수행했다.
- [ ] Day 5 Compose로 옮길 `docker run` option mapping을 작성했다.

## Next Connection
Day 5는 Compose architecture lab이다. Day 4에서 정리한 port/env/volume/network/logs 옵션을 `compose.yaml`의 services, ports, environment, volumes, networks로 옮긴다.

## Prerequisites
Day 4를 시작하기 전에 학생은 다음을 확인해야 한다.

| 항목 | 확인 명령 | 정상 기준 |
|---|---|---|
| Docker daemon | `docker version` | client와 server 정보가 모두 출력 |
| Day 3 image | `docker image ls` | `paperclip-static-site:day3` 또는 대체 실습 image |
| 기본 image | `docker image ls` | `nginx` 또는 `postgres`가 없으면 pull 가능 |
| terminal 위치 | `pwd` | repository root 또는 lab directory |
| browser/curl | `curl --version` | HTTP 확인 가능 |
| port 여유 | `18084` 또는 실습 port 사용 가능 | 충돌 시 host port 변경 |

이 표는 설치 확인이 아니라 수업 중 failure domain을 줄이기 위한 preflight다. Docker daemon이 응답하지 않으면 Dockerfile, runtime option, Compose 중 어디를 고쳐도 해결되지 않는다.

## Day 2~3 To Day 4 Mapping
Day 4는 Day 2의 storage/network와 Day 3의 image를 실제 runtime 운영 조건으로 묶는다.

| 이전 학습 | Day 4 runtime 확인 | 확인 지점 |
|---|---|---|
| Day 2 volume | mount가 붙었는지 inspect | mount source/destination |
| Day 2 network | container가 올바른 network에 있는지 inspect | network name/IP |
| Day 3 image | 올바른 tag로 실행했는지 inspect | image ID/tag |
| runtime env | 설정이 image 밖에서 들어갔는지 inspect/exec | env key, masked value |
| app state | 정상/장애를 logs로 확인 | startup/error log |
| process/filesystem | exec로 내부 확인 | command output |
| cleanup | 지울 것과 남길 것을 구분 | cleanup audit |

## Academic/Workforce Standards Alignment
Day 4는 실습 중심이지만 확인 기준은 학술성과 실무성을 함께 포함한다.

| 기준 | Day 4 적용 | 학생 확인 지점 |
|---|---|---|
| ABET 문제 분석 | 긴 명령 기반 실행의 재현성 문제 분석 | option mapping note |
| ABET 커뮤니케이션 | 다른 사람이 실행 가능한 README 작성 | run/check/cleanup section |
| CS2023 Knowledge | image, network, volume, environment, observability 개념 | 개념 설명 문항 |
| CS2023 Skill | run/logs/inspect/exec/stats 수행 | command 확인 지점 |
| CS2023 Disposition | secret과 data 삭제 위험을 책임 있게 다룸 | `.env.example`, cleanup warning |
| NIST NICE | configuration/credential hygiene | secret 비노출 확인 |
| Bloom Analyze | 장애를 config/start/runtime/cleanup으로 분류 | RCA note |
| SRE practice | 확인 지점과 postmortem-style learning | failure drill과 recheck |

## Operational Readiness Model
Day 4의 운영 준비성은 다음 네 단계로 본다.

| 단계 | 질문 | 좋은 답 |
|---|---|---|
| Start | 어떤 image와 option으로 실행하는가 | tag, port, env, volume, network 명시 |
| Check | 정상 상태는 무엇인가 | HTTP/SQL/log/status 확인 지점 |
| Recover | 실패하면 어디를 보는가 | logs, inspect, exec, stats |
| Cleanup | 무엇을 지우고 무엇을 남기는가 | container/image/network/volume 구분 |

실무에서는 start만 있는 문서는 부족하다. check와 cleanup이 빠지면 다음 사람이 정상 여부와 비용/데이터 위험을 판단할 수 없다.

## Risk Register
| 위험 | 가능성 | 영향 | Severity | 완화 |
|---|---:|---:|---|---|
| `.env` secret 노출 | 중간 | 높음 | High | `.env.example`만 commit, 값 마스킹 |
| volume data 삭제 | 중간 | 높음 | High | 실습 reset 전용으로 문서화 |
| port 충돌 | 높음 | 낮음 | Medium | `WEB_PORT` 변경 |
| DB readiness 오해 | 중간 | 중간 | Medium | healthcheck와 query 확인 |
| container name/localhost 혼동 | 높음 | 중간 | Medium | host/container 경계 표기 |
| Docker daemon 미실행 | 중간 | 중간 | Medium | preflight에서 확인 |
| image pull 실패 | 낮음 | 중간 | Medium | 사전 image 확인 또는 네트워크 점검 |

## 확인 기준
| 항목 | 0점 | 1점 | 2점 |
|---|---|---|---|
| Env | 없음 | 주입만 함 | required variable과 secret 비노출 설명 |
| Logs | 없음 | 출력만 붙임 | 정상/장애 기준 해석 |
| Inspect | 없음 | 전체 JSON dump | env/network/mount/port를 선별해 해석 |
| Exec | 없음 | shell 접속만 함 | 내부 command로 원인 확인 |
| Stats/restart | 없음 | 실행만 함 | resource/crash 의미 설명 |
| Cleanup | 없음 | container만 삭제 | image/network/volume data 경계 설명 |
| RCA | 없음 | 증상만 확인 | 원인 후보, fix, recheck, prevention |
| Handoff | 없음 | 명령만 있음 | expected result와 cleanup warning 포함 |

## Common Misconceptions
| 오해 | 바로잡기 |
|---|---|
| env는 image 안에 넣으면 편하다 | 환경별 설정은 runtime에 주입하는 것이 기본이다 |
| logs만 보면 전부 알 수 있다 | inspect/exec/stats와 함께 봐야 한다 |
| host에서 container name으로 항상 접속할 수 있다 | container name DNS는 Docker network 내부 기준이다 |
| `.env`는 secret manager다 | 로컬 편의 파일이며 공개하면 위험하다 |
| volume 삭제는 일반 cleanup이다 | named volume data를 삭제할 수 있다 |
| restart policy가 있으면 장애가 해결된다 | 반복 재시작은 원인 해결이 아니라 증상 완화일 수 있다 |

## Suggested Day 4 Board
수업 중 칠판 또는 공유 문서에 다음 보드를 유지한다.

```text
Run:
  docker run ... -e ... -p ... -v ... --network ...

Check:
  docker ps
  curl / psql / pg_isready

Failure:
  missing env / wrong port / wrong network / stale volume / bad image tag

Inspect:
  docker logs
  docker inspect
  docker exec
  docker stats

Cleanup:
  docker stop / rm
  docker image rm
  docker network rm
  docker volume rm  # data reset
```

보드는 학생이 길을 잃었을 때 돌아올 수 있는 기준점이다.

## Student Submission Template
```markdown
## Week 2 Day 4 Submission
- OS / Docker Desktop or Engine:
- Runtime command:
- Env/config 확인 지점:
- Logs 확인 지점:
- Inspect 확인 지점:
- Exec 확인 지점:
- Stats/restart 확인 지점:
- Network 확인 지점:
- Failure drill:
- cleanup 주의점:
- Compose mapping for Day 5:
- Remaining blocker:
```

## Instructor Review Checklist
- [ ] 학생이 host port와 container port를 구분한다.
- [ ] 학생이 host `localhost`와 Docker network 내부 container name을 구분한다.
- [ ] 학생이 `.env.example`과 실제 `.env`의 차이를 설명한다.
- [ ] 학생이 container/image/network/volume cleanup 차이를 설명한다.
- [ ] 학생이 logs/inspect/exec/stats를 구분해 사용한다.
- [ ] 학생이 정상과 장애를 서로 다른 확인 지점으로 확인한다.
- [ ] 학생이 실패를 blame이 아니라 RCA 학습으로 확인한다.

## Completion Definition
Day 4 완료는 다음 조건을 모두 만족할 때 선언한다.

```text
1. runtime command가 명확하다.
2. env/config 주입 방식과 secret masking 기준이 확인되어 있다.
3. logs/inspect/exec/stats 중 필요한 확인 지점을 선별해 정상/장애를 판단했다.
4. missing env, wrong port, wrong network, stale volume, bad image tag 중 하나의 failure drill이 있다.
5. container/image/network/volume cleanup 명령과 data 삭제 위험이 README에 확인되어 있다.
6. Day 5 Compose로 옮길 option mapping이 있다.
```

이 정의는 Day 5 통합 실습과 Week 2 최종 확인의 기준으로 이어진다.
