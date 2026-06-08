# 5교시: 2주차 통합 실습

## 수업 목표
- 표준 실습 앱을 Dockerfile과 Compose로 모두 실행 가능하게 정리한다.
- build/run/check/compose/cleanup evidence를 하나의 handoff package로 묶는다.
- Week 2 최종 산출물의 누락 항목을 보완한다.

## 50분 흐름
| 시간 | 활동 | 비중 | 산출 |
|---|---|---:|---|
| 0-8분 | 통합 실습 목표 고정 | 설명 10% | package 기준 |
| 8-20분 | Dockerfile build/run | 실행 30% | build/run evidence |
| 20-32분 | Compose config/up/check | 실행 25% | compose evidence |
| 32-42분 | README handoff 작성 | 실행 20% | README section |
| 42-50분 | gap list와 cleanup | 실행 15% | final checklist |

### Visual 1: 통합 실습 evidence
![Integration lab evidence](https://raw.githubusercontent.com/niceguy61/kdt_devops_lecture_2026_rev2/main/week2/day5/assets/lesson-05-integration-lab.png)

이 visual은 Dockerfile build, container run, Compose 실행, README handoff가 하나의 제출 패키지로 이어지는 흐름을 보여준다.

## 핵심 설명
통합 실습은 새 앱을 화려하게 만드는 시간이 아니다. Week 2에서 배운 Docker 기능을 하나의 재현 가능한 패키지로 닫는 시간이다.

학생은 다음 주장을 evidence로 뒷받침해야 한다.

```text
이 앱은 Dockerfile로 image를 만들 수 있고, docker run과 Compose로 실행할 수 있으며, README만 보고 정상 확인과 cleanup을 할 수 있다.
```

## 실습 경로
```bash
cd week2/day5/labs/integration-app
```

## Build/run/check
```bash
docker build -t paperclip/week2-day5-integration:local .
docker run -d --name paperclip-day5-web -p 18085:80 paperclip/week2-day5-integration:local
docker ps --filter name=paperclip-day5-web
curl -I http://localhost:18085
curl -s http://localhost:18085 | grep week2-day5-integration-v1
```

## Compose check
```bash
docker rm -f paperclip-day5-web
docker compose config
docker compose up -d
docker compose ps
curl -I http://localhost:18085
curl -s http://localhost:18085 | grep week2-day5-integration-v1
```

## README handoff minimum
```markdown
## Docker
- Build:
- Run:
- Check:
- Compose:
- Cleanup:
- Failure drill:
- Security note:
```

## integration inventory
| 항목 | 상태 | Evidence |
|---|---|---|
| Dockerfile | complete/partial/missing | |
| `.dockerignore` | complete/partial/missing | |
| local image tag | complete/partial/missing | |
| docker run HTTP | complete/partial/missing | |
| Compose config/up | complete/partial/missing | |
| README handoff | complete/partial/missing | |
| RCA | complete/partial/missing | |
| cleanup | complete/partial/missing | |

## 실무 기준
통합 패키지는 다음 사람이 fresh clone 후 따라 할 수 있어야 한다. "내 PC에서 됨"은 통합 evidence가 아니다. path, command, port, expected output, cleanup이 모두 있어야 한다.

## 학술 기준 연결
이 교시는 portfolio assessment에 해당한다. 여러 활동 산출물을 하나의 증거 묶음으로 평가한다. ABET 커뮤니케이션 outcome도 포함된다. 학생은 기술 결과를 다른 사람이 실행 가능한 문서로 전달해야 한다.

## failure drill 선택
| Drill | 명령 | 기록할 원인 |
|---|---|---|
| wrong port | `curl -I http://localhost:80` | host port 오해 |
| missing image | 잘못된 tag로 run | tag mismatch |
| compose conflict | 같은 port 중복 실행 | cleanup 누락 |
| secret risk | `.dockerignore` 설명 | build context risk |

## 오해 점검
| 오해 | 교정 |
|---|---|
| Dockerfile만 제출하면 충분하다 | run/check/cleanup이 필요하다 |
| Compose만 되면 docker run은 몰라도 된다 | 둘의 관계를 설명해야 한다 |
| README는 마지막 장식이다 | README가 handoff의 핵심 artifact다 |
| 실패 기록은 감점이다 | 좋은 RCA는 운영 역량 evidence다 |

## 평가 기준
| 기준 | 2점 evidence |
|---|---|
| build | 명시적 tag로 image build |
| run | HTTP 200과 body marker |
| compose | config/up/check 완료 |
| handoff | README가 fresh run 가능 |
| RCA | recheck/prevention 포함 |

## cleanup
```bash
docker compose down
docker rm -f paperclip-day5-web
```

선택:

```bash
docker image rm paperclip/week2-day5-integration:local
```

## 전이 과제
통합 앱이 Week 3에서 `frontend`, `api`, `db`로 나뉜다면 오늘의 README는 어떻게 바뀌어야 하는지 3줄로 적는다.

### 공식 근거 링크
- Docker build best practices: https://docs.docker.com/build/building/best-practices/
- Docker Compose: https://docs.docker.com/compose/

## 통합 패키지 품질 기준
| 품질 | 설명 |
|---|---|
| 실행 가능 | 명령을 따라 하면 container가 실행된다 |
| 확인 가능 | HTTP/log/status evidence로 정상 판단 가능 |
| 복구 가능 | failure drill과 RCA가 있다 |
| 정리 가능 | container/image/volume cleanup이 문서화됨 |
| 전달 가능 | README만으로 다른 학생이 재현 가능 |

## evidence packet 예시
```markdown
## Evidence Packet
- `docker build`: success
- `docker images`: paperclip/week2-day5-integration:local
- `docker ps`: 18085->80
- `curl -I`: HTTP/1.1 200 OK
- body: week2-day5-integration-v1
- `docker compose config`: success
- cleanup: compose down
```

## 통합 실습 채점표
| 항목 | 0 | 1 | 2 |
|---|---|---|---|
| Build | 없음 | 성공만 기록 | tag와 build output |
| Run | 없음 | container running | HTTP 200과 body marker |
| Compose | 없음 | config만 | up/check/cleanup |
| Security | 없음 | 주의 문구 | `.dockerignore`와 push gate |
| RCA | 없음 | 증상만 | fix/recheck/prevention |
| Handoff | 없음 | 명령만 | expected output과 risk |

## 제출 전 audit
```bash
docker ps --filter name=paperclip-day5
docker images paperclip/week2-day5-integration
find . -maxdepth 2 -type f -print
```

audit에서 확인할 것은 남은 resource, image tag, 위험 파일이다.

## Lesson 5 Exit Ticket
```markdown
## Exit Ticket
- 통합 패키지에서 complete인 항목:
- partial인 항목:
- missing인 항목:
- Day 5 발표 전 반드시 고칠 항목:
```

## 통합 패키지 품질 기준
| 품질 | 설명 |
|---|---|
| 실행 가능 | 명령을 따라 하면 container가 실행된다 |
| 확인 가능 | HTTP/log/status evidence로 정상 판단 가능 |
| 복구 가능 | failure drill과 RCA가 있다 |
| 정리 가능 | container/image/volume cleanup이 문서화됨 |
| 전달 가능 | README만으로 다른 학생이 재현 가능 |

## fresh clone test 사고실험
다른 사람이 이 폴더만 받았다고 가정한다. 그 사람은 다음 질문에 답할 수 있어야 한다.

1. 어디로 이동해야 하는가?
2. 어떤 image tag로 build해야 하는가?
3. 어떤 port로 접속해야 하는가?
4. 정상 결과는 어떤 문자열인가?
5. Compose와 docker run 중 무엇을 먼저 실행할 수 있는가?
6. 실습 후 무엇을 지워야 하는가?

## evidence packet 예시
```markdown
## Evidence Packet
- `docker build`: success
- `docker images`: paperclip/week2-day5-integration:local
- `docker ps`: 18085->80
- `curl -I`: HTTP/1.1 200 OK
- body: week2-day5-integration-v1
- `docker compose config`: success
- cleanup: compose down
```

## RCA 연결
```markdown
- Symptom: bind for 0.0.0.0:18085 failed
- Hypothesis: another container already uses host port 18085
- Fix: stop old container or change WEB_PORT
- Recheck: curl returns HTTP 200
- Prevention: cleanup audit before rerun
```
