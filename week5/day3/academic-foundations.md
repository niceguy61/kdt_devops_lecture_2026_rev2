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

## 오늘의 판단 기준
- ECR은 실행 서비스가 아니라 image registry다.
- ECS task definition은 "어떤 container를 어떻게 실행할지"의 정의이고, service는 그 task를 유지하는 운영 단위다.
- App Runner는 web app 실행을 단순화하지만 image, port, env, logs, health 판단은 여전히 필요하다.
- image tag만 바뀌어도 운영 변경이다. 변경 전후 evidence와 rollback 기준이 있어야 한다.
- CloudWatch Logs는 app log를 보는 곳이고, CloudWatch Metrics/Alarm은 수치와 임계값을 보는 곳이다.
