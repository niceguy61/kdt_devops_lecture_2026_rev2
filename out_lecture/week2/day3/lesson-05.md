# 5교시: named volume과 데이터 보존

## 수업 목표
- named volume이 Docker-managed persistent storage임을 설명한다.
- container lifecycle과 data lifecycle을 분리한다.
- PostgreSQL data directory를 named volume으로 보존하는 구조를 확인한다.

## 50분 흐름
| 시간 | 활동 | 비중 | 산출 |
|---|---|---:|---|
| 0-8분 | bind mount 복습 | 설명 15% | storage 비교 |
| 8-18분 | named volume 개념 | 설명 20% | volume note |
| 18-32분 | volume 생성과 DB mount | 실행 30% | volume evidence |
| 32-42분 | inspect로 mount 확인 | 실행 20% | mount JSON |
| 42-50분 | stale volume 위험 정리 | 설명 15% | cleanup note |

### Visual 1: Named volume storage lifecycle
![Named volume storage lifecycle](https://raw.githubusercontent.com/niceguy61/kdt_devops_lecture_2026_rev2/main/week2/day3/assets/lesson-05-named-volume-lifecycle.png)

이 교시에서는 runtime config와 함께 persistent storage를 연결한다. named volume은 container 삭제 후에도 남을 수 있는 별도 storage object다.

## 핵심 설명
container를 삭제하면 container writable layer는 사라진다. 하지만 named volume은 container와 별도로 남을 수 있다. 그래서 DB container를 지웠는데도 데이터가 남거나, 반대로 volume을 지워서 데이터가 사라지는 일이 생긴다.

named volume은 Docker가 관리한다. host path를 직접 지정하지 않고 volume name을 사용한다. PostgreSQL official image는 data directory로 `/var/lib/postgresql/data`를 사용하므로 이 path에 volume을 mount한다.

## 실행 명령
```bash
docker volume create paperclip-day3-pgdata

docker run -d \
  --name paperclip-day3-postgres \
  -e POSTGRES_PASSWORD=paperclip \
  -e POSTGRES_DB=paperclip \
  -v paperclip-day3-pgdata:/var/lib/postgresql/data \
  postgres:16-alpine

docker inspect paperclip-day3-postgres --format '{{json .Mounts}}'
docker volume inspect paperclip-day3-pgdata
```

## Linux 사전 테스트 결과
```text
"Type":"volume"
"Name":"paperclip-day3-pgdata"
"Destination":"/var/lib/postgresql/data"
"RW":true
```

## bind mount와 named volume 비교
| 구분 | bind mount | named volume |
|---|---|---|
| 소유 | host path 직접 지정 | Docker가 관리 |
| 이름 | path 중심 | volume name 중심 |
| 개발 편의 | host file 즉시 수정에 좋음 | DB data 보존에 좋음 |
| portability | host path 의존 큼 | Docker volume name으로 관리 |
| cleanup | host file은 직접 관리 | `docker volume rm` 필요 |

## 핵심 유의사항
volume은 container 삭제 후에도 남을 수 있다. 실습이 끝났는데 disk 사용량이 계속 늘어나는 이유가 volume일 수 있다.

DB image는 초기화 여부를 volume 내용으로 판단한다. 이미 초기화된 volume을 다시 붙이면 `POSTGRES_DB` 같은 초기화 환경변수가 기대처럼 다시 적용되지 않을 수 있다. 이것이 stale volume 문제다.

운영에서는 volume 삭제가 위험한 작업이다. 실습에서는 cleanup을 위해 삭제하지만 실제 DB volume을 지우면 데이터가 사라진다. `docker volume rm` 전에는 어떤 volume인지 확인한다.

## 자주 놓치는 지점
| 놓치는 지점 | 증상 | 확인 |
|---|---|---|
| container 삭제 후 데이터도 사라진다고 생각 | 데이터가 남아 있음 | `docker volume ls` |
| volume 삭제 위험을 가볍게 봄 | DB 데이터 손실 | volume name 확인 |
| stale volume | env 변경이 반영 안 됨 | 새 volume 사용 |
| destination path 오타 | DB 초기화 위치 불일치 | official image docs |
| bind/volume 혼동 | Source 해석 오류 | `.Mounts.Type` |

## volume evidence 명령
```bash
docker volume ls --filter name=paperclip-day3
docker volume inspect paperclip-day3-pgdata
docker inspect paperclip-day3-postgres --format '{{json .Mounts}}'
```

확인 항목:
- volume name
- mount destination
- read/write 여부
- container와 volume의 lifecycle 차이

## stale volume drill
DB container를 지우고 같은 volume으로 다시 실행하면 data directory는 유지된다.

```bash
docker rm -f paperclip-day3-postgres
docker run -d \
  --name paperclip-day3-postgres \
  -e POSTGRES_PASSWORD=paperclip \
  -e POSTGRES_DB=paperclip \
  -v paperclip-day3-pgdata:/var/lib/postgresql/data \
  postgres:16-alpine
```

확인할 것:
- volume이 남아 있으면 DB는 기존 data directory를 사용한다.
- 새 DB 초기화를 기대한다면 새 volume name을 쓰거나 기존 volume을 삭제해야 한다.
- volume 삭제는 데이터 삭제이므로 실습/운영 구분이 필요하다.

## 운영 관점
DB data는 image에 넣지 않는다. image는 실행 환경이고, DB data는 runtime storage다. 이 둘을 분리해야 image를 재배포해도 데이터 lifecycle을 별도로 관리할 수 있다.

## 확장 실습: volume 존재 여부 확인
container를 삭제한 뒤 volume이 남아 있는지 확인한다.

```bash
docker rm -f paperclip-day3-postgres
docker volume ls --filter name=paperclip-day3-pgdata
docker volume inspect paperclip-day3-pgdata
```

해석:
- container가 없어도 volume은 남을 수 있다.
- volume inspect가 성공하면 data lifecycle은 아직 끝나지 않았다.
- 새 DB 초기화를 원하면 새 volume name을 쓰거나 volume을 삭제한다.

## cleanup 의사결정
| 상황 | volume 삭제 여부 |
|---|---|
| 실습을 완전히 끝냄 | 삭제 가능 |
| DB data를 다음 실습에서 재사용 | 삭제하지 않음 |
| env 변경을 새 초기화로 확인 | 새 volume 사용 또는 삭제 |
| 운영 DB | 임의 삭제 금지 |
| disk 사용량 조사 | `docker system df`, volume inspect |

## disk 사용량 관점
volume은 container 목록에 보이지 않기 때문에 놓치기 쉽다. container가 모두 정리됐는데 disk가 줄지 않으면 image, build cache, volume을 따로 확인한다.

```bash
docker system df
docker volume ls
```

이 명령은 삭제 명령이 아니라 관찰 명령이다. 삭제는 어떤 object인지 확인한 뒤 수행한다.

## 기록 템플릿
```markdown
## Lesson 5 Volume Evidence
- volume name:
- container:
- destination:
- mount type:
- RW:
- container 삭제 후 volume 존재 여부:
- stale volume 가능성:
- cleanup 명령:
```

## 마무리 점검
```text
named volume은 container를 삭제해도 ____ 수 있다.
PostgreSQL data directory는 ____이다.
stale volume은 ____가 기대처럼 다시 적용되지 않을 때 의심한다.
```

## cleanup
```bash
docker rm -f paperclip-day3-postgres
docker volume rm paperclip-day3-pgdata
```

## 평가 기준
| 기준 | 2점 evidence |
|---|---|
| volume | named volume을 생성했다 |
| mount | destination과 RW를 확인했다 |
| lifecycle | container와 data lifecycle을 구분했다 |
| 위험 | volume 삭제 위험을 설명했다 |

### 공식 근거 링크
- Docker volumes: https://docs.docker.com/engine/storage/volumes/
- PostgreSQL Docker Official Image: https://hub.docker.com/_/postgres
