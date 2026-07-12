# Terraform Day 3: HCL 표현식과 반복 프로그래밍

## Overview

셋째 날은 HCL을 단순 설정 문법이 아니라 안전한 인프라 구성을 만드는 표현 언어로 다룬다. 타입, 변수, 함수, 조건, 컬렉션 변환을 익힌 뒤 `count`, `for_each`, `for`, `dynamic`의 주소 안정성과 가독성을 비교한다.

## Learning Goals

- primitive, collection, structural type을 구분하고 명시적인 variable type을 설계한다.
- 조건식과 함수를 이용해 입력값을 검증하고 컬렉션을 변환한다.
- `count`와 `for_each`가 만드는 Resource 주소 차이를 설명한다.
- `for` expression과 `dynamic` block을 필요한 위치에 사용한다.

## Lesson Index

| 교시 | 주제 | 50분 흐름 | 산출물 |
|---|---|---|---|
| 5교시 | 변수, 타입, locals, 표현식과 함수 | 타입 모델 15분, console 실험 15분, 변수 설계 15분, 정리 5분 | `variables.tf`, 표현식 테스트 기록 |
| 6교시 | `for`, `for_each`, `count`, `dynamic` | 반복 모델 15분, 다중 리소스 15분, 리팩터링·Plan 비교 15분, 정리 5분 | 반복 생성 코드, Plan 비교표 |

## Programming Scope

- string, number, bool, list, set, map, tuple, object
- variable validation, `nullable`, `sensitive`, `locals`, output
- conditional, `null`, splat, `for`, 주요 collection/function 변환
- `count`, `for_each`, `dynamic`, `lifecycle`, condition, `depends_on`, provider meta-argument

## Operational Decision

반복 기능은 코드 길이가 아니라 Resource 주소의 안정성, 입력 데이터의 의미, Plan 가독성을 기준으로 선택한다. 컬렉션 순서 변경만으로 기존 리소스가 교체되는 설계는 실패 사례로 관찰한다.

## Practice Files

- `lesson-01.md`: 타입, 표현식과 환경별 입력
- `lesson-02.md`: 반복과 안정적인 instance key
- `academic-foundations.md`: 공식 근거와 학술·직무 성과 연결
- `labs/expressions/`: dev/prod 입력과 validation 실습
- `labs/repetition/`: count와 for_each 주소 비교
- `assets/lesson-01-typed-environment-inputs.png`
- `assets/lesson-02-stable-instance-keys.png`

## End Of Day Checklist

- 모든 입력 변수에 목적과 타입이 드러나는가?
- Secret에 `sensitive = true`를 붙이는 것만으로 State가 안전해진다고 오해하지 않는가?
- `count`와 `for_each` 중 하나를 선택한 근거를 설명할 수 있는가?
- 반복 입력 변경 전후 Plan의 주소와 교체 수를 비교했는가?
