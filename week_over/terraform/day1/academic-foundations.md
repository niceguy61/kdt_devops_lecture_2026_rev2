# Day 1 공식·학술 기반

## Official Sources

| 근거 | 수업에서 확인할 부분 | 학생 행동 |
|---|---|---|
| https://developer.hashicorp.com/terraform/intro | Provider를 통한 API 관리, Write–Plan–Apply | Terraform 동작 경계를 설명한다 |
| https://developer.hashicorp.com/terraform/intro/core-workflow | Plan review와 개인·팀 Workflow | Plan을 승인 evidence로 판독한다 |
| https://developer.hashicorp.com/terraform/cli/commands | 주요 CLI 명령의 책임 | 명령을 검증 질문과 연결한다 |
| https://developer.hashicorp.com/terraform/cli/init | 작업 디렉터리 초기화의 범위 | 초기화 결과와 생성 파일을 확인한다 |
| https://developer.hashicorp.com/terraform/cli/commands/validate | 구문·내부 일관성 검증과 한계 | validate 성공을 원격 검증과 구분한다 |
| https://developer.hashicorp.com/terraform/language/files/dependency-lock | Provider 선택과 checksum 재현 | lock file 변경을 리뷰한다 |

## Academic/Workforce Standards Alignment

| 기준 | 관찰 가능한 학습성과 | 산출물과 채점 evidence |
|---|---|---|
| Bloom 분석·평가 | Terraform 적용 범위와 변경 위험을 분류하고 선택을 정당화한다 | IaC 적용 판단표 |
| ABET 문제 분석 | 수동 인프라 변경의 재현성·보안·비용 문제를 분석한다 | 위험, 영향, 완화책 |
| ABET 커뮤니케이션 | 다른 사람이 재현할 수 있는 실행 조건과 결과를 기록한다 | CLI evidence와 handoff note |
| CS2023 Knowledge | 선언형 구성, Provider, Plan, State 개념을 설명한다 | 오해 점검 답안 |
| CS2023 Skill | CLI Workflow를 실행하고 결과를 판독한다 | fmt/validate/plan/apply/destroy 결과 |
| CS2023 Disposition | 자동화 결과를 맹신하지 않고 승인·복구 책임을 기록한다 | Plan 승인 근거와 cleanup evidence |
| NIST NICE Task | 도구 결과와 오류를 수집해 변경 영향을 보고한다 | failure note와 Resource 주소 |
| NIST NICE Knowledge | 최소 권한, 민감정보, 변경 관리 원리를 연결한다 | Git 제외 파일과 위험 분류 |
| NIST NICE Skill | 명령 출력에서 실패 위치와 복구 결과를 식별한다 | 오류 문장, 수정, 재실행 결과 |

## Formative Feedback

첫 제출에서는 정답 여부보다 근거의 위치를 확인한다. `성공`, `안전`, `재현 가능` 같은 주장에 명령 출력, 파일 경로, Plan 요약이 없으면 보완 대상으로 표시한다. 학생은 feedback 뒤 evidence note를 한 번 수정하고 변경한 항목을 별도로 적는다.
