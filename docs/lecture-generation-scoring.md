# 강의 제작 Agent Scoring Contract

이 문서는 강의 제작 multi-agent system의 scoring 기준이다. 중앙 controller가 자체적으로 점수를 채우면 안 된다. `lecture-pattern-17-evaluation` agent가 실제 산출물을 읽고 증거 기반으로 채점해야 한다.

## 왜 다시 만들었는가

초기 구현은 17개 pattern prompt와 controller 구조를 만들었지만, `.omx/state/lecture-generation-agent.json`에 기록된 pass score가 실제 Evaluation agent의 독립 검증 결과가 아니었다. 이것은 agentic workflow 검증으로 인정할 수 없다.

따라서 scoring 기준을 다음처럼 바꾼다.

- pass/fail만 쓰지 않는다.
- 각 항목은 0, 1, 2점으로 채점한다.
- 모든 항목은 증거를 가져야 한다.
- 모든 항목이 2점이어야 pass다.
- MIT 공대생 수준의 까다로운 수강생이 보아도 만족도 90% 이상을 기대할 수 있는 깊이, 근거, 시각 설명, 실습 가능성을 갖춰야 pass다.
- 점수가 부적절하면 `invalid_scoring` 또는 `fail_rebuild_required`가 된다.

## 점수 기준

| 점수 | 의미 |
|---|---|
| 0 | 없음, 검증 안 됨, 또는 명백히 틀림 |
| 1 | 일부 있음. 하지만 얕거나 증거가 부족함 |
| 2 | 충분히 있음. 파일/섹션/링크/명령 결과로 증거가 있음 |

## 90% Quality Gate

이 scoring contract의 pass는 단순한 형식 통과가 아니다. Evaluation agent는 "MIT 공대생 수준의 높은 기준을 가진 학습자가 90% 이상 만족할 수 있는가"를 별도 gate로 판단한다.

90% gate를 통과하려면 다음을 모두 만족해야 한다.

- 각 lesson은 50분 수업을 실제로 지탱할 설명 밀도, 활동, 오해 점검, 평가 증거를 갖춘다.
- 공식/학술 출처는 source pack에만 숨지 않고 lesson 본문에 제목과 URL로 연결된다.
- 현업 DevOps 관점은 추상 조언이 아니라 운영 판단, handoff, failure mode, cost/security/reproducibility evidence로 나타난다.
- visual은 장식이 아니라 개념 구조, 흐름, evidence 위치, 판단 기준을 설명한다.
- 사람 눈 visual review와 local path 검증이 evidence로 남는다.

90% gate가 실패하면 전체 pass가 아니다. 실패 유형은 결함 크기에 따라 `fail_repair_required` 또는 `fail_rebuild_required`로 처리하고, Retrieval Gate로 돌아가 공식 문서/학교 강의자료/공식 블로그를 다시 확인한 뒤 작성과 평가를 반복한다.

## 평가 항목

| 항목 | 2점 기준 |
|---|---|
| curriculum_fit | `docs/plan.md`의 주차/일차/교시와 생성 lesson이 맞고, evidence가 있음 |
| source_grounding | 공식 문서 제목과 링크가 lesson 또는 retrieval packet에 있고, 내용과 연결됨 |
| student_facing_tone | 강사용 내부 스크립트 문구가 없고 학생용 문서로 읽힘 |
| onboarding_clarity | OT/입문 세션은 질문 과밀, 금지 목록 반복, 미래 기술 과노출로 학생을 혼동시키지 않고 운영 안내와 학습 동선을 안정적으로 제시함 |
| fifty_minute_depth | 아래 `50분 강의안 최소 구조`를 충족하고, 설명/활동/질문/증거/오해/전이 흐름이 실제 50분 수업을 지탱함 |
| visual_support | 각 lesson 본문에 학습 목적이 명확한 instructional visual 2~3개가 있고, local asset 또는 공식 이미지 링크/출처가 검증됨 |
| human_visual_review | 생성/참조된 이미지를 사람 눈으로 확인해 nonblank, readable, concept-accurate, decorative-only 아님을 evidence로 남김 |
| practice_observation | 실습, 관찰, 판단 활동이 구체적으로 있음 |
| failure_recovery | 기대 결과, 실패 증상, 복구 방향이 있음 |
| operational_readiness | 실행, 확인, 중지, 복구, 인수인계 기준이 구체적임 |
| reproducibility | OS/shell/version/path/port/env/command가 재현 가능하게 기록됨 |
| incident_rca | 실패 재현, 영향, timeline, suspected root cause, fix, recheck, prevention이 있음 |
| security_secret_safety | password, token, 2FA code, access key, payment/identity data 미노출을 검증함 |
| least_privilege | root/admin/API key를 일상 접근으로 쓰지 않고 최소 권한 계획이 있음 |
| cost_controls | budget/alarm/alert recipient/cleanup plan/pricing assumptions가 있음 |
| observability | logs, health check, status code, PID/process, config/env 등 상태 증거가 있음 |
| handoff_docs | 다음 사람이 실행/확인/정리/보완할 수 있는 README 또는 handoff note가 있음 |
| risk_classification | likelihood, impact, severity, mitigation, owner로 위험을 분류함 |
| evidence_quality | 파일, heading, 명령, 로그, 링크, 상태 코드 같은 구체 증거가 있음 |
| path_consistency | 참조한 local path가 실제 존재함 |
| state_diff_tracking | state file에 chain, handoff, files_changed, checks, risks가 증거 기반으로 기록됨 |
| practitioner_readiness | 현업 DevOps Engineer가 이어받을 수 있는 운영 증거, risk classification, handoff 기록이 있음 |
| academic_alignment | 관찰 가능한 학습성과, 선행 지식, 오해 점검, 전이 과제, 지식/기술/태도 기준이 있음 |
| standards_crosswalk | ABET/CS2023/NIST NICE/Bloom/formative assessment 중 관련 기준이 학생 행동, 산출물, 평가 증거와 연결됨 |
| professional_responsibility | 비용, 보안, 개인정보, secret, AI 검증 책임을 전문 직무 책임으로 다룸 |
| contract_tone_compliance | `docs/lecture-tone.md`의 시간 준수, 경어, 신뢰 형성, 불필요한 잡담/홍보/불평 금지, feedback 기준을 강의안에 반영함 |

## 50분 강의안 최소 구조

하나의 50분 lesson은 제목과 목표만으로 통과할 수 없다. 다음 구조 또는 동등한 밀도를 갖춰야 한다.

| 섹션 | 2점 기준 |
|---|---|
| 시간 운영 | 50분을 5~10분 단위로 나눈 흐름이 있고, 활동/설명/정리가 균형을 이룸 |
| 선행 지식 | 학생이 이미 알아야 할 개념과 오늘 처음 배우는 개념을 구분함 |
| 핵심 설명 | 개념을 최소 3개 이상의 구체 항목, 표, 절차, 판단 기준으로 설명함 |
| 공식/학술 근거 | 공식 문서/학술 기준이 단순 링크가 아니라 해당 활동의 이유와 연결됨 |
| 현업 insight | DevOps/SRE/Cloud Engineer 관점의 실제 판단 기준, 실패 모드, handoff 기준이 있음 |
| 실습/활동 절차 | 학생이 따라 할 단계, 입력, 예상 결과, 기록 위치가 구체적임 |
| 오해 점검 | 초급자가 틀리기 쉬운 오해와 확인 질문이 있음 |
| 증거 산출물 | command, URL, path, log, screenshot filename, note, table 중 무엇을 남길지 명시함 |
| 평가 기준 | strong/weak evidence 또는 0/1/2 기준이 있음 |
| 전이 과제 | 예제 상황을 자기 프로젝트 또는 다음 주차 기술로 연결함 |
| 시각 자료 | 각 lesson 본문에 imagegen/Mermaid/공식 이미지/캡처 가이드 중 2~3개가 직접 연결되고, 각 visual마다 학습 목적, 읽는 순서, 출처 또는 생성 방식이 있음 |

## OT/입문 세션 품질 기준

OT와 첫날 입문 세션은 일반 기술 강의와 다르게 채점한다. 학생의 첫 인지 부하를 낮추고 운영 동선을 안정화해야 한다.

| 항목 | 2점 기준 |
|---|---|
| 질문 밀도 | 한 세션의 공개 질문은 핵심 1~2개로 제한하고, 나머지는 개인 작성/체크리스트로 전환함 |
| 금지 목록 노출 | "오늘 하지 않는다"를 반복하지 않고, 필요한 경우 긍정형 범위 설명으로 바꿈 |
| 안내 우선순위 | 장소, 시간, 소통, 산출물, 안전, 학습 동선을 먼저 제시함 |
| AI 시대 인사이트 | AI coding agent로 작은 앱은 쉬워졌지만 business/service 단계에는 실행 환경, 보안, 비용, 관찰, handoff 책임이 필요하다는 메시지를 사례/근거와 연결함 |
| 시각자료 | OT도 lesson별 2~3개 visual을 포함하되, 장식용 hero가 아니라 로드맵, 운영 동선, 서비스화 단계 같은 instructional visual이어야 함 |
| 계약 tone | 강의 경험/현장 경력/운영 방식 소개로 신뢰를 형성하되, "처음" 표현, 개인 홍보, 운영 불평, 교육 외 상담을 포함하지 않음 |

## 시각자료 최소 기준

각 lesson은 2~3개의 instructional visual block을 본문에 포함해야 한다. README나 day-level asset만으로는 pass할 수 없다.

허용되는 visual:
- imagegen으로 만든 PNG/WebP/JPG 교안 이미지
- 공식 문서/공식 블로그/대학 강의자료의 이미지 또는 다이어그램 링크와 출처
- Mermaid 다이어그램
- 터미널/브라우저/콘솔 화면 캡처 가이드

허용되지 않는 visual:
- 본문과 연결되지 않는 장식 이미지
- 존재하지 않는 local path
- 출처 없는 외부 이미지
- 글자가 깨져 읽을 수 없는 생성 이미지
- README에만 있고 lesson 본문에는 없는 이미지

다음 중 하나라도 해당하면 `fifty_minute_depth=0` 또는 `fail_rebuild_required`다.

- lesson이 1~2개 표와 짧은 bullet만 있고 설명 흐름이 없음
- 50분 동안 진행할 활동 시간이 성립하지 않음
- 공식 링크만 있고 해당 개념/활동과 연결되지 않음
- 현업/학술 기준이 README나 assessment와 연결되지 않음
- 시각 자료가 없거나 decorative image만 있음
- lesson 본문 기준 visual 수가 2개 미만임
- OT에서 질문이 과하거나 금지/미진행 항목을 반복해 학생 혼동을 유발함
- `docs/lecture-tone.md`와 충돌하는 표현이 있음. 예: 처음이라 미숙하다는 표현, 개인 홍보, 교육장 불평, 교육과 무관한 상담, 시간 임의 조정
- 실습 결과와 실패/복구 기준이 없음
- scoring evidence가 `있음`, `완료`, `pass` 같은 주장뿐임

## 무효 Scoring 조건

다음 중 하나라도 있으면 점수는 무효다.

- controller가 Evaluation agent 없이 점수를 직접 채움
- 모든 점수가 pass인데 evidence가 없음
- handoff packet 수가 실행 chain에 비해 현저히 부족함
- lesson이 없는 asset을 참조함
- 공식 문서 근거가 없는데 source grounding을 pass 처리함
- reflection 결함을 고치지 않고 pass 처리함
- `docs/lecture-generation-principles.md`의 필수 항목을 빠뜨림
- `docs/devops-academic-assessment-standards.md`의 현업/학술 필수 기준을 lesson, README, assessment, scorecard에 반영하지 않음
- 공식 표준 링크만 있고 학생 행동, 산출물, scoring evidence와 연결된 crosswalk가 없음
- `cost_security_operations`처럼 넓은 항목 하나로 operational readiness, security, least privilege, cost controls, observability, handoff, risk를 한꺼번에 pass 처리함
- README 또는 day 자료의 공통 이미지 1~3장만 근거로 전체 lesson visual support를 pass 처리함
- imagegen asset을 생성했지만 사람 눈 검수 또는 파일 존재 검증 없이 pass 처리함

## 실패 시 동작

| 실패 유형 | 다음 동작 |
|---|---|
| invalid_scoring | state를 `failed_scoring`으로 바꾸고 Evaluation agent를 다시 실행 |
| fail_repair_required | responsible agent로 되돌려 같은 artifact를 수정 |
| fail_rebuild_required | Planning 또는 Retrieval gate로 되돌려 재작성 |
| blocked | 사용자 승인 또는 외부 조건이 필요할 때만 사용 |
