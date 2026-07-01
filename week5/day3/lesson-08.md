# 8교시: 구름 EXP 배움일기

![Container service cleanup and learning journal](./assets/lesson-08-container-cleanup-journal.png)

## 수업 목표
- ECR/ECS/App Runner/CloudWatch evidence를 정리한다.
- container service 관련 잔여 비용과 resource를 cleanup한다.
- Day4 storage/database/secret 수업으로 이어질 질문을 남긴다.

## 오늘 반드시 가져갈 것
| 필수 개념 | 왜 필수인가 | 놓치면 생기는 문제 | 확인 지점 |
|---|---|---|---|
| Image-to-service evidence | image와 실행 service가 연결되어야 배포를 설명할 수 있다 | push 성공만 기록한다 | ECR tag, service health |
| Health/log/metric | 운영 검증은 다층 증거로 한다 | URL만 보고 정상 처리한다 | health, logs, metrics |
| Cleanup | ECS/App Runner/ALB/ECR/log는 비용과 보존 정책을 남긴다 | 실습 후 비용 또는 로그 저장 누락 | service, image, log retention |

## 배움일기 템플릿
```markdown
# W5D3 AWS container service

## 1. 선택 경로
- ECS / App Runner / simulation:
- 선택 이유:

## 2. Image
- ECR repository:
- Image URI:
- Image tag:

## 3. Service
- Service name:
- Container port:
- Desired/running count 또는 service status:
- Endpoint:
- Health:

## 4. Update/Rollback
- 변경 전 tag/revision:
- 변경 후 tag/revision:
- rollback 기준:

## 5. Observability
- Log group:
- Log stream:
- Metric:
- Alarm 후보:

## 6. Cleanup
- ECS/App Runner service:
- ALB/Target Group:
- ECR image/repository:
- CloudWatch log retention:
- 비용 확인:

## 7. Day4 질문
-
-
```

## Cleanup 확인
| resource | 종료 전 확인 |
|---|---|
| ECS service | desired count 0 또는 delete |
| ECS cluster | 실습용이면 delete 여부 |
| App Runner service | pause/delete 또는 유지 사유 |
| ALB/Target Group | delete 여부 |
| ECR repository/image | 유지 사유와 retention |
| CloudWatch Logs | retention 설정 |
| IAM role | 실습용 role 잔여 여부 |

## Day4로 이어지는 질문
컨테이너 service가 실행되면 다음 질문은 data와 config다.

| 오늘 질문 | Day4 질문 |
|---|---|
| image는 어디서 가져오는가 | app data는 어디에 저장하는가 |
| env는 어디서 넣는가 | secret은 어디에 보관하는가 |
| service health는 어떻게 보는가 | database 연결 실패를 어떻게 분석하는가 |
| logs는 어디서 보는가 | storage/database 비용은 어떻게 통제하는가 |


## 50분 수업 운영 흐름
| 시간 | 활동 | 확인할 evidence |
|---|---|---|
| 0~15분 | image/service/health evidence 정리 | ECR/service table |
| 15~25분 | logs/metrics/alarm 후보 정리 | CloudWatch note |
| 25~35분 | update/rollback note 작성 | revision/tag |
| 35~45분 | cleanup audit | ECS/App Runner/ECR/log |
| 45~50분 | Day4 data/config 질문 | S3/RDS/secret questions |

## D3 배움일기의 핵심
오늘 배움일기는 URL 하나가 아니라 운영 루프 전체를 남겨야 한다. ECR image가 어떤 tag로 있고, 어떤 service가 그 image를 실행하며, health는 어디서 보고, log group은 어디인지, 문제가 생기면 어떤 revision으로 돌아갈지까지 연결되어야 한다.

## cleanup 판단
| 대상 | 삭제/유지 판단 |
|---|---|
| ECR repository | Day4 이후 계속 쓸 image가 아니면 삭제 또는 retention 계획 |
| ECS service | desired count 0 또는 delete |
| App Runner service | pause/delete 또는 유지 사유 |
| ALB/TG | ECS 연결 실습 후 삭제 |
| CloudWatch Logs | retention 설정 |
| IAM role | 실습용이면 잔여 권한 확인 |

## Day4로 이어지는 운영 질문
container app이 실행되면 곧바로 data와 secret 문제가 등장한다. DB endpoint는 어디서 가져오는가, password는 env에 넣어도 되는가, S3 object를 public으로 열어야 하는가, RDS를 private subnet에 두면 app은 어떻게 연결하는가. 이 질문들이 Day4의 중심이다.

## 좋은 산출물 예시
```markdown
Image: paperclip-w5d3-app:v2 in ECR
Service: ECS service desired=1 running=1
Health: target healthy
Logs: /ecs/paperclip-w5d3-app stream checked
Metric: ALB 5xx candidate alarm
Rollback: previous task definition revision 3
Cleanup: service deleted, ALB deleted, log retention 7 days
```

## 강사 보강 노트
이 교시는 `컨테이너 수업 정리`을 학생이 말로 설명할 수 있게 만드는 데 초점을 둔다. Console 화면을 따라 누르는 시간으로만 흘러가면 학생은 성공 화면은 보지만, 다음 날 같은 resource를 혼자 다시 만들거나 장애를 설명하지 못한다. 각 단계마다 "지금 무엇을 결정했는가", "그 결정은 비용/보안/관찰 중 어디에 영향을 주는가"를 짧게 되묻는다.

## 학생이 자주 흔들리는 지점
| 흔들리는 지점 | 강사 개입 문장 |
|---|---|
| ECR image를 남긴 채 넘어감 | "지금 화면에서 그 판단을 증명하는 값이 어디에 있나요?" |
| service endpoint만 기록하고 설정을 안 남김 | "이 값이 바뀌면 접속, 비용, 권한 중 무엇이 먼저 달라질까요?" |
| cleanup을 비용 확인 없이 끝냄 | "성공 화면 말고 실패했을 때 다시 볼 evidence를 남겼나요?" |

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
| 화면 캡처 | ECR/ECS/App Runner resource list | 성공 toast만 보이는 캡처 |
| 설정 기록 | 남길 resource 이유 | "기본값 사용"이라고만 적음 |
| 운영 판단 | Day4 질문 목록 | "잘 됨", "안 됨"으로만 적음 |

## 혼자 다시 따라오기
- 최소 재현 경로: ECR image tag, service health, CloudWatch log group을 하나의 표로 정리한다.
- 공식 문서 키워드: `ECR repository`, `ECS service`, `App Runner service`, `CloudWatch Logs`, `CloudWatch Metrics`.
- 스스로 확인할 화면: ECR Images, ECS/App Runner service detail, CloudWatch Logs/Metrics, Billing.
- 흔한 실패 3개: service를 삭제하지 않음, ECR image가 계속 쌓임, log retention을 기본값으로 방치함.
- 다음 준비 상태: Day4에서 S3/RDS/secret을 container app과 연결하는 질문을 말할 수 있어야 한다.

## 한 줄 요약
```text
W5D3의 산출물은 실행된 container URL이 아니라 image, service, health, logs, metrics, cleanup이 연결된 운영 evidence다.
```
