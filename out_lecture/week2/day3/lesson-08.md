# 8교시: README handoff와 cleanup audit

## 수업 목표
- Day 3 실행 조건을 README handoff 형식으로 정리한다.
- container, network, volume cleanup 기준을 명확히 기록한다.
- Day 4 Compose로 이동할 옵션 mapping을 만든다.

## 50분 흐름
| 시간 | 활동 | 비중 | 산출 |
|---|---|---:|---|
| 0-8분 | Day 3 evidence 모으기 | 실행 15% | evidence list |
| 8-20분 | README runtime section 작성 | 실행 25% | README draft |
| 20-32분 | cleanup audit 실행 | 실행 25% | cleanup evidence |
| 32-42분 | Compose mapping 작성 | 설명 20% | option map |
| 42-50분 | 최종 점검 | 실행 15% | handoff checklist |

### Visual 1: Runtime handoff checklist
![Runtime handoff checklist](https://raw.githubusercontent.com/niceguy61/kdt_devops_lecture_2026_rev2/main/week2/day3/assets/lesson-08-runtime-handoff-cleanup.png)

Day 3의 긴 `docker run` 옵션은 Day 4에서 Compose file로 옮겨진다. README는 그 전 단계의 handoff 문서다.

## 핵심 설명
실행됐다는 말은 handoff가 아니다. 다른 사람이 같은 결과를 재현하려면 image, container name, port, env, volume, network, check, cleanup이 모두 필요하다.

Day 3 README는 명령어 모음이 아니라 실행 계약이다. 어떤 조건으로 실행해야 하고, 어떤 결과가 정상이며, 실패했을 때 어디를 볼지 기록한다.

cleanup도 handoff의 일부다. container만 지우면 volume과 network가 남을 수 있다. volume을 지우면 데이터가 사라질 수 있다. 무엇을 남기고 무엇을 지울지 기준을 적는다.

## README runtime section 예시
README에 넣을 내용은 아래처럼 run과 check를 분리한다.

Web run:

```bash
docker run -d \
  --name paperclip-day3-web \
  -p 18083:80 \
  -v "$PWD/week2/day3/labs/runtime-site/html:/usr/share/nginx/html:ro" \
  nginx:1.27-alpine
```

Web check:

```bash
curl -I http://localhost:18083
curl -s http://localhost:18083 | grep runtime-site-v1
```

DB run:

```bash
docker network create paperclip-day3-net
docker volume create paperclip-day3-pgdata
docker run -d \
  --name paperclip-day3-postgres \
  --network paperclip-day3-net \
  -e POSTGRES_PASSWORD=<practice-password> \
  -e POSTGRES_DB=paperclip \
  -v paperclip-day3-pgdata:/var/lib/postgresql/data \
  postgres:16-alpine
```

DB check:

```bash
docker exec paperclip-day3-postgres pg_isready -U postgres
docker exec paperclip-day3-postgres psql -U postgres -d paperclip -c "select current_database();"
```

## cleanup runbook
```bash
docker rm -f paperclip-day3-web paperclip-day3-postgres
docker volume rm paperclip-day3-pgdata
docker network rm paperclip-day3-net
```

주의:
- volume 삭제는 data 삭제다.
- 실습 cleanup에서는 삭제하지만 운영 DB volume에는 그대로 적용하지 않는다.
- network 삭제가 실패하면 연결된 container가 남아 있는지 확인한다.

## Linux 사전 테스트 cleanup 기준
정상 cleanup 후 다음 명령에서 Day 3 object가 없어야 한다.

```bash
docker ps --filter name=paperclip-day3
docker volume ls --filter name=paperclip-day3
docker network ls --filter name=paperclip-day3
```

## Compose mapping
| `docker run` 옵션 | Compose 위치 |
|---|---|
| `--name` | `container_name` 또는 service name |
| `-p 18083:80` | `ports` |
| `-e KEY=value` | `environment` |
| `-v source:dest:ro` | `volumes` |
| `--network` | `networks` |
| image name | `image` |
| command | `command` |

## 핵심 유의사항
README에 secret value를 그대로 쓰지 않는다. 실습 password도 public repository에 올리는 습관을 만들면 안 된다. 값이 필요한 경우 `<practice-password>`처럼 placeholder로 두고, 실제 값은 로컬 환경이나 안전한 전달 방식으로 주입한다.

cleanup 명령은 위험도를 구분한다. `docker rm -f`는 container 삭제이고, `docker volume rm`은 data 삭제일 수 있다. 같은 cleanup block 안에 있더라도 의미가 다르다.

README에는 정상 결과도 적어야 한다. 명령만 있으면 실행 후 무엇을 확인해야 하는지 알 수 없다. `HTTP/1.1 200 OK`, `accepting connections`, `current_database = paperclip` 같은 정상 기준을 함께 둔다.

## 자주 놓치는 지점
| 놓치는 지점 | 결과 | 보완 |
|---|---|---|
| run 명령만 기록 | 정상 확인 불가 | check 명령 추가 |
| cleanup 누락 | 다음 실습 충돌 | cleanup audit 추가 |
| secret 값 노출 | repository credential risk | placeholder 사용 |
| volume 의미 누락 | 데이터 삭제 사고 | volume warning 추가 |
| Compose 연결 누락 | Day 4 전환 어려움 | option mapping 작성 |

## Day 3 최종 evidence 표
| 항목 | 정상 기준 |
|---|---|
| Web port | `18083->80/tcp` |
| Web HTTP | `HTTP/1.1 200 OK` |
| Web body | `runtime-site-v1` |
| Env | `APP_ENV=practice` 등 5개 값 |
| Network | `paperclip-day3-net` |
| DB readiness | `accepting connections` |
| SQL | `paperclip` |
| Volume | `paperclip-day3-pgdata` |
| Failure | missing `POSTGRES_PASSWORD` error |
| Cleanup | Day 3 objects 없음 |

## 기록 템플릿
```markdown
## Day 3 Handoff
- Web run:
- Web check:
- DB network:
- DB volume:
- DB run:
- DB check:
- Env variables:
- Failure drill:
- Cleanup:
- Compose mapping:
```

## 마무리 점검
```text
Day 3의 `-p`는 Compose의 ____로 이동한다.
Day 3의 `-e`는 Compose의 ____로 이동한다.
Day 3의 `-v`는 Compose의 ____로 이동한다.
volume cleanup은 ____ 삭제일 수 있으므로 주의한다.
```

## 평가 기준
| 기준 | 2점 evidence |
|---|---|
| README | run/check/cleanup을 모두 기록했다 |
| 보안 | secret value를 직접 공개하지 않았다 |
| cleanup | container/network/volume audit을 수행했다 |
| 연결 | Docker run 옵션을 Compose 항목으로 mapping했다 |

### 공식 근거 링크
- Docker Compose overview: https://docs.docker.com/compose/
- Compose services reference: https://docs.docker.com/reference/compose-file/services/
- Docker volumes: https://docs.docker.com/engine/storage/volumes/
