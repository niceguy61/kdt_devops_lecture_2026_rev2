# Week 1 Day 4: 미니 앱 범위 설정, skeleton, 구현, 실행 증거, 위험 분류, 개인 면담

## Day Goal
학생은 Week1 기준의 작은 정적 미니 앱을 범위 안에서 설계하고, skeleton 생성, data rendering 구현, 실행 증거 작성, 위험 분류, README/runbook 초안까지 완성한다. 7~8교시는 반드시 개인 면담과 보충 실습으로 운영하며 새 진도를 추가하지 않는다.

## 운영 원칙
- Week1 앱은 HTML/CSS/JS, dummy JSON, local static server, README evidence만 포함한다.
- backend, database, paid API, authentication은 제외한다.
- 기능 수보다 실행 가능성, 재현성, handoff 가능성을 우선한다.
- DORA와 Well-Architected는 Week1 독립 수업으로 다루지 않는다. 필요한 경우 변경 증거, 재현성, 위험 인식이라는 현업 습관으로만 짧게 연결한다.

## Lesson Index
| 교시 | 주제 | 핵심 산출물 |
|---|---|---|
| 1교시 | 미니 앱 요구사항과 범위 경계 | scope note, include/exclude table |
| 2교시 | 미니 앱 skeleton 생성 | file tree, minimal static app |
| 3교시 | 구현 1 - HTML/CSS/JS/dummy JSON 연결 | data rendering evidence |
| 4교시 | 구현 2 - 사용자 흐름과 error state | normal/empty/error state |
| 5교시 | 실행 증거 작성 | command, path, port, URL, HTTP/browser evidence |
| 6교시 | 운영 위험 분류와 README/runbook 기초 | risk table, runbook draft |
| 7교시 | 개인 면담 및 환경 점검 | blocker classification, recovery action |
| 8교시 | 개인 면담 및 보충 실습 | Day4 submission package, peer test note |

## Required Deliverables
| Deliverable | Minimum Evidence |
|---|---|
| working static mini app | local server URL and visible page |
| dummy JSON rendering | data value visible in browser |
| execution evidence table | command, working directory, port, URL, status/result |
| risk classification table | cost/security/reproducibility risks and responses |
| README/runbook sections | start/check/stop/troubleshoot |
| interview/blocker note | blocker type and next action |

## 50분 수업 공통 구조
각 lesson은 다음 구조로 운영한다.
1. 5분: 이전 산출물 확인과 목표 고정
2. 10~15분: 핵심 개념과 예시 설명
3. 20~25분: 개인 또는 짝 실습
4. 5~10분: evidence 기록과 평가 체크
5. 마지막 2~5분: 다음 교시 연결

7~8교시는 이 구조를 강의가 아니라 면담/보충 실습에 적용한다.

## 평가 기준 요약
- 앱이 정적 서버에서 실행된다.
- README만 보고 시작, 확인, 중지할 수 있다.
- 사용자 흐름이 1개로 제한되어 있다.
- dummy JSON, error state, 실행 evidence가 확인된다.
- 비용, 보안, 재현성 위험이 명시되어 있다.
- 개인 blocker와 보완 계획이 남아 있다.

## 다음 주차 연결
Day4 산출물은 Week2 Docker 실습의 입력이다. 앱 폴더는 build context가 되고, 실행 명령은 container command와 port mapping으로 바뀐다. README/runbook은 Docker runbook으로 확장된다.

## Visual Support
![Local service evidence flow](https://raw.githubusercontent.com/niceguy61/kdt_devops_lecture_2026_rev2/main/week1/assets/week1-service-evidence-flow.png)

Day4에서는 이 evidence flow를 미니 앱 구현에 적용한다. 구현 자체보다 command, port, status, log, README evidence가 함께 남는지 확인한다.
