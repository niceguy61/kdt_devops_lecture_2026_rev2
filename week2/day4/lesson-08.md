# 8교시: Prometheus/Grafana observability preview

## 수업 목표
- `docker logs`, `docker stats`가 observability stack으로 어떻게 확장되는지 체험한다.
- Prometheus, Grafana, cAdvisor, Loki의 역할을 구분한다.
- metrics와 logs를 같은 장애 상황에서 서로 다른 증거로 해석한다.

## 개념 설명
`logs`, `exec`, `stats`만 배우면 명령어 목록처럼 느껴질 수 있다. 하지만 운영에서는 이 명령들이 dashboard, time series, log query로 확장된다. Day 4의 마지막 장면은 이 확장을 미리 보는 것이다.

깊은 observability 수업은 아니다. 목표는 다음 차이를 감각적으로 잡는 것이다.

```text
docker logs: 지금 무슨 일이 있었는가
docker exec: container 안쪽을 직접 확인한다
docker stats: 지금 순간의 resource를 본다
Prometheus/Grafana: resource 변화의 흐름을 본다
Loki/Grafana: log를 query하고 탐색한다
```

## Preview stack
| Service | 역할 | 확인 지점 |
|---|---|---|
| `sample-web` | nginx test traffic 대상 | `curl`, access log |
| `log-generator` | 일반 log sample | `docker compose logs`, Loki |
| `load-generator` | 반복 HTTP 요청 생성 | nginx access 증가 |
| `cpu-spike` | 선택 profile, CPU spike 생성 | `docker stats`, Prometheus query |
| `cadvisor` | Docker container metrics 노출 | Prometheus target |
| `prometheus` | metrics scrape/query | `up`, CPU/memory query |
| `loki` | log 저장 | Grafana Explore |
| `promtail` | Docker log 전달 | Loki ingest |
| `grafana` | metrics/logs 탐색 UI | Explore |

## 실습 명령
```bash
cd /mnt/d/paperclip/week2/day4/labs/observability-preview
docker compose config
docker compose --profile load config
docker compose up -d
docker compose ps
for i in 1 2 3 4 5; do curl -I http://localhost:18085 || true; sleep 1; done
docker compose logs sample-web --tail 20
docker compose logs log-generator --tail 20
```

Expected:

```text
HTTP/1.1 200 OK
level=info service=log-generator event=heartbeat
```

Open:

```text
Grafana:    http://localhost:13000  admin / practice-only
Prometheus: http://localhost:19090
cAdvisor:   http://localhost:18086
```

## Impact drill
CPU spike를 일부러 만들고 snapshot과 time series를 비교한다.

```bash
docker compose --profile load up -d cpu-spike
docker stats --no-stream
sleep 20
```

Grafana Explore > Prometheus:

```promql
rate(container_cpu_usage_seconds_total[1m])
```

해석:

| 관찰 도구 | 보이는 것 | 한계 |
|---|---|---|
| `docker stats --no-stream` | 지금 순간 CPU/MEM | 이전 1분 동안의 추세를 보기 어렵다 |
| Prometheus query | 시간 window의 변화 | 어떤 log line 때문에 튀었는지는 별도 log 확인 필요 |
| Grafana Explore | metrics와 logs를 한 화면에서 탐색 | dashboard가 원인을 자동으로 고쳐주지는 않는다 |

CPU spike를 멈춘다.

```bash
docker compose stop cpu-spike
```

## Grafana Explore 확인
| Source | Query | 의미 |
|---|---|---|
| Prometheus | `up` | scrape 대상이 살아 있는지 확인 |
| Prometheus | `container_memory_usage_bytes` | container memory metrics 확인 |
| Prometheus | `rate(container_cpu_usage_seconds_total[1m])` | CPU 사용률 변화 확인 |
| Loki | `{job="docker"}` | Docker container log 확인 |

curl로 Loki를 확인할 때는 시간 범위가 있는 endpoint를 사용한다. Grafana Explore는 화면의 time range를 함께 보내지만, API를 직접 호출하면 그 범위를 명시해야 한다.

WSL/Linux:

```bash
now_ns=$(date +%s%N)
start_ns=$((now_ns - 300000000000))

curl -G -s 'http://localhost:13100/loki/api/v1/query_range' \
  --data-urlencode 'query={job="docker"}' \
  --data-urlencode "start=$start_ns" \
  --data-urlencode "end=$now_ns" \
  --data-urlencode 'limit=5'
```

macOS:

```bash
end_time=$(date -u +"%Y-%m-%dT%H:%M:%SZ")
start_time=$(date -u -v-5M +"%Y-%m-%dT%H:%M:%SZ")

curl -G -s 'http://localhost:13100/loki/api/v1/query_range' \
  --data-urlencode 'query={job="docker"}' \
  --data-urlencode "start=$start_time" \
  --data-urlencode "end=$end_time" \
  --data-urlencode 'limit=5'
```

환경에 따라 Docker Desktop/WSL에서 Promtail이 `/var/lib/docker/containers`를 읽지 못할 수 있다. 이 경우에도 `docker compose logs`로 일반 로그를 확인하고, Prometheus/cAdvisor metrics 확인까지를 preview 성공으로 본다.

## OS별 troubleshooting
| 환경 | 오류/증상 | 수업에서 잡는 포인트 |
|---|---|---|
| WSL/Linux | `docker-credential-desktop.exe` not found | Docker CLI가 Windows credential helper 설정을 참조했지만 WSL PATH에서 실행 파일을 찾지 못한 상태 |
| WSL/Linux | cAdvisor가 Docker data root를 못 읽음 | `docker info --format '{{.DockerRootDir}}'`로 실제 DockerRootDir을 확인해야 함 |
| WSL/Linux/macOS | `port is already allocated` | 이미 실행 중인 container가 host port를 점유한 상태. `docker ps`로 충돌 port를 찾음 |
| WSL/Linux/macOS | Loki instant query 오류 | log query는 시간 범위가 필요하므로 `query_range`를 사용 |
| macOS | `date +%s%N`이 동작하지 않음 | BSD `date`와 GNU `date` 옵션 차이 |
| macOS | Promtail/Loki log가 비어 있음 | Docker Desktop은 Linux VM 안에서 engine이 돌아가므로 host에서 보는 경로와 engine 내부 log 경로가 다를 수 있음 |
| macOS | cAdvisor device/mount 오류 | Docker Desktop VM 보안/장치 mount 제약. 실패 자체를 runtime 차이 관찰 사례로 다룸 |

## Cleanup
```bash
docker compose down
# dashboard/log data까지 reset할 때만
# docker compose down -v
```

## 구름 EXP 배움일기
- `docker stats`와 Prometheus query가 어떻게 다르게 보였는가
- log와 metric 중 원인 힌트가 더 빨리 보인 쪽은 무엇인가
- Grafana 화면이 있어도 결국 어떤 command/output을 같이 봐야 하는가

## 핵심 포인트
Day 4의 마지막 목표는 dashboard를 잘 꾸미는 것이 아니다. 단일 container 명령으로 보던 증거가 Compose와 observability stack에서 metrics/logs로 확장된다는 감각을 잡는 것이다.
