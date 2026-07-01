# 1교시: Week4 요약 + AWS로 넘어가는 이유

![AWS operating map with cloud guide](./assets/day1-aws-operating-map.png)

## 수업 목표
- Kubernetes 운영에서 남은 질문을 AWS resource로 연결한다.
- AWS 주간의 학습 목표를 "서비스 생성"보다 "운영 경계 이해"로 잡는다.
- 오늘 사용할 evidence note 형식을 만든다.

## 오늘 반드시 가져갈 것
| 필수 개념 | 왜 필수인가 | 놓치면 생기는 문제 | 확인 지점 |
|---|---|---|---|
| Cloud resource boundary | AWS에서는 모든 resource가 계정, Region, 권한, 비용 경계 안에 생성된다 | resource를 만들고도 어디서 비용이 나는지 모른다 | Account ID, Region selector, Billing |
| Kubernetes와 AWS의 역할 차이 | Kubernetes는 cluster 안 workload를 조율하고, AWS는 cluster 밖 compute/network/storage를 제공한다 | Service/Ingress와 ALB/VPC를 같은 계층으로 오해한다 | W4 object와 AWS service mapping |
| Evidence-first 운영 | Console 클릭보다 생성 전/후 증거가 중요하다 | 장애나 비용 질문에 답하지 못한다 | screenshot, resource ID, tag, event |

## Week4에서 남은 질문
W4D5까지 Kubernetes 안에서 다음을 확인했다.

| Kubernetes에서 본 것 | AWS에서 다시 묻는 질문 |
|---|---|
| Node capacity | node는 어떤 EC2 instance 또는 managed compute 위에서 도는가 |
| Service/Ingress/Gateway | 외부 load balancer와 public endpoint는 누가 만들고 비용은 어디서 나는가 |
| Secret/ConfigMap | cloud secret store와 parameter store는 어디에 있는가 |
| PV/PVC | 실제 disk, object storage, managed database는 어떤 service인가 |
| metrics/logs/events | CloudWatch, CloudTrail, billing data는 어디서 확인하는가 |
| RBAC/Kyverno | AWS IAM과 resource policy는 어떤 경계에서 막는가 |

Kubernetes 수업에서는 cluster 안의 선언과 controller 동작을 봤다. AWS 수업에서는 그 cluster와 app이 기대는 계정, network, compute, storage, database, observability, billing 경계를 본다.

## AWS 주간의 관점
AWS를 처음 볼 때 service 이름이 많아 보인다. 오늘은 이름을 전부 외우는 시간이 아니다. Week 1 computing spine에 다시 붙여서 읽는다.

```mermaid
flowchart LR
  Local["Local process"] --> Docker["Docker container"]
  Docker --> K8s["Kubernetes workload"]
  K8s --> AWS["AWS resource boundary"]
  AWS --> Ops["Cost, IAM, Logs, Audit"]
```

| Spine | AWS에서 볼 대표 service | 오늘의 관찰 질문 |
|---|---|---|
| Compute | EC2, ECS, Lambda | 어떤 실행 단위가 돈을 쓰는가 |
| Network | VPC, subnet, SG, ALB | 누가 어디서 접속 가능한가 |
| Storage | S3, EBS, EFS | 데이터가 resource 삭제와 함께 사라지는가 |
| Database | RDS | 누가 DB port에 접근 가능한가 |
| Identity | IAM, MFA, role | 누가 생성/삭제 권한을 갖는가 |
| Observability | CloudWatch, CloudTrail | 로그/지표/API 이벤트를 어디서 보는가 |
| Cost | Billing, Budget, Cost Explorer | 언제부터 비용이 생기고 어떻게 알림을 받는가 |

## 오늘 하지 않는 것
오늘은 EC2/ALB/ECS/RDS를 깊게 실습하지 않는다. 첫날부터 많은 resource를 만들면 학생마다 잔여 비용과 권한 상태가 달라져 다음 날 수업이 흔들린다. 오늘은 안전장치와 resource map을 먼저 잡고, 실제 EC2/ALB는 Day2에서 진행한다.


## 50분 수업 운영 흐름
| 시간 | 활동 | 확인할 evidence |
|---|---|---|
| 0~10분 | Week4 Kubernetes 운영 흐름 복기 | GitOps/Ingress/Secret/PV 질문 목록 |
| 10~20분 | AWS 계정/Region/resource boundary 소개 | Account ID, Region selector |
| 20~35분 | Kubernetes object를 AWS service로 매핑 | mapping table 완성 |
| 35~45분 | 비용/권한/관찰 질문으로 재분류 | Billing, IAM, CloudWatch 위치 |
| 45~50분 | 오늘의 안전장치 확인 | MFA/Budget/Region note |

## 강의 중 질문
- Kubernetes에서 `Service`가 외부 traffic을 받는다고 말할 때, 실제 cloud load balancer 비용은 어디에 잡히는가?
- Pod가 죽으면 Kubernetes가 다시 띄울 수 있다. 그런데 node 자체가 cloud instance라면 node 비용과 장애 경계는 누가 관리하는가?
- Secret을 Kubernetes object로 만들었다. cloud secret store와 연결하지 않으면 어떤 운영 위험이 남는가?

## 콘솔 확인 위치
| Console 위치 | 확인할 값 | 왜 보는가 |
|---|---|---|
| 오른쪽 위 Region selector | `ap-northeast-2` | resource 조회 기준 고정 |
| Billing and Cost Management | 현재 비용, Budget | 실습 전 비용 안전장치 |
| IAM dashboard | MFA, user/role | 누가 실습하는지 확인 |
| CloudTrail Event history | 최근 API event | 변경 추적 위치 preview |

## 흔한 오해와 교정
| 오해 | 교정 |
|---|---|
| AWS는 서버를 빌리는 곳이다 | AWS는 compute/network/storage/identity/observability/cost 경계를 조합하는 platform이다 |
| Kubernetes를 알면 AWS는 부가 지식이다 | managed Kubernetes도 결국 cloud resource 위에서 동작하므로 AWS 경계를 알아야 한다 |
| 오늘 resource를 많이 만들어야 진도가 나간다 | 첫날은 계정 사고와 비용 사고를 막는 운영 기준을 만드는 것이 진도다 |

## 캡처 가이드
수업 자료나 배움일기에 캡처를 남길 때는 credential, account email, MFA code, access key가 보이지 않게 한다. 캡처에는 Region selector, resource name, tag, 상태값처럼 재현에 필요한 정보만 남긴다.

## 강사 보강 노트
이 교시는 `AWS 전환 관점`을 학생이 말로 설명할 수 있게 만드는 데 초점을 둔다. Console 화면을 따라 누르는 시간으로만 흘러가면 학생은 성공 화면은 보지만, 다음 날 같은 resource를 혼자 다시 만들거나 장애를 설명하지 못한다. 각 단계마다 "지금 무엇을 결정했는가", "그 결정은 비용/보안/관찰 중 어디에 영향을 주는가"를 짧게 되묻는다.

## 학생이 자주 흔들리는 지점
| 흔들리는 지점 | 강사 개입 문장 |
|---|---|
| Service는 ALB가 될 수도 있지만 항상 같은 것은 아니다. | "지금 화면에서 그 판단을 증명하는 값이 어디에 있나요?" |
| PV는 EBS/EFS/S3/RDS 중 무엇을 쓰는지에 따라 운영 경계가 달라진다. | "이 값이 바뀌면 접속, 비용, 권한 중 무엇이 먼저 달라질까요?" |
| Secret은 Kubernetes 안에 있을 수도 있고 AWS Secrets Manager나 Parameter Store와 연결될 수도 있다. | "성공 화면 말고 실패했을 때 다시 볼 evidence를 남겼나요?" |

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
| 화면 캡처 | Region selector가 보이는 Console 화면 | 성공 toast만 보이는 캡처 |
| 설정 기록 | Week4 object와 AWS service mapping 표 | "기본값 사용"이라고만 적음 |
| 운영 판단 | 오늘 만들지 않을 resource 목록 | "잘 됨", "안 됨"으로만 적음 |

## Evidence Note
```markdown
# W5D1S1 AWS transition
- 오늘 사용할 AWS Account ID:
- 오늘 사용할 Region:
- Week4에서 AWS로 연결되는 질문 3개:
- 가장 걱정되는 비용/권한 지점:
- 오늘 만들거나 확인할 evidence:
```

## 혼자 다시 따라오기
- 최소 재현 경로: Week4에서 배운 Kubernetes object 3개를 고르고, AWS에서 대응되는 service 후보를 적는다.
- 공식 문서 키워드: `AWS Regions`, `IAM root user`, `VPC security groups`, `S3 Block Public Access`.
- 스스로 확인할 화면: AWS Console 오른쪽 위 Region selector, Billing console, IAM dashboard.
- 흔한 실패 3개: Region을 바꿔놓고 resource를 못 찾음, root user로 계속 작업함, resource 생성 전 비용 알림을 확인하지 않음.
- 다음 준비 상태: 오늘 사용할 account, Region, Budget 상태를 말로 설명할 수 있어야 한다.

## 한 줄 요약
```text
AWS 수업의 첫 질문은 "무엇을 만들까"가 아니라 "어느 계정, 어느 Region, 어떤 권한과 비용 경계 안에서 만들까"이다.
```
