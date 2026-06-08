# 3교시: environment variable과 runtime config

## 수업 목표
- environment variable이 image build 결과가 아니라 runtime config임을 설명한다.
- `docker run -e`로 설정을 주입하고 container 안에서 값을 확인한다.
- 실습용 설정과 secret 관리 위험을 구분한다.

## 50분 흐름
| 시간 | 활동 | 비중 | 산출 |
|---|---|---:|---|
| 0-8분 | Dockerfile config와 runtime config 비교 | 설명 15% | 비교표 |
| 8-18분 | `-e` 옵션 설명 | 설명 20% | env note |
| 18-32분 | env-report 실습 | 실행 30% | env output |
| 32-42분 | DB env 연결 | 실행 20% | `POSTGRES_PASSWORD` note |
| 42-50분 | secret 유의사항과 README 기록 | 설명 15% | handoff 문장 |

### Visual 1: Runtime environment variables
![Runtime environment variables](https://raw.githubusercontent.com/niceguy61/kdt_devops_lecture_2026_rev2/main/week2/day3/assets/lesson-03-runtime-env-vars.png)

이 이미지는 image artifact와 runtime environment variable을 분리해서 보여준다. 같은 image라도 실행할 때 주입한 환경변수에 따라 설정이 달라질 수 있다.

## 핵심 설명
Dockerfile에 값을 굳히면 image를 다시 build해야 바꿀 수 있다. environment variable은 container 실행 시점에 주입되므로 같은 image를 여러 환경에서 다르게 실행할 수 있다.

예를 들어 `APP_ENV=practice`, `DB_HOST=postgres`는 image 파일 자체가 아니라 실행 조건이다. Day 4 Compose에서는 이 값들이 `environment:` 항목으로 이동한다.

환경변수는 설정 분리에 유용하지만 secret을 안전하게 보관하는 만능 도구는 아니다. `docker inspect`, shell history, logs, README에 값이 남을 수 있다. 실습에서는 값을 보여주기 위해 사용하지만 운영에서는 secret manager, 파일 권한, 접근 통제까지 함께 고려한다.

## 실행 명령
```bash
cd week2/day3/labs/env-report

docker run --rm \
  -e APP_ENV=practice \
  -e APP_PORT=8080 \
  -e FEATURE_FLAG=on \
  -e DB_HOST=postgres \
  -e DB_PORT=5432 \
  -v "$PWD/report.sh:/workspace/report.sh:ro" \
  alpine:3.20 sh /workspace/report.sh
```

## Linux 사전 테스트 결과
```text
APP_ENV=practice
APP_PORT=8080
FEATURE_FLAG=on
DB_HOST=postgres
DB_PORT=5432
```

## env 읽는 법
| 변수 | 의미 | 운영 질문 |
|---|---|---|
| `APP_ENV` | 실행 환경 이름 | dev/stage/prod를 구분하는가 |
| `APP_PORT` | 앱이 사용할 port 설정 | 실제 listen port와 일치하는가 |
| `FEATURE_FLAG` | 기능 on/off | 배포 없이 기능을 제어하는가 |
| `DB_HOST` | DB 접근 hostname | Docker network name과 맞는가 |
| `DB_PORT` | DB 접근 port | internal port와 host publish port를 혼동하지 않는가 |

## 핵심 유의사항
environment variable 이름은 문서화해야 한다. 값 자체가 secret이면 공개 README에 쓰지 않고, 어떤 이름이 필요하고 어디서 주입해야 하는지만 적는다.

`-e KEY=value`는 container 실행 시점의 값이다. 이미 실행 중인 container의 environment를 바꾸고 싶다면 일반적으로 container를 새로 실행해야 한다. 실행 중 container 안에서 export를 해도 container 재생성에는 남지 않는다.

`--rm`은 container 종료 후 자동 제거를 뜻한다. env-report처럼 결과만 출력하고 끝나는 실습에는 적합하지만, logs나 inspect evidence를 나중에 봐야 하는 실습에서는 `--rm`을 쓰지 않는 편이 낫다.

## 자주 놓치는 지점
| 놓치는 지점 | 증상 | 확인 |
|---|---|---|
| `-e KEY value`처럼 잘못 입력 | 값이 비어 있거나 command로 해석 | `-e KEY=value` |
| env를 image 설정으로 착각 | rebuild가 필요하다고 생각 | run command 확인 |
| secret을 README에 기록 | credential 노출 | 변수 이름만 기록 |
| container 재사용 기대 | 새 값이 반영 안 됨 | container 재생성 |
| host env와 container env 혼동 | host에는 값이 있는데 container에는 없음 | `docker exec env` |

## PostgreSQL env 연결
PostgreSQL official image는 초기화되지 않은 DB에 superuser password가 필요하다.

```bash
docker run --name paperclip-day3-postgres-missing-env postgres:16-alpine
```

Linux 사전 테스트 실패:

```text
Error: Database is uninitialized and superuser password is not specified.
You must specify POSTGRES_PASSWORD to a non-empty value for the superuser.
```

이 실패는 image가 깨진 것이 아니다. runtime configuration이 빠진 것이다. 원인은 Dockerfile이 아니라 `docker run -e POSTGRES_PASSWORD=...` 누락이다.

## 실무에서 챙기면 좋은 것
| 항목 | 기준 |
|---|---|
| 변수 이름 | 대문자 snake case로 통일 |
| 기본값 | 없어도 실행 가능한 값과 반드시 필요한 값을 구분 |
| secret | README에는 값이 아니라 주입 방법만 기록 |
| 로그 | env 값이 통째로 출력되지 않게 주의 |
| 변경 | config 변경 시 container 재생성 필요 여부 기록 |

## 확장 실습: 값 누락과 기본값 비교
`report.sh`는 값이 없으면 `missing`을 출력한다. 일부 변수를 빼고 실행하면 어떤 값이 빠졌는지 바로 확인할 수 있다.

```bash
docker run --rm \
  -e APP_ENV=practice \
  -v "$PWD/report.sh:/workspace/report.sh:ro" \
  alpine:3.20 sh /workspace/report.sh
```

기대 해석:
- `APP_ENV`만 `practice`로 출력된다.
- 나머지 값은 `missing`으로 출력된다.
- 이것은 image 문제가 아니라 runtime config 누락이다.

## 운영 질문
| 질문 | 확인 이유 |
|---|---|
| 이 변수는 필수인가 선택인가 | 누락 시 container가 죽어야 하는지 판단 |
| 값이 secret인가 | README와 logs에 남겨도 되는지 판단 |
| 기본값이 안전한가 | 누락 시 위험한 기본 동작을 피함 |
| 변경 시 재시작이 필요한가 | runtime handoff에 반영 |
| Compose로 옮길 때 이름이 유지되는가 | Day 4 전환 준비 |

## README에 남길 방식
좋은 예시는 값과 책임을 분리한다.

```text
Required env:
- APP_ENV: practice/stage/prod 중 하나
- DB_HOST: Docker network 안의 DB service name
- POSTGRES_PASSWORD: local secret, README에 실제 값 기록 금지
```

나쁜 예시는 실제 secret 값을 그대로 남긴다.

```text
POSTGRES_PASSWORD=paperclip
```

## 기록 템플릿
```markdown
## Lesson 3 Env Evidence
- image:
- command:
- APP_ENV:
- APP_PORT:
- FEATURE_FLAG:
- DB_HOST:
- DB_PORT:
- missing env failure:
- secret으로 취급해야 할 값:
```

## 마무리 점검
```text
environment variable은 image에 굳힌 값이 아니라 ____ config다.
PostgreSQL 초기화에 필요한 env는 ____다.
secret 값은 README에 ____ 않고, 필요한 변수 이름과 주입 방법만 적는다.
```

## 평가 기준
| 기준 | 2점 evidence |
|---|---|
| env 주입 | `-e`로 값을 전달했다 |
| 출력 | container 내부에서 값을 확인했다 |
| 분류 | missing env를 runtime config 문제로 분류했다 |
| 보안 | secret 기록 위험을 설명했다 |

### 공식 근거 링크
- Docker run reference: https://docs.docker.com/reference/cli/docker/container/run/
- PostgreSQL Docker Official Image: https://hub.docker.com/_/postgres
- Twelve-Factor App Config: https://12factor.net/config
