<sub>[🏠 과정 목차](../../README.md) › [3주차](../README.md) › [4일차](README.md) › 8/8교시</sub>

# 8교시 · Pod 디버깅 종합 — 안 닿을 때 · `kubectl debug`

> [!NOTE]
> **이번 시간에 할 일**
>
> - "Service로 안 붙어요"를 **엔드포인트 → 포트 → 이름(DNS)** 순서로 좁힙니다.
> - 6교시의 셀렉터 오타와 다른 두 장애 — **targetPort 오류**, **다른 네임스페이스의 이름** — 를 만들고 구분합니다.
> - 셸도 `curl`도 없는 Pod 옆에 **임시 디버그 컨테이너**를 붙여 안을 봅니다(`kubectl debug`).
> - 노드 안까지 들어가 컨테이너 로그 파일을 직접 봅니다.
> - 오늘 하루의 진단 순서를 **한 장의 표**로 정리합니다.

> [!IMPORTANT]
> **3교시는 'Pod가 안 뜰 때', 오늘은 'Pod는 떴는데 안 닿을 때'**
>
> 3교시의 세 장애(ImagePullBackOff · CrashLoopBackOff · Pending)는 `kubectl get pods`만 봐도 빨갛게 보였습니다. 운영에서 더 까다로운 것은 **모든 Pod가 `Running`인데 요청이 실패하는** 경우입니다. 이때는 Pod가 아니라 **Pod 사이의 길**을 봐야 합니다.

## 실습 17 · 준비 — 진단용 Pod 하나 띄워 두기

매번 `kubectl run tmp --rm …`을 치는 대신, 진단 도구가 든 Pod를 하나 띄워 두고 계속 씁니다.

```bash
cd ~/devops-lab/k8s/day4
kubectl get deploy,svc catalog-api
kubectl run toolbox --image=nicolaka/netshoot:v0.17 -- sleep infinity
kubectl wait --for=condition=Ready pod/toolbox --timeout=90s
kubectl exec toolbox -- curl -s -m 3 http://catalog-api/api/info; echo
```

- `nicolaka/netshoot` : `curl` · `dig` · `ss` · `tcpdump` 등 네트워크 진단 도구를 모은 이미지 (1주차 3일차 8교시의 트렌드)
- `sleep infinity` : 아무 일도 안 하고 **계속 살아 있기만** — 들어가서 도구를 쓰려고

> **🟢 확인: 이렇게 나오면 성공**
>
> ```text
> deployment.apps/catalog-api   3/3     3            3           …
> service/catalog-api           ClusterIP   10.96.142.87   <none>   80/TCP   …
> {"database":"not configured (sample data)","env":"kind",…}
> ```

## 실습 18 · 장애 A — 엔드포인트는 있는데 거절

Service의 `targetPort`를 틀리게 바꿉니다(앱은 8000에서 듣는데 8080으로).

```bash
kubectl patch service catalog-api --type=json \
  -p '[{"op":"replace","path":"/spec/ports/0/targetPort","value":8080}]'
kubectl exec toolbox -- curl -s -m 3 http://catalog-api/api/info; echo "종료 코드: $?"
```

> **🟢 확인: 실패합니다**
>
> ```text
> 종료 코드: 7
> ```
> `curl`의 7은 **연결 실패(refused)**입니다.

이제 순서대로 좁힙니다.

```bash
kubectl get endpointslices -l kubernetes.io/service-name=catalog-api
```

> **🟢 확인: 엔드포인트는 있다**
>
> ```text
> NAME                ADDRESSTYPE   PORTS   ENDPOINTS                          AGE
> catalog-api-x7k2p   IPv4          8080    10.244.1.5,10.244.2.3,10.244.2.4   …
> ```
> 6교시의 셀렉터 오타와 **다릅니다.** 받는 Pod는 세 개나 있습니다. 그런데 `PORTS`가 **8080**입니다.

```bash
POD_IP=$(kubectl get pod -l app=catalog-api -o jsonpath='{.items[0].status.podIP}')
kubectl exec toolbox -- curl -s -m 3 -o /dev/null -w '%{http_code}\n' http://$POD_IP:8000/health
kubectl exec toolbox -- curl -s -m 3 -o /dev/null -w '%{http_code}\n' http://$POD_IP:8080/health
```

> **🟢 확인: Pod에 직접 물어보면**
>
> ```text
> 200
> 000
> ```
> Pod는 **8000**에서 멀쩡히 답하고, 8080에는 아무도 없습니다. Service가 엉뚱한 문을 두드리고 있었습니다.

```bash
kubectl apply -f service.yaml
kubectl exec toolbox -- curl -s -m 3 -o /dev/null -w '%{http_code}\n' http://catalog-api/health
```

| | 6교시 셀렉터 오타 | 오늘 targetPort 오류 |
|---|---|---|
| DNS | 답함 | 답함 |
| EndpointSlice | **비었다** | **있다**, 포트가 이상 |
| Pod IP:앱 포트로 직접 | 됨 | 됨 |
| 고칠 곳 | `selector` 또는 Pod 라벨 | `targetPort` 또는 `containerPort` |

## 실습 19 · 장애 B — 다른 네임스페이스에서는 이름이 안 보인다

```bash
kubectl create namespace other-team
kubectl run probe -n other-team --image=nicolaka/netshoot:v0.17 -- sleep infinity
kubectl wait -n other-team --for=condition=Ready pod/probe --timeout=90s
kubectl exec -n other-team probe -- curl -s -m 3 http://catalog-api/health; echo "종료 코드: $?"
kubectl exec -n other-team probe -- dig +short catalog-api.default.svc.cluster.local
kubectl exec -n other-team probe -- curl -s -m 3 http://catalog-api.default/health; echo
```

> **🟢 확인: 이렇게 나옵니다**
>
> ```text
> 종료 코드: 6
> 10.96.142.87
> {"status":"ok"}
> ```
> - `curl`의 6은 **이름을 찾지 못함**입니다(1주차 3일차 8교시의 `Could not resolve host`).
> - 짧은 이름 `catalog-api`는 **같은 네임스페이스** 안에서만 찾아집니다. 다른 네임스페이스에서는 `catalog-api.default`(또는 전체 이름 `catalog-api.default.svc.cluster.local`)로 부릅니다.

> [!TIP]
> **짧은 이름이 동작하는 이유**
>
> ```bash
> kubectl exec -n other-team probe -- cat /etc/resolv.conf
> ```
> `search other-team.svc.cluster.local svc.cluster.local cluster.local`이 보입니다. 짧은 이름을 받으면 **자기 네임스페이스부터** 붙여 찾아보는 규칙입니다. 그래서 내일 DevMart를 `devmart` 네임스페이스에 모아 두면, 서비스끼리는 짧은 이름으로 부를 수 있습니다.

```bash
kubectl delete namespace other-team
```

## 실습 20 · `kubectl debug` — 셸이 없는 Pod 옆에 붙기

`catalog-api` 컨테이너에는 `curl`도 `ps`도 없습니다(2교시의 "운영용 이미지는 최소한으로").

```bash
POD=$(kubectl get pod -l app=catalog-api -o jsonpath='{.items[0].metadata.name}')
kubectl exec $POD -- ps
```

> **🟢 확인: 도구가 없다**
>
> ```text
> exec: "ps": executable file not found in $PATH
> ```

임시 디버그 컨테이너를 **같은 Pod 안에** 붙입니다.

```bash
kubectl debug -it $POD --image=nicolaka/netshoot:v0.17 --target=catalog-api -- bash
```

들어간 셸에서:

```bash
ps aux | head -5
ss -tlnp
curl -s localhost:8000/health
exit
```

> **🟢 확인: 보이는 것**
>
> ```text
> PID   USER     COMMAND
>     1 appuser  /usr/local/bin/python3.14 /usr/local/bin/gunicorn --bind 0.0.0.0:8000 …
>     7 appuser  /usr/local/bin/python3.14 /usr/local/bin/gunicorn …
> State   Local Address:Port
> LISTEN  0.0.0.0:8000
> {"status":"ok"}
> ```
> - `--target=catalog-api` : 앱 컨테이너와 **프로세스 목록을 공유**한다. 그래서 gunicorn이 보인다
> - 같은 Pod라서 **네트워크도 공유** — `localhost:8000`이 앱이다
> - 앱 이미지를 바꾸지도, 다시 시작하지도 않았다. 임시 컨테이너는 Pod가 다시 만들어질 때 사라진다

```bash
kubectl get pod $POD -o jsonpath='{.spec.ephemeralContainers[*].name}'; echo
```

`debugger-xxxxx`처럼 붙였던 임시 컨테이너 이름이 기록에 남습니다. **누가 운영 Pod에 무엇을 붙였는지**가 감사 기록이 되는 이유입니다(4주차 5일차에 이 권한을 RBAC으로 좁힙니다).

### 노드 안까지 — `kubectl debug node/`

```bash
NODE=$(kubectl get pod $POD -o jsonpath='{.spec.nodeName}')
kubectl debug node/$NODE -it --image=busybox:1.37 -- sh
```

`$POD`가 놓인 노드로 들어갑니다.

들어간 셸에서:

```bash
ls /host/var/log/pods | head -5
tail -2 /host/var/log/pods/default_catalog-api-*/catalog-api/0.log 2>/dev/null | head -2
exit
```

- 노드의 파일 시스템이 `/host`에 붙습니다. `kubectl logs`가 결국 읽는 것이 **이 파일**입니다
- 남은 디버그 Pod 정리: `kubectl get pods | grep node-debugger` → `kubectl delete pod <그 이름>`

> [!WARNING]
> **노드 디버깅은 노드의 root와 같다**
>
> `/host`로 노드 전체를 읽고 쓸 수 있습니다. 실습 클러스터에서만 하고, 운영에서는 이 권한을 가진 사람을 아주 적게 둡니다.

## 오늘의 진단 순서 — 한 장

| 증상 | 1 | 2 | 3 | 본 곳 |
|---|---|---|---|---|
| Pod가 `Running`이 아님 | `get pods` 상태 이름 | `describe` Events | `logs --previous` | 3교시 |
| `Running`인데 Service로 안 닿음 | `get endpointslices` — 비었나? | 포트가 맞나? Pod IP로 직접 | 이름 — 같은 네임스페이스인가? | 6교시 · 오늘 |
| 안에서 무슨 일인지 모름 | `kubectl debug --target` | `ss` · `ps` · `curl localhost` | 노드 로그 파일 | 오늘 |
| 무엇이 언제 일어났나 | `kubectl events --for pod/이름` | `get events -A --sort-by=.lastTimestamp` | — | 오늘 |

> **🧹 정리: 정리**
>
> ```bash
> kubectl delete pod toolbox
> kubectl get pods
> ```
> `catalog-api` Deployment와 Service는 7교시처럼 **내일 아침까지 남겨 둡니다.**

> **🎓 학술 노트 — 디버깅의 아홉 규칙 (Agans, 2002)**
>
> 엔지니어 **데이비드 에이건스(David Agans)**는 『Debugging: The 9 Indispensable Rules』(2002)에서 수십 년의 하드웨어 · 소프트웨어 장애 사례를 아홉 규칙으로 정리했습니다. 그중 오늘 쓴 것이 셋입니다. **"보지 말고 보라(Quit thinking and look)"** — 추측하지 말고 `endpointslices`와 Pod IP로 **직접 확인**했습니다. **"나눠서 정복하라(Divide and conquer)"** — DNS → 엔드포인트 → 포트로 길을 반씩 잘라 문제 구간을 찾았습니다. **"한 번에 하나만 바꿔라"** — 각 장애에서 하나만 고장 내고, 하나만 고쳐 확인했습니다. 2주차 2일차의 "디버깅은 가설 검증"과 같은 뿌리입니다.
>
> - Agans, D. J. (2002). *Debugging: The 9 Indispensable Rules for Finding Even the Most Elusive Software and Hardware Problems*. AMACOM.

> **📈 트렌드 — 디버깅도 '임시로 붙였다 떼는' 방식으로**
>
> 예전에는 진단 도구를 넣으려고 **이미지를 다시 만들거나** 운영 Pod에 SSH로 들어갔습니다. 임시 컨테이너(ephemeral container)가 Kubernetes 1.25에서 정식 기능이 된 뒤로는 오늘처럼 **이미지는 최소로 두고, 필요할 때만 붙였다 뗍니다.** `kubectl debug`에는 `--profile=netadmin`처럼 필요한 권한만 주는 프로필도 생겼습니다. 증상과 Events를 모아 원인 후보를 제안하는 AI 도구(k8sgpt 등 CNCF 프로젝트)도 나왔지만, 제안을 **확인하는 순서**는 오늘의 표 그대로입니다.

## 정리

- `Running`인데 안 닿으면: **EndpointSlice → 포트(Pod IP로 직접) → 이름(네임스페이스)** 순서.
- 엔드포인트가 **비었으면** 셀렉터 · 라벨, **있는데 거절**이면 `targetPort`.
- 다른 네임스페이스는 `이름.네임스페이스`로 부릅니다. `/etc/resolv.conf`의 `search`가 짧은 이름의 비밀입니다.
- 셸 없는 Pod에는 `kubectl debug --target`으로 **임시 컨테이너**를 붙입니다. 노드는 `kubectl debug node/`.

> **✅ 확인 문제**
>
> 1. Service로 요청하면 거절되는데, EndpointSlice에 IP 세 개가 있습니다. 다음에 무엇을 확인하나요?
> 2. `default`의 `catalog-api`를 `shop` 네임스페이스의 Pod에서 부르려면 이름을 어떻게 쓰나요?
> 3. `curl` 종료 코드 6과 7의 차이는?
> 4. `kubectl debug`에 `--target=앱컨테이너`를 주면 무엇이 달라지나요?
> 5. 운영 Pod에 디버그 컨테이너를 붙이는 권한을 좁게 줘야 하는 이유는?
>
> <details><summary>정답</summary>
>
> 1. EndpointSlice의 포트가 앱이 실제로 듣는 포트와 같은지 — Pod IP:앱 포트로 직접 불러 비교합니다.
> 2. `catalog-api.default` (또는 `catalog-api.default.svc.cluster.local`)
> 3. 6은 이름을 찾지 못함(DNS), 7은 연결 실패(받는 쪽 없음)
> 4. 앱 컨테이너와 프로세스 목록을 공유해 `ps`로 앱 프로세스를 볼 수 있습니다.
> 5. 붙인 컨테이너는 앱과 네트워크 · 프로세스를 공유해 비밀값이나 트래픽에 접근할 수 있기 때문입니다.
>
> </details>

> [!NOTE]
> **오늘의 배움일기 — 수업 뒤 각자**
>
> - kubectl 루프 다섯 동사 중 오늘 가장 많이 쓴 것과, 가장 도움이 된 것
> - 장애 셋(Pending · ImagePullBackOff · CrashLoopBackOff) 중 하나를 골라, 처음 보는 동료에게 진단 순서를 설명하듯이
> - 자가 치유 실험 넷 중 가장 의외였던 것 — 왜?
> - Pod · ReplicaSet · Deployment · Service의 관계를 **라벨**이라는 말을 넣어 한 문단으로
> - 롤링 업데이트 중 FAIL이 몇 번 났는지, 그게 실제 쇼핑몰이었다면 어떤 일이 생겼을지
> - 내일 전에 궁금한 것: catalog-api가 DB 비밀번호를 받으려면? DB 데이터는 Pod가 바뀌면 어떻게 될까?

## 참고 문헌

- Agans, D. J. (2002). *Debugging: The 9 Indispensable Rules*. AMACOM.
- Kubernetes Documentation. *Debug Services*; *Debug Running Pods — Ephemeral containers, Debugging a node*; *DNS for Services and Pods*.
- Kubernetes Documentation. *kubectl debug — --target, --profile*; *kubectl events*.
- curl. *Exit codes*. everything.curl.dev/cmdline/exitcode
- nicolaka/netshoot. *A Docker + Kubernetes network trouble-shooting swiss-army container*. github.com/nicolaka/netshoot

---

| 이전 | 목차 | 다음 |
|:--|:--:|--:|
| ⬅️ [7교시 · 롤링 업데이트와 되돌리기](lesson-07.md) | [⬆️ 4일차 목차](README.md) | [3주차 5일차 목차](../day5/README.md) ➡️ |
