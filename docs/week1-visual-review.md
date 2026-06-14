# Week 1 Visual Review Evidence

이 문서는 Week 1 강의안의 시각자료 검수 evidence다. 목적은 decorative image 통과가 아니라, 각 lesson의 visual이 수업 개념과 활동을 실제로 설명하는지 확인하는 것이다.

## 검수 기준
- 각 `week1/day*/lesson-*.md` 본문에 `##/### Visual` 또는 `##/### 시각 자료` block이 2~3개 있어야 한다.
- local image path는 실제 파일로 존재해야 한다.
- imagegen 이미지는 nonblank, readable, concept-accurate, decorative-only 아님을 사람 눈으로 확인한다.
- Mermaid/table/capture guide visual은 학습 목적, 읽는 순서, evidence 연결이 있어야 한다.
- README 또는 day-level 이미지만으로 lesson visual을 대체하지 않는다.

## 생성 이미지 검수
| File | Visual Check | Verdict |
|---|---|---|
| `week1/day1/assets/lesson-01-ot-flow.png` | Day 1 OT의 입장, 소통, evidence, safety 흐름을 한 장에서 읽을 수 있음 | Pass |
| `week1/day1/assets/lesson-02-roadmap.png` | 5주 로드맵을 Week1 computing spine에서 Week2~5 기술로 연결함 | Pass |
| `week1/day1/assets/lesson-03-ai-service-boundary.png` | AI coding agent와 business/service 운영 책임의 경계를 시각적으로 구분함 | Pass |
| `week1/day1/assets/lesson-04-datacenter-vs-cloud.png` | 데이터센터와 클라우드의 책임 이동, CAPEX/OPEX/TCO/Cloud Cost 관점을 설명함 | Pass |
| `week1/day2/assets/lesson-02-git-vscode-roles.png` | GitHub, Git, VS Code의 책임과 clone/commit/push 경계를 설명함 | Pass |
| `week1/day2/assets/lesson-03-mfa-pat-git-flow.png` | MFA, PAT, Git push 인증 흐름을 단계별로 보여주며 토큰 값 기록 금지를 명시함 | Pass |
| `week1/day2/assets/lesson-04-ai-doc-verification.png` | AI 답변을 공식 문서, 명령 출력, README evidence로 검증하는 경로를 설명함 | Pass |
| `week1/day2/assets/lesson-05-cli-observation.png` | CLI 명령을 운영 질문과 evidence 유형에 연결함 | Pass |
| `week1/day2/assets/lesson-07-memory-storage.png` | Memory와 storage의 보존성 차이를 Docker/Kubernetes storage 복선으로 설명함 | Pass |
| `week1/day3/assets/lesson-02-log-config-secret.png` | Log, config, secret의 책임과 보호 경계를 설명하며 실제 secret 값을 노출하지 않음 | Pass |
| `week1/day3/assets/lesson-04-readme-runbook.png` | README를 실행 가능한 runbook 단계로 설명함 | Pass |
| `week1/day3/assets/lesson-05-rca-flow.png` | RCA에서 증상, 영향, timeline, recheck, prevention의 절차를 설명함 | Pass |
| `week1/day3/assets/lesson-07-ai-risk-check.png` | AI 제안을 공식 문서, 보안, 비용, 재현성 기준으로 검토하게 함 | Pass |
| `week1/day4/assets/lesson-01-day4-direction-lanes.png` | Day4를 새 앱 개발이나 상태 코드 반복이 아닌 기본/복구/선택 lane으로 분기하는 수업으로 설명함 | Pass |
| `week1/day4/assets/lesson-02-file-skeleton.png` | 미니 앱 파일을 HTML/CSS/JS/JSON/README 책임으로 구분함 | Pass |
| `week1/day4/assets/lesson-03-html-css-js-json.png` | 브라우저 렌더링 결과가 구조, 표현, 동작, 데이터의 결합임을 설명함 | Pass |
| `week1/day4/assets/lesson-04-empty-error-state.png` | 정상, 빈 데이터, 오류 상태를 비교하고 상태별 evidence 캡처 필요성을 설명함 | Pass |
| `week1/day4/assets/lesson-04-ai-debug-prompt.png` | 모호한 오류 보고를 OS, 경로, 명령, URL/상태, 확인한 것으로 나누어 AI 디버깅 질문으로 바꾸는 흐름을 설명함 | Pass |
| `week1/day4/assets/lesson-05-small-change-recovery.png` | 작은 변경, 관찰, 작은 오류, 복구 후 재확인의 안전한 루프를 설명함 | Pass |
| `week1/day4/assets/lesson-06-risk-runbook.png` | 비용, 보안, 재현성, 운영 위험을 대응 행동과 evidence로 연결함 | Pass |
| `week1/day4/assets/lesson-07-interview-recovery.png` | Day4 7교시를 새 진도가 아닌 blocker 분류와 회복 lane으로 설명함 | Pass |
| `week1/day4/assets/lesson-08-waiting-choice-activities.png` | 면담 대기 시간을 앱 소개, 증상 정리, Docker 질문, README 빈칸 채우기 선택 활동으로 연결함 | Pass |
| `week1/day5/assets/lesson-07-feedback-recheck.png` | 질문을 개념, 실행, 문서 문제로 분류하고 수정 후 recheck evidence로 닫는 흐름을 설명함 | Pass |
| `week1/assets/week1-computing-spine.png` | compute, storage, network, configuration, identity/access, observability, cost boundary의 spine을 설명함 | Pass |
| `week1/assets/week1-service-evidence-flow.png` | local evidence가 handoff/runbook/operation으로 이어지는 흐름을 설명함 | Pass |
| `week1/assets/week1-docker-preview-mapping.png` | Week1 computing spine이 Week2 Docker component preview로 연결되는 복선을 설명함 | Pass |

## 검증 명령 Evidence
```bash
for f in week1/day*/lesson-*.md; do
  vis=$(rg -c '^#{2,3} (Visual|시각 자료)' "$f" || true)
  if [ "$vis" -lt 2 ] || [ "$vis" -gt 3 ]; then
    echo "VIS_OUT_OF_RANGE $f $vis"
  fi
done
```

기대 결과: 출력 없음.

```bash
while IFS= read -r line; do
  f=${line%%:*}
  path=$(printf '%s' "$line" | sed -E 's/.*\]\((\.{1,2}\/[^)]+)\).*/\1/')
  dir=$(dirname "$f")
  if [ ! -f "$dir/$path" ]; then
    echo "missing $f -> $path"
  fi
done < <(rg -n '\]\((\.{1,2}/[^)]+\.(png|jpg|jpeg|webp|svg))\)' week1/day*/lesson-*.md)
```

기대 결과: 출력 없음.

## 판정
Week 1 lesson 본문 visual은 장식용이 아니라 운영 흐름, 컴퓨팅 구조, evidence 위치, 위험 분류, handoff 판단을 설명한다. 각 lesson은 2~3개 visual block을 갖고, local image path는 검증 대상으로 유지한다.
