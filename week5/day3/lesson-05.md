# 5교시: 배포 변경과 rollback preview

![Container deployment update and rollback](./assets/lesson-05-deploy-rollback.png)

## 수업 목표
- 새 image tag를 service에 반영하는 배포 변경 흐름을 이해한다.
- 실패한 image 또는 health check 실패를 이전 정상 revision으로 되돌리는 기준을 잡는다.
- image tag, task definition revision, deployment history를 evidence로 남긴다.

## 오늘 반드시 가져갈 것
| 필수 개념 | 왜 필수인가 | 놓치면 생기는 문제 | 확인 지점 |
|---|---|---|---|
| Image tag update | container 배포 변경의 기본 단위다 | 어떤 version이 실행 중인지 모른다 | ECR image tag, task definition |
| Revision | ECS task definition은 revision으로 변경을 추적한다 | rollback 기준이 흐려진다 | task definition revision |
| Health-based rollback | 새 배포가 healthy인지 확인한 뒤 유지한다 | 실패 배포를 계속 serving한다 | deployment status, target health |
| Evidence before/after | 변경 전후 상태가 있어야 복구할 수 있다 | "아까 됐는데"만 남는다 | old/new tag, curl, logs |

## 변경 흐름
```mermaid
flowchart LR
  V1["Image v1"] --> Service["Service healthy"]
  Service --> V2["Image v2"]
  V2 --> Deploy["Service update"]
  Deploy --> Check["Health/Logs"]
  Check -->|ok| Keep["Keep v2"]
  Check -->|fail| Rollback["Rollback to v1"]
```

## ECS rollback preview
ECS에서는 image tag가 바뀌면 보통 task definition 새 revision을 만들고 service update로 반영한다. 실패하면 이전 task definition revision으로 service를 다시 update하는 방식으로 되돌릴 수 있다.

| 단계 | Evidence |
|---|---|
| 변경 전 | task definition revision, image tag, target health |
| 변경 | new image tag, new revision |
| 검증 | running count, target health, CloudWatch Logs |
| rollback | previous revision, previous tag |

## App Runner rollback preview
App Runner는 deployment history와 image source를 기준으로 이전 정상 image로 되돌리는 사고방식을 잡는다. Console 기능은 계정/시점에 따라 다르게 보일 수 있으므로, 오늘은 "이전 image tag로 service를 다시 배포한다"는 원리를 강조한다.

## 실패 image 예시
수업에서 실제로 실패 image를 만들지 않아도 된다. 다만 실패 시나리오는 구분한다.

| 실패 | 증상 |
|---|---|
| bad image tag | image pull 실패 |
| app crash | task stopped, logs error |
| wrong port | health check fail |
| wrong env | app 5xx, logs config error |

## Evidence Note
```markdown
# W5D3S5 deploy rollback
- Previous image tag:
- New image tag:
- Service/revision before:
- Service/revision after:
- Health check result:
- Logs result:
- Rollback 기준:
```

## 혼자 다시 따라오기
- 최소 재현 경로: service가 사용하는 image tag와 변경 전 revision을 기록한다.
- 공식 문서 키워드: `ECS deployment`, `task definition revision`, `App Runner deployment`, `image tag`.
- 스스로 확인할 화면: ECS service deployments, Task definition revisions, App Runner deployments, ECR Images.
- 흔한 실패 3개: `latest`만 써서 이전 version을 모름, health 확인 없이 성공 처리함, rollback할 revision을 기록하지 않음.
- 다음 준비 상태: 새 image 배포 전후 어떤 evidence를 남길지 설명할 수 있어야 한다.

## 한 줄 요약
```text
Rollback은 감으로 되돌리는 것이 아니라 이전 image tag와 revision evidence로 되돌리는 작업이다.
```
