# Week 5 Day 5: AWS 통합 운영 실습

## Overview
W5D5는 Week 5에서 다룬 AWS 계정, 네트워크, compute, container, storage, database, observability, security, cost를 하나의 운영 실습으로 묶는다. 목표는 새로운 서비스를 더 많이 만드는 것이 아니라, 이미 배운 resource를 운영자가 설명할 수 있는 evidence, decision, runbook, cleanup 기준으로 정리하는 것이다.

오늘 산출물은 Week 5의 최종 운영 패킷이다. 학생은 AWS Console에서 본 화면을 단순 캡처로 모으는 것이 아니라, 장애가 났을 때 무엇을 먼저 확인할지, 비용이 남았을 때 어디서 찾을지, 공개된 endpoint와 secret을 어떻게 점검할지, 다음 사람이 같은 판단을 반복할 수 있는지까지 문서화한다.

![Integrated AWS operations map](./assets/lesson-01-integrated-operations-map.png)

## Learning Goals
- Week 5의 AWS resource를 account, network, compute, data, observability, security, cost 경계로 재분류한다.
- CloudWatch, CloudTrail, Cost Explorer, service health 화면을 evidence 중심으로 연결한다.
- 보안 리뷰에서 MFA, IAM, Security Group, public endpoint, secret 노출 여부를 점검한다.
- FinOps 리뷰에서 Budget, Cost Explorer, tag, cleanup 후보를 근거로 비용 판단을 작성한다.
- 장애 분석 흐름과 운영 runbook을 작성하고 portfolio packet으로 정리한다.

## Lesson Index
| 교시 | 주제 | 핵심 확인 |
|---|---|---|
| 1교시 | Week 5 통합 운영 지도 | account, network, compute, observability, cost, runbook 연결 |
| 2교시 | AWS Operations Evidence Dashboard | health, logs, metrics, CloudTrail, Cost Explorer |
| 3교시 | AWS Security Review Dashboard | MFA, IAM, SG, public endpoint, S3 public access, secret, CloudTrail audit |
| 4교시 | AWS FinOps Review Dashboard | Budget, Cost Explorer, service inventory, cleanup decision |
| 5교시 | AWS Incident Drill | symptom, scope, recent change, evidence, action, verification |
| 6교시 | AWS Operations Runbook | trigger, owner, evidence, action, verify, cleanup |
| 7교시 | Cloud Operations Portfolio Packet | architecture, evidence, incident, security/cost/cleanup proof |
| 8교시 | Final AWS Cleanup And Handoff | resource inventory, retained reason, deleted proof, Terraform handoff |

## Practice Files
| 자료 | 용도 |
|---|---|
| `academic-foundations.md` | 공식 문서 기반 개념 근거와 읽을 키워드 |
| `lesson-01.md` ~ `lesson-08.md` | 교시별 강의 자료 |
| `labs/operations-evidence-dashboard/README.md` | W5D5S2 health/log/metric/CloudTrail/cost evidence dashboard 실습 템플릿 |
| `labs/security-review-dashboard/README.md` | W5D5S3 AWS Console 기반 security review dashboard 실습 템플릿 |
| `labs/finops-review/README.md` | W5D5S4 비용 후보 inventory와 cleanup decision 실습 템플릿 |
| `labs/incident-drill/README.md` | W5D5S5 장애 주입/시뮬레이션 incident note 실습 템플릿 |
| `labs/operations-runbook/README.md` | W5D5S6 운영 runbook 작성 템플릿 |
| `labs/portfolio-packet/README.md` | W5D5S7 포트폴리오 패킷 README 템플릿 |
| `labs/cleanup-handoff/README.md` | W5D5S8 최종 resource cleanup/handoff 템플릿 |
| `assets/lesson-01-integrated-operations-map.png` | Week 5 통합 운영 지도 |
| `assets/lesson-02-operations-evidence-dashboard.png` | 운영 evidence dashboard |
| `assets/lesson-03-security-review-matrix.png` | Security review matrix |
| `assets/lesson-04-finops-review-board.png` | FinOps review board |
| `assets/lesson-05-incident-analysis-flow.png` | 장애 분석 흐름 |
| `assets/lesson-06-runbook-template.png` | runbook template |
| `assets/lesson-07-portfolio-packet.png` | portfolio packet 구성 |
| `assets/lesson-08-cleanup-handoff-review.png` | cleanup/handoff review |

## Official References
| Topic | Reference |
|---|---|
| AWS Well-Architected Operational Excellence | https://docs.aws.amazon.com/wellarchitected/latest/operational-excellence-pillar/welcome.html |
| AWS Well-Architected Security | https://docs.aws.amazon.com/wellarchitected/latest/security-pillar/welcome.html |
| AWS Well-Architected Cost Optimization | https://docs.aws.amazon.com/wellarchitected/latest/cost-optimization-pillar/welcome.html |
| CloudWatch dashboards | https://docs.aws.amazon.com/AmazonCloudWatch/latest/monitoring/CloudWatch_Dashboards.html |
| CloudWatch alarms | https://docs.aws.amazon.com/AmazonCloudWatch/latest/monitoring/AlarmThatSendsEmail.html |
| CloudTrail Event history | https://docs.aws.amazon.com/awscloudtrail/latest/userguide/view-cloudtrail-events.html |
| IAM security best practices | https://docs.aws.amazon.com/IAM/latest/UserGuide/best-practices.html |
| AWS Budgets | https://docs.aws.amazon.com/cost-management/latest/userguide/budgets-managing-costs.html |
| Cost Explorer | https://docs.aws.amazon.com/cost-management/latest/userguide/ce-what-is.html |
| Tagging AWS resources | https://docs.aws.amazon.com/tag-editor/latest/userguide/tagging.html |

## Preparation Checklist
- W5D1-D4 evidence note를 하나의 폴더 또는 markdown에 모을 수 있다.
- 실습 Region과 account를 확인한다.
- CloudWatch, CloudTrail, Cost Explorer, Billing/Budget 접근 권한을 확인한다.
- Week 5에서 남긴 resource가 있다면 유지 사유와 삭제 예정 시각을 적어둔다.
- screenshot에서 account email, access key, secret value, token이 보이지 않도록 정리한다.

## Deliverables
- Week 5 integrated operations map
- operations evidence dashboard
- security review dashboard
- FinOps review dashboard
- incident drill note
- AWS operations runbook
- portfolio packet README
- final cleanup/handoff inventory

## End Of Day Checklist
- 남아 있는 resource inventory를 작성했는가
- public endpoint와 Security Group 노출을 확인했는가
- secret 값과 access key가 문서에 남지 않았는가
- Budget/Cost Explorer/tag 기준으로 비용 후보를 확인했는가
- Day5 runbook과 portfolio packet이 다음 사람이 재현할 수 있는 수준인가
