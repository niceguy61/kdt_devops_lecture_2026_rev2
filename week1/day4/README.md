# Week 1 Day 4: 클라우드 기본 구성요소, AWS 계정, 비용/보안, 공식 문서 읽기

## Overview
4일차는 로컬 컴퓨터와 미니 웹앱에서 배운 실행 조건을 클라우드의 기본 구성요소로 확장한다. 오늘의 목표는 AWS 서비스를 많이 생성하는 것이 아니라, 클라우드 리소스를 만들기 전에 반드시 확인해야 하는 위치, 권한, 비용, 보안, 공식 문서 기준을 세우는 것이다.

클라우드는 필요한 자원을 빠르게 빌려 쓰게 해 주지만, 잘못 켜 둔 리소스, 과한 권한, 노출된 secret, 확인하지 않은 리전 선택은 실제 비용과 보안 사고로 이어질 수 있다. 그래서 1주차 4일차는 계정 생성과 콘솔 탐색을 하더라도 "무엇을 만들 수 있는가"보다 "무엇을 만들기 전에 어떤 증거를 확인해야 하는가"에 초점을 둔다.

![4일차 클라우드 안전 지도](./assets/week1-day4-overview.png)

## Learning Goals
- Region, Availability Zone, Compute, Storage, Network, IAM을 클라우드 운영의 기본 지도 안에서 설명한다.
- IaaS, PaaS, SaaS, Managed Service, Shared Responsibility Model의 차이를 운영 책임 관점에서 구분한다.
- AWS 계정 생성 전 확인할 과금 구조, Free Tier, 결제 수단, MFA, root 계정 주의사항을 설명한다.
- AWS 콘솔 로그인, MFA 설정, Billing 접근 확인, 비용 알림 확인 흐름을 따라간다.
- CAPEX, OPEX, TCO, ROI와 사용량 기반 과금의 차이를 간단한 계산으로 비교한다.
- 최소 권한, secret 관리, 공식 문서 검증, AI 답변 크로스체크를 실습 전 습관으로 만든다.
- AWS 계정, MFA, Billing, Docker 실행 상태를 개인별로 점검하고 문제를 기록한다.
- 만들고 싶은 서비스 아이디어를 필요한 리소스, 비용 위험, 보안 위험, 1주차 범위 조정 관점에서 정리한다.

## Lesson Index
- 1교시: 클라우드 기본 구성 요소 - Region, AZ, Compute, Storage, Network, IAM의 큰 그림
- 2교시: 클라우드 서비스 모델 - IaaS, PaaS, SaaS, Managed Service, Shared Responsibility Model
- 3교시: AWS 계정 생성 전 안내 - 과금 구조, Free Tier, 결제 수단, MFA, root 계정 주의사항
- 4교시: AWS 계정 생성 및 보안 기본 설정 - 계정 생성, MFA 설정, Billing 알림 확인, 콘솔 로그인
- 5교시: 클라우드 비용 관리 기본 - 데이터센터 비용과 클라우드 비용 비교, 사용량 기반 과금, 낭비 사례
- 6교시: 보안 기본 원칙과 공식 Documentation 읽는 법 - 최소 권한, secret 관리, AI 답변 검증, 버전과 전제 조건 확인
- 7교시: 개인 면담 및 환경 점검 - AWS 계정, MFA, Billing 알림, Docker 실행 상태 확인
- 8교시: 프로젝트 아이디어 면담 - 만들고 싶은 서비스, 필요한 리소스, 예상 위험 요소 정리

## Official References
- AWS Documentation: What is cloud computing?
  https://docs.aws.amazon.com/whitepapers/latest/aws-overview/what-is-cloud-computing.html
- AWS Documentation: Regions and Availability Zones
  https://docs.aws.amazon.com/AWSEC2/latest/UserGuide/using-regions-availability-zones.html
- AWS Documentation: AWS global infrastructure
  https://docs.aws.amazon.com/whitepapers/latest/aws-overview/global-infrastructure.html
- AWS Documentation: Security best practices in IAM
  https://docs.aws.amazon.com/IAM/latest/UserGuide/best-practices.html
- AWS Documentation: AWS account root user
  https://docs.aws.amazon.com/IAM/latest/UserGuide/id_root-user.html
- AWS Documentation: Multi-factor authentication in IAM
  https://docs.aws.amazon.com/IAM/latest/UserGuide/id_credentials_mfa.html
- AWS Billing and Cost Management User Guide
  https://docs.aws.amazon.com/awsaccountbilling/latest/aboutv2/billing-what-is.html
- AWS Free Tier
  https://aws.amazon.com/free/
- AWS Pricing Calculator
  https://calculator.aws/
- AWS Well-Architected Framework: Security pillar
  https://docs.aws.amazon.com/wellarchitected/latest/security-pillar/welcome.html
- AWS Well-Architected Framework: Cost Optimization pillar
  https://docs.aws.amazon.com/wellarchitected/latest/cost-optimization-pillar/welcome.html
- AWS Shared Responsibility Model
  https://aws.amazon.com/compliance/shared-responsibility-model/

## Today's Key Terms
- Region: 클라우드 리소스가 배치되는 지리적 지역
- Availability Zone: 한 Region 안에서 분리된 데이터센터 묶음
- Compute: 애플리케이션을 실행하는 계산 자원
- Storage: 데이터를 저장하는 자원
- Network: 요청과 응답이 이동하는 통신 경로
- IAM: AWS 리소스 접근 권한을 관리하는 서비스
- Root User: AWS 계정의 최고 권한 사용자
- MFA: 비밀번호 외 추가 인증 요소
- Free Tier Credits: 신규 고객에게 제공될 수 있는 AWS 사용 크레딧
- Always Free: 일부 서비스가 제공하는 월별 무료 사용량 또는 상시 무료 범위
- Billing: 사용량과 비용 청구를 확인하는 영역
- Shared Responsibility Model: 클라우드 제공자와 사용자의 보안 책임 분담 모델
- Least Privilege: 필요한 작업에 필요한 최소 권한만 부여하는 원칙
- CAPEX: 초기 투자 비용
- OPEX: 운영 중 계속 발생하는 비용

자세한 용어 정리는 [Week 1 Glossary](../glossary.md)를 참고한다.

## Setup And Permissions
오늘은 AWS 계정과 보안 설정을 확인하지만, 원칙적으로 비용이 발생하는 리소스 생성 실습은 하지 않는다. 학생 개인 상황에 따라 계정 생성이 이미 완료되었을 수도 있고, 결제 수단 인증 또는 보호자/회사 승인 때문에 오늘 완료하지 못할 수도 있다. 완료 여부보다 중요한 것은 비용과 보안 기준을 이해하고, 완료하지 못한 항목을 정확히 기록하는 것이다.

필요한 준비:
- 개인 이메일 또는 교육용 이메일
- 휴대폰 인증 가능 상태
- MFA 앱 또는 passkey 사용 가능 환경
- 결제 수단 준비 여부 확인
- 브라우저에서 AWS Console 접속 가능
- Docker Desktop 실행 상태 확인 가능

## Required Files And Assets
- `lesson-01.md`: 클라우드 기본 구성요소
- `lesson-02.md`: 클라우드 서비스 모델과 책임 분담
- `lesson-03.md`: AWS 계정 생성 전 과금/보안 안내
- `lesson-04.md`: AWS 계정 생성 및 보안 기본 설정
- `lesson-05.md`: 클라우드 비용 관리 기본
- `lesson-06.md`: 보안 원칙과 공식 문서 읽는 법
- `lesson-07.md`: 개인 면담 및 환경 점검
- `lesson-08.md`: 프로젝트 아이디어 면담
- `assets/week1-day4-overview.png`: 4일차 클라우드 안전 지도 인포그래픽
- `assets/lesson-02-service-model-overview.png`: IaaS, PaaS, SaaS, Managed Service 책임 경계 오버뷰
- `assets/lesson-02-platform-permission-control.png`: 플랫폼별 권한 제어와 책임 범위 다이어그램

## Deliverables
- 클라우드 기본 구성요소 매핑표
- 서비스 모델별 책임 분담 표
- AWS 계정 생성 전 체크리스트와 Free plan/Paid plan 확인 기록
- MFA와 Billing 접근 확인 기록
- 교육용 비용 계산 예제와 낭비 리소스 점검표
- 공식 문서 검증 기록
- 개인 환경 점검표
- 프로젝트 아이디어 리소스/비용/보안 위험 분석표

## End-Of-Day Checklist
- Region과 AZ의 차이를 설명할 수 있다.
- Compute, Storage, Network, IAM이 어떤 운영 문제와 연결되는지 말할 수 있다.
- IaaS, PaaS, SaaS, Managed Service에서 사용자가 책임지는 범위가 달라짐을 설명할 수 있다.
- AWS root user를 일상 작업에 쓰지 않아야 하는 이유를 설명할 수 있다.
- MFA가 설정되었는지 확인하거나, 설정하지 못한 이유와 다음 조치를 기록했다.
- Billing 또는 비용 확인 화면 접근 가능 여부를 확인했다.
- AWS 신규 고객 크레딧과 일부 서비스의 무료 사용량이 "무조건 무료"와 다르다는 점을 설명할 수 있다.
- 클라우드 비용을 시간당 비용, 월 비용, 유휴 리소스 비용으로 계산할 수 있다.
- AI 답변을 공식 문서의 전제 조건, 날짜, 리전, 서비스명으로 검증할 수 있다.
- 만들고 싶은 프로젝트의 필요한 리소스와 비용/보안 위험을 1차로 줄여 설명할 수 있다.
