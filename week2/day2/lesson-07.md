# 7교시 · 실패 사례 다섯 가지

> [!NOTE]
> **이번 시간에 할 일**
>
> - 초보자가 가장 자주 만나는 Docker 실패 다섯 가지를 일부러 만듭니다.
> - 에러 메시지에서 원인을 찾는 연습을 합니다.
> - "컨테이너는 Up인데 안 돼요"를 1주차 3일차 지식으로 풉니다.
> - 나만의 문제 해결 표를 만들어 저장소에 올립니다.

## 오늘의 디버깅 순서

1주차 3일차 6교시의 "앞에서부터 하나씩 좁혀 가기"를 컨테이너에 맞게 바꾸면 이렇습니다.

![컨테이너 디버깅 순서 — 이미지, 상태, 로그, 포트, 안쪽 순서로 좁혀 간다](../../assets/week2/day2/w2d2-debug-order.png)

| 순서 | 질문 | 명령 |
|---|---|---|
| 1 | 이미지 이름이 맞나? | `docker images`, 에러 메시지의 이름 |
| 2 | 컨테이너가 살아 있나? | `docker ps -a` (STATUS와 종료 코드) |
| 3 | 컨테이너가 무슨 말을 남겼나? | `docker logs 이름` |
| 4 | 포트가 제대로 이어졌나? | `docker port 이름`, `-p 바깥:안` 순서 |
| 5 | 안에서는 되나? | `docker exec 이름 …` |

## 실패 1 · 이름 충돌

> **🧪 실습: 만들어 보기**
>
> ```bash
> docker run -d --name web -p 8080:80 nginx:1.30-alpine
> docker run -d --name web -p 8081:80 nginx:1.30-alpine
> ```

> **🟢 확인: 보이는 에러**
>
> ```text
> docker: Error response from daemon: Conflict. The container name "/web" is already in use by
> container "7c1e3a9b…". You have to remove (or rename) that container to be able to reuse that name.
> ```

| 원인 | 해결 |
|---|---|
| 같은 이름의 컨테이너가 이미 있다 (멈춘 것 포함!) | 다른 이름을 쓰거나 `docker rm -f web` 후 다시 |

에러 메시지가 해결 방법(`remove (or rename)`)까지 알려 줍니다. 멈춘 컨테이너도 이름을 차지한다는 것이 함정입니다. `docker ps`가 아니라 **`docker ps -a`**로 확인해야 보입니다.

```bash
docker rm -f web
```

## 실패 2 · 태그 오타

> **🧪 실습: 만들어 보기**
>
> ```bash
> docker run -d --name web -p 8080:80 nginx:1.30-alpin
> ```

> **🟢 확인: 보이는 에러**
>
> ```text
> Unable to find image 'nginx:1.30-alpin' locally
> docker: Error response from daemon: failed to resolve reference
> "docker.io/library/nginx:1.30-alpin": docker.io/library/nginx:1.30-alpin: not found
> ```

| 원인 | 해결 |
|---|---|
| 레지스트리에 그 태그가 없다 (`alpin`) | Docker Hub의 이미지 페이지(Tags 탭)에서 정확한 태그 확인 |

어제 7교시의 **저장소 이름 오타**(`hello-wrold`)는 `repository does not exist`, 오늘의 **태그 오타**는 `not found`로 나옵니다. 메시지의 차이로 어느 부분이 틀렸는지 알 수 있습니다.

## 실패 3 · 컨테이너가 바로 꺼져요

> **🧪 실습: 만들어 보기**
>
> ```bash
> docker run -d --name quick alpine:3.24
> docker ps
> docker ps -a --format "table {{.Names}}\t{{.Status}}\t{{.Command}}"
> ```

> **🟢 확인: 보이는 결과**
>
> ```text
> NAMES     STATUS                     COMMAND
> quick     Exited (0) 3 seconds ago   "/bin/sh"
> ```
> 에러는 없는데 `docker ps`에 없습니다.

| 원인 | 해결 |
|---|---|
| alpine의 기본 명령은 `/bin/sh`. 백그라운드(`-d`)에서는 입력할 사람이 없으니 셸이 **바로 끝나고**, PID 1이 끝나면 컨테이너도 끝난다 | 들어가서 쓰려면 `docker run -it`, 계속 살려 두려면 끝나지 않는 명령을 준다 |

```bash
docker rm quick
docker run -d --name alive alpine:3.24 sleep 3600
docker ps --format "table {{.Names}}\t{{.Status}}"
docker rm -f alive
```

`sleep 3600`(1시간 동안 잠자기)처럼 **끝나지 않는 PID 1**을 주면 계속 Up입니다. 3교시 학술 노트의 "PID 1이 끝나면 컨테이너도 끝난다"의 실제 사례입니다. 실무에서 "컨테이너가 계속 재시작해요"의 상당수가 **앱이 시작하자마자 에러로 끝나는** 경우이며, 그때는 `docker logs`가 답을 알려 줍니다.

## 실패 4 · Up인데 접속이 안 돼요 (`127.0.0.1`의 함정)

> **🧪 실습: 만들어 보기**
>
> 파이썬에 들어 있는 간단한 웹 서버를 **일부러 `127.0.0.1`에서만** 기다리게 실행합니다.
>
> ```bash
> docker run -d --name py-bad -p 8090:8000 python:3.14-slim \
>   python -m http.server 8000 --bind 127.0.0.1
> docker ps --format "table {{.Names}}\t{{.Ports}}\t{{.Status}}"
> curl http://localhost:8090
> ```
> - 줄 끝의 `\`는 "명령이 다음 줄로 이어진다"는 뜻입니다.

> **🟢 확인: 보이는 결과**
>
> ```text
> NAMES     PORTS                                       STATUS
> py-bad    0.0.0.0:8090->8000/tcp, [::]:8090->8000/tcp   Up 5 seconds
> curl: (56) Recv failure: Connection reset by peer
> ```
> (Docker Desktop에서는 `curl: (52) Empty reply from server`로 나오기도 합니다.) 컨테이너는 Up, 포트 연결도 화살표가 있는데 접속이 안 됩니다.

> [!IMPORTANT]
> **1주차 3일차 3교시의 그 함정**
>
> 컨테이너 안에서 앱이 **`127.0.0.1`(나 자신)**에서만 기다리면, 바깥에서 포트 연결을 타고 들어온 손님은 **컨테이너의 네트워크 카드**로 들어오기 때문에 앱에 닿지 못합니다. 건물(컨테이너)의 정문으로 손님을 안내했는데, 직원은 **안쪽 사무실 문(127.0.0.1)**만 열어 둔 셈입니다. 컨테이너 안의 앱은 **`0.0.0.0`(모든 문)**에서 기다려야 합니다.

```bash
docker exec py-bad python -c "import urllib.request; print(urllib.request.urlopen('http://127.0.0.1:8000').status)"
```

> **🟢 확인: 안에서는 된다**
>
> ```text
> 200
> ```
> 디버깅 순서 5번 — **안에서는 되고 밖에서는 안 된다**면, 앱이 기다리는 주소를 의심합니다.

```bash
docker rm -f py-bad
docker run -d --name py-good -p 8090:8000 python:3.14-slim python -m http.server 8000
curl -s http://localhost:8090 | head -3
docker rm -f py-good
```

`--bind`를 빼면 파이썬 웹 서버는 모든 주소에서 기다리므로 이번에는 디렉터리 목록 HTML이 나옵니다. 3일차에 만드는 DevMart API가 `--bind 0.0.0.0:8000`으로 실행되는 이유입니다.

## 실패 5 · 포트 순서를 거꾸로

> **🧪 실습: 만들어 보기**
>
> ```bash
> docker run -d --name rev -p 80:8080 nginx:1.30-alpine
> curl http://localhost:8080
> curl http://localhost:80
> ```

> **🟢 확인: 보이는 결과**
>
> ```text
> curl: (7) Failed to connect to localhost port 8080 after 0 ms: Couldn't connect to server
> curl: (56) Recv failure: Connection reset by peer
> ```
> (호스트의 80번이 이미 사용 중이면 `port is already allocated`가 날 수도 있습니다.)

| 원인 | 해결 |
|---|---|
| `-p 80:8080`은 "노트북 80 → 컨테이너 8080". 그런데 nginx는 컨테이너 안 **80**에서 기다린다 | **바깥:안** — `-p 8080:80` |

첫 번째 curl은 노트북 8080에 아무도 없어서(**refused**), 두 번째는 컨테이너 8080에 아무도 없어서 실패했습니다. 1주차 3일차의 에러 표가 여기서도 그대로 통합니다.

```bash
docker rm -f rev
```

## 실습 16 · 나만의 문제 해결 표

> **🧪 실습: 실습 목표**
>
> 오늘 만난 에러를 내 말로 정리해 저장소에 남깁니다. 다음 주, 다음 달의 내가 읽을 **첫 번째 런북**입니다(1주차 5일차 6교시).

VS Code에서 `~/devops-lab/day2/troubleshooting.md`를 만들고 아래 표를 **내 말로** 채웁니다.

```markdown
# Docker 문제 해결 표 (2주차 2일차)

| 보인 에러 / 증상 | 원인 | 해결 명령 |
|---|---|---|
| port is already allocated | | |
| Conflict. The container name ... is already in use | | |
| ...: not found (이미지) | | |
| docker ps에 없고 ps -a에서 Exited (0) | | |
| Up인데 Connection reset / Empty reply | | |
| Exited (137) | | |
```

```bash
cd ~/devops-lab
git add day2/troubleshooting.md
git commit -m "2일차: Docker 문제 해결 표"
git push
```

> **🧹 정리: 오늘의 정리**
>
> ```bash
> docker ps -a
> docker container prune
> docker ps -a
> ```
> 머리줄만 남으면 깨끗합니다. 이미지(`alpine`, `nginx`, `python`)는 내일도 쓰므로 남겨 둡니다.

> **🎓 학술 노트 — 디버깅은 가설 검증이다**
>
> 컴퓨터 과학자 안드레아스 첼러(Andreas Zeller)는 『Why Programs Fail』(2009)에서 디버깅을 **과학적 방법**으로 설명했습니다. ① 실패를 관찰하고, ② 원인에 대한 **가설**을 세우고, ③ 가설을 확인할 **실험**을 설계하고, ④ 결과로 가설을 받아들이거나 버리는 과정을 반복하는 것입니다. 무작정 이것저것 바꿔 보는 것이 아니라, **한 번에 하나씩** 바꾸며 범위를 좁혀 가는 것이 핵심입니다.
>
> 오늘 실패 4에서 우리는 "앱이 127.0.0.1에서만 기다린다"는 가설을 세우고, **안에서 접속하는 실험**(`docker exec … urlopen`)으로 확인한 뒤, `--bind`를 빼는 한 가지 변경으로 고쳤습니다. 이것이 디버깅의 정석입니다. 1주차 5일차 5교시 장애 대응에서 "원인을 몰라도 먼저 피해를 멈추고, 원인 분석은 차분히"라고 한 그 차분한 분석이 바로 이 과정입니다.
>
> - Zeller, A. (2009). *Why Programs Fail: A Guide to Systematic Debugging* (2nd ed.). Morgan Kaufmann.
> - Agans, D. J. (2002). *Debugging: The 9 Indispensable Rules*. AMACOM.

> **📈 트렌드 — AI에게 에러를 물을 때**
>
> 에러 메시지를 AI 도구에 붙여 넣고 원인을 묻는 것은 이제 흔한 일입니다. Docker Desktop에도 AI 도우미가 들어가 있습니다. 하지만 AI는 여러분의 노트북을 직접 볼 수 없으므로, 위 디버깅 순서 1~5의 **결과를 함께** 주어야 정확한 답을 받습니다(1주차 1일차의 "좋은 질문"). 그리고 AI가 제안한 명령, 특히 `prune`, `rm -rf`, `--volumes`, `sudo`가 들어간 명령은 **무엇을 지우는지 읽고 나서** 실행합니다. 오늘 만든 문제 해결 표를 AI에게 맥락으로 함께 주면, AI도 여러분 환경에 맞는 답을 더 잘 합니다.

## 정리 — 오늘 손에 익힌 명령

| 하고 싶은 것 | 명령 |
|---|---|
| 이미지 받기 / 목록 | `docker pull 이미지:태그` / `docker images` |
| 들어가 보기 (새 컨테이너) | `docker run -it --rm 이미지 sh` |
| 백그라운드 실행 + 포트 | `docker run -d --name 이름 -p 바깥:안 이미지` |
| 목록 | `docker ps` / `docker ps -a` |
| 관찰 | `docker logs -f`, `docker exec -it 이름 sh`, `docker inspect`, `docker stats` |
| 멈추기 / 켜기 / 지우기 | `docker stop` / `docker start` / `docker rm -f` |
| 정리 | `docker container prune`, `docker image rm`, `docker system df` |

> **✅ 확인 문제**
>
> 1. 멈춘 컨테이너도 이름을 차지하나요? 어떻게 확인하나요?
> 2. 이미지 **태그** 오타와 **저장소 이름** 오타는 에러 메시지가 어떻게 다른가요?
> 3. `docker run -d alpine:3.24`가 바로 Exited (0)가 되는 이유는?
> 4. 컨테이너가 Up이고 포트도 연결됐는데 Connection reset이 나면 무엇을 의심하나요?
> 5. nginx를 `-p 80:8080`으로 띄우면 왜 접속이 안 되나요?
>
> <details><summary>정답</summary>
>
> 1. 차지한다. `docker ps -a`로 확인한다
> 2. 태그 오타는 `not found`, 저장소 이름 오타는 `repository does not exist`
> 3. 기본 명령인 sh가 입력이 없어 바로 끝나고, PID 1이 끝나면 컨테이너도 끝나기 때문
> 4. 앱이 컨테이너 안에서 127.0.0.1에서만 기다리는지 (0.0.0.0이어야 한다)
> 5. 바깥 80 → 안 8080으로 연결되는데, nginx는 안의 80에서 기다리기 때문 (바깥:안 순서)
>
> </details>

> [!NOTE]
> **오늘의 배움일기**
>
> - 오늘 본 에러 중 가장 당황스러웠던 것과, 이제 원인을 한 문장으로 설명해 보기
> - 이미지와 컨테이너의 차이를 1주차 2일차의 "프로그램과 프로세스"에 빗대어 설명해 보기
> - `docker top`에서 PID 1이 다른 번호로 보인 것을 보고 든 생각
> - 내일 Dockerfile 시간에 만들고 싶은 이미지 아이디어 하나

## 참고 문헌

- Docker Docs. *Troubleshoot Docker Engine*, *docker container run reference*. docs.docker.com
- Python Docs. *http.server — HTTP servers (--bind)*. docs.python.org/3/library/http.server.html
- Zeller, A. (2009). *Why Programs Fail* (2nd ed.). Morgan Kaufmann.
- Agans, D. J. (2002). *Debugging: The 9 Indispensable Rules*. AMACOM.
