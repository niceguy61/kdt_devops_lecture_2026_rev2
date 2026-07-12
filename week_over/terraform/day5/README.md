# Terraform Day 5: 기존 인프라 Import 통합 핸즈온

## Overview

마지막 날은 두 교시를 하나의 연속 핸즈온으로 운영한다. 기존 AWS 리소스의 소유권과 identity를 조사하고 Terraform 주소를 설계한 뒤 선언적 `import` 블록으로 State에 편입한다. Import 성공 자체가 아니라 코드와 실제 객체가 일치하는 최종 Plan과 인수인계 문서를 완성하는 것이 목표다.

## Learning Goals

- Import 대상의 실제 ID와 Terraform Resource 주소를 정확히 매핑한다.
- Provider 공식 문서에서 Resource별 Import 형식을 찾는다.
- 선언적 `import` 블록과 기존 CLI Import 방식의 차이를 설명한다.
- Import 후 State와 Plan을 검토해 의도하지 않은 변경과 교체를 차단한다.

## Lesson Index

| 교시 | 주제 | 50분 흐름 | 산출물 |
|---|---|---|---|
| 9교시 | 기존 인프라 조사와 Import 설계 | inventory 15분, 문서 조사 10분, 주소·코드 설계 15분, 사전 Plan 10분 | inventory, ID/주소 매핑표, `imports.tf` |
| 10교시 | Import 실행, 코드 정합화와 handoff | Import 10분, State 확인 10분, 코드 보완·Plan 반복 20분, 인수인계 10분 | 최종 코드, Plan, 장애 기록, Runbook |

## Hands-On Success Criteria

- Import 전에 대상 계정, Region, 소유자, Resource ID와 비용 영향을 기록한다.
- 같은 원격 객체를 둘 이상의 Resource 주소로 관리하지 않는다.
- Import 후 `terraform state list`와 `terraform state show`로 binding을 확인한다.
- 최종 Plan은 변경 없음이거나 모든 잔여 변경에 명시적인 승인 근거가 있다.
- replace 또는 destroy가 나타나면 실행하지 않고 원인과 복구 방향을 기록한다.

## Deliverables

- 기존 리소스 inventory
- Provider 문서 및 Import ID 근거
- `resource`와 `import` 블록
- Import 전 State 백업
- Import 전후 State/Plan 비교
- 실패 증상, 영향, 원인, 수정, 재확인을 포함한 장애 기록
- 실행, 확인, 복구, 정리, 비용 책임을 포함한 handoff 문서

## Practice Files

- `lesson-01.md`: Inventory, identity, 주소와 위험 Gate
- `lesson-02.md`: Import 실행, 정합화와 handoff
- `academic-foundations.md`: 공식 근거와 학술·직무 성과 연결
- `labs/import-hands-on/`: 선언적 Import 실습
- `assets/lesson-01-import-inventory-mapping.png`
- `assets/lesson-02-import-convergence-workbench.png`

## End Of Course Checklist

- 기존 리소스가 올바른 Terraform 주소에 연결되었는가?
- 코드가 실제 객체의 중요한 설정을 표현하는가?
- 다음 `plan`과 `apply`에서 발생할 변경을 설명할 수 있는가?
- State와 자격증명이 Git 또는 제출물에 노출되지 않았는가?
- 실습 리소스를 삭제했거나 유지 이유, 비용, 소유자, 삭제 기한을 기록했는가?
