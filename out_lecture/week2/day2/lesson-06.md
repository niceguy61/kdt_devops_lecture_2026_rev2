# 6교시: 컨테이너 실행 검증

## 수업 목표
- build한 image에서 실행한 container가 실제로 소스 파일을 제공하는지 검증한다.
- `docker ps`, `curl`, `docker logs`, `docker exec`를 이용해 port, HTTP, log, 내부 파일 evidence를 확보한다.
- 확인 후 container를 정리한다.

## 50분 흐름
| 시간 | 활동 | 비중 | 학생 산출 |
|---|---|---:|---|
| 0-5분 | 검증 목표 확인 | 설명 10% | evidence plan |
| 5-15분 | container 실행/ps 확인 | 실행 20% | ps output |
| 15-25분 | HTTP와 source text 확인 | 실행 25% | curl output |
| 25-35분 | logs와 내부 파일 확인 | 실행 25% | log/exec evidence |
| 35-45분 | cleanup/recheck | 실행 15% | cleanup evidence |
| 45-50분 | 다음 tag 수업 연결 | 설명 5% | tag question |

### Visual 1: 컨테이너 실행 검증
![컨테이너 실행 검증](https://raw.githubusercontent.com/niceguy61/kdt_devops_lecture_2026_rev2/main/week2/day2/assets/lesson-06-container-verification.png)

이 이미지는 실행 검증을 `ps`, HTTP, logs, `exec`, cleanup으로 나눈다. 하나만 성공해도 충분하다고 보지 않고 서로 다른 증거를 모아 정상 상태를 확정한다.

## Hands-on
```bash
docker run -d --name paperclip-day2-static -p 18082:80 paperclip-static-site:day2
docker ps --filter name=paperclip-day2-static
curl -I http://localhost:18082
curl -s http://localhost:18082 | grep "Dockerfile로 만든 표준 실습 앱"
docker logs paperclip-day2-static
docker exec paperclip-day2-static ls -l /usr/share/nginx/html
docker stop paperclip-day2-static
docker rm paperclip-day2-static
```

## Linux 사전 테스트 결과
내부 파일 확인:

```text
total 12
-rw-r--r--    1 root root   497 50x.html
-rwxrwxrwx    1 root root  1188 index.html
-rwxrwxrwx    1 root root  1156 styles.css
```

source text 확인:

```text
<h1>Dockerfile로 만든 표준 실습 앱</h1>
```

## 다중 evidence가 필요한 이유
하나의 evidence만으로는 운영 판단이 약할 수 있다. `docker ps`에서 container가 `Up`이어도 HTTP가 실패할 수 있고, HTTP가 200이어도 기대한 source가 image에 들어갔는지는 확인되지 않을 수 있다. 그래서 Day 2는 최소 네 종류의 evidence를 모은다.

| evidence | 확인하는 층 | 놓칠 수 있는 것 |
|---|---|---|
| `docker ps` | container lifecycle, port binding | 앱 내용이 맞는지 |
| `curl -I` | HTTP status/header | body 내용이 맞는지 |
| `curl -s ... grep` | source content | 내부 path 구조 |
| `docker logs` | process log/request log | image에 파일이 있는지 |
| `docker exec ls` | container filesystem | 외부 접속 가능 여부 |

이렇게 층을 나누어 보면 장애 분석도 쉬워진다. `ps`는 정상인데 `curl`이 실패하면 port/network 쪽을 본다. `curl -I`는 200인데 body가 다르면 build context나 COPY 결과를 본다. `exec`에서 파일이 없으면 Dockerfile의 `WORKDIR`/`COPY`를 다시 본다.

## 운영 handoff 기준
다른 엔지니어에게 넘길 때는 "실행됩니다"가 아니라 다음 정보가 필요하다.

```text
image: paperclip-static-site:day2
container: paperclip-day2-static
host port: 18082
container port: 80
expected status: HTTP/1.1 200 OK
expected text: Dockerfile로 만든 표준 실습 앱
cleanup: docker stop + docker rm
```

## 핵심 유의사항
6교시는 검증 중심 수업이다. `curl` 한 번 성공했다고 끝내면 evidence가 부족하다. container lifecycle, network/port, HTTP header, body content, 내부 filesystem은 서로 다른 층의 evidence다. 한 층이 정상이어도 다른 층이 틀릴 수 있다.

`docker logs`는 application log이면서 nginx access log 역할도 한다. `curl`을 실행한 뒤 logs를 보면 요청 흔적이 남는다. 이 연결을 보여주면 학생은 "내가 보낸 요청이 container 안 process까지 도달했는가"를 확인하는 감각을 갖게 된다.

`docker exec`는 container 안으로 들어가서 수정하라는 명령이 아니다. 초급 과정에서는 내부 상태 확인 도구로 사용한다. container 안 파일을 직접 수정하면 image build와 runtime writable layer를 혼동하게 되므로, 수정은 host source를 바꾸고 rebuild하거나 bind mount 실습에서 다룬다.

cleanup은 선택이 아니다. 실습 container가 남아 있으면 다음 학생이나 다음 교시에서 port 충돌이 생긴다. 특히 7교시 bind mount 실습은 같은 nginx port를 다시 쓰므로 6교시 끝에서 `docker ps` 재확인까지 해야 한다.

## 자주 놓치는 검증 지점
| 놓치는 지점 | 겉으로 보이는 증상 | 바로잡는 확인 |
|---|---|---|
| `docker ps`만 보고 성공 처리 | HTTP 접속 실패를 늦게 발견 | `curl -I`까지 실행 |
| header만 확인 | 예전 image의 body를 보고 있음 | body text `grep` |
| logs를 안 봄 | 요청이 container까지 갔는지 모름 | `docker logs` |
| exec를 수정 도구로 사용 | image와 writable layer 혼동 | `exec ls`처럼 read-only 확인 |
| cleanup 생략 | 다음 실습 port/name 충돌 | `docker ps --filter name=paperclip` |

## 장애 분기표
| 관찰 결과 | 가능성 | 다음 명령 |
|---|---|---|
| `docker ps`에 container 없음 | process가 종료됨 | `docker ps -a`, `docker logs` |
| container는 Up, `curl` 실패 | port publish 문제 | `docker ps` PORTS 확인 |
| `curl -I` 200, body text 없음 | 다른 image/tag 실행 가능성 | `docker images`, run command 확인 |
| body는 맞지만 logs 없음 | 요청 방식 또는 log 확인 시점 문제 | `curl` 재실행 후 `docker logs` |
| exec에서 파일 없음 | `WORKDIR`/`COPY` 문제 | `docker history`, Dockerfile 확인 |

## 학생 기록 템플릿
```markdown
## Lesson 6 Runtime Verification Evidence
- image:
- container name:
- `docker ps` status:
- PORTS:
- HTTP status:
- body text check:
- logs에서 확인한 요청:
- 내부 파일 목록:
- cleanup 후 `docker ps` 결과:
```

## 빠른 학생 확장
시간이 남으면 같은 image를 다른 container name과 host port로 실행해 본다.

```bash
docker run -d --name paperclip-day2-static-alt -p 18084:80 paperclip-static-site:day2
curl -I http://localhost:18084
docker logs paperclip-day2-static-alt
docker rm -f paperclip-day2-static-alt
```

이 확장은 image와 container instance의 차이를 다시 확인한다. image는 같지만 container name과 host port는 다를 수 있다. 반대로 같은 container name은 동시에 두 번 사용할 수 없다.

## cleanup audit
마무리 단계에서 아래 명령을 실행한다.

```bash
docker ps --filter name=paperclip
docker ps -a --filter name=paperclip
```

정상 기준은 실행 중인 Day 2 container가 없고, 다음 실습에서 사용할 name과 port가 비어 있는 것이다. 만약 남아 있다면 이름을 확인하고 수업용 container인지 판단한 뒤 정리한다.

## 평가 기준
| 기준 | 2점 evidence |
|---|---|
| ps | container status와 port binding을 확인했다. |
| HTTP | `curl -I`와 source text를 확인했다. |
| logs | nginx startup 또는 request log를 찾았다. |
| exec | container 내부 파일 위치를 확인했다. |
| cleanup | stop/rm 후 남은 container가 없음을 확인했다. |

### 공식 근거 링크
- Docker exec: https://docs.docker.com/reference/cli/docker/container/exec/
- Docker logs: https://docs.docker.com/reference/cli/docker/container/logs/
- Docker run: https://docs.docker.com/reference/cli/docker/container/run/
