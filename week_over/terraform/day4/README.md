# Terraform Day 4: Module, State와 Remote Backend

## Overview

넷째 날은 재사용과 협업의 경계를 다룬다. 단일 구성을 Child Module로 분리하면서 Resource 주소 변경 위험을 관찰하고, Configuration·State·실제 인프라 사이의 binding을 이해한 뒤 Remote Backend 이전과 복구 절차를 설계한다.

## Learning Goals

- 파일 분리와 Module 경계의 차이를 설명한다.
- Module 입력, 출력, Provider 전달과 버전 고정 기준을 적용한다.
- State가 Resource 주소와 실제 객체 identity를 연결하는 방식을 설명한다.
- Backend의 저장, 암호화, 접근 제어, Locking, 버전 관리, 복구 요구사항을 평가한다.

## Lesson Index

| 교시 | 주제 | 50분 흐름 | 산출물 |
|---|---|---|---|
| 7교시 | Module 설계와 안전한 리팩터링 | 경계 설계 15분, Module 분리 20분, Plan·주소 검증 10분, 정리 5분 | Local Module, 리팩터링 evidence |
| 8교시 | State, Drift와 Remote Backend | State 모델 15분, 명령 관찰 10분, Backend 이전 15분, 복구·정리 10분 | migration evidence, 복구 Runbook |

## Backend Safety Requirements

- State 저장 데이터의 암호화와 최소 권한 접근
- 동시 변경 충돌을 막는 Locking
- 실수와 손상에 대비한 버전 관리 및 복구
- Backend 인증정보를 코드와 Plan에 포함하지 않는 주입 방식
- 이전 전 백업과 실패 시 Rollback 절차

## Scope Boundary

Terraform CLI Workspace는 간단한 동일 구성의 복제에는 사용할 수 있지만, 별도 자격증명과 강한 접근 제어가 필요한 환경 분리의 기본 해법으로 사용하지 않는다.

## Practice Files

- `lesson-01.md`: Module과 환경별 Root/State 분리
- `lesson-02.md`: State, Backend, Locking과 복구
- `academic-foundations.md`: 공식 근거와 학술·직무 성과 연결
- `labs/module-environments/`: 공통 Child Module을 dev/prod에서 호출하는 실습
- `labs/backend-reference/`: 최신 S3 Backend 참고 구성
- `assets/lesson-01-module-environment-factory.png`
- `assets/lesson-02-state-backend-control-room.png`

## End Of Day Checklist

- Module 이동 전후 Plan에서 의도하지 않은 destroy/create가 없는가?
- State 파일을 직접 편집하지 않고 지원되는 명령을 사용하는가?
- Backend 이전 전 백업과 이전 후 Resource 주소를 확인했는가?
- 다음 사람이 State 위치, 접근 방법, Lock과 복구 절차를 확인할 수 있는가?
