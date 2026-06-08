# Week 2 Day 5 Hands-on Lab: Build, Tag, Run, Compose, Handoff

## 목적
이 문서는 Day 5 전체 실습을 하나의 실행 흐름으로 묶는다. 목표는 Dockerfile과 Compose를 따로 아는 것이 아니라, build/run/check/cleanup/RCA/handoff를 하나의 운영 패키지로 완성하는 것이다.

## Phase A: preflight
```bash
cd week2/day5/labs/integration-app
docker version
docker compose version
docker compose config
```

기대 결과:

```text
Docker server information is shown
Docker Compose version is shown
services:
  web:
```

## Phase B: Dockerfile review
```bash
sed -n '1,160p' Dockerfile
sed -n '1,120p' .dockerignore
```

기록할 항목:

| 항목 | 질문 |
|---|---|
| `FROM` | base image tag가 명시적인가 |
| `COPY` | 필요한 파일만 image에 들어가는가 |
| `EXPOSE` | container 내부 service port가 무엇인가 |
| `HEALTHCHECK` | 정상 상태를 어떻게 확인하는가 |
| `.dockerignore` | secret과 불필요 파일을 제외하는가 |

## Phase C: build
```bash
docker build -t paperclip/week2-day5-integration:local .
docker images paperclip/week2-day5-integration
```

기대 결과:

```text
paperclip/week2-day5-integration   local
```

## Phase D: run and check
```bash
docker run -d \
  --name paperclip-day5-web \
  -p 18085:80 \
  paperclip/week2-day5-integration:local

docker ps --filter name=paperclip-day5-web
curl -I http://localhost:18085
curl -s http://localhost:18085 | grep week2-day5-integration-v1
docker logs paperclip-day5-web
```

기대 결과:

```text
0.0.0.0:18085->80/tcp
HTTP/1.1 200 OK
week2-day5-integration-v1
```

## Phase E: tag flow
```bash
docker tag paperclip/week2-day5-integration:local paperclip/week2-day5-integration:v1
docker images paperclip/week2-day5-integration
```

기록:

```markdown
local tag:
release-style tag:
why not only latest:
```

## Phase F: Compose verification
```bash
docker rm -f paperclip-day5-web
docker compose config
docker compose up -d
docker compose ps
curl -I http://localhost:18085
curl -s http://localhost:18085 | grep week2-day5-integration-v1
```

## Phase G: failure drill
하나를 선택한다.

| Drill | 방법 | 기대 분류 |
|---|---|---|
| wrong port | `curl -I http://localhost:80` | host port 오해 |
| build context | `.dockerignore` 의미 설명 | context risk |
| tag confusion | `latest`만 있을 때 문제 설명 | reproducibility |
| cleanup | container/image가 남는 문제 | resource hygiene |

## Phase H: RCA 기록
```markdown
## Day 5 RCA
- Symptom:
- Failed command:
- Error excerpt:
- Category: build / run / port / tag / security / cleanup
- Hypothesis:
- Fix:
- Recheck:
- Prevention:
```

## Phase I: security gate
```bash
find . -maxdepth 2 -type f -print
```

확인할 것:
- `.env`가 build context에 들어가지 않는가?
- token, password, MFA code, SSH key가 문서에 없는가?
- public push를 하지 않아도 제출 evidence가 충분한가?
- Dockerfile이 불필요한 파일을 COPY하지 않는가?

## Phase J: cleanup
```bash
docker compose down
docker rm -f paperclip-day5-web
docker ps --filter name=paperclip-day5
```

선택 image cleanup:

```bash
docker image rm paperclip/week2-day5-integration:local
docker image rm paperclip/week2-day5-integration:v1
```

## Phase K: handoff package
```markdown
## Week 2 Docker Handoff
- Build:
- Run:
- Check:
- Compose:
- Security:
- Failure:
- Cleanup:
- Week 3 question:
```

## Strong Evidence Checklist
- [ ] Dockerfile review note exists.
- [ ] `.dockerignore` review note exists.
- [ ] build command and image tag are recorded.
- [ ] run command and HTTP evidence are recorded.
- [ ] Compose config/up/check are recorded.
- [ ] RCA includes recheck and prevention.
- [ ] README can be followed by another student.
- [ ] Week 3 MSA readiness question is written.

## Completion Statement
```text
I built a local Docker image, ran it as a container, verified HTTP evidence, verified Compose execution, documented security and cleanup risks, and prepared a handoff package for Week 3.
```
