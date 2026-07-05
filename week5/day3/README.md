# Week 5 Day 3: AWS 컨테이너 실행과 관찰

## Overview
W5D3는 Docker와 Kubernetes에서 배운 container image, port, health check, rollout, log 개념을 AWS의 ECR, ECS 또는 App Runner, CloudWatch로 연결한다. W5D2에서 EC2와 ALB를 직접 다뤘다면, 오늘은 container image를 AWS registry에 넣고 managed container 실행 서비스에서 app을 실행하는 흐름을 본다.

계정 권한, 비용, Docker Hub/ECR 인증 상태에 따라 ECS와 App Runner 중 하나를 실습 경로로 선택할 수 있다. EKS는 선택 심화 실습으로 다루며, 일단 lab 전용 IAM user credential과 `AdministratorAccess`, `aws eks update-kubeconfig`, `kubectl get nodes`를 통해 Week4 Kubernetes 경험을 AWS managed Kubernetes에 연결한다. 중요한 것은 특정 Console 화면을 외우는 것이 아니라, image -> service -> health -> logs -> update -> rollback의 운영 루프와, EKS를 선택할 때 생기는 kubeconfig/IAM/VPC/비용 경계를 이해하는 것이다. AdministratorAccess는 랩 안정성을 위한 시작점이며, 수업 뒤 least privilege로 줄인다.

## Learning Goals
- Docker/Kubernetes 관점에서 ECR, ECS, EKS, App Runner의 역할 차이를 설명한다.
- ECR repository, image tag, push/pull 인증 흐름을 이해한다.
- ECS task definition, service, desired count 또는 App Runner service의 실행 단위를 설명한다.
- container service와 ALB/listener/target group/health check 연결을 이해한다.
- image tag 변경, service update, 실패 시 이전 image 또는 revision 복구 흐름을 설명한다.
- CloudWatch Logs/Metrics/Alarm의 기본 위치와 확인 순서를 익힌다.
- 선택 심화로 EKS cluster와 local `kubectl`을 kubeconfig로 연결하는 절차를 설명한다.

## Lesson Index
| 교시 | 주제 | 핵심 확인 |
|---|---|---|
| 1교시 | Day2 요약 + 컨테이너 실행 서비스 매핑 | ECR, ECS, EKS, App Runner 역할 비교 |
| 2교시 | ECR 실습 | repository, image tag, auth, push/pull 주의 |
| 3교시 | ECS 또는 App Runner 맛보기 | task/service, desired count, logs, health |
| 4교시 | Container service와 ALB 연결 | listener, target group, container port, health check |
| 5교시 | 배포 변경과 rollback preview | 새 image tag, service update, previous revision |
| 6교시 | CloudWatch Logs 기본 | log group, log stream, app stdout/stderr |
| 7교시 | CloudWatch Metrics와 Alarm | CPU, memory, ALB target health, threshold |
| 8교시 | 구름 EXP 배움일기 | ECR/ECS/App Runner/CloudWatch evidence와 cleanup |

## Practice Files
| 자료 | 용도 |
|---|---|
| `academic-foundations.md` | 공식 문서 기반 개념 근거와 읽을 키워드 |
| `eks-kubectl-lab.md` | 선택 심화 EKS/kubectl 연결 실습 |
| `lesson-01.md` ~ `lesson-08.md` | 교시별 강의 자료 |
| `assets/lesson-01-container-service-map.png` | AWS container service map |
| `assets/lesson-02-ecr-image-flow.png` | ECR image push/pull flow |
| `assets/lesson-03-ecs-apprunner-service.png` | ECS/App Runner 실행 단위 |
| `assets/lesson-04-container-alb-link.png` | container service와 ALB 연결 |
| `assets/lesson-05-deploy-rollback.png` | image update와 rollback |
| `assets/lesson-06-cloudwatch-logs.png` | CloudWatch Logs 흐름 |
| `assets/lesson-07-cloudwatch-metrics-alarm.png` | Metrics와 Alarm |
| `assets/lesson-08-container-cleanup-journal.png` | 배움일기와 cleanup board |

## Official References
| Topic | Reference |
|---|---|
| Amazon ECR private repositories | https://docs.aws.amazon.com/AmazonECR/latest/userguide/Repositories.html |
| Pushing Docker image to ECR | https://docs.aws.amazon.com/AmazonECR/latest/userguide/docker-push-ecr-image.html |
| Amazon ECS task definitions | https://docs.aws.amazon.com/AmazonECS/latest/developerguide/task_definitions.html |
| Amazon ECS services | https://docs.aws.amazon.com/AmazonECS/latest/developerguide/ecs_services.html |
| ECS service load balancing | https://docs.aws.amazon.com/AmazonECS/latest/developerguide/service-load-balancing.html |
| AWS App Runner | https://docs.aws.amazon.com/apprunner/latest/dg/what-is-apprunner.html |
| App Runner image service | https://docs.aws.amazon.com/apprunner/latest/dg/service-source-image.html |
| EKS kubeconfig connection | https://docs.aws.amazon.com/eks/latest/userguide/create-kubeconfig.html |
| EKS Auto Mode CLI start | https://docs.aws.amazon.com/eks/latest/userguide/automode-get-started-cli.html |
| EKS cluster API endpoint | https://docs.aws.amazon.com/eks/latest/userguide/cluster-endpoint.html |
| IAM user access keys | https://docs.aws.amazon.com/IAM/latest/UserGuide/id_credentials_access-keys.html |
| AWS CLI configuration | https://docs.aws.amazon.com/cli/latest/userguide/cli-chap-configure.html |
| IAM least privilege | https://docs.aws.amazon.com/IAM/latest/UserGuide/getting-started-reduce-permissions.html |
| CloudWatch Logs | https://docs.aws.amazon.com/AmazonCloudWatch/latest/logs/WhatIsCloudWatchLogs.html |
| CloudWatch metrics | https://docs.aws.amazon.com/AmazonCloudWatch/latest/monitoring/working_with_metrics.html |
| CloudWatch alarms | https://docs.aws.amazon.com/AmazonCloudWatch/latest/monitoring/AlarmThatSendsEmail.html |

## Preparation Checklist
- W5D2 cleanup 완료 또는 유지 resource 사유 기록
- AWS CLI 사용 가능 여부 확인. CLI가 어렵다면 Console 중심 시뮬레이션 경로 사용
- Docker login/build/tag/push 기본 흐름 이해
- ECR repository 생성 권한 확인
- ECS 또는 App Runner 생성 권한과 비용 가능성 확인
- 선택 심화 EKS 경로를 사용할 경우 lab 전용 IAM user, `AdministratorAccess`, access key, AWS CLI profile, `kubectl`, EKS cluster 접근 권한 확인
- CloudWatch Logs/Metrics 접근 권한 확인
- 수업 종료 전 ECR image, ECS/App Runner service, ALB/target group, log retention cleanup 기준 확인

## Deliverables
- ECR repository/image tag evidence
- ECS task/service 또는 App Runner service evidence
- container port와 health check mapping note
- deployment update/rollback note
- CloudWatch Logs/Metrics 확인 note
- 선택 심화: EKS kubeconfig context와 `kubectl get nodes` evidence
- cleanup checklist

## End Of Day Checklist
- ECS service/App Runner service가 계속 비용을 만들지 않는지 확인했는가
- ALB/target group을 만들었다면 삭제 또는 유지 사유를 남겼는가
- ECR repository와 image retention을 확인했는가
- EKS 선택 실습을 했다면 cluster, node, load balancer, kubeconfig context, CloudWatch log group 잔여 상태를 확인했는가
- CloudWatch log group retention을 확인했는가
- Day4 S3/RDS 수업으로 넘어가기 전 container app의 config/secret/database 연결 질문을 남겼는가
