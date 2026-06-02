# Week 1 Day 4 학술 근거와 교육 설계 기준

## 교육 설계 의도
Day4는 작은 정적 앱을 만드는 활동이지만, 평가 중심은 기능 수가 아니라 제한 조건 안에서 실행 가능한 artifact를 만들고 증거를 남기는 능력이다. 학생은 요구사항 범위, 파일 구조, 데이터 렌더링, 실행 증거, 위험 분류를 하나의 개발-운영 흐름으로 경험한다.

## Crosswalk
| Standard / Theory | Observable Action | Evidence |
|---|---|---|
| ABET-style design | 제한 조건 안에서 작은 앱을 구현한다. | mini app, scope note |
| ABET-style professional responsibility | 비용/보안/재현성 위험을 분류한다. | risk table |
| CS2023 software practice | UI, script, data file 책임을 분리한다. | file tree, source files |
| CS2023 systems perspective | file, process, port, HTTP evidence를 연결한다. | execution evidence |
| NIST NICE-style task | secret/API/resource 위험을 피한다. | exclusion note |
| Bloom create/evaluate | 앱을 만들고 운영 기준으로 평가한다. | README/runbook |
| Cognitive load theory | backend/auth/DB 변수를 제외해 초보자 부담을 낮춘다. | scope rule |
| Mastery learning | 7~8교시에서 개인 blocker를 복구한다. | interview note |

## 평가 설계
| 평가 영역 | 관찰 가능한 증거 |
|---|---|
| 범위 통제 | include/exclude table, excluded feature reasons |
| 구현 | static app, JSON rendering, one user flow |
| 실행 검증 | command, path, port, URL, browser/curl result |
| 운영 사고 | risk classification, troubleshoot runbook |
| 회복과 보완 | blocker type, next action, peer test note |

## 필수 면담 블록
4일차 7~8교시는 새 진도 없이 개인 면담과 보충 실습으로 운영한다. 면담은 환경, 범위, 구현, 증거, 자신감 blocker를 분류하고 다음 행동을 정하는 형식이어야 한다.

## 현업 DevOps 연결
Day4에서 다루는 현업 관점은 독립 프레임워크 수업이 아니라 다음 습관으로 제한한다.
- 실행 조건을 문서화한다.
- 실패 상태를 숨기지 않는다.
- 위험을 비용, 보안, 재현성으로 분류한다.
- handoff 가능한 README/runbook을 만든다.

Week1에는 DORA와 Well-Architected를 독립 수업으로 배치하지 않는다.
