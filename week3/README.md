# Week 3: MSA 운영, GitHub 협업, Kubernetes 입문

## Overview
3주차는 Week 2의 Docker/Compose 경험을 운영 흐름으로 확장한다. 앞의 2일은 MSA를 개발 방법론이 아니라 인프라가 운영해야 하는 서비스 토폴로지로 다룬다. 3일차는 GitHub 협업과 GitHub Actions CI gate를 하루에 압축한다. 4~5일차는 학생 기대가 큰 Kubernetes로 진입해 kind cluster, kubectl, Pod, Deployment, Service를 실제로 확인한다.

중심 질문은 다음과 같다.

```text
여러 서비스로 나뉜 애플리케이션을 어떻게 실행하고, 협업하고, 검증하고, Kubernetes로 옮길 준비를 할 것인가?
```

## Weekly Flow
| Day | 주제 | 핵심 실습 |
|---|---|---|
| Day 1 | MSA 토폴로지와 첫 실행 | `msa-demo` compose 실행, frontend/api/worker/db 상태 확인 |
| Day 2 | 장애 전파와 운영 증거 | health, readiness, timeout/retry, queue/worker, correlation id, 운영 리포트 |
| Day 3 | GitHub 협업과 CI gate | branch/PR/merge/rebase/revert/tag, Actions workflow |
| Day 4 | Kubernetes 배경과 kind 설치 | Kubernetes 컨셉, kind 단일 표준, WSL/macOS 설치, cluster 생성 |
| Day 5 | Kubernetes 샘플앱 실행 | Pod, Deployment, Service, rollout 맛보기 |

## Learning Goals
- MSA를 서비스 경계, 의존성, 장애 전파, 운영 비용 관점으로 설명한다.
- Compose로 frontend, api, worker, db를 실행하고 `ps`, `logs`, `curl`, health 응답으로 상태를 판단한다.
- service name DNS, host port, container port, environment, volume, healthcheck를 연결해서 읽는다.
- GitHub Flow, PR gate, merge/rebase/revert/tag를 배포 사고 예방 흐름으로 설명한다.
- GitHub Actions workflow, event, job, step, runner, secret의 위치를 설명하고 실패 로그를 읽는다.
- Kubernetes cluster/node/control plane/worker node/kubectl의 역할을 설명한다.
- kind에서 Pod, Deployment, Service를 실행하고 `get`, `describe`, `logs`, `events`, `rollout`으로 증거를 확인한다.

## Required Evidence
| Evidence | 기준 |
|---|---|
| MSA topology note | frontend/api/worker/db 역할과 연결 방향 |
| MSA failure report | 증상, 영향 범위, 원인 후보, 확인 명령, 복구 기준 |
| GitHub workflow note | branch, PR, merge/rebase/revert/tag 선택 기준 |
| Actions CI evidence | workflow 파일, 실패 로그, 재실행 결과 |
| Kubernetes install evidence | Docker/kubectl/kind version, context, node |
| Kubernetes app evidence | Pod/Deployment/Service manifest와 실행 결과 |

## Practice Environment
| 항목 | 기준 |
|---|---|
| Docker | `docker version`, `docker compose version` 가능 |
| MSA demo ports | frontend `18083`, api debug `18084` |
| GitHub | push, PR, Actions 실행 가능 |
| Kubernetes | kind, kubectl 사용 가능 |
| Cloud cost | Week 3는 로컬 실습 중심. cloud resource 생성 없음 |
| Security | `.env`, token, DB password를 screenshot/README에 그대로 남기지 않음 |

## Week 3 To Week 4 Mapping
| Week 3 | Week 4에서 확장 |
|---|---|
| Compose service | Deployment |
| service name DNS | Kubernetes Service DNS |
| environment variable | ConfigMap/Secret |
| health endpoint | liveness/readiness probe |
| image tag | rollout/rollback |
| PR CI gate | 배포 전 검증 조건 |
