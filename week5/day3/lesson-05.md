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


## 50분 수업 운영 흐름
| 시간 | 활동 | 확인할 evidence |
|---|---|---|
| 0~10분 | 현재 service 상태 기록 | old tag/revision |
| 10~20분 | 새 image tag 개념 | v2 tag |
| 20~30분 | service update preview | deployment status |
| 30~40분 | 실패 image 시나리오 분석 | health/log fail |
| 40~50분 | rollback 기준 작성 | previous revision |

## 변경 전 evidence가 필요한 이유
배포 실패 후 가장 어려운 질문은 "정상 상태가 무엇이었나"이다. 이전 image tag, task definition revision, target health, 주요 metric을 기록하지 않으면 rollback이 감이 된다. 운영에서 rollback은 빠른 복구지만, 기준 없는 rollback은 또 다른 장애가 될 수 있다.

## 실패 시나리오별 rollback 판단
| 실패 | rollback 우선도 | 이유 |
|---|---|---|
| image pull 실패 | 높음 | 새 image를 실행조차 못 함 |
| container crash | 높음 | service capacity 감소 |
| wrong health path | 설정 수정 가능 | image 문제가 아닐 수 있음 |
| latency 증가 | metric 확인 후 판단 | rollback 또는 scale 조정 |

## update와 rollback evidence template
```markdown
Before: image=v1, revision=3, target=healthy
Change: image=v2, revision=4
Check: target=unhealthy, logs=port error
Action: service update to revision=3
Recheck: target=healthy, curl=200
```

## 비용/위험
배포 실패 task가 반복 생성되면 log가 쌓이고 service가 불안정해진다. 실패 배포를 방치하지 말고 desired count, deployment status, log 증가를 함께 확인한다.

## 강사 보강 노트
이 교시는 `배포와 롤백`을 학생이 말로 설명할 수 있게 만드는 데 초점을 둔다. Console 화면을 따라 누르는 시간으로만 흘러가면 학생은 성공 화면은 보지만, 다음 날 같은 resource를 혼자 다시 만들거나 장애를 설명하지 못한다. 각 단계마다 "지금 무엇을 결정했는가", "그 결정은 비용/보안/관찰 중 어디에 영향을 주는가"를 짧게 되묻는다.

## 학생이 자주 흔들리는 지점
| 흔들리는 지점 | 강사 개입 문장 |
|---|---|
| rollback 대상을 모름 | "지금 화면에서 그 판단을 증명하는 값이 어디에 있나요?" |
| tag를 덮어써 이전 이미지를 잃음 | "이 값이 바뀌면 접속, 비용, 권한 중 무엇이 먼저 달라질까요?" |
| 배포 실패와 health check 실패를 구분하지 못함 | "성공 화면 말고 실패했을 때 다시 볼 evidence를 남겼나요?" |

## 실습 중 멈춤 포인트
- 첫 번째 멈춤: 학생이 resource를 생성하기 전에 이름, Region, tag, 예상 비용 발생 지점을 말하게 한다.
- 두 번째 멈춤: 성공 화면이 나온 직후 resource ID와 상태값을 evidence note에 적게 한다.
- 세 번째 멈춤: 실패나 지연이 생기면 새로 클릭하기 전에 이전 단계의 화면과 명령을 다시 보게 한다.
- 네 번째 멈춤: 정리 단계에서 "삭제했다"가 아니라 "검색해도 남아 있지 않다"를 확인하게 한다.

## 확인 질문
1. 오늘 만든 resource가 어느 Region과 어느 계정 경계에 있는가?
2. 이 resource가 비용을 만들기 시작하는 시점은 언제인가?
3. 접속이 실패하면 app, network, permission 중 무엇을 먼저 확인할 것인가?
4. 수업이 끝난 뒤 남겨도 되는 resource와 지워야 하는 resource는 무엇인가?

## 제출 evidence 기준
| evidence | 좋은 예 | 부족한 예 |
|---|---|---|
| 화면 캡처 | before tag | 성공 toast만 보이는 캡처 |
| 설정 기록 | after tag | "기본값 사용"이라고만 적음 |
| 운영 판단 | deployment event 또는 service status | "잘 됨", "안 됨"으로만 적음 |

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
