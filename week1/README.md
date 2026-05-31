# Week 1: Cloud Native 기본기와 운영 마인드셋

## Overview
1주차는 Cloud Native 과정을 시작하기 위한 공통 언어를 만든다. 학생은 Docker, Kubernetes, AWS, Terraform을 바로 배우기 전에 컴퓨터, 네트워크, 스토리지, 프로세스, 포트, 로그, 비용, 보안, 협업 문서가 왜 중요한지 이해해야 한다.

이번 주의 핵심은 "도구를 많이 아는 사람"이 아니라 "서비스를 운영 가능한 상태로 만들고 설명할 수 있는 주니어 인프라/DevOps 엔지니어"가 되는 것이다.

## Learning Goals
- Cloud Native를 배우는 이유와 DevOps 엔지니어의 역할을 설명한다.
- 로컬 컴퓨터에서 웹 서비스가 실행되고 접속되는 기본 흐름을 설명한다.
- GitHub, VS Code, Docker, AI Coding Tool 계정 생성, 설치, 로그인, 기본 동작 확인을 완료한다.
- 간단한 웹 애플리케이션을 만들고, 로컬 또는 Docker 환경에서 실행한다.
- 로그, 포트, 프로세스, HTTP 요청을 이용해 기본적인 문제 원인 분석을 수행한다.
- 비용, 보안, 공식 문서, 운영 지표를 기술 선택의 일부로 바라본다.

## Keywords
- cloud native
- devops
- cloud
- datacenter
- linux
- network
- git
- github
- vscode
- ai coding tool
- observability
- cost
- security

## Schedule Index
- Day 1: 오리엔테이션, Cloud Native/DevOps 마인드셋, GitHub/VS Code/Git 환경 준비
- Day 2: 컴퓨팅, Linux/CLI, HTTP, 포트, 로그, 원인 분석 기본기
- Day 3: 배포, Docker 필요성, AI Coding Tool 실습, 미니 웹앱 시작
- Day 4: 클라우드 기본 구성요소, AWS 계정, 비용/보안, 공식 문서 읽기
- Day 5: Well-Architected, DORA, 통합 체크리스트, 미니 챌린지 발표

## Deliverables
- GitHub 저장소 1개
- README.md 1개
- 브라우저에서 실행 가능한 미니 웹 애플리케이션 1개
- 로컬 실행 명령 또는 Docker 실행 명령
- 간단한 장애 분석 기록 1개
- 2주차 Docker 학습 전 개인 체크리스트

## Required Environment
- GitHub 계정
- Git
- Visual Studio Code
- 터미널 또는 shell
- Docker Desktop
- 브라우저 개발자 도구
- AI Coding Tool 계정 또는 사용 가능 환경
- AWS 계정과 MFA

## Official References
- GitHub Docs: Getting started with your GitHub account  
  https://docs.github.com/en/get-started/onboarding/getting-started-with-your-github-account
- GitHub Docs: Set up Git  
  https://docs.github.com/en/get-started/git-basics/set-up-git
- Visual Studio Code Docs: Getting started  
  https://code.visualstudio.com/docs/getstarted/getting-started
- Visual Studio Code Docs: Setup overview  
  https://code.visualstudio.com/docs/setup/setup-overview
- AWS: What is DevOps?  
  https://aws.amazon.com/devops/what-is-devops/
- AWS Documentation: What is cloud computing?  
  https://docs.aws.amazon.com/whitepapers/latest/aws-overview/what-is-cloud-computing.html
- AWS Well-Architected Framework: The pillars of the framework  
  https://docs.aws.amazon.com/wellarchitected/latest/framework/the-pillars-of-the-framework.html

## Glossary
- [Week 1 Glossary](./glossary.md)

이번 주 핵심 용어는 Cloud Native, Cloud Computing, Compute, Network, Storage, DevOps, Deployment, Build, Docker Image, Container, GitHub, Git, CAPEX, OPEX, TCO다. 각 교안에서는 용어가 처음 나올 때 짧은 뜻을 함께 적고, 자세한 복습은 glossary에서 한다.

## Cost And Security Notes
- 1주차에는 원칙적으로 비용이 발생하는 클라우드 리소스를 만들지 않는다.
- AWS 계정 생성 시 MFA를 반드시 설정하고 root 계정 사용을 최소화한다.
- GitHub 공개 저장소에 API key, password, token, 개인 정보, 과금 정보가 포함되지 않도록 한다.
- 설치와 계정 생성 중 생기는 오류는 수업의 문제 해결 훈련으로 다룬다.

## Connection To Week 2
1주차의 산출물과 실행 명령은 2주차 Docker 실습의 기반이 된다. 특히 README, 실행 명령, 로그 확인, 포트 개념은 Dockerfile과 Compose를 이해하기 위한 전제다.
