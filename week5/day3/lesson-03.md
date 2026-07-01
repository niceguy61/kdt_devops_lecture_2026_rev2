# 3교시: ECS 또는 App Runner 맛보기

![ECS and App Runner service paths](./assets/lesson-03-ecs-apprunner-service.png)

## 수업 목표
- ECS task definition/service 또는 App Runner service의 실행 단위를 이해한다.
- image, port, env, desired count, logs, health를 확인한다.
- 계정/비용/권한 상태에 따라 실제 생성 또는 시뮬레이션 경로를 선택한다.

## 오늘 반드시 가져갈 것
| 필수 개념 | 왜 필수인가 | 놓치면 생기는 문제 | 확인 지점 |
|---|---|---|---|
| Task definition | ECS에서 container 실행 방법을 정의한다 | image/port/env가 어디에 있는지 모른다 | task definition revision |
| Service | desired count만큼 task를 유지한다 | task 1회 실행과 운영 서비스를 혼동한다 | desired/running count |
| App Runner service | image/source에서 web service를 단순 실행한다 | managed service여도 health/log를 안 본다 | service URL, logs |
| Port mapping | container가 listen하는 port와 외부 연결 port가 맞아야 한다 | health check와 traffic이 실패한다 | container port |

## ECS 경로
ECS를 선택하면 다음 구조를 본다.

```text
ECR image
  -> Task Definition
  -> ECS Service
  -> Desired Count
  -> Logs/Health
```

| 항목 | 확인 |
|---|---|
| Cluster | service가 속한 논리적 묶음 |
| Task Definition | image, CPU/memory, port, env, log config |
| Service | desired count, deployment, load balancer |
| Task | 실제 실행 단위 |
| Logs | CloudWatch log group/stream |

## App Runner 경로
App Runner를 선택하면 ECR image 또는 source에서 web service를 빠르게 만들 수 있다.

| 항목 | 확인 |
|---|---|
| Source | ECR image 또는 source repository |
| Port | app이 listen하는 port |
| Service URL | public endpoint |
| Deployment | image 변경 반영 |
| Logs | build/deploy/app log |

## 실습 판단
| 상황 | 추천 |
|---|---|
| IAM/ECS 권한 충분, ALB 연결까지 보고 싶음 | ECS |
| 빠른 web service 실행과 logs를 보고 싶음 | App Runner |
| 비용/권한이 불안정함 | Console 시뮬레이션 + 개념 evidence |

## Evidence Note
```markdown
# W5D3S3 service taste
- 선택 경로: ECS / App Runner / simulation
- Image URI:
- Container port:
- Desired count 또는 service instance:
- Service URL 또는 endpoint:
- Health:
- Logs 위치:
```

## 혼자 다시 따라오기
- 최소 재현 경로: ECS task definition 또는 App Runner service 화면에서 image, port, env, logs 위치를 찾는다.
- 공식 문서 키워드: `ECS task definition`, `ECS service`, `desired count`, `App Runner image service`.
- 스스로 확인할 화면: ECS Task definitions, ECS Services, App Runner Services, CloudWatch Logs.
- 흔한 실패 3개: container port를 잘못 설정함, desired count 0을 정상 서비스로 착각함, service 생성 후 logs를 안 봄.
- 다음 준비 상태: "image를 어떻게 실행 서비스가 가져와서 web endpoint로 노출하는가"를 설명할 수 있어야 한다.

## 한 줄 요약
```text
ECS/App Runner 실습의 핵심은 image가 service로 실행되고 health/log로 검증되는 흐름이다.
```
