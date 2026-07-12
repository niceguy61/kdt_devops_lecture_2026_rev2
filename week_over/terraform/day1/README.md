# Terraform Day 1: IaC와 Terraform 실행 생명주기

## Overview

첫날은 Terraform 명령보다 Terraform이 해결하려는 운영 문제를 먼저 다룬다. 수동 변경과 IaC를 비교하고 Terraform Core, Provider, API, State의 경계를 잡은 뒤 작은 로컬 리소스로 Write–Plan–Apply–Destroy 흐름을 완주한다.

## Learning Goals

- 선언형 IaC와 수동·명령형 자동화의 차이를 사례로 설명한다.
- Terraform의 사용 범위와 사용하지 말아야 할 작업을 분류한다.
- `init`, `fmt`, `validate`, `plan`, `apply`, `show`, `destroy`의 목적을 설명하고 실행한다.
- Plan에서 생성, 수정, 교체, 삭제 위험을 식별한다.

## Lesson Index

| 교시 | 주제 | 50분 흐름 | 산출물 |
|---|---|---|---|
| 1교시 | IaC와 Terraform의 정의·범위·특장점·주의점 | 문제 사례 10분, 동작 모델 15분, 비교·판단 15분, 정리 10분 | IaC 적용 판단표, 위험 분류표 |
| 2교시 | 설치와 Write–Plan–Apply 생명주기 | 환경 확인 10분, 코드 작성 10분, 실행 20분, 관찰·정리 10분 | 최초 Plan, 실행 로그, cleanup evidence |

## Core Terms

IaC, declarative, imperative, provider, resource, desired state, plan, apply, dependency graph, idempotency

## Practice Files

- `lesson-01.md`: IaC와 Terraform 운영 모델
- `lesson-02.md`: CLI 생명주기 실습
- `academic-foundations.md`: 공식 문서와 학술·직무 성과 연결
- `labs/cli-lifecycle/`: 외부 Provider와 클라우드 비용이 없는 CLI 생명주기 실습
- `assets/lesson-01-terraform-operating-model.png`: 코드·Plan·실제 인프라 운영 모델
- `assets/lesson-02-write-plan-apply-workbench.png`: Write–Plan–Apply 학습 장면

## Preparation And Safety

- Terraform CLI 설치 가능 여부와 OS/CPU architecture를 확인한다.
- Git 저장소에서 Secret, State, Plan 파일 제외 규칙을 확인한다.
- 첫 실습은 비용이 발생하지 않는 로컬 리소스로 수행한다.

## End Of Day Checklist

- Terraform이 관리하는 대상과 관리하지 않는 대상을 설명할 수 있는가?
- `validate` 성공과 `plan`의 변경 수를 evidence로 남겼는가?
- 생성한 리소스를 정리하고 결과를 다시 확인했는가?
- 다음 날 Registry에서 Provider 문서를 찾을 수 있는 최소 프로젝트가 남아 있는가?
