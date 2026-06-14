# 1주차 4일차 학술 근거와 교육 설계 기준

## 교육 설계 의도
Day4는 국내 IT 기업 사례를 통해 Docker 이전에 필요한 현대 애플리케이션 구성요소를 이해하는 날이다. 목적은 회사 소개가 아니라, 비즈니스가 커질수록 어떤 시스템 유지 노력이 늘어나는지 보고, 그 노력이 실행 조건 표준화로 이어지는 흐름을 만드는 것이다.

첫 1:1 면담은 Day4 7~8교시에서 진행하지 않는다. 환경, 용어, 속도, 자신감 회복이 필요한 학생은 Day6로 태깅한다.

## Crosswalk
| 기준 / 이론 | 관찰 가능한 행동 | 확인 기록 |
|---|---|---|
| ABET-style problem analysis | 비즈니스 증가 요인을 기술 구성요소와 연결한다. | company-component note |
| ABET-style communication | 회사 사례 하나를 자기 말로 설명한다. | reflection sentence |
| CS2023 systems perspective | frontend, backend, data, cache, queue, network, config, observability, compute를 구분한다. | component map |
| CS2023 software practice | runtime, dependency, command, port, data path, config, logs를 찾는다. | execution condition map |
| NIST NICE-style task thinking | 신뢰성, 비용, 보안, 복구 부담을 인식한다. | challenge note |
| Bloom analyze/evaluate | 내 로컬 앱과 회사 시스템을 비교한다. | local mapping table |
| Advance organizer | Docker 명령 전에 Docker가 필요한 이유를 먼저 만든다. | Docker 필요성 문장 |
| Cognitive load management | 익숙한 국내 서비스로 추상도를 낮춘다. | company hook |

## 평가 설계
| 평가 영역 | 관찰 가능한 증거 |
|---|---|
| 구성요소 인식 | 현대 애플리케이션 구성요소 5개 이상 |
| 비즈니스-시스템 사고 | 증가 요인 1개와 운영 부담 1개 |
| 로컬 매핑 | command, port, data, config, dependency 중 1개 |
| Docker 준비도 | 수동 설치가 고통스러운 이유 1개 |
| 멘토링 라우팅 | Day6 회복 대상 태깅 |

## 현업 DevOps 연결
Day4는 도구 이름에서 시작하지 않는다. 서비스가 운영되기 위한 조건에서 시작한다.

학생이 가져가야 할 문장:
- 현대 애플리케이션은 여러 실행 조건의 조합이다.
- 회사 규모가 커질수록 데이터, 트래픽, 의존성, 자원 유지 비용이 늘어난다.
- Docker는 이 실행 조건을 수동 설치가 아니라 포장과 재현으로 다루기 위해 등장한다.

Week1에서는 Docker 명령을 실행하지 않는다. Docker hands-on은 Week2에서 시작한다.
