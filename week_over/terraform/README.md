# Terraform 보강 과정: 재현 가능한 AWS 인프라 운영

## Overview

이 과정은 Week 5에서 AWS Console로 만들고 관찰한 리소스를 Terraform 코드로 재현하는 5일 보강 수업이다. Terraform 명령을 외우는 데 그치지 않고 공식 문서에서 리소스 명세를 찾고, 실행 계획과 State를 근거로 변경 위험을 판단하며, 기존 리소스를 안전하게 코드 관리 대상으로 편입하는 데 초점을 둔다.

수업은 하루 2교시로 운영한다. 각 교시는 50분이며 교시 사이에 10분 휴식을 둔다. 전체 운영 시간은 10시간이고 실제 수업 시간은 500분이다.

## Learning Goals

- IaC와 Terraform의 적용 범위, 장점, 한계와 운영 위험을 설명한다.
- HashiCorp Developer와 Terraform Registry에서 Provider, Resource, Data Source, Module 명세를 찾는다.
- HCL의 타입, 표현식, 함수, 조건, 반복 기능을 사용해 재사용 가능한 구성을 작성한다.
- Resource 주소, 의존성, Module, State의 관계를 설명하고 Plan의 변경 영향을 판독한다.
- Remote Backend의 저장, 접근 제어, 암호화, Locking, 복구 요구사항을 평가한다.
- 기존 AWS 리소스를 선언적 `import` 블록으로 편입하고 변경 없는 Plan 또는 설명 가능한 Plan을 만든다.

## Prerequisites And Scope

- Week 5의 AWS Region, VPC, Subnet, Security Group, EC2, S3 기본 개념을 알고 있어야 한다.
- Git의 add, commit, diff와 터미널 기본 명령을 사용할 수 있어야 한다.
- 실습 Region은 기본적으로 `ap-northeast-2`를 사용한다.
- Terraform은 AWS 자체를 대신 학습하는 도구가 아니라 이미 이해한 리소스를 재현하고 변경하는 도구로 다룬다.
- Custom Provider 개발, Terraform Plugin Framework, 대규모 HCP Terraform 운영은 심화 범위로 둔다.

## Schedule Index

| 일차 | 1교시 | 2교시 | 핵심 산출물 |
|---|---|---|---|
| [Day 1](./day1/README.md) | IaC와 Terraform의 정의·범위·주의점 | 설치와 Write–Plan–Apply 생명주기 | IaC 판단표, 최초 Plan과 정리 evidence |
| [Day 2](./day2/README.md) | 공식 문서와 Registry 탐색 | 주요 블록과 객체 모델 | 문서 탐색표, 객체 관계도 |
| [Day 3](./day3/README.md) | 변수·타입·표현식·함수 | `for`, `for_each`, `count`, `dynamic` | 타입 기반 변수, 반복 생성 코드 |
| [Day 4](./day4/README.md) | Module과 안전한 리팩터링 | State와 Remote Backend | Local Module, State 복구 Runbook |
| [Day 5](./day5/README.md) | Import 조사와 설계 | Import 실행과 코드 정합화 | Import 코드, 최종 Plan, handoff 문서 |

## Course Deliverables

- Terraform 공식 문서 탐색 워크시트
- 재사용 가능한 Terraform Root/Child Module
- `fmt`, `validate`, `plan` 검증 기록
- State 및 Backend 보안·복구 점검표
- 기존 AWS 리소스 Import 전후 evidence
- 비용, 보안, 권한, 변경 위험을 포함한 운영 인수인계 문서
- [위험 민감 리소스 관리 가이드](./risk-sensitive-resources.md)를 이용한 Resource/Data Source/Import 소유권 판단표
- [GitOps Drift 탐지와 제한적 자동 복구](./drift-remediation-guide.md) 설계 및 Slack 운영 보고서
- [EKS + IRSA 실제 생성·검증·삭제 핸즈온](./eks-hands-on/README.md)

## Environment And Safety

- Terraform과 AWS Provider 버전을 파일에 명시하고 `.terraform.lock.hcl`을 버전 관리한다.
- `.terraform/`, `*.tfstate`, 저장된 Plan, 인증정보는 Git에 올리지 않는다.
- AWS root user와 장기 Access Key 사용을 피하고 실습용 최소 권한 자격증명을 사용한다.
- 모든 `apply` 전 Plan에서 create, update, replace, destroy 수를 확인한다.
- 비용이 발생하는 리소스는 공통 Tag, 종료 시각, 삭제 책임자를 기록한다.
- State 조작과 Backend 이전 전에는 복구 가능한 백업과 Rollback 절차를 준비한다.

## Lesson Writing And Visual Contract

이 과정의 모든 `lesson-*.md`는 학생에게 직접 설명하는 자연스러운 구어체로 작성한다. 문장은 짧고 분명하게 쓰되 용어의 정확성은 공식 문서에 맞춘다. 같은 정의나 주의사항을 제목만 바꿔 반복하지 않으며, 앞에서 설명한 내용은 다음 활동에서 관찰·판단·복구로 발전시킨다.

각 50분 세션에는 다음 세 가지 시각 요소를 **각각 최소 1개** 포함한다.

| 필수 요소 | 최소 기준 | 용도 | 인정하지 않는 형태 |
|---|---:|---|---|
| 표 | 1개 | 비교, 의사결정, 명령 결과, 위험 분류 중 하나를 학생이 판단하는 데 사용 | 목차나 시간표만 옮긴 표 |
| Mermaid | 1개 | 의존성, 상태 변화, 실행 흐름, 장애 분석처럼 관계가 중요한 내용을 표현 | 본문과 연결되지 않은 장식용 흐름도 |
| imagegen 이미지 | 1개 | 개념을 기억하거나 복잡한 구조를 한눈에 파악하도록 돕는 래스터 학습 이미지 | SVG, 글자만 많은 포스터, 세션 일정표 |

imagegen 결과물은 PNG, WebP 또는 JPG 같은 래스터 이미지로 해당 Day의 `assets/`에 저장한다. SVG 인포그래픽은 imagegen 필수 이미지 수에 포함하지 않는다. 이미지 본문에는 정확한 명령, 버전, 긴 코드, URL처럼 생성 과정에서 깨지기 쉬운 텍스트를 넣지 않는다.

모든 시각 요소 바로 아래에는 다음 내용을 짧게 적는다.

- 무엇부터 어떤 순서로 볼 것인지
- 이 시각 요소가 설명하는 개념이나 판단이 무엇인지
- 생성 이미지라면 파일 경로와 생성 목적

### Conversational Tone Rules

- 학생에게 `이제 Plan을 같이 읽어보겠습니다`처럼 직접 안내하는 자연스러운 문장을 사용한다.
- `매우 중요합니다`, `핵심입니다`, `반드시 기억하세요` 같은 강조 문구를 반복하지 않는다.
- 정의를 나열한 뒤 다시 같은 내용을 요약하지 않는다. 정의 다음에는 예제, 관찰 결과, 실패 증상 또는 선택 기준으로 넘어간다.
- AI가 자주 사용하는 추상적인 도입과 결론 대신 실제 파일, 명령, 상태, 판단 근거를 말한다.
- 친근하게 설명하되 반말, 과도한 유행어, 불필요한 농담은 사용하지 않는다.
- 학생용 `lesson-*.md`에는 `50분 진행`, `0~10분` 같은 분 단위 운영표를 넣지 않는다. 시간 배분은 Day README 또는 내부 제작 계획에서만 관리한다.

### Per-Lesson Visual Gate

lesson 하나라도 다음 조건을 만족하지 못하면 완성으로 처리하지 않는다.

- 학습 목적이 있는 표가 1개 이상 있는가?
- 렌더링 가능한 Mermaid가 1개 이상 있는가?
- 실제로 존재하고 눈으로 검수한 PNG/WebP/JPG imagegen asset이 1개 이상 있는가?
- 세 시각 요소가 본문 설명이나 활동에서 직접 참조되는가?
- 이미지의 글자가 깨지지 않고 개념적으로 잘못된 연결이 없는가?
- 동일한 내용을 표, Mermaid, 이미지에 단순 복제하지 않았는가?

## Official References

| 주제 | 공식 문서 |
|---|---|
| Terraform 개요 | https://developer.hashicorp.com/terraform/intro |
| Terraform Language | https://developer.hashicorp.com/terraform/language |
| Providers | https://developer.hashicorp.com/terraform/language/providers |
| Expressions | https://developer.hashicorp.com/terraform/language/expressions |
| Meta-arguments | https://developer.hashicorp.com/terraform/language/meta-arguments |
| Modules | https://developer.hashicorp.com/terraform/language/modules |
| State | https://developer.hashicorp.com/terraform/language/state |
| Backend | https://developer.hashicorp.com/terraform/language/backend |
| Import | https://developer.hashicorp.com/terraform/language/import |
| Registry | https://registry.terraform.io/ |

## Next Step

각 Day는 두 개의 50분 lesson과 실습 자료로 확장한다. Day 1부터 개념, 공식 근거, 실습, 실패 재현, 복구, evidence, 혼자 다시 따라오기를 포함한 학생용 교안을 작성한다. 각 lesson은 위 Visual Contract에 따라 표, Mermaid, imagegen 래스터 이미지를 각각 최소 1개 포함한다.
