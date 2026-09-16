# Week 3 Day1: MSA 토폴로지와 첫 실행

## Overview
Day 1은 Week 2 Compose 경험을 MSA 운영 토폴로지로 확장한다. 표준 `msa-demo` 앱을 기준으로 frontend, api, worker, db의 역할과 요청 흐름을 읽고 실제로 실행한다.

## Learning Goals
- Monolith와 MSA를 배포 단위, 장애 영향 범위, 네트워크 의존성 관점으로 비교한다.
- frontend/api/worker/db의 역할, port, env, health, log 위치를 설명한다.
- `docker compose config/up/ps/logs/curl`로 정상 상태를 증거로 확인한다.
- API URL 오류, DB host 오류, env 누락 같은 연결 실패의 첫 확인 지점을 말한다.
- 8교시에 구름 EXP 배움일기로 MSA 토폴로지와 연결 실패 증거를 정리한다.

## Lesson Index
| 교시 | 주제 | 핵심 확인 |
|---|---|---|
| 1교시 | Week2 10분 요약 + MSA를 운영 토폴로지로 보기 | 단일 컨테이너에서 여러 서비스로 확장되는 흐름 |
| 2교시 | Monolith vs MSA | 배포 단위, 장애 영향 범위, 네트워크 의존성, 운영 복잡도 비교 |
| 3교시 | 인프라 엔지니어가 MSA에서 알아야 할 것 | 서비스 목록, 포트, 프로토콜, 의존성, 설정, health, 로그 위치 |
| 4교시 | 표준 MSA 실습 앱 토폴로지 | frontend, api, worker, database 역할과 요청 흐름 |
| 5교시 | Compose로 전체 서비스 실행 | 실행 전 성공 기준, `ps`/health/HTTP/log baseline, cleanup |
| 6교시 | 서비스 간 통신 확인 | frontend -> api, api -> db, worker -> api 흐름을 로그와 상태로 추적 |
| 7교시 | 장애 시나리오 1 | API URL 오류, DB host 오류, 환경변수 누락을 logs/inspect/exec로 분리 |
| 8교시 | 구름 EXP 배움일기 | MSA 토폴로지, 서비스별 실행 조건, 연결 실패에서 먼저 볼 증거 |

## Practice Files
| 자료 | 용도 |
|---|---|
| `hands-on-lab.md` | 당일 실습 명령과 확인 순서 |
| `academic-foundations.md` | 공식/현업 기준 mapping |
| `assets/` | 보조 시각 자료 |
| `labs/` | 실행 가능한 실습 파일 |

## Evidence Policy
| Evidence | 제출 기준 |
|---|---|
| command evidence | 명령과 핵심 출력 요약 |
| failure note | 증상, 첫 확인 명령, 원인 후보, 복구 기준 |
| handoff note | 다음 운영자 또는 다음 주제로 넘길 정보 |
| goorm EXP note | 8교시 배움일기 항목 |

## Official References
| Topic | Reference |
|---|---|
| Microservices on AWS | https://docs.aws.amazon.com/whitepapers/latest/microservices-on-aws/microservices.html |
| Docker Compose services | https://docs.docker.com/reference/compose-file/services/ |
| Twelve-Factor App | https://12factor.net/ |

## End-Of-Day Checklist
- [ ] 오늘의 핵심 흐름을 한 문장으로 설명했다.
- [ ] 명령 실행 결과를 evidence로 남겼다.
- [ ] 실패 로그 또는 이벤트를 하나 이상 읽었다.
- [ ] 다음 교시 또는 Week 4로 넘길 질문을 적었다.

## 학습 제어: 회상·핵심·복구

### 시작 5분 회상
자료를 다시 보지 않고 다음 질문에 답한다.
- MSA에서 서비스 경계와 의존성은 어떻게 다른가?
- 요청 실패가 발생했을 때 첫 번째 증거는 무엇인가?
- `service name`, `port`, `health` 중 무엇이 바뀌면 통신이 깨지는가?

### 오늘 반드시 가져갈 것
1. 서비스 경계는 코드 분할이 아니라 책임·데이터·장애 영향 범위의 경계다.
2. 서비스가 `Running`이어도 의존성·health·timeout을 확인해야 한다.
3. 모든 장애 기록은 증상 → 영향 범위 → 증거 → 가설 → 복구 → 재확인 순서로 남긴다.

### 최소 복구 경로
`docker compose ps` → 관련 서비스 `logs` → health endpoint `curl` → 의존 서비스 이름/port 확인 순서로 최소 한 건의 실패를 다시 분류한다. 다음 날로 넘어가기 전 frontend/api/worker/db의 역할과 호출 방향을 한 줄씩 설명할 수 있어야 한다.