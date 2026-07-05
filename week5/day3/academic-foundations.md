# Week 5 Day 3 Academic And Official Foundations

## 공식 문서 기준
오늘 수업은 Docker image를 AWS에서 실행 가능한 운영 단위로 연결한다. ECR, ECS, App Runner, CloudWatch는 빠르게 바뀌는 서비스이므로 Console 화면보다 공식 문서의 개념 단어를 기준으로 읽는다.

| 주제 | 공식 문서 | 읽을 키워드 |
|---|---|---|
| ECR repository | https://docs.aws.amazon.com/AmazonECR/latest/userguide/Repositories.html | private repository, image, tag |
| ECR push | https://docs.aws.amazon.com/AmazonECR/latest/userguide/docker-push-ecr-image.html | authenticate, tag, push |
| ECS task definition | https://docs.aws.amazon.com/AmazonECS/latest/developerguide/task_definitions.html | container definition, image, portMappings |
| ECS service | https://docs.aws.amazon.com/AmazonECS/latest/developerguide/ecs_services.html | desired count, deployment, maintain tasks |
| ECS load balancing | https://docs.aws.amazon.com/AmazonECS/latest/developerguide/service-load-balancing.html | target group, load balancer, container port |
| App Runner | https://docs.aws.amazon.com/apprunner/latest/dg/what-is-apprunner.html | web application, container image, managed service |
| App Runner image source | https://docs.aws.amazon.com/apprunner/latest/dg/service-source-image.html | image repository, deployment |
| EKS kubeconfig | https://docs.aws.amazon.com/eks/latest/userguide/create-kubeconfig.html | kubeconfig, aws eks get-token, kubectl, sts identity |
| EKS Auto Mode start | https://docs.aws.amazon.com/eks/latest/userguide/automode-get-started-cli.html | cluster, node, VPC subnet, IAM role |
| EKS API endpoint | https://docs.aws.amazon.com/eks/latest/userguide/cluster-endpoint.html | public endpoint, private endpoint, IAM, Kubernetes RBAC |
| IAM user access key | https://docs.aws.amazon.com/IAM/latest/UserGuide/id_credentials_access-keys.html | access key ID, secret access key, programmatic access |
| AWS CLI config | https://docs.aws.amazon.com/cli/latest/userguide/cli-chap-configure.html | named profile, Region, output, credentials file |
| IAM least privilege | https://docs.aws.amazon.com/IAM/latest/UserGuide/getting-started-reduce-permissions.html | AdministratorAccess 이후 권한 축소 |
| CloudWatch Logs | https://docs.aws.amazon.com/AmazonCloudWatch/latest/logs/WhatIsCloudWatchLogs.html | log group, log stream |
| CloudWatch Metrics | https://docs.aws.amazon.com/AmazonCloudWatch/latest/monitoring/working_with_metrics.html | namespace, metric, dimension |
| CloudWatch Alarms | https://docs.aws.amazon.com/AmazonCloudWatch/latest/monitoring/AlarmThatSendsEmail.html | threshold, alarm state, notification |

## Workforce 기준 연결
| 역량 | 오늘의 행동 | Evidence |
|---|---|---|
| 배포 단위 이해 | image tag와 running service를 연결한다 | ECR/service evidence |
| 운영 안정성 | health check와 desired count를 확인한다 | health/service note |
| 변경 관리 | 새 image tag update와 rollback 기준을 남긴다 | deployment note |
| 관찰 가능성 | stdout/stderr가 CloudWatch log stream으로 연결되는지 확인한다 | log group/log stream |
| 비용 통제 | service, ALB, image, log retention 잔여 비용을 정리한다 | cleanup checklist |
| Kubernetes cloud 연결 | IAM user credential, kubeconfig, kubectl context를 연결한다 | `aws sts get-caller-identity`, `kubectl get nodes` |

## 오늘의 판단 기준
- ECR은 실행 서비스가 아니라 image registry다.
- ECS task definition은 "어떤 container를 어떻게 실행할지"의 정의이고, service는 그 task를 유지하는 운영 단위다.
- App Runner는 web app 실행을 단순화하지만 image, port, env, logs, health 판단은 여전히 필요하다.
- EKS는 Kubernetes control plane을 AWS managed service로 사용하는 경로다. `kubectl` 연결은 kubeconfig와 AWS IAM identity가 함께 맞아야 한다.
- EKS cluster endpoint는 public/private 접근 설정과 IAM, Kubernetes RBAC가 함께 보안 경계를 만든다.
- EKS lab은 일단 IAM user credential과 AdministratorAccess로 랩 실패를 줄이고, 수업 뒤 access key 폐기와 least privilege 축소를 반드시 수행한다.
- image tag만 바뀌어도 운영 변경이다. 변경 전후 evidence와 rollback 기준이 있어야 한다.
- CloudWatch Logs는 app log를 보는 곳이고, CloudWatch Metrics/Alarm은 수치와 임계값을 보는 곳이다.
