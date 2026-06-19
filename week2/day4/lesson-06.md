# 6교시: Cleanup과 security audit

![Cleanup and security audit infographic](./assets/lesson-07-cleanup-security-audit.png)

## 수업 목표
- container, image, network, volume cleanup의 차이를 구분한다.
- 삭제하면 안 되는 data와 지워도 되는 실습 자원을 나눈다.
- secret/context 흔적이 남았는지 점검한다.

## 개념 설명
cleanup은 `다 지우기`가 아니다. container 삭제는 실행 중인 process와 그 writable layer를 없애는 일이고, image 삭제는 다음 실행 때 다시 pull/build가 필요하게 만드는 일이다. network 삭제는 연결 공간을 없애는 일이고, volume 삭제는 data 삭제일 수 있다.

Day 4 장애 드릴 뒤에는 실패 container와 임시 network가 남는다. 이것을 정리하지 않으면 다음 수업에서 같은 이름 충돌, port 충돌, stale volume 혼동이 생긴다.

환경별 env file도 cleanup 대상이다. `.env.dev`, `.env.staging`, `.env.prod`를 실습 중 만들었다면 실제 secret이 없더라도 로컬 실습 산출물인지 확인하고 정리한다. 반대로 `.env.example`은 공유용 형식 문서이므로 남겨도 된다.

## Audit 명령
```bash
docker ps -a --filter name=paperclip-day4
docker network ls | grep paperclip-day4 || true
docker volume ls | grep paperclip-day4 || true
docker system df
```

Expected:

```text
paperclip-day4-nginx
paperclip-day4-pg-ok
paperclip-day4-net-a
paperclip-day4-net-b
paperclip-day4-pgdata
```

## Cleanup 명령
```bash
docker rm -f paperclip-day4-nginx paperclip-day4-log-env paperclip-day4-env-inspect paperclip-day4-pg-ok paperclip-day4-pg-missing-env paperclip-day4-net-web paperclip-day4-crash paperclip-day4-restart-missing-env paperclip-day4-pg-volume || true
docker network rm paperclip-day4-net-a paperclip-day4-net-b || true
rm -f /mnt/d/paperclip/week2/day4/labs/env-report/.env /mnt/d/paperclip/week2/day4/labs/env-report/.env.dev /mnt/d/paperclip/week2/day4/labs/env-report/.env.staging /mnt/d/paperclip/week2/day4/labs/env-report/.env.prod
```

## 삭제 판단 표
| 대상 | 기본 판단 | 이유 |
|---|---|---|
| 실패 container | 삭제 | 다음 실습 이름 충돌 방지 |
| 임시 network | 삭제 | 실습 전용 연결 공간 |
| `.env` | 삭제 또는 local 보관 | 실제 값 노출 방지 |
| `.env.dev/staging/prod` | 실습 파일이면 삭제 | 환경별 secret 혼동 방지 |
| `.env.example` | 유지 | 공유용 형식 문서 |
| image | 보통 유지 | 다음 실습에서 재사용 가능 |
| named volume | 신중히 판단 | DB data 삭제 가능 |

## 위험한 명령
```bash
docker system prune --volumes
```

이 명령은 사용하지 않는다. volume까지 포함한 prune은 실습 DB data나 다른 프로젝트 data를 삭제할 수 있다.

실습 reset이 필요해 `paperclip-day4-pgdata`를 지우려면 명시적으로 판단한 뒤 실행한다.

```bash
docker volume rm paperclip-day4-pgdata
```

이 명령은 PostgreSQL data를 삭제한다. `stale volume`을 해결할 때는 유용하지만, 보존해야 하는 data라면 실행하면 안 된다.

## 다음 연결
다음 교시는 Day 5 Compose로 옮길 option mapping을 표로 정리한다.
