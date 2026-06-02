# Week 1 Glossary

## Spine Components
### Compute
- 뜻: CPU가 명령을 실행해 process를 움직이는 영역.
- Week 1 evidence: 실행 명령, process 이름, exit code.
- Later mapping: Docker container, Kubernetes Pod, AWS EC2/ECS/Lambda.

### Memory
- 뜻: 실행 중인 process가 사용하는 임시 작업 공간.
- Week 1 evidence: memory 사용 관찰 note.
- Later mapping: container memory limit, Kubernetes requests/limits, instance size.

### Storage
- 뜻: 파일과 데이터가 저장되고 다시 읽히는 영역.
- Week 1 evidence: project path, `data/*.json`, README path.
- Later mapping: Docker volume, Kubernetes Volume, AWS S3/EBS/RDS.

### Network
- 뜻: 요청이 주소, 포트, 프로토콜을 통해 이동하는 경로.
- Week 1 evidence: URL, localhost, port, HTTP status.
- Later mapping: Docker port binding, Kubernetes Service/Ingress, AWS VPC/ALB/security group.

### Process Lifecycle
- 뜻: 프로그램이 시작, 실행, 실패, 중지, 재시작되는 흐름.
- Week 1 evidence: start/check/stop/recheck command.
- Later mapping: Docker run/stop, Kubernetes rollout/probe, Terraform apply/destroy.

### Configuration
- 뜻: 같은 코드가 다른 환경에서 다르게 동작하도록 주입되는 값.
- Week 1 evidence: config key, environment variable name, secret non-exposure note.
- Later mapping: Docker env, Kubernetes ConfigMap/Secret, AWS Parameter Store.

### Identity And Access
- 뜻: 누가 무엇을 할 수 있는지 정하는 계정, 권한, 인증 정보.
- Week 1 evidence: public/private repo decision, token non-exposure.
- Later mapping: Kubernetes ServiceAccount/RBAC, AWS IAM/MFA/role.

### Observability
- 뜻: 시스템 상태를 밖에서 판단하게 해주는 log, status, metric, event, trace.
- Week 1 evidence: log excerpt, HTTP status, RCA table.
- Later mapping: Docker logs, Kubernetes events/probes, AWS CloudWatch/CloudTrail.

### Cost Or Resource Boundary
- 뜻: 컴퓨터 자원과 비용이 무한하지 않다는 제한.
- Week 1 evidence: paid API excluded note, local resource blocker.
- Later mapping: Kubernetes capacity, AWS billing/budget, Terraform destroy.

## Professional Terms
### DevOps
- 뜻: 개발과 운영을 잇는 문화, practice, automation의 조합.
- 공식 참고: https://aws.amazon.com/devops/what-is-devops/
- Week 1 사용 위치: Day 1, Day 5 handoff.

### Handoff
- 뜻: 다른 사람이 산출물을 이어받아 실행, 확인, 문제 대응을 할 수 있게 넘기는 것.
- Week 1 evidence: README, known issue, risk table.

### RCA
- 뜻: 장애나 실패를 증상, 영향, 원인 후보, 수정, 재확인, 예방으로 기록하는 절차.
- 공식 연결: Google SRE postmortem culture.

### README
- 뜻: 저장소의 목적, 실행 방법, 확인 방법, 제한을 설명하는 기본 문서.
- 공식 참고: https://docs.github.com/en/repositories/managing-your-repositorys-settings-and-features/customizing-your-repository/about-readmes

### Future Anchor
- 뜻: Week 1에서 깊게 가르치지 않고, 나중에 배울 기술이 어떤 문제를 해결하는지만 연결하는 용어.
- 예: Docker, Kubernetes, AWS, Terraform, Well-Architected, DORA.
