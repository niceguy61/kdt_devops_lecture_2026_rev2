# Week 5 Day 5 Academic Foundations

## 학습 근거
클라우드 운영의 결과물은 실행 중인 resource만이 아니다. 운영자는 evidence, decision, runbook, cleanup, handoff를 남겨야 한다. AWS Well-Architected Framework는 운영 우수성, 보안, 비용 최적화를 별도 주제로 다루며, 이는 Week 5의 모든 실습을 묶는 기준이 된다.

D5는 새로운 기능을 추가로 배우는 날이 아니라, 이미 만든 resource와 evidence를 운영 가능한 형태로 재구성하는 날이다. 학생은 Console 화면을 많이 아는 것보다, 장애/보안/비용 질문이 들어왔을 때 어느 화면에서 어떤 값을 확인할지 설명할 수 있어야 한다.

## 공식 문서 읽기 키워드
| 주제 | 공식 문서에서 확인할 키워드 | 수업에서 연결할 질문 |
|---|---|---|
| Operational Excellence | runbook, observability, operations as code | 반복 가능한 운영 절차가 있는가 |
| Security | identity, least privilege, detective controls | 누가 접근했고 무엇이 공개되어 있는가 |
| Cost Optimization | cost visibility, tags, budget, utilization | 비용 원인을 owner/purpose 기준으로 설명할 수 있는가 |
| CloudWatch | dashboard, metric, alarm, log group | service 상태를 어떤 evidence로 보는가 |
| CloudTrail | event history, user, event source, API call | 최근 변경을 누가 했는가 |
| Incident analysis | impact, recent change, rollback, verification | 증상에서 조치까지 근거가 이어지는가 |

## AWS 공식 자료
- AWS Well-Architected Operational Excellence Pillar: https://docs.aws.amazon.com/wellarchitected/latest/operational-excellence-pillar/welcome.html
- AWS Well-Architected Security Pillar: https://docs.aws.amazon.com/wellarchitected/latest/security-pillar/welcome.html
- AWS Well-Architected Cost Optimization Pillar: https://docs.aws.amazon.com/wellarchitected/latest/cost-optimization-pillar/welcome.html
- CloudWatch dashboards: https://docs.aws.amazon.com/AmazonCloudWatch/latest/monitoring/CloudWatch_Dashboards.html
- CloudTrail Event history: https://docs.aws.amazon.com/awscloudtrail/latest/userguide/view-cloudtrail-events.html
- IAM security best practices: https://docs.aws.amazon.com/IAM/latest/UserGuide/best-practices.html
- AWS Budgets: https://docs.aws.amazon.com/cost-management/latest/userguide/budgets-managing-costs.html
- Cost Explorer: https://docs.aws.amazon.com/cost-management/latest/userguide/ce-what-is.html

## 평가 기준
| 산출물 | 통과 기준 | 부족한 상태 |
|---|---|---|
| Evidence | resource 이름, Region, 상태, 변경 근거가 있다 | screenshot만 모여 있고 판단이 없다 |
| Security review | MFA/IAM/SG/public endpoint/secret/audit을 확인했다 | "보안 확인함"으로 끝난다 |
| FinOps review | Budget, Cost Explorer, tag, cleanup 후보가 연결된다 | 비용을 추측으로 설명한다 |
| Incident note | symptom, scope, change, evidence, action, verification이 있다 | 원인 추정과 조치가 섞여 있다 |
| Runbook | 다음 사람이 같은 순서로 따라할 수 있다 | 개인 기억에 의존한다 |
| Portfolio | architecture, evidence, incident, security, cost, cleanup이 한 패킷에 있다 | 파일만 흩어져 있다 |
