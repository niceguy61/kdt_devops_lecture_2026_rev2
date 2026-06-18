# 8교시: Compose mapping handoff와 구름 EXP 배움일기

## 수업 목표
- Day 4에서 사용한 긴 `docker run` option을 Compose 항목으로 매핑한다.
- runtime config, 관찰 명령, cleanup 기준을 표로 정리한다.
- Day 5 Compose 수업에 가져갈 질문을 남긴다.

## 개념 설명
Day 4는 Compose를 배우는 날이 아니라 Compose가 왜 필요한지 몸으로 느끼는 날이다. `docker run` 명령에 port, env, env file, volume, network, restart option이 계속 붙으면 길고 실수하기 쉬워진다. Day 5에서는 이 조건을 `compose.yaml`에 남긴다.

오늘의 mapping은 Week 2에서 끝나지 않는다. Compose의 `environment`, `env_file`, `volumes`, `networks`는 Kubernetes의 ConfigMap/Secret, Volume, Service/NetworkPolicy를 이해하는 다리가 된다. Terraform에서는 같은 환경 분리 사고가 `dev.tfvars`, `staging.tfvars`, `prod.tfvars` 같은 variable 파일과 workspace/환경별 state 판단으로 이어진다.

## Mapping 표
| Day 4에서 사용한 것 | 의미 | Day 5 Compose 위치 |
|---|---|---|
| `docker run -d --name ...` | service process 시작 | `services.<name>` |
| `-p 18084:80` | host/container port publish | `services.<name>.ports` |
| `-e KEY=value` | runtime env 직접 주입 | `services.<name>.environment` |
| `--env-file .env` | env file 사용 | `env_file` 또는 `${VARIABLE}` |
| `.env.dev/.env.staging/.env.prod` | 환경별 설정 파일 | 환경별 Compose project 또는 env file |
| `-v source:target` | mount/volume 연결 | `services.<name>.volumes` |
| `--network name` | network 연결 | `networks` |
| `docker logs` | log 확인 | `docker compose logs` |
| `docker exec` | 내부 명령 실행 | `docker compose exec` |
| cleanup 명령 | 종료/삭제 | `docker compose down`, 필요 시 `down -v` |

## 다음 기술로 이어지는 표
| Day 4 개념 | Compose | Kubernetes | Terraform |
|---|---|---|---|
| `-e KEY=value` | `environment` | ConfigMap/Secret env | variable |
| `--env-file .env.dev` | `env_file` | 환경별 ConfigMap/Secret | `dev.tfvars` |
| `-p host:container` | `ports` | Service/Ingress | load balancer/security group |
| `-v volume:/path` | `volumes` | Volume/PVC | storage resource |
| `--network` | `networks` | Service DNS/network policy | VPC/subnet/security group |
| cleanup 판단 | `down` vs `down -v` | delete resource vs preserve PVC | destroy/retain state |

## 제출 표
학생은 다음 표를 채운다.

| 구분 | 내가 확인한 내용 | 증거 명령 | Day 5로 넘길 질문 |
|---|---|---|---|
| env/config |  |  |  |
| secret 비노출 |  |  |  |
| logs |  |  |  |
| inspect |  |  |  |
| exec |  |  |  |
| stats/restart |  |  |  |
| failure RCA |  |  |  |
| cleanup |  |  |  |
| Compose mapping |  |  |  |
| K8s/Terraform 연결 |  |  |  |

## 최종 확인 명령
```bash
docker ps -a --filter name=paperclip-day4
docker network ls | grep paperclip-day4 || true
docker volume ls | grep paperclip-day4 || true
```

Expected:

```text
cleanup 후 실습 container/network가 남지 않는다.
volume은 삭제 여부를 의식적으로 판단한다.
```

## 구름 EXP 배움일기
- `Up`과 정상 응답을 구분한 순간
- logs/inspect/exec/stats 중 가장 유용했던 명령
- 내가 재현한 실패와 첫 확인 명령
- cleanup에서 지우면 안 된다고 판단한 것
- Day 5 Compose로 옮기면 편해질 option
- Kubernetes/Terraform에서 다시 만날 것 같은 설정 분리 질문

## 핵심 포인트
Day 4의 완료 기준은 명령을 많이 실행한 것이 아니라, 실행 조건과 관찰 증거를 분리해서 설명할 수 있는 것이다.
