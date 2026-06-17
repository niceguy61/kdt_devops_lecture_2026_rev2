# Week 2 Day 4 Academic Foundations

Day 4는 runtime configuration, observability, failure drill을 다룬다. Day 3에서 만든 image가 실제 실행 환경에서 어떤 env, port, log, process, restart policy와 만나는지 확인한다.

| 근거 | Day 4 연결 |
|---|---|
| Docker run reference | env, ports, mounts, restart option의 공식 동작 |
| Docker logs | stdout/stderr 기반 로그 확인 |
| Docker inspect | container metadata, network, env, mount 확인 지점 확인 |
| Docker exec | container 내부 process와 filesystem을 제한적으로 확인 |
| Docker stats | resource usage 관찰 |
| Twelve-Factor App config | config를 code/image와 분리 |
| SRE incident practice | 실패 재현, fix, recheck, prevention 확인 |

## Conceptual Rationale

Runtime 설정은 image를 새로 만들지 않고 실행 조건을 바꾸는 경계다. 같은 image도 env, port, network, mount, restart policy에 따라 운영 의미가 달라진다. Day 4에서는 "container running"을 완료 기준으로 삼지 않고, log, inspect, exec, stats, failure drill로 상태를 증명한다.

Observability는 Kubernetes부터 시작하는 주제가 아니다. 로컬 Docker에서도 stdout/stderr, process list, metadata, resource usage를 확인하는 습관이 있어야 한다. 학생은 실패를 보면 먼저 logs, inspect, port, env, process 중 어디에서 확인 지점을 얻을지 판단한다.

## Official Links

- Docker run reference: https://docs.docker.com/reference/cli/docker/container/run/
- Docker container logs: https://docs.docker.com/reference/cli/docker/container/logs/
- Docker inspect: https://docs.docker.com/reference/cli/docker/inspect/
- Docker exec: https://docs.docker.com/reference/cli/docker/container/exec/
- Docker stats: https://docs.docker.com/reference/cli/docker/container/stats/
- Start containers automatically: https://docs.docker.com/engine/containers/start-containers-automatically/
- Twelve-Factor App Config: https://12factor.net/config

## Standards Crosswalk

| 기준 | 학생 행동 |
|---|---|
| Bloom analyze/evaluate | 실행 실패를 env, port, process, resource, image 문제로 분류 |
| ABET-style problem solving | 증상, 원인 후보, 수정, 재검증을 RCA note로 작성 |
| Professional responsibility | secret 출력, root 실행, 불필요한 privileged option을 피함 |
| SRE/DevOps 확인 지점 | logs, inspect, exec, stats, curl 결과를 함께 남김 |

## 완료 전 주의할 점

학생은 Day 4 종료 시점에 다음을 설명할 수 있어야 한다.

- env가 runtime에서 적용된 증거
- log로 정상/비정상 상태를 구분한 증거
- `inspect`로 port, mount, network, env 일부를 확인한 증거
- `exec`로 process 또는 filesystem을 확인한 증거
- 의도적 실패를 재현하고 fix/recheck/prevention을 확인한 RCA
