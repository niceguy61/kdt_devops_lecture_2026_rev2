# 8교시: 보충 실습과 Compose handoff 정리

## 수업 목표
- Compose 실습을 완료하지 못한 학생이 최소 evidence까지 회복한다.
- 개인 프로젝트 또는 표준 실습 앱에 Compose section을 추가한다.
- Day 5 통합 실습으로 넘어갈 README handoff를 완성한다.

## 50분 흐름
| 시간 | 활동 | 비중 | 산출 |
|---|---|---:|---|
| 0-8분 | 현재 상태 분류 | 상담 15% | recovery target |
| 8-25분 | config/up/check 재실행 | 실행 35% | compose evidence |
| 25-38분 | README handoff 작성 | 실행 25% | README section |
| 38-45분 | cleanup audit | 실행 15% | cleanup evidence |
| 45-50분 | Day 5 연결 | 설명 10% | integration checklist |

### Visual 1: Compose recovery flow
![Compose recovery flow](https://raw.githubusercontent.com/niceguy61/kdt_devops_lecture_2026_rev2/main/week2/day4/assets/lesson-08-compose-recovery.png)

이 visual은 보충 실습의 최소 회복 순서를 보여준다. 볼 지점은 config, up, check, 기록을 분리하는 것이다.

## 최소 회복 명령
```bash
cd week2/day4/labs/compose-app
cp .env.example .env
docker compose config
docker compose up -d
docker compose ps
curl -I http://localhost:18084
curl -s http://localhost:18084 | grep compose-site-v1
docker compose run --rm db-client
```

## README handoff 예시
````markdown
## Compose Run
```bash
cp .env.example .env
docker compose config
docker compose up -d
```

## Compose Check
```bash
docker compose ps
curl -I http://localhost:18084
docker compose run --rm db-client
```

## Compose Cleanup
```bash
docker compose down
```

DB data까지 초기화해야 하는 실습 상황에서만 사용:

```bash
docker compose down -v
```
````

## 핵심 설명
보충 실습의 목표는 모든 변형을 다 해보는 것이 아니라 Day 5 통합 실습을 시작할 수 있는 최소 실행 계약을 만드는 것이다. `compose.yaml`이 있고, config가 통과하고, web과 db를 확인하고, cleanup 기준을 알고 있으면 다음 단계로 갈 수 있다.

README에는 정상 경로와 위험 경로를 구분한다. `down`은 일반 정리이고, `down -v`는 data 삭제가 포함된 초기화다. 두 명령을 같은 의미처럼 적으면 handoff 위험이 생긴다.

## 최종 evidence 표
| 항목 | 정상 기준 |
|---|---|
| Config | `docker compose config` 성공 |
| Web status | `docker compose ps`에서 running |
| DB status | running 또는 healthy |
| HTTP | `HTTP/1.1 200 OK` |
| Body | `compose-site-v1` |
| DB query | `paperclip` database/user |
| Failure | missing env 또는 wrong port RCA |
| Cleanup | `down`과 `down -v` 차이 기록 |

## 기록 템플릿
```markdown
## Day 4 Handoff
- Compose file:
- Required env:
- Run:
- Check:
- Failure drill:
- Cleanup:
- Data deletion warning:
- Day 5 remaining work:
```

## 평가 기준
| 기준 | 2점 evidence |
|---|---|
| 회복 | 최소 Compose 실행 흐름을 완료했다 |
| 문서화 | run/check/cleanup이 README에 있다 |
| 안전 | volume 삭제 위험을 명시했다 |

### 공식 근거 링크
- Docker Compose: https://docs.docker.com/compose/
- Networking in Compose: https://docs.docker.com/compose/how-tos/networking/

## 선행 지식과 범위 경계
이 교시는 보충 실습 시간이지만, 단순히 못 끝낸 명령을 따라 치는 시간이 아니다. 목표는 Day 5 통합 실습으로 넘어갈 수 있는 최소 실행 계약을 완성하는 것이다.

완벽한 Compose file보다 중요한 것은 `config -> up -> check -> handoff -> cleanup` 흐름을 자기 손으로 한 번 닫는 것이다.

## 학술 기준 연결
이 교시는 revision action 중심의 formative feedback이다. 학습자는 실패한 지점에서 다시 시도하고, 결과를 증거로 기록하고, 다음 행동을 수정한다.

| 학습 요소 | 적용 |
|---|---|
| reflection | 왜 실패했는지 짧게 기록 |
| revision | config/env/port/volume 중 하나 수정 |
| transfer | 개인 프로젝트 README에 적용 |
| communication | run/check/cleanup을 다른 사람이 읽게 작성 |

## 최소 완료 기준
보충 실습의 최소 완료 기준은 다음 6개다.

| 기준 | 명령 또는 산출물 |
|---|---|
| 파일 존재 | `compose.yaml` |
| 실행 전 검증 | `docker compose config` |
| project 실행 | `docker compose up -d` |
| web 확인 | `curl -I`와 body marker |
| DB 확인 | `db-client` 또는 `pg_isready` |
| cleanup | `down`과 `down -v` 차이 기록 |

이 중 하나라도 없으면 Day 5 발표에서 "Compose로 실행 가능"이라고 말하기 어렵다.

## README handoff 보강판
README에는 명령만 넣지 말고 기대 결과도 넣는다.

````markdown
## Compose Setup
```bash
cp .env.example .env
```

`.env`의 password는 로컬 실습용 값으로 바꾼다. 실제 secret은 commit하지 않는다.

## Compose Run
```bash
docker compose config
docker compose up -d
```

Expected:
```text
web service: running
db service: running or healthy
```

## Compose Check
```bash
docker compose ps
curl -I http://localhost:18084
curl -s http://localhost:18084 | grep compose-site-v1
docker compose run --rm db-client
```

Expected:
```text
HTTP/1.1 200 OK
compose-site-v1
current_database = paperclip
```

## Compose Cleanup
```bash
docker compose down
```

DB data까지 초기화하는 실습 reset:
```bash
docker compose down -v
```

주의: `down -v`는 named volume data를 삭제한다.
````

## 실무 handoff quality
| 품질 | README 모습 |
|---|---|
| 낮음 | "docker compose up 하면 됨" |
| 보통 | run 명령과 cleanup 명령이 있음 |
| 높음 | setup, run, check, expected result, failure, cleanup warning이 있음 |

높은 품질의 handoff는 다음 사람이 질문 없이 실행할 수 있게 만든다. 이것이 Week 2의 핵심 산출물이다.

## 보충 실습 경로별 처방
| 현재 상태 | 우선 작업 |
|---|---|
| config 실패 | YAML indentation과 `.env` 확인 |
| up 실패 | image, port, daemon 상태 확인 |
| web 실패 | `ports`, bind mount, body marker 확인 |
| DB 실패 | env, logs, healthcheck, volume 확인 |
| cleanup 불안 | `down`과 `down -v` 차이 설명 후 실행 |
| README 미완성 | 명령보다 expected result부터 보강 |

## RCA 압축 양식
보충 시간에는 긴 RCA를 다 쓰기 어려울 수 있다. 최소 양식은 다음으로 줄인다.

```markdown
## Short RCA
- Failed command:
- Error line:
- Category: config / port / env / volume / network / readiness
- Fix:
- Recheck:
- Prevention:
```

## 오해 점검 문항
| 문항 | 기대 답 |
|---|---|
| 보충 실습은 모든 내용을 다시 듣는 시간인가 | 아니다. 최소 evidence 회복 시간이다 |
| README에는 성공 명령만 쓰면 되는가 | 아니다. check와 expected result가 필요하다 |
| `down -v`를 항상 cleanup으로 쓰는가 | 아니다. data 삭제가 필요할 때만 쓴다 |
| Day 5 전까지 꼭 완벽한 개인 앱이 필요한가 | 아니다. 표준 실습 앱 기준 evidence가 먼저다 |

## Day 5 연결
Day 5에서는 Week 2 전체를 통합한다. Dockerfile은 image build 기준이고, Compose는 multi-container runtime 기준이다. 발표에서는 다음 문장을 evidence로 뒷받침해야 한다.

```text
이 앱은 Dockerfile로 image를 만들 수 있고, Compose로 web과 dependency를 함께 실행할 수 있으며, README만 보고 다른 사람이 확인하고 정리할 수 있다.
```

이 문장을 말하려면 build log, compose ps, HTTP status, DB query, cleanup note가 필요하다.

## 자기 평가 체크
학생은 수업 종료 전 다음을 0/1/2로 표시한다.

| 항목 | 0 | 1 | 2 |
|---|---|---|---|
| config | 실행 못함 | 실행했지만 해석 못함 | 출력 구조 설명 가능 |
| up | 실패 | 일부 service만 실행 | web/db 실행 |
| check | 없음 | ps만 있음 | HTTP와 DB evidence 있음 |
| RCA | 없음 | 증상만 있음 | 원인 후보와 recheck 있음 |
| README | 없음 | 명령만 있음 | expected result와 cleanup warning 있음 |

## 전이 과제
개인 프로젝트 또는 표준 실습 앱 README에 다음 section을 실제로 추가한다.

```markdown
## Docker Compose
- Purpose:
- Required files:
- Required environment:
- Run:
- Check:
- Failure drill:
- Cleanup:
- Data warning:
```

이 과제는 Week 2 최종 산출물의 직접 일부가 된다.
