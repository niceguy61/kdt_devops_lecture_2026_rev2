# DevOps 현업 및 학술 강의/평가 기준

이 문서는 강의 제작 agent가 lesson, README, assessment, scorecard를 만들 때 반드시 반영해야 하는 추가 기준이다. 기존 `docs/lecture-generation-principles.md`가 강의 품질 기준이라면, 이 문서는 강의와 평가의 현업성, 학술성, 채점 가능성을 보강한다.

Last verified: 2026-06-02

## 공식/권위 참고 자료

- DORA: DORA's software delivery performance metrics  
  https://dora.dev/guides/dora-metrics/
- Google SRE Book: Postmortem Culture  
  https://sre.google/sre-book/postmortem-culture/
- NIST NICE Workforce Framework  
  https://www.nist.gov/itl/applied-cybersecurity/nice/nice-cybersecurity-workforce-framework
- ACM/IEEE-CS/AAAI CS2023: Introduction to Competency Framework  
  https://csed.acm.org/final-report/
- ABET Criteria for Accrediting Computing Programs, Student Outcomes  
  https://www.abet.org/accreditation/accreditation-criteria/criteria-for-accrediting-computing-programs-2025-2026/
- NIST SP 800-181 Rev. 1: Workforce Framework for Cybersecurity (NICE Framework)  
  https://csrc.nist.gov/pubs/sp/800/181/r1/final
- ACM CCECC: Bloom's Taxonomy  
  https://ccecc.acm.org/assessment/blooms
- AAC&U VALUE Rubrics  
  https://www.aacu.org/initiatives/value-initiative/value-rubrics

## DevOps Engineer 현업 기준

강의와 평가 자료는 학생이 도구를 실행했는지만 보지 않는다. 주니어 DevOps/Cloud Engineer 후보가 현업에서 인수인계 가능한 증거를 남기는지 확인해야 한다.

필수 관점:

| 기준 | 평가 질문 |
|---|---|
| Operational readiness | 이 결과물을 다른 사람이 실행, 확인, 중지, 복구할 수 있는가? |
| Reproducibility | 경로, 명령, 버전, 포트, 환경변수가 재현 가능하게 기록되었는가? |
| Observability | 로그, 상태 코드, 프로세스, 포트, 비용 화면처럼 판단 증거가 있는가? |
| Incident learning | 실패를 숨기지 않고 증상, 영향, 원인 후보, 조치, 재확인을 기록했는가? |
| Risk classification | 비용, 보안, 권한, 데이터, 외부 API 위험을 severity로 분류했는가? |
| Least privilege | root/admin/secret/API key 사용을 최소화하고 이유를 설명했는가? |
| Cost control | 계속 켜두면 비용이 나는 항목과 삭제/알림 계획을 기록했는가? |
| Handoff documentation | 다음 사람이 이어받을 수 있는 README, 체크리스트, blocker 기록이 있는가? |
| Delivery metrics awareness | 배포 빈도, 변경 리드타임, 변경 실패율, 복구 시간 같은 지표를 초급 수준에서 연결하는가? |

## 학술/교육 기준

강의와 평가 자료는 지식 암기가 아니라 관찰 가능한 학습성과를 측정해야 한다. CS2023의 competency 관점처럼 지식, 기술, 태도를 함께 보며, ABET의 학생 성과처럼 분석, 설계/평가, 커뮤니케이션, 전문적 책임을 확인한다.

필수 관점:

| 기준 | 평가 질문 |
|---|---|
| Observable outcome | "이해한다"가 아니라 설명, 실행, 분석, 평가, 기록 같은 관찰 가능한 행동인가? |
| Knowledge-Skill-Disposition | 개념 지식, 수행 기술, 책임 있는 태도가 함께 평가되는가? |
| Prerequisite clarity | 해당 섹션을 풀기 위해 필요한 선행 개념이 명시되었는가? |
| Concept boundary | 오늘 다루는 범위와 다음 주차로 넘길 범위가 구분되는가? |
| Misconception check | 초급자가 흔히 오해할 지점을 직접 확인하는 문항이 있는가? |
| Transfer task | 예제 그대로가 아니라 자기 프로젝트/다른 상황에 적용하는 문항이 있는가? |
| Evidence-based assessment | 점수가 관찰 증거, 파일, 명령, 로그, 링크에 의해 뒷받침되는가? |
| Professional communication | 결과를 팀원, 강사, 미래의 자신에게 전달 가능한 형식으로 쓰는가? |
| Ethical/professional responsibility | 비용, 보안, 개인정보, secret, AI 검증 책임을 명시하는가? |

## 공식 표준 Crosswalk 필수화

Week 1 이후 강의와 평가 자료는 공식 표준을 단순 참고 링크로만 두지 않는다. 각 표준은 `학생 행동 -> 산출물 -> 채점 증거`로 연결되어야 한다.

| 표준/이론 | 강의 제작 적용 규칙 |
|---|---|
| ABET Computing Student Outcomes | 문제 분석, 해결안 평가/구현, 커뮤니케이션, 전문적 책임, 협업 중 해당되는 결과를 활동과 평가에 매핑한다. |
| CS2023 Competency Framework | 모든 전문 실무형 lesson은 Knowledge, Skill, Disposition을 구분한다. |
| NIST NICE Framework | 보안, secret, least privilege, incident evidence, handoff는 Task/Knowledge/Skill 형태로 표현한다. |
| Bloom's Taxonomy | 목표 문장은 `이해한다`만 쓰지 말고 설명, 분류, 실행, 분석, 평가, 문서화, 정당화, 개선 같은 관찰 가능한 동사를 포함한다. |
| Experiential learning/reflection | 실습은 `무엇을 했는가 -> 어떤 증거가 있는가 -> 어떤 원리와 연결되는가 -> 다음 실험은 무엇인가`로 닫는다. |
| Formative assessment/rubrics | 발표/피드백 활동은 strong/weak evidence, descriptive feedback, self-assessment, revision action을 포함한다. |

## 학술 Crosswalk 산출물

하나의 day 또는 lesson 묶음은 다음 중 하나를 반드시 포함한다.

- day README 안의 `Academic/Workforce Standards Alignment` 섹션
- 별도 `academic-foundations.md`
- 평가 자료의 `학술 outcome mapping`

필수 항목:

- 공식 기준명과 링크
- 관찰 가능한 학습성과
- ABET-style outcome mapping
- CS2023 Knowledge/Skill/Disposition
- NIST NICE-style Task/Knowledge/Skill
- Bloom level 또는 action verb
- formative feedback/revision 구조
- professional responsibility: 비용, 보안, 개인정보, secret, least privilege, AI 검증

## 강의/평가 자료 필수 섹션

Week 1 이후 lesson, README, assessment 중 평가와 연결되는 자료는 다음 섹션 또는 동등한 내용을 포함해야 한다.

- 현업 DevOps Engineer 기준
- 학술/교육 기준
- 선행 지식과 범위 경계
- 오해 점검 문항
- 전이 과제
- 위험 분류표
- 인수인계 가능성 체크
- 증거 기반 scoring 기준
- 공식 표준/이론 crosswalk
- Knowledge/Skill/Disposition mapping
- Task/Knowledge/Skill mapping
- formative feedback와 revision action

## SRE-Grade Scoring Dimensions

넓은 `cost/security/operations` 항목 하나로는 통과할 수 없다. 다음 항목을 독립적으로 평가한다.

| 항목 | 2점 기준 |
|---|---|
| Operational readiness | start/check/stop/cleanup/recover 절차와 healthy state가 있음 |
| Reproducibility | OS, shell, version, path, port, env, command가 재현 가능하게 기록됨 |
| Incident/RCA | severity, impact, timeline, suspected root cause, fix, recheck, prevention이 있음 |
| Security/secret safety | secret, token, 2FA, payment, identity data 미노출 확인 |
| Least privilege | root/admin/API key 사용 제한과 최소 권한 계획 |
| Cost controls | budget/alarm, alert recipient, pricing assumptions, cleanup plan |
| Observability | logs, health check, status code, PID/process, config/env 증거 |
| Handoff docs | 다음 사람이 fresh clone 또는 계정 상태를 이어받아 확인 가능 |
| Risk classification | likelihood, impact, severity, mitigation, owner |
| Evidence quality | command output, log excerpt, URL, file path, screenshot filename 등 구체 증거 |

## Scoring 반영

각 평가 자료와 scorecard는 기존 0/1/2 루브릭에 다음 항목을 추가한다.

| 항목 | 2점 기준 |
|---|---|
| practitioner_readiness | 현업에서 이어받을 수 있는 운영 증거와 handoff가 있음 |
| academic_alignment | 관찰 가능한 학습성과, 선행 지식, 오해 점검, 전이 과제, 공식 표준 crosswalk가 있음 |
| risk_classification | 비용/보안/권한/외부 API/데이터 위험을 severity와 조치로 분류 |
| professional_communication | 팀원이 재현하고 판단할 수 있는 문서 형식 |
