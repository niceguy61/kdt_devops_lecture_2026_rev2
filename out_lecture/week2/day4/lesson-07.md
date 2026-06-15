# 7교시: 개인 면담 및 환경 점검

## 수업 목표
- Dockerfile, image build/run, Compose 실행 상태를 개인별로 점검한다.
- Docker Hub pull/tag/login 문제와 로컬 Docker Desktop 문제를 분리한다.
- Day 5 통합 실습 전에 blocker를 evidence 기준으로 정리한다.

## 50분 흐름
| 시간 | 활동 | 비중 | 산출 |
|---|---|---:|---|
| 0-8분 | 점검 기준 안내 | 설명 10% | readiness board |
| 8-20분 | Dockerfile/build/run 확인 | 실행 25% | build evidence |
| 20-32분 | Compose config/up/check 확인 | 실행 30% | compose evidence |
| 32-42분 | Docker Hub와 README 확인 | 실행 20% | handoff note |
| 42-50분 | 개인 blocker 분류 | 상담 15% | recovery task |

### Visual 1: 개인 점검 보드
![Compose readiness board](https://raw.githubusercontent.com/niceguy61/kdt_devops_lecture_2026_rev2/main/week2/day4/assets/lesson-07-compose-readiness-board.png)

이 visual은 개인 점검에서 빠지면 안 되는 evidence를 보여준다. 볼 지점은 "설치됨"이 아니라 실행과 확인 결과다.

## 점검 명령
```bash
docker version
docker compose version
docker images
cd week2/day4/labs/compose-app
docker compose config
docker compose up -d
docker compose ps
curl -I http://localhost:18084
docker compose run --rm db-client
```

## blocker 분류
| blocker | 증상 | 우선 확인 |
|---|---|---|
| Docker Desktop 미실행 | Docker daemon 연결 실패 | Desktop 상태, WSL/가상화 |
| Compose CLI 없음 | `docker compose` 인식 실패 | Docker Desktop 버전 |
| image pull 실패 | network/auth/rate 문제 | `docker pull nginx:1.27-alpine` |
| port 충돌 | bind error, 접속 실패 | `compose ps`, host port 변경 |
| env 누락 | config 실패 | `.env` |
| DB 미준비 | query 실패 | `logs db`, healthcheck |

## 핵심 설명
면담 시간은 새로운 내용을 많이 넣는 시간이 아니라 Day 1부터 Day 4까지의 실행 조건을 개인별로 맞추는 시간이다. 막힌 지점은 "안 됨"이 아니라 설치, 권한, 네트워크, port, env, volume, README 중 어디인지 분류해서 기록한다.

Day 5 통합 실습은 Dockerfile과 Compose를 모두 사용한다. 따라서 Day 4 종료 전에는 최소한 `docker compose config`, `up`, `ps`, HTTP check, DB check 중 어디까지 되는지 명확해야 한다.

## 기록 템플릿
```markdown
## Day 4 Readiness Check
- docker version:
- compose version:
- Dockerfile build/run:
- compose config:
- compose up:
- web check:
- db check:
- Docker Hub status:
- README status:
- blocker:
- next action:
```

## 평가 기준
| 기준 | 2점 evidence |
|---|---|
| 환경 | Docker와 Compose version을 확인했다 |
| 실행 | Compose web/db 실행 evidence가 있다 |
| 회복 | blocker를 분류하고 다음 행동을 정했다 |

### 공식 근거 링크
- Docker Desktop: https://docs.docker.com/desktop/
- Docker Compose: https://docs.docker.com/compose/

## 선행 지식과 범위 경계
이 교시는 새로운 개념을 많이 넣는 시간이 아니라 개인별 실행 환경을 증거 기준으로 정렬하는 시간이다. Day 5 통합 실습에 들어가기 전에 Dockerfile, image, container, Compose, README handoff 중 어디가 막혀 있는지 분류한다.

면담은 감으로 판단하지 않는다. "안 됩니다"라는 말은 출발점일 뿐이고, 최종 기록은 명령, 출력, 상태, 다음 조치로 남긴다.

## 학술 기준 연결
형성평가(formative assessment)는 최종 점수보다 현재 위치와 다음 수정 행동을 알려주는 평가다. Lesson 7은 형성평가 세션이다.

| 평가 관점 | 적용 |
|---|---|
| observable outcome | version, config, HTTP, DB query로 상태 확인 |
| descriptive feedback | 막힌 지점을 구체적으로 분류 |
| revision action | 다음 실습 전 수행할 한 가지 조치 결정 |
| self-assessment | 학생이 자기 blocker를 직접 기록 |

## 개인 점검의 원칙
개인 점검은 모든 학생에게 같은 속도를 요구하지 않는다. 대신 최소 evidence 기준을 맞춘다.

| 단계 | 최소 evidence |
|---|---|
| Docker 준비 | `docker version` server 응답 |
| Compose 준비 | `docker compose version` |
| 이미지 실행 | nginx 또는 표준 앱 run evidence |
| Compose config | `docker compose config` 성공 |
| Web 확인 | HTTP 200 또는 명확한 실패 로그 |
| DB 확인 | healthy, `pg_isready`, query 중 하나 |
| README | run/check/cleanup 초안 |

## blocker interview 질문
면담에서는 다음 질문을 짧게 묻고 evidence를 확인한다.

1. 마지막으로 성공한 명령은 무엇인가?
2. 처음 실패한 명령은 무엇인가?
3. 실패 출력의 핵심 한 줄은 무엇인가?
4. Docker Desktop 또는 daemon은 실행 중인가?
5. 같은 port를 쓰는 container가 있는가?
6. `.env` 파일 또는 required variable은 준비되어 있는가?
7. cleanup을 해도 되는 실습 data인가?

이 질문은 학생을 추궁하기 위한 것이 아니라 failure domain을 좁히기 위한 것이다.

## 실무 triage table
| 증상 | 가능 원인 | 다음 행동 |
|---|---|---|
| Cannot connect to Docker daemon | Desktop 미실행, 권한 문제 | Docker Desktop 상태 확인 |
| `docker compose` 없음 | 오래된 Docker 설치 | Docker Desktop/CLI version 확인 |
| config variable error | `.env` 누락 | `.env.example` 복사 |
| port bind error | host port 충돌 | `WEB_PORT` 변경 |
| DB unhealthy | env/init/data 문제 | `logs db` 확인 |
| HTTP 200 but wrong page | mount 경로 또는 cache | body marker 확인 |

## 전문 커뮤니케이션 기준
현업에서 좋은 blocker report는 다음 형식에 가깝다.

```markdown
## Blocker Report
- Environment: Windows 11 + WSL2 / macOS / Linux
- Last success:
- First failure:
- Command:
- Output excerpt:
- Suspected category:
- Tried:
- Need:
```

나쁜 report는 "안 돼요" 한 문장이다. 좋은 report는 다음 사람이 같은 실패를 재현하거나 다음 확인을 바로 할 수 있게 한다.

## 위험과 권한 주의
개인 환경 점검 중 다음 행동은 주의한다.

| 행동 | 위험 | 기준 |
|---|---|---|
| Docker Desktop 재설치 | 시간 소모, 설정 변화 | version/daemon 확인 후 결정 |
| volume 전체 삭제 | data 손실 | 실습 volume인지 확인 |
| 관리자 권한 실행 | 권한 습관 악화 | 필요한 경우에만 이유 기록 |
| secret 공유 | credential 노출 | 화면 공유/README에서 masking |

## 오해 점검 문항
| 문항 | 기대 답 |
|---|---|
| `docker version` client만 나오면 충분한가 | server 응답도 필요하다 |
| port 충돌이면 container port를 바꾸는가 | 보통 host port를 바꾼다 |
| 친구 PC에서 되는 compose.yaml이면 내 PC도 항상 되는가 | port, arch, Docker 상태, env가 다를 수 있다 |
| blocker 기록은 평가 감점용인가 | 아니다. 회복 경로를 찾기 위한 evidence다 |

## 점검 결과 분류
| 상태 | 의미 | 다음 행동 |
|---|---|---|
| Green | config/up/check 모두 성공 | README 보완 |
| Yellow | web 또는 DB 중 하나 실패 | failure drill/RCA 작성 |
| Red | Docker daemon 또는 Compose 실행 불가 | 환경 복구 우선 |
| Gray | 결과 미확인 | 명령 재실행과 evidence 확보 |

## 전이 과제
수업 종료 전 개인별로 한 줄을 작성한다.

```text
Day 5 통합 실습 전 내가 해결해야 할 가장 작은 blocker는 ____이고, 확인 명령은 ____이다.
```

이 문장을 기준으로 Day 5 시작 시 빠르게 readiness를 확인한다.

## 강사-학생 피드백 계약
피드백은 인상 평가가 아니라 다음 행동을 정하는 정보여야 한다. 따라서 면담 후에는 다음 세 가지 중 하나로 끝낸다.

| 피드백 유형 | 예 |
|---|---|
| 유지 | `config`와 web check는 통과했으니 README를 보강한다 |
| 수정 | DB query가 실패했으니 `logs db`와 `.env`를 확인한다 |
| 축소 | 개인 프로젝트 적용은 보류하고 표준 실습 앱 evidence를 먼저 완성한다 |

이 방식은 학생이 실패를 개인 능력 문제로 받아들이지 않고, 시스템 상태와 다음 실험으로 다루게 돕는다.

## Day 5 입장 기준
Day 5 통합 실습에 들어가기 전 최소 입장 기준은 다음이다.

| 기준 | 통과 조건 |
|---|---|
| Docker | daemon 응답 확인 |
| Dockerfile | build 또는 run evidence 1개 |
| Compose | config 성공 |
| Web | HTTP 200 또는 명확한 failure note |
| DB | healthy/query 또는 명확한 failure note |
| Handoff | README에 다음 action 기록 |

모든 항목이 완벽할 필요는 없다. 다만 실패한 항목도 evidence와 next action이 있어야 한다.
