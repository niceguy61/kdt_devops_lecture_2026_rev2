# 8교시: 보충 실습 - 기본 명령 재실습과 Day 2 준비

## 수업 목표
- Day 1 Docker 기본 cycle을 반복 실행해 명령 목적과 evidence 기록을 안정화한다.
- 실행 중 container와 stopped container를 정리하고, 다음 실습에 영향을 주지 않는 상태로 마감한다.
- Day 2 Dockerfile 학습을 위해 image, container, command, port, log의 의미를 readiness note로 정리한다.

## 50분 흐름
| 시간 | 활동 | 비중 | 학생 산출 |
|---|---|---:|---|
| 0-5분 | 보충 실습 목표 확인 | 설명 10% | 자기 목표 선택 |
| 5-20분 | 기본 명령 cycle 반복 | 실행 30% | evidence table |
| 20-35분 | nginx 재실행과 HTTP 확인 | 실행 30% | `200 OK` 기록 |
| 35-42분 | HTML 수정 반영 또는 cleanup 확인 | 실행 15% | source edit / cleanup check |
| 42-47분 | Day 2 Dockerfile readiness note | 실행 5% | readiness note |
| 47-50분 | 질문 1개와 마감 | 설명 10% | next question |

### Visual 1: Docker Day 1 보충 실습 보드
![Docker Day 1 보충 실습 보드](https://raw.githubusercontent.com/niceguy61/kdt_devops_lecture_2026_rev2/main/week2/day1/assets/lesson-08-supplemental-practice-board.png)

이 이미지는 반복 실행, nginx 재실행, 정리 확인, Day 2 준비를 하나의 보드로 보여준다. 학생은 빈칸을 채우듯 command, 결과 요약, screenshot filename, blocker를 기록한다.

## 반복 실습 A: 기본 명령 cycle

```bash
docker version
docker pull nginx:latest
docker images
```

기록할 것:
- Client/Server가 모두 보이는가
- `nginx:latest`가 pull 가능한가
- image 목록에서 `nginx`와 `hello-world`를 구분할 수 있는가

## 반복 실습 B: nginx 재실행

```bash
docker run -d --name paperclip-day1-nginx -p 18080:80 nginx:latest
docker ps --filter name=paperclip-day1-nginx
curl -I http://localhost:18080
docker logs paperclip-day1-nginx
```

정상 기준:
- `docker run -d`가 container ID를 출력한다.
- `docker ps`에서 `Up` 상태와 `18080->80/tcp` port binding이 보인다.
- `curl -I`에서 `HTTP/1.1 200 OK`가 보인다.
- `docker logs`에서 nginx startup log가 보인다.

## 반복 실습 C: HTML 수정 반영 확인

6교시에서 시간이 부족했던 학생은 여기서 10분 안에 bind mount 실습을 반복한다.

```bash
docker run -d \
  --name paperclip-day1-nginx-edit \
  -p 18081:80 \
  -v "$PWD/week2/day1/labs/nginx-html:/usr/share/nginx/html:ro" \
  nginx:latest

curl -s http://localhost:18081
```

[labs/nginx-html/index.html](./labs/nginx-html/index.html)의 `<h1>` 문구를 수정하고 다시 `curl -s http://localhost:18081`을 실행한다. 응답에 수정된 문구가 보이면 host file이 container nginx에 반영된 것이다.

정리:

```bash
docker stop paperclip-day1-nginx-edit
docker rm paperclip-day1-nginx-edit
```

## 반복 실습 D: 정리 확인

```bash
docker stop paperclip-day1-nginx
docker rm paperclip-day1-nginx
docker ps --filter name=paperclip-day1-nginx
docker ps -a --filter name=paperclip-day1-nginx
```

정상 기준:
- `stop`과 `rm`은 container 이름을 반환한다.
- 정리 후 `docker ps`와 `docker ps -a`에서 해당 container가 보이지 않는다.

## Linux 사전 테스트 요약
| 항목 | 테스트 결과 |
|---|---|
| OS | Ubuntu 24.04.3 LTS on Linux 6.6.87.2 WSL2 |
| Docker | Client `29.0.2`, Server `29.3.1` |
| hello-world | `Hello from Docker!` 출력 성공 |
| nginx run | `paperclip-day1-nginx` 실행 성공 |
| HTTP check | `HTTP/1.1 200 OK` |
| bind mount source edit | v1 HTML 응답 확인 후 host file 수정, v2 응답 확인 |
| logs | nginx `Configuration complete; ready for start up` 확인 |
| cleanup | `stop`, `rm`, recheck 성공 |

## Day 2 readiness note
```markdown
## Dockerfile Readiness
- 오늘 실행한 image:
- 오늘 실행한 container name:
- container start command:
- host source path:
- host port -> container port:
- 정상 확인 방법:
- log 확인 방법:
- 정리 방법:
- Day 2 질문:
```

## 흔한 오해
| 오해 | 바로잡기 |
|---|---|
| 보충 실습은 느린 학생만 한다. | 반복 실행은 명령 목적을 몸에 익히는 정상 학습이다. |
| cleanup은 선택이다. | 다음 실습의 port 충돌을 막기 위해 필수다. |
| Dockerfile은 완전히 새로운 내용이다. | Dockerfile은 오늘 실행한 image, command, port, file 조건을 build 문서로 옮기는 것이다. |

## 평가 기준
| 기준 | 2점 evidence |
|---|---|
| 반복 실행 | 기본 cycle을 한 번 이상 재실행했다. |
| HTTP 확인 | `curl -I` 또는 browser로 `200 OK`를 확인했다. |
| cleanup | running/stopped container가 남지 않게 정리했다. |
| readiness | Day 2 Dockerfile readiness note를 작성했다. |
| 질문 | 다음 수업으로 가져갈 질문 1개를 남겼다. |

### 공식 근거 링크
- Docker Docs: Writing a Dockerfile, https://docs.docker.com/guides/docker-concepts/building-images/writing-a-dockerfile/
- Docker Docs: Running containers, https://docs.docker.com/get-started/docker-concepts/running-containers/

### 다음 연결
Day 2는 오늘의 실행 조건을 Dockerfile로 고정한다. `nginx` image를 실행해 본 경험을 바탕으로 `FROM`, `COPY`, `CMD`, `EXPOSE`가 어떤 실행 조건을 문서화하는지 배운다.
