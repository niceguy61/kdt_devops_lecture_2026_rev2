# Terraform Day 2: 공식 문서 탐색과 객체 모델

## Overview

둘째 날은 정답 코드를 받아 적지 않고 공식 문서에서 직접 오브젝트를 찾는 법을 익힌다. AWS Console의 개념을 Provider Resource와 Data Source로 연결하고 Terraform의 주요 블록, 주소, 참조, 의존성을 하나의 객체 모델로 정리한다.

## Learning Goals

- 공식 Provider와 Module을 구분하고 호환 버전을 확인한다.
- Resource 문서에서 required/optional argument, exported attribute, import 형식을 찾는다.
- `terraform`, `provider`, `resource`, `data`, `variable`, `locals`, `output`, `module` 블록을 구분한다.
- Resource 주소와 암묵적·명시적 의존성을 판독한다.

## Lesson Index

| 교시 | 주제 | 50분 흐름 | 산출물 |
|---|---|---|---|
| 3교시 | HashiCorp Developer와 Registry 탐색 | 탐색 지도 10분, 문서 읽기 15분, AWS 객체 조사 20분, 정리 5분 | 공식 문서 탐색 워크시트 |
| 4교시 | 주요 블록, 주소, 참조와 의존성 | 객체 모델 15분, 코드 연결 15분, graph 실습 15분, 정리 5분 | 객체 관계도, 의존성 evidence |

## Documentation Reading Order

1. Provider namespace와 현재 선택한 버전을 확인한다.
2. Example Usage에서 최소 구성을 찾는다.
3. Argument Reference에서 입력 조건을 찾는다.
4. Attribute Reference에서 다른 리소스가 참조할 출력을 찾는다.
5. Import 섹션에서 Resource identity 형식을 확인한다.

## Practice Targets

`aws_vpc`, `aws_subnet`, `aws_security_group`, `aws_instance`, `aws_s3_bucket`, `data.aws_ami`

## Practice Files

- `lesson-01.md`: 공식 문서와 Registry 탐색
- `lesson-02.md`: 블록, 주소, 참조와 의존성
- `academic-foundations.md`: 공식 근거와 학술·직무 성과 연결
- `labs/document-research/`: Provider 문서 조사표
- `labs/object-model/`: 비용과 자격증명 없이 주소·의존성을 확인하는 실습
- `assets/lesson-01-registry-research-desk.png`: 공식 문서 조사 장면
- `assets/lesson-02-object-address-workbench.png`: 객체 주소와 연결 관계 학습 장면

## End Of Day Checklist

- AI나 검색 결과의 코드가 현재 Provider 문서와 일치하는지 검증했는가?
- AWS 객체 이름을 Terraform Resource 주소로 매핑했는가?
- 암묵적 의존성이 생기는 attribute reference를 찾았는가?
- 불필요한 `depends_on`을 추가하지 않았는가?
