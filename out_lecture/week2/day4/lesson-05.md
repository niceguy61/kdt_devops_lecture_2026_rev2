# 5교시: Stats, resource, restart policy

## 수업 목표
- `docker stats --no-stream`으로 resource 사용량을 확인한다.
- restart policy가 무엇을 해주고 무엇을 해주지 못하는지 설명한다.
- crash loop를 증상 완화와 원인 해결로 구분한다.

## 개념 설명
`docker stats`는 container의 CPU, memory, network, block I/O를 보여준다. Day 4에서는 성능 튜닝을 깊게 하지 않는다. 대신 `실행 중인 container가 resource를 쓰고 있는지`, `비정상적으로 반복 재시작되는지`를 관찰하는 입구로 사용한다.

Restart policy는 container process가 죽었을 때 다시 시작할지 정하는 정책이다. 하지만 설정 누락, 잘못된 command, port 충돌 같은 원인을 고치지는 않는다. 반복 재시작은 장애를 숨길 수도 있으므로 logs와 함께 봐야 한다.

환경 설정이 잘못된 상태에서 restart policy를 붙이면 더 헷갈릴 수 있다. 예를 들어 required env가 없어서 바로 죽는 container에 `--restart on-failure`를 붙이면 container가 반복해서 재시작한다. 이때 해결책은 restart 횟수를 늘리는 것이 아니라 missing env를 고치는 것이다.

## 실습 명령
```bash
docker stats paperclip-day4-nginx --no-stream
docker inspect paperclip-day4-nginx --format 'before={{json .HostConfig.RestartPolicy}}'
docker update --restart unless-stopped paperclip-day4-nginx
docker inspect paperclip-day4-nginx --format 'after={{json .HostConfig.RestartPolicy}}'
```

Expected:

```text
NAME                   CPU %     MEM USAGE / LIMIT
before={"Name":"no","MaximumRetryCount":0}
after={"Name":"unless-stopped","MaximumRetryCount":0}
```

## crash loop 맛보기
```bash
docker rm -f paperclip-day4-crash || true
docker run -d --name paperclip-day4-crash --restart on-failure:3 alpine:3.20 sh -c 'echo crash-now; exit 1'
sleep 3
docker ps -a --filter name=paperclip-day4-crash
docker logs paperclip-day4-crash
docker inspect paperclip-day4-crash --format 'RestartCount={{.RestartCount}} Status={{.State.Status}} ExitCode={{.State.ExitCode}}'
```

Expected:

```text
crash-now
RestartCount=3
ExitCode=1
```

## config 실패와 restart 구분
```bash
docker rm -f paperclip-day4-restart-missing-env || true
docker run -d --name paperclip-day4-restart-missing-env --restart on-failure:2 postgres:16-alpine
sleep 3
docker inspect paperclip-day4-restart-missing-env --format 'RestartCount={{.RestartCount}} Status={{.State.Status}} ExitCode={{.State.ExitCode}}'
docker logs paperclip-day4-restart-missing-env --tail 20 || true
```

Expected:

```text
RestartCount=2
POSTGRES_PASSWORD
```

해석: restart policy는 missing env를 해결하지 못한다. `POSTGRES_PASSWORD`를 주입해야 한다.

## 판단 기준
| 출력 | 해석 |
|---|---|
| `RestartCount` 증가 | process가 반복 실패 |
| `ExitCode=1` | command가 실패 종료 |
| logs에 같은 줄 반복 | restart가 원인을 해결하지 못함 |
| `POSTGRES_PASSWORD` 반복 | config 누락을 restart로 가리고 있음 |

## 다음 연결
다음 교시는 여러 failure를 한 번에 분류하고 복구 기준을 세운다.
