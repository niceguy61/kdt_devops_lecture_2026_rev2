# Day 5 공식·학술 기반

| 기준 | 학생 행동 | 산출물·evidence |
|---|---|---|
| Terraform Import | 공식 identity를 찾아 기존 객체를 단일 주소에 binding | Inventory와 Import Plan |
| Terraform State | Import 후 주소·ID·Plan 수렴을 검증 | state show와 no-change |
| Bloom 분석·평가 | add/update/replace/destroy를 분류하고 승인 여부 판단 | action classification |
| CS2023 Knowledge/Skill/Disposition | Import 의미를 설명하고 실행하며 위험한 replace를 중단 | Stop evidence와 handoff |
| ABET/NIST NICE | RDS·DNS·ACM 등 SPOF의 복구·소통 책임을 수행 | probe, backup, approver 기록 |

공식 근거: https://developer.hashicorp.com/terraform/language/import, https://developer.hashicorp.com/terraform/cli/commands/state
