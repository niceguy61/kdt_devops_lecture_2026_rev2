# Week 2 Day 5: Docker 운영 관점 통합, 보안, 이미지 배포 흐름, 발표

## Overview
Day 5는 Week 2 Docker 학습을 하나의 운영 가능한 handoff package로 통합한다. 학생은 Dockerfile, image, container, tag, Compose, README, 장애 기록을 따로따로 제출하지 않고, 다른 사람이 실행하고 확인하고 정리할 수 있는 형태로 묶는다.

오늘의 핵심 질문은 다음과 같다.

```text
Docker로 실행 환경을 표준화했다면, 그 결과물을 운영 관점에서 안전하고 재현 가능하게 전달하려면 무엇을 확인해야 하는가?
```

Day 5는 새로운 도구를 많이 늘리는 날이 아니다. 컨테이너가 VM이 아니라는 점, stateless app과 persistent data의 차이, 좋은 Dockerfile, secret 제외, image tag와 registry 흐름, 발표 evidence를 정리한다. Week 3의 MSA로 넘어가기 전에 단일 앱 Docker 실행 계약을 확실히 닫는다.

## Learning Goals
- container와 VM의 차이를 운영 관점에서 설명한다.
- stateless app, immutable image, persistent volume의 경계를 설명한다.
- 좋은 Dockerfile의 기준을 작고 명확하며 secret을 포함하지 않는 image 관점으로 평가한다.
- `.dockerignore`, base image tag, `CMD`, `EXPOSE`, healthcheck의 의미를 설명한다.
- root 실행, image 출처, tag 고정, secret 노출, public push 위험을 분류한다.
- build, tag, push, pull, run 흐름을 배포 파이프라인의 축소판으로 설명한다.
- 표준 실습 앱을 Dockerfile과 Compose로 실행 가능하게 정리한다.
- Week 2 발표에서 실행 방법, evidence, 장애/RCA, 남은 위험, Week 3 연결을 말한다.

## Lesson Index
| 교시 | 주제 | 핵심 산출물 |
|---|---|---|
| 1교시 | Docker 운영 관점 정리 | container/VM/stateless/immutable map |
| 2교시 | 좋은 Dockerfile 작성 원칙 | Dockerfile review checklist |
| 3교시 | 컨테이너 보안 기초 | secret/image/root/tag risk note |
| 4교시 | 이미지 배포 흐름 | build-tag-push-pull-run evidence map |
| 5교시 | 2주차 통합 실습 | build/run/compose/README package |
| 6교시 | 2주차 발표 | evidence-centered presentation card |
| 7교시 | 발표 피드백 및 live Q&A | improvement patch list |
| 8교시 | 다음 주차 Overview | Week 3 MSA readiness checklist |

## Practice Files And Assets
| 자료 | 용도 |
|---|---|
| `labs/integration-app/Dockerfile` | 좋은 Dockerfile 기준 실습 |
| `labs/integration-app/.dockerignore` | build context와 secret 제외 실습 |
| `labs/integration-app/compose.yaml` | 통합 Compose 실행 |
| `labs/integration-app/html/index.html` | HTTP body marker |
| `labs/integration-app/README.md` | 실습 앱 run/check/cleanup |
| `labs/integration-app/release-checklist.md` | 제출 전 이미지/보안/handoff 점검 |
| `hands-on-lab.md` | Day 5 전체 실행 흐름 |
| `academic-foundations.md` | 학술/현업 기준 mapping |
| `assets/lesson-01-docker-ops-model.png` | Docker 운영 모델 |
| `assets/lesson-02-good-dockerfile.png` | 좋은 Dockerfile 기준 |
| `assets/lesson-03-container-security.png` | 컨테이너 보안 기초 |
| `assets/lesson-04-image-flow.png` | image 배포 흐름 |
| `assets/lesson-05-integration-lab.png` | 통합 실습 evidence |
| `assets/lesson-06-presentation-evidence.png` | 발표 구조 |
| `assets/lesson-07-feedback-loop.png` | 피드백 수정 흐름 |
| `assets/lesson-08-week3-bridge.png` | Week 3 MSA 연결 |

## Required Evidence
| Evidence | 제출 기준 |
|---|---|
| Dockerfile evidence | base image, COPY 범위, CMD/EXPOSE/healthcheck 설명 |
| Build evidence | local image tag와 build 성공 기록 |
| Run evidence | `docker run`, `docker ps`, HTTP 200, body marker |
| Compose evidence | `docker compose config`, `up`, `ps`, HTTP check |
| Security evidence | secret 제외, `.dockerignore`, public push 주의 |
| Tag evidence | local tag와 tag naming 근거 |
| Failure evidence | build/run/port/secret/volume 중 하나 RCA |
| Handoff evidence | README build/run/check/cleanup section |
| Presentation evidence | 3분 발표 카드와 peer feedback |
| Week 3 readiness | service/network/dependency 질문 목록 |

## Official References
| Topic | Reference | 확인할 키워드 |
|---|---|---|
| Docker overview | https://docs.docker.com/engine/docker-overview/ | image, container, registry |
| Dockerfile reference | https://docs.docker.com/reference/dockerfile/ | FROM, COPY, CMD, EXPOSE, HEALTHCHECK |
| Build best practices | https://docs.docker.com/build/building/best-practices/ | small image, cache, context |
| Docker Scout base image policy | https://docs.docker.com/scout/policy/ | image update, vulnerabilities |
| Docker Hub repositories | https://docs.docker.com/docker-hub/repos/ | push, pull, tag |
| Docker security | https://docs.docker.com/engine/security/ | daemon, containers, isolation |
| Twelve-Factor App | https://12factor.net/ | config, backing services, build/release/run |

## Academic/Workforce Standards Alignment
| 기준 | Day 5 적용 | 학생 evidence |
|---|---|---|
| ABET problem analysis | Docker 운영 위험을 분류 | risk table |
| ABET communication | 실행 가능한 README와 발표 | handoff package |
| CS2023 Knowledge | image/container/tag/registry/security 개념 | concept map |
| CS2023 Skill | build/run/compose/tag/check 수행 | command evidence |
| CS2023 Disposition | secret 비노출과 cleanup 책임 | security note |
| NIST NICE | credential hygiene, least privilege, image trust | security checklist |
| Bloom Evaluate | Dockerfile과 image push 위험 평가 | review rubric |
| SRE practice | failure drill, RCA, evidence presentation | RCA note |

## Risk Register
| 위험 | 가능성 | 영향 | Severity | 완화 |
|---|---:|---:|---|---|
| secret을 image에 COPY | 중간 | 높음 | High | `.dockerignore`, review |
| `latest`만 제출 | 높음 | 중간 | Medium | explicit tag 사용 |
| public push 실수 | 낮음 | 높음 | High | push 전 checklist |
| root/admin 과용 | 중간 | 중간 | Medium | 최소 권한 설명 |
| cleanup 누락 | 높음 | 낮음 | Medium | container/image audit |
| port 충돌 | 높음 | 낮음 | Medium | host port 변경 |
| build context 과대 | 중간 | 중간 | Medium | `.dockerignore` |

## End-Of-Day Checklist
- [ ] Dockerfile을 읽고 각 instruction의 운영 의미를 설명했다.
- [ ] `.dockerignore`로 secret과 불필요 파일을 제외했다.
- [ ] local image를 build하고 tag를 확인했다.
- [ ] `docker run`으로 HTTP 200과 body marker를 확인했다.
- [ ] Compose로 같은 앱을 실행하고 확인했다.
- [ ] image push 위험과 tag 기준을 설명했다.
- [ ] 장애/RCA 기록 1개를 완성했다.
- [ ] README에 build/run/check/cleanup을 기록했다.
- [ ] 3분 발표에서 evidence와 남은 위험을 설명했다.
- [ ] Week 3 MSA readiness 질문을 작성했다.

## Completion Definition
Day 5는 다음 문장을 evidence와 함께 말할 수 있을 때 완료된다.

```text
이 표준 앱은 Dockerfile로 build할 수 있고, 명시적 tag로 식별할 수 있으며, docker run과 Compose 두 방식으로 HTTP evidence를 확인할 수 있다. README는 다음 사람이 실행, 확인, 정리, 장애 대응을 재현할 수 있게 한다.
```

## Next Connection
Week 3는 MSA로 넘어간다. Day 5에서 정리한 단일 service의 build/run/check/handoff 기준은 Week 3에서 frontend, api, database, worker 등 여러 service의 topology, dependency, network, health check, failure propagation을 다루는 기준이 된다.

## Final Submission Packet
| Artifact | Required Evidence |
|---|---|
| Dockerfile | instruction review note |
| `.dockerignore` | secret/context exclusion note |
| local image | explicit tag and build output |
| run evidence | `docker ps`, HTTP 200, body marker |
| Compose evidence | config/up/ps/check |
| security note | no secret, push decision |
| RCA | symptom, fix, recheck, prevention |
| README | build/run/check/cleanup |
| presentation card | evidence-centered 3-minute structure |
| Week 3 question | MSA readiness |

## Review Sequence
1. 파일이 있는지 본다.
2. 명령이 실행 가능한지 본다.
3. expected output이 있는지 본다.
4. 실패 기록이 있는지 본다.
5. secret과 cleanup 위험이 문서화됐는지 본다.
6. 다른 사람이 fresh clone 후 따라 할 수 있는지 본다.

## Day 5 Instructor Notes
- 새 기능 추가보다 handoff와 evidence를 우선한다.
- Docker Hub push는 기본 요구하지 않는다.
- 학생이 public push를 원하면 secret/content gate를 먼저 확인한다.
- 발표는 UI 시연보다 build/run/check/RCA/security 중심으로 유도한다.
- Week 3 preview는 MSA를 정답처럼 말하지 않고 운영 trade-off로 소개한다.
