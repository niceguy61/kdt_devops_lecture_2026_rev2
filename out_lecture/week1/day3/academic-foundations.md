# Week 1 Day 3 학술 근거와 교육 설계 기준

## Crosswalk
| Standard | Observable action | 확인 기록 |
|---|---|---|
| ABET-style problem analysis | 실패를 재현, 관찰, 원인 후보로 나눈다. | RCA record |
| CS2023 software development | 실행 조건과 README를 작성한다. | reproducibility checklist |
| NIST NICE-style skill | 시스템 상태와 위험을 식별한다. | risk/API/secret scan |
| Bloom analyze/evaluate | AI 답변과 실행 결과를 검증한다. | AI verification note |

## DevOps Practitioner Lens
재현성은 자동화 이전 단계의 운영 능력이다. README로 실행되지 않는 앱은 Dockerfile로도 안정적으로 옮기기 어렵다.

## 왜 Day 3에서 일부러 오류를 만드는가
초보자는 오류를 피해야 할 대상으로만 받아들이기 쉽다. 그러나 운영 관점에서 오류는 시스템을 이해하는 가장 좋은 관찰 지점이다. Day 3의 의도적 404 실습은 안전한 실패를 만든 뒤, 증상과 원인 후보를 분리하고, 같은 방식으로 다시 확인하는 훈련이다.

이 실습은 학습자의 책임감을 높인다. `curl -I`로 상태 코드를 확인하고, 서버 터미널의 request log를 찾고, README에 prevention note를 남기면 "안 됐다"라는 막연한 표현이 "없는 파일 경로를 요청했고, 서버는 404로 응답했으며, 정상 경로는 200으로 재확인했다"라는 운영 언어로 바뀐다.

## Evidence Alignment
| Learning outcome | Practice | Evidence |
|---|---|---|
| HTTP 요청과 응답을 설명한다. | 정상 URL과 없는 URL을 각각 요청한다. | 200/404 상태 코드 비교 |
| 수정 결과를 검증한다. | `index.html` 본문을 바꾸고 다시 요청한다. | 변경된 body text가 응답에 포함됨 |
| 오류 로그를 해석한다. | 서버 터미널에서 실패 요청 log를 찾는다. | `/no-such-file.html` log excerpt |
| 비밀값을 보호한다. | log와 README 발췌 전 민감정보를 점검한다. | secret value excluded note |
| RCA 구조를 적용한다. | reproduce/observe/hypothesize/fix/recheck/prevent를 작성한다. | RCA table |

## Assessment 기준
Day 3 평가는 결과물이 예쁜지보다 확인 기록이 충분한지를 본다. 최소 통과 기준은 다음과 같다.

- 정상 실행 evidence: start command, URL, 200 계열 상태 코드.
- 수정 확인 evidence: 바꾼 body 문구와 재확인 결과.
- 오류 evidence: 의도적 404, 서버 log excerpt, 원인 후보 분류.
- 재현성 evidence: README의 start/check/stop/expected/troubleshooting.
- 보안 evidence: secret/token/API key 값을 기록하지 않았다는 명시.

## Instructor-independent 복구성
자료만 읽고 다시 따라오는 학생은 서버 터미널과 확인 터미널을 분리해야 한다. 이 구분을 놓치면 서버 프로세스를 중단한 뒤 같은 터미널에서 `curl`을 실행하고 `connection refused`를 파일 문제로 오해할 수 있다. Day 3 교안은 모든 실습에서 현재 경로, 실행 중인 프로세스, 포트, URL 경로, 상태 코드, 로그를 함께 기록하게 만들어 이 혼동을 줄인다.

## Later-week Transfer
Day 3의 작은 루프는 이후 주차의 큰 도구로 그대로 전이된다.

| Day 3 local concept | Later tool | 같은 질문 |
|---|---|---|
| `python3 -m http.server` process | Docker container, Kubernetes Pod | 프로세스가 실제로 살아 있는가? |
| `localhost:8000` | port publish, Service, Load Balancer | 어떤 입구로 들어가는가? |
| `index.html` 수정 | image rebuild, rollout | 변경이 실행 결과에 반영됐는가? |
| 404 request log | container logs, app logs, ingress logs | 실패 요청이 어디까지 도달했는가? |
| README runbook | Dockerfile, compose.yaml, manifest | 다른 사람이 재현할 수 있는가? |
