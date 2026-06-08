# Week 2 Day 5 Academic Foundations

## 핵심 근거
| 근거 | Day 5 연결 |
|---|---|
| Docker overview | image, container, registry, Docker Engine의 공식 개념 |
| Dockerfile reference | Dockerfile instruction의 공식 동작 |
| Docker build best practices | 작은 image, cache, context, layer 관리 |
| Docker security docs | daemon 권한, container isolation, image trust |
| Docker Hub repositories | tag, push, pull, repository 흐름 |
| Twelve-Factor App | build/release/run 분리, config 분리 |
| Google SRE postmortem culture | 장애 기록을 blame이 아니라 learning으로 다룸 |

## Day 5 핵심 학습성과
| 학습성과 | 관찰 가능한 행동 | 산출 evidence |
|---|---|---|
| Docker 운영 모델 설명 | container, image, volume, registry 구분 | concept map |
| Dockerfile 평가 | build context, COPY, CMD, healthcheck 검토 | Dockerfile review |
| 보안 위험 분류 | secret, root, image source, tag 위험 설명 | security note |
| 배포 흐름 이해 | build-tag-push-pull-run 순서 설명 | image flow map |
| 통합 실행 | Dockerfile과 Compose로 앱 실행 | build/run/compose evidence |
| RCA 작성 | build/run/port/secret failure 분석 | RCA note |
| 전문 커뮤니케이션 | 발표와 README로 handoff | presentation card |
| 전이 준비 | Week 3 service dependency 질문 작성 | MSA readiness checklist |

## ABET-style Outcome Mapping
| ABET-style outcome | Day 5 적용 | 평가 증거 |
|---|---|---|
| 문제 분석 | Docker 운영 위험과 재현성 gap 분석 | risk register |
| solution 설계/구현/평가 | Dockerfile, Compose, README 통합 | integration package |
| 커뮤니케이션 | 3분 발표와 README handoff | presentation card |
| 전문적 책임 | secret, public push, cleanup 위험 설명 | security checklist |
| 협업 | peer feedback을 반영한 수정 | improvement patch list |

## CS2023 Knowledge, Skill, Disposition
| 범주 | Day 5 내용 |
|---|---|
| Knowledge | image, container, tag, registry, immutable image, stateless app |
| Skill | build, tag, run, compose, check, cleanup, RCA 작성 |
| Disposition | 운영 증거를 우선하고 secret과 data를 책임 있게 다룸 |

## NIST NICE-style Task/Knowledge/Skill
| 구분 | Day 5 적용 |
|---|---|
| Task | containerized application artifact를 검토하고 안전한 handoff 작성 |
| Knowledge | image trust, credential handling, runtime isolation, logging |
| Skill | build context 점검, secret 제외, failure evidence 수집 |
| Professional behavior | public registry push 전 검토와 최소 권한 태도 |

## Bloom's Taxonomy 적용
| Bloom 단계 | Day 5 질문 |
|---|---|
| Remember | image, container, registry, tag 용어를 말한다 |
| Understand | container가 VM이 아닌 이유를 설명한다 |
| Apply | Dockerfile로 image를 build하고 container를 실행한다 |
| Analyze | Dockerfile과 README에서 운영 위험을 찾는다 |
| Evaluate | push 가능 여부와 cleanup 위험을 판단한다 |
| Create | Week 2 최종 handoff package를 만든다 |

## SRE/DevOps 실무 기준
| 기준 | Day 5 구현 |
|---|---|
| Operational readiness | build/run/check/cleanup/recover 절차 포함 |
| Reproducibility | Dockerfile, tag, port, path, expected output 기록 |
| Observability | `docker ps`, `curl`, logs, healthcheck |
| Incident learning | failure drill과 RCA 템플릿 |
| Security | secret 제외, image trust, public push gate |
| Handoff | README와 발표 카드 |
| Risk classification | likelihood, impact, severity, mitigation |

## 공식 문서와 수업 활동 연결
| 공식 문서 | 수업에서 확인할 것 |
|---|---|
| Docker overview | container는 VM이 아니라 process isolation 모델임 |
| Dockerfile reference | 각 instruction의 build/runtime 영향 |
| Build best practices | 작은 image와 build context 관리 이유 |
| Docker security | daemon과 container 권한 위험 |
| Docker Hub repositories | tag, push, pull 흐름 |
| Twelve-Factor App | build/release/run 분리 |

## 필수 오해 점검
| 오해 | 바로잡는 설명 |
|---|---|
| container는 작은 VM이다 | kernel을 공유하는 isolated process model이다 |
| image 안에 설정을 다 넣으면 편하다 | config/secret은 image와 분리해야 한다 |
| `latest` tag면 충분하다 | 재현 가능한 evidence로는 부족하다 |
| build 성공이면 운영 준비 완료다 | run/check/log/cleanup이 필요하다 |
| public push는 단순 공유다 | secret, license, privacy, trust risk가 있다 |
| 보안은 Kubernetes부터 보면 된다 | image와 Dockerfile 단계부터 시작된다 |

## 평가 루브릭
| 항목 | 0점 | 1점 | 2점 |
|---|---|---|---|
| Dockerfile | 없음 | build만 됨 | instruction 의미 설명 |
| Build | 없음 | image만 있음 | tag와 build evidence 있음 |
| Run | 없음 | container running | HTTP 200과 body marker |
| Compose | 없음 | config만 있음 | up/check/cleanup 완료 |
| Security | 없음 | 주의 문구 | secret 제외와 push gate |
| RCA | 없음 | 증상만 있음 | fix/recheck/prevention 포함 |
| Handoff | 없음 | 명령만 있음 | expected result와 risk 포함 |
| Presentation | 없음 | 기능 소개 | evidence와 남은 위험 설명 |

## Day 5 완료 판정
| 완료 조건 | 증거 |
|---|---|
| 실행 가능성 | build/run/compose 성공 |
| 관찰 가능성 | HTTP status, body marker, logs |
| 보안성 | `.dockerignore`, secret 비노출 |
| 재현성 | explicit tag, README command |
| 회복 가능성 | RCA와 troubleshooting |
| 전달 가능성 | 발표 카드와 README |

## Week 3 전이
Day 5가 끝나면 학생은 단일 container app의 운영 계약을 설명할 수 있어야 한다. Week 3에서는 이 계약이 여러 service로 확장된다. service가 늘어나면 port, network, dependency, health, log, deployment unit이 모두 늘어난다. Day 5의 handoff 기준은 Week 3 topology 문서의 최소 단위가 된다.

## Professional Responsibility
| 책임 | 학생 행동 |
|---|---|
| Credential safety | secret을 image와 README에 넣지 않음 |
| Reproducibility | explicit tag와 expected output 기록 |
| Operational hygiene | cleanup과 resource audit 작성 |
| Communication | 발표와 README로 재현 경로 제공 |
| Incident learning | 실패를 RCA로 남김 |
| Scope control | push/cloud/Kubernetes를 필요 이상으로 확장하지 않음 |

## Formative Assessment Loop
```text
present -> receive feedback -> classify severity -> patch docs/code -> recheck -> record
```

이 loop가 있어야 발표가 평가 이벤트를 넘어 학습 이벤트가 된다.

## Evidence Anti-patterns
| Anti-pattern | 문제 |
|---|---|
| "성공" 한 단어 | 평가할 수 없음 |
| screenshot만 제출 | 재현 명령 부재 |
| Dockerfile만 제출 | runtime evidence 부재 |
| tag 없이 image 제출 | artifact 식별 불가 |
| cleanup 누락 | 다음 실습 충돌 |
| failure 숨김 | 운영 학습 부재 |
