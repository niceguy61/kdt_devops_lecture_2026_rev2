# 2교시 · 첫 Pod

> [!NOTE]
> **이번 시간에 할 일**
>
> - 매니페스트 한 장으로 catalog-api **Pod**를 만들고, 상태가 바뀌는 과정을 지켜봅니다.
> - Pod의 IP · 노드 · Events · 로그를 읽습니다.
> - `port-forward`로 내 노트북에서 Pod에 접속하고, `exec`로 Pod 안을 봅니다.
> - Pod를 지우면 **아무도 되살려 주지 않는다**는 것을 확인합니다.

## 매니페스트 읽기

```bash
cat pod.yaml
```

```yaml
apiVersion: v1
kind: Pod
metadata:
  name: catalog-api
  labels:
    app: catalog-api
spec:
  containers:
    - name: catalog-api
      image: ghcr.io/niceguy61/devmart-catalog-api:sha-7f3c2e1
      ports:
        - containerPort: 8000
```

| 줄 | 뜻 | 2주차 Compose라면 |
|---|---|---|
| `apiVersion: v1` · `kind: Pod` | 가장 기본 묶음(core)의 Pod | — |
| `metadata.name` | Pod 이름. 네임스페이스 안에서 하나뿐 | `services:` 아래 이름 |
| `metadata.labels` | 꼬리표. 4 · 6교시에 Deployment와 Service가 이것으로 찾는다 | — |
| `containers:` | 목록 — Pod 안에 컨테이너가 여럿일 수 있다(3일차 3교시) | — |
| `image` | GHCR의 SHA 태그 이미지 | `image:` |
| `containerPort: 8000` | 컨테이너가 듣는 포트. **정보용 표시**일 뿐, 포트를 여는 것은 아니다 | `expose:` 에 가깝다 (`ports:` 아님) |

> **❓ 오해 — containerPort를 적어야 포트가 열린다**
>
> 아닙니다. 컨테이너 안의 gunicorn은 `containerPort`가 있든 없든 8000에서 듣습니다. 이 칸은 "이 컨테이너는 8000을 쓴다"는 **설명**이고, 다른 도구가 읽어 가는 정보입니다. 노트북에서 접속하려면 `port-forward`(이번 교시)나 Service(6교시)가 따로 필요합니다. 2주차 Dockerfile의 `EXPOSE`와 같은 성격입니다.

## 실습 2 · Pod 만들고 지켜보기

> **🧪 실습: 실습 목표**
>
> Pod를 만들고, 어제 배운 6단계가 상태 변화로 나타나는 것을 봅니다.

### 단계 1 — 만들기

터미널을 **두 개** 엽니다. 터미널 A에서 지켜보기를 먼저 겁니다.

```bash
# 터미널 A
kubectl get pods -w
```

```bash
# 터미널 B
cd ~/devops-lab/k8s/day4
kubectl apply -f pod.yaml
```

> **🟢 확인: 터미널 B**
>
> ```text
> pod/catalog-api created
> ```

> **🟢 확인: 터미널 A — 몇 초에 걸쳐 한 줄씩**
>
> ```text
> NAME          READY   STATUS              RESTARTS   AGE
> catalog-api   0/1     Pending             0          0s
> catalog-api   0/1     Pending             0          0s
> catalog-api   0/1     ContainerCreating   0          0s
> catalog-api   1/1     Running             0          9s
> ```
> | 보이는 상태 | 어제 6단계 중 |
> |---|---|
> | `Pending` (첫 줄) | 2 — etcd에 저장됨, 아직 노드 없음 |
> | `Pending` (둘째 줄) | 3 — 스케줄러가 노드를 정함 (상태 이름은 그대로) |
> | `ContainerCreating` | 4 · 5 — kubelet이 발견, 이미지 받는 중 |
> | `Running` · `1/1` | 6 — 컨테이너가 떴다고 보고 |
>
> 처음엔 이미지를 받느라 `ContainerCreating`이 10초 이상 걸릴 수 있습니다. 터미널 A는 Ctrl+C로 멈춥니다.

### 단계 2 — 어디에, 어떤 IP로

```bash
kubectl get pod catalog-api -o wide
```

> **🟢 확인: 보이는 것**
>
> ```text
> NAME          READY   STATUS    RESTARTS   AGE   IP           NODE              NOMINATED NODE   READINESS GATES
> catalog-api   1/1     Running   0          40s   10.244.2.3   devmart-worker2   <none>           <none>
> ```
> - **IP** `10.244.x.y` — kindnet이 준 Pod 전용 주소. 노드마다 대역이 다릅니다(worker는 `10.244.1.*`, worker2는 `10.244.2.*`).
> - **NODE** — 스케줄러가 고른 노드. 컨트롤 플레인이 아닌 것을 확인하세요(어제 7교시 단계 7의 테인트).

### 단계 3 — Events 읽기

```bash
kubectl describe pod catalog-api
```

긴 출력입니다. 위에서부터 **이름 · 노드 · 라벨 · IP**, 가운데 **컨테이너 정보**, 맨 아래 **Events**가 있습니다. 맨 아래부터 봅니다.

> **🟢 확인: Events (맨 아래)**
>
> ```text
> Events:
>   Type    Reason     Age   From               Message
>   ----    ------     ----  ----               -------
>   Normal  Scheduled  60s   default-scheduler  Successfully assigned default/catalog-api to devmart-worker2
>   Normal  Pulling    59s   kubelet            Pulling image "ghcr.io/niceguy61/devmart-catalog-api:sha-7f3c2e1"
>   Normal  Pulled     52s   kubelet            Successfully pulled image "ghcr.io/…" in 7.1s …
>   Normal  Created    52s   kubelet            Created container: catalog-api
>   Normal  Started    52s   kubelet            Started container catalog-api
> ```
> **From** 칸을 보세요. `Scheduled`는 **스케줄러**가, 나머지는 worker2의 **kubelet**이 남겼습니다. 어제 2 · 3교시에 "결정은 본부, 실행은 현장"이라고 한 것이 기록으로 남아 있습니다.

> [!TIP]
> **Events는 금방 사라진다**
>
> Events는 기본 **1시간** 뒤 지워집니다. 장애가 지나간 뒤에 보면 이미 없을 수 있습니다. 그래서 운영 환경에서는 Events도 로그처럼 따로 모아 둡니다(4주차 2일차).

### 단계 4 — 로그

```bash
kubectl logs catalog-api
```

> **🟢 확인: 보이는 것**
>
> ```text
> [2026-11-26 01:12:40 +0000] [1] [INFO] Starting gunicorn 27.0.1
> [2026-11-26 01:12:40 +0000] [1] [INFO] Listening at: http://0.0.0.0:8000 (1)
> [2026-11-26 01:12:40 +0000] [1] [INFO] Using worker: sync
> [2026-11-26 01:12:40 +0000] [7] [INFO] Booting worker with pid: 7
> ```
> 2주차에 `docker logs`로 보던 것과 같습니다. 컨테이너의 표준 출력을 kubelet이 모아 두었다가 보여 줍니다.

## 실습 3 · Pod에 접속하기

### 단계 1 — port-forward

Pod의 IP `10.244.2.3`은 클러스터 **안**의 주소라, 노트북에서 바로 `curl`할 수 없습니다. `port-forward`로 임시 통로를 뚫습니다.

```bash
# 터미널 A
kubectl port-forward pod/catalog-api 8000:8000
```

- `8000:8000` : 내 노트북의 8000 → Pod의 8000

> **🟢 확인: 터미널 A — 이 상태로 기다린다**
>
> ```text
> Forwarding from 127.0.0.1:8000 -> 8000
> Forwarding from [::1]:8000 -> 8000
> ```

```bash
# 터미널 B
curl -s localhost:8000/api/info; echo
curl -s localhost:8000/api/products; echo
```

> **🟢 확인: 보이는 것**
>
> ```text
> {"env":"local","hostname":"catalog-api","service":"catalog-api","version":"2.0.0"}
> {"detail":"KeyError","error":"database unavailable"}
> ```
> - `hostname` 이 **Pod 이름**과 같습니다. Kubernetes는 컨테이너의 호스트 이름을 Pod 이름으로 줍니다(6교시에 이 값으로 부하 분산을 눈으로 봅니다).
> - `/api/products`는 **503**입니다. DB가 없기 때문입니다. `KeyError`는 `DB_HOST` 환경 변수가 없어서 난 오류입니다. Pod는 `Running`인데 기능은 실패하는 경우 — 3교시 장애 지도의 마지막 줄입니다. DB는 내일 올립니다.

터미널 A는 Ctrl+C로 통로를 닫습니다.

> [!WARNING]
> **port-forward는 디버깅용**
>
> `port-forward`는 **kubectl이 켜져 있는 동안만** 열리는 개인용 통로입니다. 터미널을 닫으면 끊기고, 다른 사람은 쓸 수 없고, Pod 하나에만 붙습니다. 서비스로 여는 방법은 6교시의 Service입니다.

### 단계 2 — Pod 안에서 명령

```bash
kubectl exec catalog-api -- env | grep -E '^(HOSTNAME|APP_|KUBERNETES_SERVICE)'
kubectl exec catalog-api -- python -c "import socket; print(socket.gethostname())"
```

- `--` 뒤가 컨테이너 안에서 실행할 명령 (2주차 `docker exec`와 같다)

> **🟢 확인: 보이는 것**
>
> ```text
> HOSTNAME=catalog-api
> APP_VERSION=2.0.0
> KUBERNETES_SERVICE_HOST=10.96.0.1
> KUBERNETES_SERVICE_PORT=443
> catalog-api
> ```
> `APP_VERSION`은 Dockerfile의 `ENV`에서 왔습니다. `KUBERNETES_SERVICE_*`는 내가 넣지 않았는데 있습니다 — Kubernetes가 모든 Pod에 **apiserver의 클러스터 안 주소**를 넣어 줍니다. 6교시 Service에서 이 주소의 정체를 봅니다.

## 실습 4 · Pod를 지우면

```bash
kubectl delete pod catalog-api
kubectl get pods
```

> **🟢 확인: 보이는 것**
>
> ```text
> pod "catalog-api" deleted
> No resources found in default namespace.
> ```
> **사라지고 끝입니다.** 어제 실험 1에서 coredns Pod는 지우자마자 새로 생겼는데, 이번엔 아무도 다시 만들지 않습니다. 차이는? coredns Pod 뒤에는 "2개여야 한다"고 지키는 **Deployment**가 있었고, 지금 만든 Pod 뒤에는 아무도 없습니다.

> [!IMPORTANT]
> **Pod를 직접 만드는 일은 거의 없다**
>
> 직접 만든 Pod는 **reconcile 반복 밖**에 있습니다. 노드가 꺼져도, 실수로 지워도 그만입니다. 그래서 실무에서는 Pod를 직접 만들지 않고 Deployment(4교시) 같은 **컨트롤러에게 Pod를 맡깁니다.** 오늘 Pod를 직접 만든 것은 가장 작은 단위를 손으로 만져 보기 위해서입니다. 3교시의 망가진 Pod 실험까지만 직접 만듭니다.

> **🎓 학술 노트 — 왜 Pod는 IP를 하나씩 받는가**
>
> Docker는 처음에 컨테이너들이 **호스트의 IP를 나눠 쓰고 포트로 구분**하는 방식이었습니다(2주차 `-p 8080:80`). 그러면 같은 포트를 쓰는 앱 두 개가 한 서버에 못 올라가고, 포트 번호를 서로 조율해야 합니다. Borg에서 이 문제를 겪은 Kubernetes 설계자들은 **Pod마다 고유 IP**를 주기로 했습니다. 모든 Pod가 NAT 없이 서로의 IP로 바로 통신할 수 있어야 한다는 것이 Kubernetes 네트워크 모델의 기본 규칙입니다. 3일차 1교시의 Burns 외(2016)가 Borg의 교훈 중 하나로 이것을 꼽습니다.

> **📈 트렌드 2026 — 디버깅용 임시 컨테이너**
>
> 운영용 이미지는 보안을 위해 셸이나 `curl` 없이 최소한으로 만드는 경우가 늘었습니다(distroless 등). 그러면 `kubectl exec … -- sh`가 안 됩니다. 이때 쓰는 것이 **`kubectl debug`** 입니다. 실행 중인 Pod 옆에 도구가 든 **임시 컨테이너**(ephemeral container)를 붙여 같은 네트워크 · 프로세스를 들여다봅니다. 예: `kubectl debug -it catalog-api --image=busybox:1.37 --target=catalog-api`.

> **✅ 확인 문제**
>
> 1. `kubectl get pods -w`에서 `Pending`이 두 번 나오는 이유는?
> 2. `describe`의 Events에서 `Scheduled`를 남긴 것은 누구이고, `Pulled`를 남긴 것은 누구인가요?
> 3. Pod가 `Running`인데 `/api/products`가 503입니다. 무엇을 봐야 하나요?
> 4. 직접 만든 Pod를 지웠을 때 되살아나지 않는 이유는?
>
> <details><summary>정답</summary>
>
> 1. 첫 줄은 저장 직후(노드 없음), 둘째 줄은 스케줄러가 노드를 정한 직후. 상태 이름은 같지만 단계가 다르다
> 2. Scheduled — default-scheduler(컨트롤 플레인), Pulled — kubelet(노드)
> 3. 앱의 로그와 응답 내용 (`kubectl logs`, 응답의 `detail`) — 클러스터는 할 일을 다 했고, 문제는 앱 안이다
> 4. 그 Pod를 '몇 개여야 한다'고 지키는 컨트롤러가 없기 때문
>
> </details>

## 참고 문헌

- Kubernetes Docs. *Pods* · *Pod Lifecycle*. kubernetes.io/docs/concepts/workloads/pods
- Kubernetes Docs. *Use Port Forwarding to Access Applications in a Cluster*. kubernetes.io/docs/tasks
- Kubernetes Docs. *Debug Running Pods — Ephemeral containers*. kubernetes.io/docs/tasks/debug
- Kubernetes Docs. *Cluster Networking — The Kubernetes network model*. kubernetes.io/docs/concepts/cluster-administration/networking
