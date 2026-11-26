<sub>[🏠 과정 목차](../../README.md) › [2주차](../README.md) › [2일차](README.md) › 8/8교시</sub>

# 8교시 · 자원 제한과 안전한 실행 옵션

> [!NOTE]
> **이번 시간에 할 일**
>
> - 컨테이너 하나가 **메모리 · CPU를 얼마까지** 쓸지 정하고, 한도를 넘으면 무슨 일이 생기는지 직접 봅니다.
> - 종료 코드 **137**과 `OOMKilled`를 `inspect`로 확인합니다(1주차 2일차 8교시의 그것).
> - 컨테이너를 **root가 아닌 사용자로**, **읽기 전용 파일 시스템**으로, **권한(capability)을 덜어 내고** 실행합니다.
> - 다섯 옵션을 합쳐 "안전하게 실행한 nginx"를 띄웁니다.

> [!IMPORTANT]
> **기본값은 '무제한 · root'다**
>
> `docker run`은 아무 옵션이 없으면 컨테이너에게 **호스트의 메모리와 CPU를 한도 없이** 쓰게 하고, 안에서는 **root**로 실행합니다. 노트북에서 연습할 때는 편하지만, 서버에서는 컨테이너 하나의 버그가 **옆의 모든 컨테이너를 함께 멈추게** 하고(시끄러운 이웃), 컨테이너가 뚫렸을 때 피해가 커집니다. 오늘은 그 기본값을 하나씩 바꿉니다.

## 실습 17 · 메모리 한도 — 넘으면 죽는다

> **🧪 실습: 실습 목표**
>
> 메모리 64MiB 한도를 건 컨테이너에서 일부러 메모리를 계속 쓰게 하고, 커널이 그 컨테이너만 정확히 죽이는 것을 확인합니다.

### 단계 1 — 메모리를 끝없이 먹는 명령

```bash
docker run --name oom -m 64m --memory-swap 64m alpine:3.24 sh -c 'head -c 500m /dev/zero | tail'
echo "종료 코드: $?"
```

- `-m 64m` : 메모리 한도 64MiB
- `--memory-swap 64m` : 스왑까지 합친 한도도 64MiB → 스왑으로 버티지 못하게
- `head -c 500m /dev/zero | tail` : 0 바이트 500MB를 `tail`에 흘려보냅니다. 줄바꿈이 하나도 없어서 `tail`은 "마지막 줄"을 찾느라 받은 것을 **전부 메모리에 쌓습니다.** 메모리 누수를 흉내 내는 한 줄입니다.

> **🟢 확인: 이렇게 나오면 성공**
>
> 몇 초 뒤 아무 메시지 없이 끝나고:
> ```text
> 종료 코드: 137
> ```

### 단계 2 — 왜 죽었는지 확인

```bash
docker inspect oom --format 'OOMKilled={{.State.OOMKilled}} ExitCode={{.State.ExitCode}}'
docker rm oom
```

> **🟢 확인: 이렇게 나오면 성공**
>
> ```text
> OOMKilled=true ExitCode=137
> ```
> 137 = 128 + 9(SIGKILL). 커널의 **OOM Killer**가 이 컨테이너만 골라 죽였습니다. 1주차 2일차 8교시의 표 두 번째 줄을 지금 직접 만든 것입니다. 3주차 5일차에는 Kubernetes에서 같은 일이 `OOMKilled`라는 Pod 상태로 보입니다.

> [!TIP]
> **로그에 아무것도 없는데 137이라면**
>
> OOM으로 죽은 프로그램은 **마지막 말을 남길 틈이 없습니다**(SIGKILL은 막을 수 없음). 그래서 `docker logs`는 조용합니다. 이럴 때 `inspect`의 `OOMKilled`를 먼저 봅니다.

## 실습 18 · CPU 한도 — 넘으면 느려진다

메모리는 한도를 넘으면 **죽지만**, CPU는 한도를 넘으면 **기다립니다.** 둘의 차이를 봅니다.

```bash
docker run -d --name busy --cpus 0.5 alpine:3.24 sh -c 'while :; do :; done'
docker stats --no-stream busy
```

> **🟢 확인: 이렇게 나오면 성공**
>
> ```text
> NAME   CPU %    MEM USAGE / LIMIT     …
> busy   50.12%   520KiB / 7.6GiB
> ```
> 무한 반복으로 CPU를 최대로 쓰려 해도 **50% 근처**에서 멈춥니다. `--cpus 0.5` = 코어 반 개. 넘는 만큼은 다음 차례까지 **기다리게(throttling)** 됩니다. 메모리 한도는 정하지 않았으므로 LIMIT은 호스트 전체입니다.

```bash
docker rm -f busy
```

| | 메모리 한도 | CPU 한도 |
|---|---|---|
| 옵션 | `-m 256m` | `--cpus 0.5` |
| 넘으면 | **강제 종료** (137, OOMKilled) | **느려짐** (기다림) |
| 3주차 Kubernetes | `limits.memory` | `limits.cpu` |
| 정하는 법 | 평소 사용량(`docker stats`)보다 넉넉히 | 기다려도 되는 일이면 작게 |

## 실습 19 · root가 아니게, 읽기 전용으로, 권한을 덜고

### 단계 1 — 안에서 나는 누구인가

```bash
docker run --rm alpine:3.24 id
docker run --rm --user 1000:1000 alpine:3.24 id
docker run --rm --user 1000:1000 alpine:3.24 touch /etc/hacked
```

> **🟢 확인: 이렇게 나오면 성공**
>
> ```text
> uid=0(root) gid=0(root) groups=0(root),…
> uid=1000 gid=1000 groups=1000
> touch: /etc/hacked: Permission denied
> ```
> 기본은 **root**입니다. `--user`를 주면 일반 사용자로 바뀌고, 시스템 파일을 고칠 수 없습니다. 1주차 2일차 4교시의 **최소 권한**을 컨테이너에 적용한 것입니다. 내일 Dockerfile에서는 `USER` 한 줄로 이미지에 아예 적어 둡니다.

### 단계 2 — 파일 시스템을 읽기 전용으로

```bash
docker run --rm --read-only alpine:3.24 touch /tmp/x
docker run --rm --read-only --tmpfs /tmp alpine:3.24 sh -c 'touch /tmp/x && echo "tmp에는 쓸 수 있다"'
```

> **🟢 확인: 이렇게 나오면 성공**
>
> ```text
> touch: /tmp/x: Read-only file system
> tmp에는 쓸 수 있다
> ```
> - `--read-only` : 이미지에서 온 파일을 **아무것도 바꿀 수 없게** 한다. 공격자가 들어와도 도구를 내려받아 깔거나 설정을 바꿀 수 없다
> - `--tmpfs /tmp` : 꼭 써야 하는 곳만 **메모리 위의 임시 폴더**로 열어 준다(컨테이너가 끝나면 사라짐)

### 단계 3 — root의 '특권'을 덜어 내기

Linux는 root의 힘을 **capability**라는 작은 조각 40여 개로 나눕니다(파일 주인 바꾸기, 시간 바꾸기, 네트워크 설정 등). Docker는 그중 일부만 컨테이너에 줍니다. 이것도 더 덜어 낼 수 있습니다.

```bash
docker run --rm alpine:3.24 chown nobody /tmp && echo "chown 됨"
docker run --rm --cap-drop ALL alpine:3.24 chown nobody /tmp
```

> **🟢 확인: 이렇게 나오면 성공**
>
> ```text
> chown 됨
> chown: /tmp: Operation not permitted
> ```
> 같은 root인데 `--cap-drop ALL` 쪽은 파일 주인을 바꾸는 조각(`CAP_CHOWN`)이 없어서 실패했습니다. **root라는 이름보다 실제로 가진 조각이 중요합니다.**

## 실습 20 · 다섯 옵션을 합친 nginx

```bash
docker run -d --name safe-web -p 8082:80 \
  -m 128m --cpus 0.5 \
  --read-only --tmpfs /var/cache/nginx --tmpfs /run \
  --cap-drop ALL --cap-add CHOWN --cap-add SETUID --cap-add SETGID --cap-add NET_BIND_SERVICE \
  --security-opt no-new-privileges \
  nginx:1.30-alpine
curl -sI http://localhost:8082 | head -1
docker stats --no-stream safe-web
```

| 옵션 | 이유 |
|---|---|
| `-m 128m --cpus 0.5` | 이웃을 괴롭히지 못하게 |
| `--read-only` + `--tmpfs` 두 곳 | nginx가 꼭 쓰는 캐시 · PID 파일 자리만 열어 줌 |
| `--cap-drop ALL` + 네 개만 `--cap-add` | nginx가 시작할 때 필요한 것만: 80번 포트 열기, 일꾼 프로세스를 일반 사용자로 바꾸기 |
| `--security-opt no-new-privileges` | 안에서 실행한 프로그램이 **권한을 더 얻지 못하게** |

> **🟢 확인: 이렇게 나오면 성공**
>
> ```text
> HTTP/1.1 200 OK
> NAME       CPU %   MEM USAGE / LIMIT    …
> safe-web   0.00%   3.1MiB / 128MiB
> ```
> LIMIT 칸이 이제 **128MiB**입니다.

> **🛠️ 막혔다면: 막혔다면**
>
> | 증상 | 원인 | 해결 |
> |---|---|---|
> | 컨테이너가 바로 종료, 로그에 `Read-only file system` + 경로 | nginx가 쓰려는 곳이 하나 더 있음 | 로그의 그 경로를 `--tmpfs`로 추가 |
> | 로그에 `Operation not permitted` | 필요한 capability까지 뺐음 | 위 네 개가 모두 있는지 확인 |
> | `port is already allocated` | 8082를 이미 쓰는 컨테이너 | `docker ps`로 찾아 지우거나 다른 포트 |

> **🧹 정리: 정리**
>
> ```bash
> docker rm -f safe-web
> docker ps -a
> ```

> **📘 현업에서는 어디에 적나**
>
> 오늘처럼 옵션을 매번 손으로 붙이지 않습니다. 5일차 **Compose 파일**에 `mem_limit`, `read_only`, `cap_drop`으로 적고, 3주차 **Kubernetes**에서는 `resources.limits`와 `securityContext`(`runAsNonRoot`, `readOnlyRootFilesystem`, `capabilities.drop`)로 적습니다. 4주차 5일차에는 이 칸이 비어 있는 배포를 **정책으로 막습니다.**

> **🎓 학술 노트 — cgroups의 시작 (Menage, 2007)**
>
> 1주차 2일차 7교시에서 "쓰는 양을 제한한다"고만 배운 **cgroups**는 구글의 엔지니어 **폴 메나지(Paul Menage)**와 동료들이 만들어 2007년 리눅스 심포지엄(OLS)에서 「Adding Generic Process Containers to the Linux Kernel」로 발표하고, 그해 리눅스 커널 2.6.24에 들어갔습니다. 구글은 한 서버에서 검색 · 메일 · 일괄 작업을 함께 돌리면서, **한 작업이 다른 작업의 자원을 빼앗지 못하게** 묶어 둘 장치가 필요했습니다(1주차 2일차의 Borg). 오늘 `-m`과 `--cpus` 한 줄이 그 장치를 쓰는 가장 쉬운 방법입니다.
>
> - Menage, P. B. (2007). Adding generic process containers to the Linux kernel. *Proceedings of the Linux Symposium*, Vol. 2, 45–57.

> **📈 트렌드 — 컨테이너 안의 root를 밖에서는 아무것도 아니게**
>
> 오늘의 `--user`는 컨테이너 **안**에서 root를 쓰지 않는 방법이었습니다. 한 걸음 더 나아가, 안에서는 root처럼 보여도 **호스트에서는 권한 없는 일반 사용자**로 바꿔 주는 **사용자 네임스페이스(user namespace)**가 보급되고 있습니다. Docker의 rootless 모드, Podman이 이 방식을 쓰고, Kubernetes도 1.33(2025)부터 Pod의 사용자 네임스페이스 지원을 기본으로 켜, 컨테이너 탈출 취약점의 피해를 크게 줄이고 있습니다.

## 정리

- 기본값은 **무제한 · root**입니다. 서버에서는 바꿉니다.
- 메모리 한도를 넘으면 **죽고**(137, `OOMKilled`), CPU 한도를 넘으면 **기다립니다**.
- `--user`(root 아님), `--read-only` + `--tmpfs`(필요한 곳만 쓰기), `--cap-drop ALL`(필요한 조각만 다시), `no-new-privileges`.
- 같은 내용을 Compose(5일차), Kubernetes `resources` · `securityContext`(3주차), 정책(4주차)으로 적어 갑니다.

> **✅ 확인 문제**
>
> 1. 컨테이너가 로그 없이 종료 코드 137로 끝났습니다. 무엇을 먼저 확인하나요?
> 2. `--cpus 0.5`인 컨테이너가 CPU를 더 쓰려 하면 어떻게 되나요?
> 3. `--read-only`로 실행한 앱이 `/tmp`에 임시 파일을 써야 합니다. 어떻게 하나요?
> 4. 컨테이너 안에서 `id`가 `uid=0(root)`입니다. 이 컨테이너는 무엇이든 할 수 있나요?
> 5. 이 옵션들을 3주차 Kubernetes에서는 어디에 적나요?
>
> <details><summary>정답</summary>
>
> 1. `docker inspect 이름 --format '{{.State.OOMKilled}}'` — 메모리 한도 초과로 죽었는지
> 2. 죽지 않고, 한도만큼만 쓰도록 기다리게 됩니다(느려짐).
> 3. `--tmpfs /tmp`로 그 폴더만 메모리 위의 임시 폴더로 열어 줍니다.
> 4. 아닙니다. 실제로 할 수 있는 일은 가진 capability와 사용자 네임스페이스 설정에 달려 있습니다.
> 5. `resources.limits`(메모리 · CPU)와 `securityContext`(사용자 · 읽기 전용 · capability)
>
> </details>

> [!NOTE]
> **오늘의 배움일기 — 수업 뒤 각자**
>
> - 오늘 본 에러 중 가장 당황스러웠던 것과, 이제 원인을 한 문장으로 설명해 보기
> - 이미지와 컨테이너의 차이를 1주차 2일차의 "프로그램과 프로세스"에 빗대어 설명해 보기
> - `docker top`에서 PID 1이 다른 번호로 보인 것을 보고 든 생각
> - 내일 Dockerfile 시간에 만들고 싶은 이미지 아이디어 하나

## 참고 문헌

- Menage, P. B. (2007). Adding generic process containers to the Linux kernel. *Proceedings of the Linux Symposium*.
- Docker Docs. *Resource constraints*; *docker container run — --read-only, --tmpfs, --cap-drop, --security-opt*; *Rootless mode*.
- man7.org. *capabilities(7)*; *user_namespaces(7)*.
- Kubernetes Blog (2025.4). *Kubernetes v1.33: User Namespaces enabled by default!*
- CIS. *CIS Docker Benchmark* — 5.x Container Runtime.

---

| 이전 | 목차 | 다음 |
|:--|:--:|--:|
| ⬅️ [7교시 · 실패 사례 다섯 가지](lesson-07.md) | [⬆️ 2일차 목차](README.md) | [2주차 3일차 목차](../day3/README.md) ➡️ |
