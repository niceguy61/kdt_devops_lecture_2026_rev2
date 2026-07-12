# Day 2 공식·학술 기반

## Official Sources

| 근거 | 수업에서 확인할 부분 | 학생 행동 |
|---|---|---|
| https://developer.hashicorp.com/terraform/language | block, argument, expression, 선언형 관계 | 코드를 구성요소로 분해한다 |
| https://developer.hashicorp.com/terraform/registry/providers/docs | Provider 문서와 release version의 연결 | 버전이 고정된 근거를 수집한다 |
| https://developer.hashicorp.com/terraform/language/data-sources | Data Source의 읽기 동작과 지연 조건 | Resource와 조회 책임을 구분한다 |
| https://developer.hashicorp.com/terraform/language/resources/configure | 암묵적·명시적 의존성 | 참조에서 그래프 관계를 찾는다 |
| https://developer.hashicorp.com/terraform/language/block/terraform | CLI/Provider/Backend 설정 경계 | Core와 Provider 설정을 구분한다 |

## Academic/Workforce Standards Alignment

| 기준 | 관찰 가능한 학습성과 | 산출물과 evidence |
|---|---|---|
| Bloom 적용·분석 | 공식 문서에서 입력·출력·identity를 찾아 코드에 적용한다 | Resource research worksheet |
| ABET 문제 분석 | 관리와 조회, 암묵적·명시적 의존성을 구분한다 | 선택 근거와 graph |
| ABET 커뮤니케이션 | 출처, 버전, 확인 날짜를 재현 가능한 형태로 전달한다 | 문서 URL과 조사표 |
| CS2023 Knowledge | block, address, reference, dependency를 설명한다 | 오해 점검 답안 |
| CS2023 Skill | State와 graph에서 Resource 관계를 확인한다 | CLI evidence |
| CS2023 Disposition | AI·블로그 예제를 공식 버전 문서와 Plan으로 검증한다 | 검증 질문과 수정 기록 |
| NIST NICE Task | 외부 기술 문서를 조사하고 구성 위험을 보고한다 | argument·attribute·Import·위험 표 |
| NIST NICE Knowledge | 버전, 공급망, 권한과 소유권 경계를 이해한다 | Provider source와 owner 기록 |
| NIST NICE Skill | 오류 주소를 선언 위치와 연결해 복구한다 | failure/fix/recheck note |

## Formative Feedback

첫 조사표에서 URL만 제출하면 다시 돌려보낸다. 강사는 `이 argument가 필요한 근거가 어디인가`, `이 값은 입력인가 출력인가`, `어떤 버전 문서인가`를 표시한다. 학생은 문서 위치와 Plan evidence를 보완하고 수정 전후 차이를 한 줄로 기록한다.
