# Week 1: Cloud Native를 위한 컴퓨팅 펀더멘털과 운영 증거

## Overview
1주차는 Docker, Kubernetes, AWS, Terraform을 바로 실습하기 전에 필요한 컴퓨팅 좌표계를 만든다. 학생은 도구 이름을 먼저 외우지 않고, 서비스가 실행되는 조건과 운영 증거를 먼저 배운다.

이번 주의 중심 질문은 다음과 같다.

```text
내 로컬 컴퓨터에서 실행되는 작은 서비스는 compute, memory, storage, network, configuration, identity, observability 관점에서 어떻게 설명되는가?
```

## 처음이면 여기부터
수업을 시작하기 전에 GitHub 계정, Git, VS Code, Python 3, curl이 준비되어야 한다. 설치가 막히면 혼자 추측하지 말고 OS, 실행한 명령, 에러 메시지, 확인한 공식 문서 URL을 기록한다.

- macOS/Linux A-to-Z 설치 절차: [필수 소프트웨어 설치 가이드](https://raw.githubusercontent.com/niceguy61/kdt_devops_lecture_2026_rev2/main/docs/software-installation-guide.md)
- Week 1 최소 확인 명령: `git --version`, `python3 --version`, `curl -I https://example.com`
- VS Code는 `code --version`이 실패해도 VS Code 안의 terminal에서 `pwd`와 `git --version`이 되면 진행 가능하다.
- password, token, MFA code, verification code는 README와 스크린샷에 남기지 않는다.

## 학습 목표
- Cloud Native와 DevOps를 도구 목록이 아니라 운영 가능한 서비스를 만드는 관점으로 설명한다.
- compute, memory, storage, network, process lifecycle, configuration, identity/access, observability, cost/resource boundary를 구분한다.
- 로컬 웹 서비스를 실행하고 command, port, HTTP status, log, file path로 증거를 남긴다.
- GitHub, Git, VS Code, README를 이용해 다른 사람이 재현 가능한 handoff 문서를 만든다.
- 작은 정적 웹앱과 더미 JSON을 만들고, 비용/보안/재현성 위험을 기록한다.
- Week 2~5의 Docker, MSA, Kubernetes, AWS, Terraform 개념을 Week 1 컴퓨팅 spine에 연결한다.

## Schedule Index
- Day 1: 과정별 OT, 5주 로드맵, Cloud Native/DevOps 마인드셋, 아이스브레이킹, 학습 준비
- Day 2: 컴퓨팅 구성요소 spine, Linux/CLI, process, filesystem, network, HTTP, log/config/secret
- Day 3: 로컬 정적 서버 실행 조건, 재현성, 관찰 가능성, RCA, AI 보조 개발 검증, AI 정적 웹사이트 챌린지
- 4일차: 국내 IT 기업 사례로 현대 애플리케이션 구성요소, 비즈니스 증가 압력, 운영 challenge, Docker 필요성 이해
- 5일차: 로컬 환경 설치/버전/포트/설정/삭제 시나리오로 Docker 필요성 빌드업, 비공식 미니 공유
- 6일차: 첫 1:1 멘토링, 환경 회복, 용어 회복, 작은 성공 경험, Week2 Docker 준비도 점검

## Computing Component Spine
![Week 1 computing component spine](https://raw.githubusercontent.com/niceguy61/kdt_devops_lecture_2026_rev2/main/week1/assets/week1-computing-spine.png)

| Component | Week 1 local evidence | Week 2 Docker | Week 4 Kubernetes | Week 5 AWS + Terraform/IaC |
|---|---|---|---|---|
| Compute | process, command, exit code | container process | Pod, Deployment | EC2, ECS, Lambda, compute resource |
| Memory | process memory note | memory limit | requests/limits | instance memory, variable |
| Storage | file path, data path | image layer, volume | Volume, ConfigMap mount | S3, EBS, EFS, RDS, bucket/volume/db resource |
| Network | localhost, port, HTTP status | port binding, bridge | Service, Ingress | VPC, SG, ALB, Route 53, VPC/SG resource |
| Lifecycle | start/stop/recheck | run/stop/restart | rollout/probe | service scaling, plan/apply/destroy |
| Configuration | env var, config file | `-e`, `.env` | ConfigMap, Secret | Parameter Store, variable/sensitive |
| Identity/access | account, permission, token risk | registry auth | ServiceAccount/RBAC | IAM/MFA/role, provider/IAM |
| Observability | log, status, RCA | logs/inspect/stats | logs/events/probes | CloudWatch/CloudTrail, output/drift |
| Cost boundary | local limits, excluded paid API | running resource count | node capacity | billing/budget, cost assumption |

## Official And Academic Foundations
- ABET Criteria for Accrediting Computing Programs, Student Outcomes  
  https://www.abet.org/accreditation/accreditation-criteria/criteria-for-accrediting-computing-programs-2025-2026/
- ACM/IEEE-CS/AAAI CS2023 Final Report  
  https://csed.acm.org/final-report/
- NIST NICE Workforce Framework  
  https://www.nist.gov/itl/applied-cybersecurity/nice/nice-cybersecurity-workforce-framework
- Vanderbilt Center for Teaching: Bloom's Taxonomy  
  https://cft.vanderbilt.edu/guides-sub-pages/blooms-taxonomy/
- AWS: What is DevOps?  
  https://aws.amazon.com/devops/what-is-devops/
- Google SRE Book: Postmortem Culture  
  https://sre.google/sre-book/postmortem-culture/
- GitHub Docs: About README files  
  https://docs.github.com/en/repositories/managing-your-repositorys-settings-and-features/customizing-your-repository/about-readmes
- MDN Web Docs: An overview of HTTP  
  https://developer.mozilla.org/en-US/docs/Web/HTTP/Guides/Overview

## Required Deliverables
- GitHub repository URL
- `README.md` with start/check/stop/troubleshoot sections
- Static frontend mini app
- `data/*.json` dummy data file
- Computing spine mapping note
- AI verification note
- One RCA record
- Risk classification table
- Week2 Docker 준비 note

## Assessments
- [Week 1 객관식 문제 세트](https://raw.githubusercontent.com/niceguy61/kdt_devops_lecture_2026_rev2/main/week1/assessments/week1-multiple-choice-questions.md)
- [Week 1 Foundations Scorecard](https://raw.githubusercontent.com/niceguy61/kdt_devops_lecture_2026_rev2/main/week1/assessments/week1-foundations-scorecard.md)

## Glossary
1주차 용어는 [glossary.md](https://raw.githubusercontent.com/niceguy61/kdt_devops_lecture_2026_rev2/main/week1/glossary.md)를 기준으로 정리한다. 처음 읽을 때는 정의를 외우기보다 각 용어가 어떤 command, output, path, URL evidence로 확인되는지 함께 본다.

## Week 1 Boundaries
- Docker command practice starts in Week 2.
- AWS account creation and cloud resources start in Week 5.
- Well-Architected is taught as an architecture-risk framework in Week 5.
- DORA metrics are taught when deployment/operation evidence is concrete enough, later in the course.
- Week 1 may mention those terms only as future anchors mapped to the computing spine.

## Visual Asset Plan
| Asset | Use | Source |
|---|---|---|
| ![Local service evidence flow](https://raw.githubusercontent.com/niceguy61/kdt_devops_lecture_2026_rev2/main/week1/assets/week1-service-evidence-flow.png) | Day 2~3 command, process, port, HTTP, log, README, RCA evidence flow | imagegen generated asset |
| ![Week 1 to Docker preview mapping](https://raw.githubusercontent.com/niceguy61/kdt_devops_lecture_2026_rev2/main/week1/assets/week1-docker-preview-mapping.png) | Day5 Docker preview mapping - 로컬 실행 문제가 Docker 구성요소로 확장되는 흐름 | imagegen generated asset |
| `assets/week1-computing-spine.png` | Week 1 component spine mapped to later platforms | imagegen generated asset |

Official diagrams may be linked with attribution when a later week introduces Docker, Kubernetes, AWS, or Terraform in depth.
