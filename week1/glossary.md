# Week 1 Glossary: Cloud Native 기본기와 운영 마인드셋

## Cloud And Infrastructure

### Cloud Native
- 한 줄 뜻: 클라우드 환경에 맞게 빠르게 배포하고 안정적으로 운영하는 접근
- 왜 중요한가: Docker, Kubernetes, MSA, Observability, IaC를 하나의 운영 흐름으로 연결한다.
- 수업에서 다시 나오는 곳: Week 1 Day 1, Week 4 Kubernetes, Week 5 AWS
- 공식 참고: https://glossary.cncf.io/

### Cloud Computing
- 한 줄 뜻: 필요한 컴퓨팅 자원을 빌려 쓰는 사용량 기반 컴퓨팅
- 왜 중요한가: 서버 구매 중심 사고에서 서비스 조합과 비용 최적화 사고로 전환한다.
- 수업에서 다시 나오는 곳: Week 1 Day 1, Week 5 AWS
- 공식 참고: https://docs.aws.amazon.com/whitepapers/latest/aws-overview/what-is-cloud-computing.html

### Compute
- 한 줄 뜻: 프로그램이 실행되는 계산 자원
- 왜 중요한가: Docker container, Kubernetes Pod, EC2, ECS, EKS를 이해하는 바닥 개념이다.
- 수업에서 다시 나오는 곳: Week 2 Docker, Week 4 Kubernetes, Week 5 AWS
- 공식 참고: https://docs.aws.amazon.com/whitepapers/latest/aws-overview/compute-services.html

### Network
- 한 줄 뜻: 요청과 응답이 이동하는 통신 경로
- 왜 중요한가: 포트, DNS, Security Group, Service, Ingress, VPC를 이해하는 기반이다.
- 수업에서 다시 나오는 곳: Week 1 Day 2, Week 3 MSA, Week 4 Kubernetes, Week 5 AWS
- 공식 참고: https://docs.aws.amazon.com/whitepapers/latest/aws-overview/networking-services.html

### Storage
- 한 줄 뜻: 데이터가 저장되고 유지되는 공간
- 왜 중요한가: 컨테이너 삭제, 볼륨, S3, EBS, RDS의 차이를 이해하게 한다.
- 수업에서 다시 나오는 곳: Week 2 Docker volume, Week 5 AWS
- 공식 참고: https://docs.aws.amazon.com/whitepapers/latest/aws-overview/storage-services.html

### Managed Service
- 한 줄 뜻: 운영 일부를 클라우드 제공자가 대신 관리하는 서비스
- 왜 중요한가: 운영 부담은 줄지만 비용, 제약, 책임 경계는 반드시 이해해야 한다.
- 수업에서 다시 나오는 곳: Week 1 Day 4, Week 4 Kubernetes plugins, Week 5 AWS
- 공식 참고: https://docs.aws.amazon.com/whitepapers/latest/aws-overview/introduction.html

### Region
- 한 줄 뜻: 클라우드 리소스가 배치되는 지리적 지역
- 왜 중요한가: 지연 시간, 서비스 제공 여부, 비용, 규제 조건에 영향을 준다.
- 수업에서 다시 나오는 곳: Week 1 Day 4, Week 5 AWS
- 공식 참고: https://docs.aws.amazon.com/AWSEC2/latest/UserGuide/using-regions-availability-zones.html

### Availability Zone
- 한 줄 뜻: 한 Region 안에서 분리된 데이터센터 묶음
- 왜 중요한가: 단일 장애 지점을 줄이고 고가용성 구조를 이해하는 기본 단위다.
- 수업에서 다시 나오는 곳: Week 1 Day 4, Week 5 AWS
- 공식 참고: https://docs.aws.amazon.com/AWSEC2/latest/UserGuide/using-regions-availability-zones.html

### IAM
- 한 줄 뜻: Identity and Access Management, AWS 접근 권한 관리 서비스
- 왜 중요한가: 누가 어떤 리소스를 만들고 변경할 수 있는지 통제하는 보안 경계다.
- 수업에서 다시 나오는 곳: Week 1 Day 4, Week 5 AWS, Week 6 Terraform
- 공식 참고: https://docs.aws.amazon.com/IAM/latest/UserGuide/introduction.html

### Root User
- 한 줄 뜻: AWS 계정의 모든 권한을 가진 최상위 사용자
- 왜 중요한가: 일상 작업에 사용하면 실수나 탈취의 피해 범위가 계정 전체로 커진다.
- 수업에서 다시 나오는 곳: Week 1 Day 4, Week 5 AWS
- 공식 참고: https://docs.aws.amazon.com/IAM/latest/UserGuide/id_root-user.html

### MFA
- 한 줄 뜻: Multi-Factor Authentication, 비밀번호 외 추가 인증
- 왜 중요한가: 비밀번호가 노출되어도 계정 탈취 위험을 줄이는 기본 보호 장치다.
- 수업에서 다시 나오는 곳: Week 1 Day 4, Week 5 AWS
- 공식 참고: https://docs.aws.amazon.com/IAM/latest/UserGuide/id_credentials_mfa.html

### Free Tier
- 한 줄 뜻: 신규 고객 크레딧과 일부 서비스 무료 사용량을 포함한 AWS 무료 사용 구조
- 왜 중요한가: 무조건 무료가 아니므로 크레딧, 계정 plan, 서비스별 사용량, 기간, 초과 비용을 확인해야 한다.
- 수업에서 다시 나오는 곳: Week 1 Day 4, Week 5 AWS
- 공식 참고: https://aws.amazon.com/free/

### AWS Credits
- 한 줄 뜻: AWS 사용 요금을 상쇄하는 계정 단위 크레딧
- 왜 중요한가: 현금이 아니며, 잔액과 만료, 적용 가능한 서비스와 사용량을 확인해야 한다.
- 수업에서 다시 나오는 곳: Week 1 Day 4, Week 5 AWS
- 공식 참고: https://docs.aws.amazon.com/awsaccountbilling/latest/aboutv2/free-tier-FAQ.html

### Billing
- 한 줄 뜻: 클라우드 사용량과 비용 청구를 확인하는 영역
- 왜 중요한가: 비용을 보지 못하면 안전한 실습과 운영 판단을 할 수 없다.
- 수업에서 다시 나오는 곳: Week 1 Day 4, Week 5 AWS
- 공식 참고: https://docs.aws.amazon.com/awsaccountbilling/latest/aboutv2/billing-what-is.html

### Shared Responsibility Model
- 한 줄 뜻: 클라우드 제공자와 사용자의 보안 책임 분담 모델
- 왜 중요한가: 관리형 서비스를 써도 계정, 데이터, 권한, 설정 책임은 사용자에게 남는다.
- 수업에서 다시 나오는 곳: Week 1 Day 4, Week 5 AWS
- 공식 참고: https://aws.amazon.com/compliance/shared-responsibility-model/

### Least Privilege
- 한 줄 뜻: 필요한 작업에 필요한 최소 권한만 부여하는 원칙
- 왜 중요한가: 실수나 침해가 발생했을 때 피해 범위를 줄인다.
- 수업에서 다시 나오는 곳: Week 1 Day 4, Week 5 AWS, Week 6 Terraform
- 공식 참고: https://docs.aws.amazon.com/IAM/latest/UserGuide/best-practices.html

## Local Execution And Web Basics

### CPU
- 한 줄 뜻: 명령을 계산하고 처리하는 장치
- 왜 중요한가: 요청 처리, 암호화, 압축, 데이터 계산의 병목을 이해한다.
- 수업에서 다시 나오는 곳: Week 1 Day 2, Week 4 Kubernetes requests/limits, Week 5 EC2
- 공식 참고: https://docs.aws.amazon.com/whitepapers/latest/aws-overview/compute-services.html

### Memory
- 한 줄 뜻: 실행 중인 데이터가 잠시 올라가는 공간
- 왜 중요한가: 애플리케이션 실행, 캐시, 프로세스 종료 원인을 이해한다.
- 수업에서 다시 나오는 곳: Week 1 Day 2, Week 2 Docker, Week 4 Kubernetes
- 공식 참고: https://docs.aws.amazon.com/whitepapers/latest/aws-overview/compute-services.html

### Disk
- 한 줄 뜻: 파일과 데이터를 저장하는 공간
- 왜 중요한가: 로그, 정적 파일, 데이터베이스, 볼륨의 바닥 개념이다.
- 수업에서 다시 나오는 곳: Week 1 Day 2, Week 2 Docker volume, Week 5 EBS/S3
- 공식 참고: https://docs.aws.amazon.com/whitepapers/latest/aws-overview/storage-services.html

### Process
- 한 줄 뜻: 실행 중인 프로그램
- 왜 중요한가: 웹 서버 실행, 포트 점유, 로그 출력, 종료 처리를 이해한다.
- 수업에서 다시 나오는 곳: Week 1 Day 2, Week 2 Docker container, Week 4 Pod
- 공식 참고: https://www.kernel.org/doc/man-pages/

### CLI
- 한 줄 뜻: Command Line Interface, 명령어로 컴퓨터를 조작하는 인터페이스
- 왜 중요한가: 서버 상태 확인, 자동화, Docker/Kubernetes/Terraform 명령의 기반이다.
- 수업에서 다시 나오는 곳: 전체 실습
- 공식 참고: https://www.gnu.org/software/coreutils/manual/coreutils.html

### HTTP
- 한 줄 뜻: 웹 요청과 응답을 주고받는 프로토콜
- 왜 중요한가: 브라우저 접속, API 호출, status code, 장애 분석의 기본이다.
- 수업에서 다시 나오는 곳: Week 1 Day 2, Week 3 MSA, Week 4 Ingress
- 공식 참고: https://developer.mozilla.org/en-US/docs/Web/HTTP/Guides/Overview

### DNS
- 한 줄 뜻: 도메인 이름을 IP 주소로 찾는 체계
- 왜 중요한가: 접속 실패가 이름 조회 문제인지 서버 문제인지 구분한다.
- 수업에서 다시 나오는 곳: Week 3 MSA, Week 4 Kubernetes DNS, Week 5 Route 53
- 공식 참고: https://developer.mozilla.org/en-US/docs/Learn/Common_questions/Web_mechanics/What_is_a_domain_name

### Port
- 한 줄 뜻: 한 컴퓨터 안에서 서비스 입구를 구분하는 번호
- 왜 중요한가: 로컬 서버, Docker port binding, Kubernetes Service를 이해한다.
- 수업에서 다시 나오는 곳: Week 1 Day 2, Week 2 Docker, Week 4 Kubernetes
- 공식 참고: https://www.iana.org/assignments/service-names-port-numbers/service-names-port-numbers.xhtml

### localhost
- 한 줄 뜻: 내 컴퓨터 자신을 가리키는 이름
- 왜 중요한가: 로컬 실행과 외부 접속 가능 상태를 구분한다.
- 수업에서 다시 나오는 곳: Week 1 Day 2, Week 2 Docker networking
- 공식 참고: https://developer.mozilla.org/en-US/docs/Web/HTTP/Guides/Overview

### Environment Variable
- 한 줄 뜻: 실행 시점에 주입하는 설정값
- 왜 중요한가: 이미지나 코드 안에 환경별 설정을 박아 넣지 않게 한다.
- 수업에서 다시 나오는 곳: Week 2 Docker, Week 4 Kubernetes ConfigMap/Secret, Week 6 Terraform
- 공식 참고: https://12factor.net/config

### Secret
- 한 줄 뜻: 노출되면 위험한 비밀번호, token, key 같은 민감정보
- 왜 중요한가: GitHub, Docker image, Terraform state에 잘못 남기면 보안 사고가 된다.
- 수업에서 다시 나오는 곳: Week 2 Docker, Week 4 Kubernetes Secret, Week 5 IAM
- 공식 참고: https://12factor.net/config

### stdout
- 한 줄 뜻: 프로그램의 일반 출력 통로
- 왜 중요한가: 컨테이너와 서버 로그 수집의 기본 출력 경로다.
- 수업에서 다시 나오는 곳: Week 1 Day 2, Week 2 Docker logs, Week 5 CloudWatch
- 공식 참고: https://www.gnu.org/software/coreutils/manual/coreutils.html

### Root Cause Analysis
- 한 줄 뜻: 증상 뒤의 실제 원인을 증거 기반으로 찾는 분석 과정
- 왜 중요한가: 재발 방지와 운영 기록을 만든다.
- 수업에서 다시 나오는 곳: Week 1 Day 2, 전체 장애 분석 실습
- 공식 참고: https://sre.google/sre-book/monitoring-distributed-systems/

## Application Architecture

### 3-tier Architecture
- 한 줄 뜻: 서비스를 화면/입구 계층, 애플리케이션 처리 계층, 데이터 저장 계층으로 나누어 보는 구조
- 왜 중요한가: 웹 앱, DB, 캐시, 로드 밸런서가 어디에 놓이는지 이해하는 기본 지도다.
- 수업에서 다시 나오는 곳: Week 1 Day 3, Week 3 MSA, Week 5 AWS
- 공식 참고: https://docs.aws.amazon.com/prescriptive-guidance/latest/patterns/build-a-three-tier-architecture-on-aws.html

### Load Balancer
- 한 줄 뜻: 들어온 요청을 여러 서버 중 적절한 대상으로 나누어 보내는 입구
- 왜 중요한가: 서버 한 대 장애나 트래픽 증가 상황에서 서비스 접속을 유지하는 핵심 컴포넌트다.
- 수업에서 다시 나오는 곳: Week 1 Day 3, Week 4 Kubernetes Ingress, Week 5 ALB
- 공식 참고: https://docs.aws.amazon.com/elasticloadbalancing/latest/userguide/what-is-load-balancing.html

### Application Server
- 한 줄 뜻: API, 인증, 업무 로직처럼 서비스의 실제 기능을 실행하는 서버
- 왜 중요한가: 인프라 엔지니어가 로그, 응답 시간, 오류율, 리소스 사용량을 함께 봐야 하는 중심 실행 지점이다.
- 수업에서 다시 나오는 곳: Week 1 Day 3, Week 2 Docker, Week 4 Kubernetes
- 공식 참고: https://12factor.net/processes

### Database
- 한 줄 뜻: 재시작 후에도 남아야 하는 데이터를 영속적으로 저장하는 시스템
- 왜 중요한가: 데이터 손실, 백업, 복구, 연결 수, 쿼리 성능은 서비스 안정성과 직접 연결된다.
- 수업에서 다시 나오는 곳: Week 1 Day 3, Week 3 MSA, Week 5 RDS
- 공식 참고: https://docs.aws.amazon.com/AmazonRDS/latest/UserGuide/Welcome.html

### Cache
- 한 줄 뜻: 자주 읽는 데이터를 더 빠르게 제공하기 위해 잠시 저장하는 계층
- 왜 중요한가: 응답 속도와 비용을 줄일 수 있지만, 오래된 데이터나 무효화 문제를 함께 관리해야 한다.
- 수업에서 다시 나오는 곳: Week 1 Day 3, Week 3 MSA, Week 5 ElastiCache
- 공식 참고: https://docs.aws.amazon.com/AmazonElastiCache/latest/dg/WhatIs.html

### Object Storage
- 한 줄 뜻: 이미지, 첨부파일, 백업처럼 파일 단위 객체를 저장하는 서비스
- 왜 중요한가: 앱 서버 디스크에 파일을 묶어두지 않아 확장, 복구, 배포를 더 단순하게 만든다.
- 수업에서 다시 나오는 곳: Week 1 Day 3, Week 5 S3
- 공식 참고: https://docs.aws.amazon.com/AmazonS3/latest/userguide/Welcome.html

## Cost And Cloud Economics

### CAPEX
- 한 줄 뜻: Capital Expenditure, 초기 투자 비용
- 왜 중요한가: 서버와 데이터센터를 직접 구매하는 방식의 비용 구조를 이해한다.
- 수업에서 다시 나오는 곳: Week 1 Day 1 Lesson 3, Week 5 FinOps
- 공식 참고: https://aws.amazon.com/economics/

### OPEX
- 한 줄 뜻: Operational Expenditure, 운영 중 계속 발생하는 비용
- 왜 중요한가: 클라우드는 사용량 기반 운영 비용 중심으로 비용 구조가 바뀐다.
- 수업에서 다시 나오는 곳: Week 1 Day 1 Lesson 3, Week 5 FinOps
- 공식 참고: https://aws.amazon.com/economics/

### TCO
- 한 줄 뜻: Total Cost of Ownership, 총소유비용
- 왜 중요한가: 서버 가격뿐 아니라 전력, 공간, 인력, 장애 대응, 폐기 비용까지 함께 본다.
- 수업에서 다시 나오는 곳: Week 1 Day 1 Lesson 3, Week 5 FinOps
- 공식 참고: https://aws.amazon.com/economics/

### ROI
- 한 줄 뜻: Return on Investment, 투자 대비 효과
- 왜 중요한가: 클라우드 전환이 비용, 속도, 안정성 측면에서 의미 있는지 판단한다.
- 수업에서 다시 나오는 곳: Week 1 Day 1 Lesson 3, Week 5 FinOps
- 공식 참고: https://aws.amazon.com/economics/

## DevOps

### DevOps
- 한 줄 뜻: 개발과 운영이 같은 목표로 빠르고 안정적인 전달을 만드는 문화와 실천
- 왜 중요한가: 이 과정의 모든 도구를 협업, 자동화, 관찰, 피드백 루프로 연결한다.
- 수업에서 다시 나오는 곳: Week 1 Day 1, Week 6 Terraform
- 공식 참고: https://aws.amazon.com/devops/what-is-devops/

### Deployment
- 한 줄 뜻: 소프트웨어 변경을 사용 가능한 환경에 반영하고 검증하는 절차
- 왜 중요한가: 단순 파일 복사가 아니라 실행, 설정, 로그, health check, 복구 기준을 포함한다.
- 수업에서 다시 나오는 곳: Week 1 Day 3, Week 4 Kubernetes rollout, Week 5 AWS
- 공식 참고: https://12factor.net/build-release-run

### Build
- 한 줄 뜻: 소스 코드를 실행 가능한 산출물로 만드는 과정
- 왜 중요한가: 배포 전에 문법, 의존성, 산출물 생성을 검증하는 단계다.
- 수업에서 다시 나오는 곳: Week 1 Day 3, Week 2 Dockerfile, Week 6 CI/IaC
- 공식 참고: https://12factor.net/build-release-run

### Artifact
- 한 줄 뜻: 빌드 결과로 만들어지는 배포 대상
- 왜 중요한가: 무엇을 배포했는지 추적해야 rollback과 장애 분석이 가능하다.
- 수업에서 다시 나오는 곳: Week 1 Day 3, Week 2 Docker image
- 공식 참고: https://12factor.net/build-release-run

### Reproducibility
- 한 줄 뜻: 같은 입력과 절차로 같은 결과를 다시 만들 수 있는 성질
- 왜 중요한가: Docker, Terraform, runbook이 모두 재현 가능성을 높이기 위한 도구다.
- 수업에서 다시 나오는 곳: Week 1 Day 3, Week 2 Docker, Week 6 Terraform
- 공식 참고: https://12factor.net/build-release-run

### IaC
- 한 줄 뜻: Infrastructure as Code, 인프라 구성을 코드로 기록하고 관리하는 방식
- 왜 중요한가: 수동 콘솔 작업을 리뷰, 반복, 추적 가능한 변경으로 바꾼다.
- 수업에서 다시 나오는 곳: Week 1 Day 3, Week 6 Terraform
- 공식 참고: https://developer.hashicorp.com/terraform/docs

### Docker Image
- 한 줄 뜻: 애플리케이션 실행에 필요한 파일과 환경을 묶은 읽기 전용 실행 재료
- 왜 중요한가: 실행 환경 차이를 줄이고 배포 단위를 명확히 한다.
- 수업에서 다시 나오는 곳: Week 1 Day 3, Week 2 Docker
- 공식 참고: https://docs.docker.com/get-started/docker-concepts/the-basics/what-is-an-image/

### Container
- 한 줄 뜻: image를 바탕으로 실행 중인 격리된 프로세스
- 왜 중요한가: Docker, Kubernetes Pod, 포트 바인딩, 로그 수집의 기본 실행 단위다.
- 수업에서 다시 나오는 곳: Week 1 Day 3, Week 2 Docker, Week 4 Kubernetes
- 공식 참고: https://docs.docker.com/get-started/docker-concepts/the-basics/what-is-a-container/

### Deployment Frequency
- 한 줄 뜻: 얼마나 자주 배포하는지 나타내는 지표
- 왜 중요한가: 배포 절차가 작고 안정적으로 반복되는지 보여준다.
- 수업에서 다시 나오는 곳: Week 1 Day 5, Week 4 Kubernetes rollout
- 공식 참고: https://cloud.google.com/devops

### Lead Time For Changes
- 한 줄 뜻: 변경이 운영 환경에 도달하기까지 걸리는 시간
- 왜 중요한가: 개발부터 배포까지 병목이 어디 있는지 보여준다.
- 수업에서 다시 나오는 곳: Week 1 Day 5, Week 6 Terraform
- 공식 참고: https://cloud.google.com/devops

### Change Failure Rate
- 한 줄 뜻: 변경이 장애를 만드는 비율
- 왜 중요한가: 배포 안정성과 검증 품질을 판단한다.
- 수업에서 다시 나오는 곳: Week 1 Day 5, Week 4 Kubernetes
- 공식 참고: https://cloud.google.com/devops

### Time To Restore Service
- 한 줄 뜻: 장애 후 서비스를 복구하는 데 걸리는 시간
- 왜 중요한가: 관찰 가능성, rollback, runbook의 효과를 보여준다.
- 수업에서 다시 나오는 곳: Week 1 Day 5, Week 5 Observability
- 공식 참고: https://cloud.google.com/devops

## Tools And Collaboration

### GitHub
- 한 줄 뜻: Git 저장소를 원격에서 관리하고 협업하는 서비스
- 왜 중요한가: 코드, README, 실습 기록, 장애 기록을 남기는 기본 협업 공간이다.
- 수업에서 다시 나오는 곳: Week 1 Day 1, 전체 실습
- 공식 참고: https://docs.github.com/

### Repository
- 한 줄 뜻: 코드와 문서, 변경 이력을 담는 저장소
- 왜 중요한가: 실습 산출물과 운영 기록을 한 곳에 모은다.
- 수업에서 다시 나오는 곳: Week 1 Day 1, Week 6 Terraform
- 공식 참고: https://docs.github.com/en/repositories

### VS Code
- 한 줄 뜻: 코드와 문서를 편집하고 터미널을 함께 쓰는 개발 도구
- 왜 중요한가: 실습 파일 작성, README 수정, 터미널 명령 실행의 기본 도구다.
- 수업에서 다시 나오는 곳: Week 1 Day 1, 전체 실습
- 공식 참고: https://code.visualstudio.com/docs

### Git
- 한 줄 뜻: 파일 변경 이력을 기록하고 되돌릴 수 있게 하는 버전 관리 도구
- 왜 중요한가: 인프라 코드와 문서 변경도 추적 가능하게 만든다.
- 수업에서 다시 나오는 곳: Week 1 Day 1, Week 6 Terraform
- 공식 참고: https://git-scm.com/book/en/v2

### Commit
- 한 줄 뜻: 변경 내용을 이유와 함께 저장한 기록
- 왜 중요한가: 누가, 언제, 왜 바꿨는지 운영 이력을 남긴다.
- 수업에서 다시 나오는 곳: Week 1 Day 1, Week 6 Terraform
- 공식 참고: https://docs.github.com/en/get-started/using-git/about-git

### Push
- 한 줄 뜻: 로컬 변경 기록을 원격 저장소에 올리는 작업
- 왜 중요한가: 개인 작업을 팀과 공유 가능한 상태로 만든다.
- 수업에서 다시 나오는 곳: Week 1 Day 1, 전체 실습
- 공식 참고: https://docs.github.com/en/get-started/using-git/pushing-commits-to-a-remote-repository

## AI-Assisted Learning And Work

### Prompt
- 한 줄 뜻: AI에게 전달하는 작업 요청 문장
- 왜 중요한가: 요구사항, 제약, 검증 기준을 어떻게 쓰느냐에 따라 답변 품질이 크게 달라진다.
- 수업에서 다시 나오는 곳: Week 1 Day 3, 전체 AI 보조 실습
- 공식 참고: https://platform.openai.com/docs

### Persona
- 한 줄 뜻: AI가 어떤 역할과 관점으로 답할지 정하는 설정
- 왜 중요한가: 초보자 설명, 인프라 엔지니어 관점, 비용 관점처럼 같은 개념을 다른 눈높이로 이해하게 한다.
- 수업에서 다시 나오는 곳: Week 1 Day 3, 전체 AI 보조 실습
- 공식 참고: https://docs.anthropic.com/en/docs/build-with-claude/prompt-engineering/overview

### Agent
- 한 줄 뜻: 특정 목적을 수행하도록 역할, 도구, 절차를 묶은 작업 단위
- 왜 중요한가: 로그 분석, 문서 검토, 코드 리뷰처럼 반복되는 일을 구조화할 수 있지만 권한 범위를 신중히 정해야 한다.
- 수업에서 다시 나오는 곳: Week 1 Day 3, Week 6 IaC 리뷰
- 공식 참고: https://docs.anthropic.com/en/docs/claude-code/sub-agents

### Skill
- 한 줄 뜻: 반복 작업에 필요한 절차, 기준, 예시를 재사용 가능하게 묶은 지침
- 왜 중요한가: 공식 문서 확인, 제약 정리, 실습 체크리스트처럼 반복 품질을 높이는 데 도움이 된다.
- 수업에서 다시 나오는 곳: Week 1 Day 3, 전체 실습 문서화
- 공식 참고: https://docs.anthropic.com/en/docs/claude-code/skills

### Cross Check
- 한 줄 뜻: AI 답변이나 판단을 다른 근거로 다시 확인하는 과정
- 왜 중요한가: 인프라 변경은 비용, 보안, 장애 영향이 크므로 공식 문서, 강사, 전문가, 팀 합의로 검증해야 한다.
- 수업에서 다시 나오는 곳: Week 1 Day 3, Week 5 AWS, Week 6 Terraform
- 공식 참고: https://docs.aws.amazon.com/wellarchitected/latest/framework/welcome.html

### Dummy JSON
- 한 줄 뜻: 데이터베이스나 외부 API 없이 화면 데이터를 표현하기 위해 준비한 로컬 JSON 파일
- 왜 중요한가: 비용, 계정, 네트워크, API key 문제 없이 프론트엔드 기능과 데이터 구조를 먼저 검증하게 한다.
- 수업에서 다시 나오는 곳: Week 1 Day 3, Week 2 Docker static app, Week 3 MSA API contract
- 공식 참고: https://developer.mozilla.org/en-US/docs/Learn/JavaScript/Objects/JSON
