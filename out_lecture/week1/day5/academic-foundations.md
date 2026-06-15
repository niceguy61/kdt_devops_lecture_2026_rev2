# 1주차 5일차 학술 근거와 교육 설계 기준

## 교육 설계 의도
Day5는 초보자가 Docker를 배우기 전에 반드시 겪는 로컬 실행 환경 문제를 구조화하는 수업이다. 학생이 아직 Docker 명령어를 실행하지 않아도, 왜 Docker가 필요한지 자신의 언어로 설명할 수 있어야 한다.

Day5 1교시 분량을 Day4 마지막 시간에 선행 진행한 경우, Day5는 기존 DB 시나리오를 `2-1 DB 직접 설치 관찰`과 `2-2 DB 버전 충돌 관찰`로 나누어 보강한다. 이때 설치 성공 자체보다 service, port, data path, config처럼 OS에 남는 실행 조건을 관찰하는 데 목표를 둔다.

이 날의 핵심은 다음 순서다.

```text
직접 설치 관찰 -> 불편함 경험 -> 원인 분류 -> 실행 환경 개념화 -> Docker 필요성 예고
```

## Crosswalk
| 기준 / 이론 | Day5 적용 | 확인 가능한 증거 |
|---|---|---|
| Cognitive load management | Docker 명령어를 바로 투입하지 않고 로컬 DB 직접 설치, port, 설정, 삭제 시나리오로 나누어 제시한다. | 시나리오별 메모 |
| Bloom understand | runtime, dependency, port, config, data path를 자기 말로 설명한다. | 개념 문장 |
| Bloom analyze | DB 중복 설치, port 충돌, 설정 drift, 삭제 잔여물을 원인별로 나눈다. | 문제 분류표 |
| CS2023 systems perspective | 애플리케이션 실행 조건을 compute, network, storage, configuration 관점으로 본다. | 실행 조건 지도 |
| DevOps practitioner lens | 재현 가능한 환경과 cleanup을 개발 단계의 운영 역량으로 연결한다. | README 실행 체크리스트 |
| Mastery learning | 8교시에서 부담 없는 공유로 이해 상태와 질문을 확인한다. | 미니 공유 메모 |

## 이해 확인 기준
Day5의 확인은 산출물 완성보다 개념 언어화에 둔다.

| 확인 영역 | 관찰 가능한 증거 |
|---|---|
| 실행 조건 이해 | 코드 외 실행 조건 4개 이상을 말한다. |
| 직접 설치 관찰 | DB 설치 후 service, port, data path, config 중 3개 이상을 찾는다. |
| 충돌 시나리오 이해 | 버전, port, 설정, 데이터 중 2개 이상을 원인으로 설명한다. |
| cleanup 이해 | 삭제해도 남을 수 있는 흔적 2개 이상을 말한다. |
| 재현성 이해 | 새 컴퓨터에서 다시 맞춰야 할 항목을 5개 이상 적는다. |
| Docker preview | Docker가 줄여 줄 불편함 1개와 대신 해결하지 못하는 것 1개를 말한다. |

## 산업 DevOps 연결
실무에서 환경 문제는 실력 부족이 아니라 재현성과 관리의 문제로 다룬다. 좋은 개발 환경은 다음 질문에 답할 수 있어야 한다.

- 어떤 runtime과 version이 필요한가?
- 어떤 외부 프로그램이 필요한가?
- 어떤 port를 사용하는가?
- 설정값은 어디에서 주입되는가?
- 데이터는 어디에 남는가?
- 새 컴퓨터에서도 같은 환경을 만들 수 있는가?
- 필요 없을 때 깔끔하게 정리할 수 있는가?

Day5는 이 질문을 학생의 로컬 컴퓨터 수준에서 이해시키고, Week2에서 Docker 명령어와 Compose로 옮긴다.

## AI 엔지니어링 연결
최근 AI 기능이 들어간 애플리케이션은 실행 환경이 더 복잡하다.

- LLM API key와 model 설정이 필요하다.
- vector DB나 embedding cache가 필요할 수 있다.
- prompt, retrieval 설정, temperature가 결과에 영향을 준다.
- GPU, driver, library version이 맞아야 하는 경우가 있다.
- 실험 결과와 로그가 빠르게 쌓인다.

따라서 AI 엔지니어링에서는 코드 작성 능력뿐 아니라 실행 환경을 기록하고 재현하고 정리하는 능력이 중요하다.
