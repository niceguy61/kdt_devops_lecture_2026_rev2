<sub>[🏠 과정 목차](../../README.md) › [3주차](../README.md) › [3일차](README.md) › 7/8교시</sub>

# 7교시 · 첫 클러스터 — 둘러보고, 지우고, 끄기

> [!NOTE]
> **이번 시간에 할 일**
>
> - 설정 파일로 **노드 세 대짜리 kind 클러스터**를 만듭니다.
> - 오전에 배운 부품들을 클러스터 안에서 **직접 찾아봅니다** — apiserver · etcd · scheduler · controller-manager · kubelet · kube-proxy · CNI.
> - 시스템 Pod를 지우고, 노드를 끄고, 컨트롤 플레인을 멈춰 보며 **reconcile과 장애 증상**을 눈으로 확인합니다.
> - 1교시의 "Compose로 안 되는 일" 표를 완성합니다.

## 실습 10 · 클러스터 만들기

> **🧪 실습: 실습 목표**
>
> `devmart`라는 이름의 클러스터(컨트롤 플레인 1 + 워커 2)를 만들고, kubectl이 연결되는 것을 확인합니다.

### 단계 1 — 실습 파일 복사

```bash
cd ~/course && git pull
mkdir -p ~/devops-lab/k8s
cp ~/course/labs/week3/day3/* ~/devops-lab/k8s/
cd ~/devops-lab/k8s
ls
```

> **🟢 확인: 보이는 것**
>
> ```text
> README.md  cluster-tour.sh  install-tools.sh  kind-devmart.yaml
> ```

### 단계 2 — 설정 파일 읽기

```bash
cat kind-devmart.yaml
```

```yaml
kind: Cluster
apiVersion: kind.x-k8s.io/v1alpha4
name: devmart
nodes:
  - role: control-plane
    image: kindest/node:v1.37.0@sha256:a1ed56cf…
    extraPortMappings:
      - containerPort: 30080
        hostPort: 30080
        protocol: TCP
  - role: worker
    image: kindest/node:v1.37.0@sha256:a1ed56cf…
  - role: worker
    image: kindest/node:v1.37.0@sha256:a1ed56cf…
```

- `kind: Cluster` · `apiVersion` : 4교시 매니페스트와 같은 모양이다. kind의 설정도 **선언형**이다
- `name: devmart` : 클러스터 이름. 노드 컨테이너 이름이 `devmart-…`가 된다
- `nodes:` : 노드 세 대 — 역할(role)만 다르다
- `image: …@sha256:…` : 노드 이미지를 **다이제스트로 고정**한다. kind 릴리스 노트가 권하는 방식이다. 태그만 쓰면 나중에 다른 이미지가 올 수 있다(2주차 4일차)
- `extraPortMappings` : 노트북의 30080 포트 → 컨트롤 플레인 노드 컨테이너의 30080. 내일 서비스를 브라우저로 볼 통로다

> [!TIP]
> **메모리가 4GiB보다 작다면**
>
> 마지막 `- role: worker` 두 줄을 지워 워커 1대로 만듭니다. 오늘 실습의 '노드 끄기' 실험만 결과가 조금 달라집니다.

### 단계 3 — 만들기

```bash
kind create cluster --config kind-devmart.yaml
```

1~3분 걸립니다. 노드 이미지를 처음 받는다면 더 걸립니다.

> **🟢 확인: 이렇게 나오면 성공 (줄 끝의 그림 문자는 생략)**
>
> ```text
> Creating cluster "devmart" ...
>  ✓ Ensuring node image (kindest/node:v1.37.0)
>  ✓ Preparing nodes
>  ✓ Writing configuration
>  ✓ Starting control-plane
>  ✓ Installing CNI
>  ✓ Installing StorageClass
>  ✓ Joining worker nodes
> Set kubectl context to "kind-devmart"
> You can now use your cluster with:
>
> kubectl cluster-info --context kind-devmart
>
> Thanks for using kind!
> ```

각 줄이 오전에 배운 무엇에 해당하는지 짚어 봅니다.

| kind 출력 | 실제로 한 일 | 관련 교시 |
|---|---|---|
| Preparing nodes | 노드 컨테이너 3개 실행 | 5교시 (kind = 노드가 컨테이너) |
| Starting control-plane | `kubeadm init` — apiserver · etcd · scheduler · controller-manager 시작 | 2교시 |
| Installing CNI | Pod 네트워크 플러그인 kindnet 설치 | 3교시 |
| Installing StorageClass | 디스크를 자동으로 만들어 줄 local-path 설치 | 5일차 (DB 볼륨) |
| Joining worker nodes | 워커의 kubelet이 apiserver에 "나 합류" — `kubeadm join` | 3교시 |
| Set kubectl context | `~/.kube/config`에 접속 정보 기록 | 6교시 단계 6의 그 파일 |

> **🛠️ 막혔다면: 자주 만나는 실패**
>
> | 메시지 | 원인 | 해결 |
> |---|---|---|
> | `Bind for 0.0.0.0:30080 failed: port is already allocated` | 30080을 다른 컨테이너가 쓰는 중 | `docker ps`로 찾아 내리기. 2일차 DevMart가 남아 있지 않은지 |
> | `node(s) already exist for a cluster with the name "devmart"` | 이미 만든 적이 있다 | 그대로 쓰거나, `kind delete cluster --name devmart` 후 다시 |
> | `failed to create cluster: … cgroup` | Docker가 cgroup v1 | 6교시 단계 2. 강사에게 알리기 |
> | `Starting control-plane`에서 수 분 멈춤 뒤 실패 | 메모리 부족이 가장 흔하다 | Docker 메모리 늘리기, 또는 워커 1대로 |

### 단계 4 — 연결 확인

```bash
kubectl cluster-info
kubectl get nodes
```

> **🟢 확인: 이렇게 나오면 성공**
>
> ```text
> Kubernetes control plane is running at https://127.0.0.1:41235
> CoreDNS is running at https://127.0.0.1:41235/api/v1/namespaces/kube-system/services/kube-dns:dns/proxy
>
> To further debug and diagnose cluster problems, use 'kubectl cluster-info dump'.
> ```
> ```text
> NAME                    STATUS   ROLES           AGE   VERSION
> devmart-control-plane   Ready    control-plane   2m    v1.37.0
> devmart-worker          Ready    <none>          95s   v1.37.0
> devmart-worker2         Ready    <none>          95s   v1.37.0
> ```
> - 포트 번호(`41235`)는 사람마다 다릅니다. kind가 비어 있는 포트를 고릅니다.
> - 워커가 잠깐 `NotReady`일 수 있습니다. CNI가 자리 잡는 동안입니다. 30초쯤 뒤 다시 확인합니다.

6교시 단계 6에서 거절당하던 `kubectl version`도 다시 해 봅니다. 이번엔 `Server Version: v1.37.0`이 함께 나옵니다.

## 실습 11 · 클러스터 둘러보기

> **🧪 실습: 실습 목표**
>
> 2 · 3교시의 그림을 옆에 펴 두고, 부품을 하나씩 찾아 체크합니다.

### 단계 1 — 노드는 정말 컨테이너인가

```bash
docker ps --filter label=io.x-k8s.kind.cluster=devmart \
  --format 'table {{.Names}}\t{{.Status}}\t{{.Ports}}'
```

- `--filter label=…` : kind가 노드 컨테이너에 붙이는 라벨로 골라낸다

> **🟢 확인: 보이는 것**
>
> ```text
> NAMES                   STATUS          PORTS
> devmart-worker2         Up 3 minutes
> devmart-control-plane   Up 3 minutes    0.0.0.0:30080->30080/tcp, 127.0.0.1:41235->6443/tcp
> devmart-worker          Up 3 minutes
> ```
> 컨트롤 플레인의 `127.0.0.1:41235->6443/tcp`가 kubectl이 들어가는 문입니다. **6443**은 kube-apiserver의 표준 포트입니다. `127.0.0.1`에만 열려 있어 **내 노트북 밖에서는 접근할 수 없습니다.**

### 단계 2 — kubectl은 어디로 말하나 (kubeconfig)

```bash
kubectl config get-contexts
kubectl config view --minify | grep -E 'server|name:'
```

> **🟢 확인: 보이는 것**
>
> ```text
> CURRENT   NAME           CLUSTER        AUTHINFO       NAMESPACE
> *         kind-devmart   kind-devmart   kind-devmart
> ```
> ```text
>     server: https://127.0.0.1:41235
>   name: kind-devmart
>   name: kind-devmart
>   name: kind-devmart
> ```

> **📖 용어 — kubeconfig와 컨텍스트**
>
> **kubeconfig**(`~/.kube/config`)는 kubectl의 주소록입니다. 세 가지를 적습니다 — **클러스터**(apiserver 주소와 그 인증서), **사용자**(나를 증명할 인증서나 토큰), 그리고 둘을 짝지은 **컨텍스트**(context). `*` 표시가 지금 쓰는 컨텍스트입니다. 5주차에 EKS를 연결하면 이 목록에 한 줄이 늘고, `kubectl config use-context`로 오갑니다. 회사에서 "운영 클러스터에 실수로 명령을 날렸다"는 사고의 대부분이 **컨텍스트 착각**입니다.

> [!WARNING]
> **kubeconfig는 열쇠 꾸러미**
>
> 이 파일에는 클러스터 관리자 인증서가 들어 있습니다. kind는 노트북 안에서만 열리니 괜찮지만, 진짜 클러스터의 kubeconfig는 `.env`처럼 다룹니다 — **Git에 올리지 않고, 채팅에 붙여 넣지 않습니다.** `kubectl config view`가 인증서를 `DATA+OMITTED`로 가려 보여 주는 이유입니다.

### 단계 3 — kubectl은 결국 HTTPS 요청 (2교시 확인)

```bash
kubectl get nodes -v=6 2>&1 | grep -E 'GET|Response'
```

- `-v=6` : kubectl이 보내는 HTTP 요청을 보여 준다 (숫자가 클수록 자세히)

> **🟢 확인: 이런 줄이 보이면 성공**
>
> ```text
> … "Response" verb="GET" url="https://127.0.0.1:41235/api/v1/nodes?limit=500" status="200 OK" milliseconds=8
> ```
> 로그 형식은 kubectl 버전에 따라 조금 다릅니다. 핵심은 **`GET /api/v1/nodes` → `200 OK`** 입니다. 2주차에 `curl`로 DevMart API를 부른 것과 같은 일입니다.

### 단계 4 — 네임스페이스와 시스템 Pod

```bash
kubectl get namespaces
```

> **🟢 확인: 보이는 것**
>
> ```text
> NAME                 STATUS   AGE
> default              Active   4m
> kube-node-lease      Active   4m
> kube-public          Active   4m
> kube-system          Active   4m
> local-path-storage   Active   4m
> ```
> **네임스페이스**는 클러스터 안의 폴더입니다(5일차에 자세히). `kube-system`에 Kubernetes 자신의 부품이 들어 있습니다. 내 앱은 기본으로 `default`에 들어갑니다.

```bash
kubectl get pods -n kube-system \
  -o custom-columns=NAME:.metadata.name,STATUS:.status.phase,NODE:.spec.nodeName
```

- `-n kube-system` : 이 네임스페이스에서
- `-o custom-columns=…` : 이름 · 상태 · **어느 노드에 있는지**만 골라 보기

> **🟢 확인: 보이는 것 (해시 부분은 사람마다 다름)**
>
> ```text
> NAME                                            STATUS    NODE
> coredns-5d4b8c7f9d-7hx2p                        Running   devmart-control-plane
> coredns-5d4b8c7f9d-qm9vt                        Running   devmart-control-plane
> etcd-devmart-control-plane                      Running   devmart-control-plane
> kindnet-4tq8w                                   Running   devmart-worker
> kindnet-9fzcl                                   Running   devmart-control-plane
> kindnet-x7m2d                                   Running   devmart-worker2
> kube-apiserver-devmart-control-plane            Running   devmart-control-plane
> kube-controller-manager-devmart-control-plane   Running   devmart-control-plane
> kube-proxy-6hbqk                                Running   devmart-worker2
> kube-proxy-lz5rn                                Running   devmart-control-plane
> kube-proxy-v8wcd                                Running   devmart-worker
> kube-scheduler-devmart-control-plane            Running   devmart-control-plane
> ```

이 목록을 2 · 3교시 그림과 맞춰 봅니다.

| 보이는 Pod | 정체 | 어디에 | 개수 |
|---|---|---|---|
| `kube-apiserver-…` · `etcd-…` · `kube-scheduler-…` · `kube-controller-manager-…` | 컨트롤 플레인 네 부품 (2교시) | 컨트롤 플레인 노드만 | 1개씩 |
| `kube-proxy-…` | 노드마다 하나 (3교시) | **모든 노드** | 3 |
| `kindnet-…` | CNI 플러그인 (3교시) | **모든 노드** | 3 |
| `coredns-…` | 클러스터 안의 DNS — 서비스 이름으로 찾기 (내일) | 아무 노드 | 2 |

> [!IMPORTANT]
> **kubelet은 목록에 없다**
>
> 3교시에 "가장 중요하다"던 **kubelet이 Pod 목록에 없습니다.** kubelet은 Pod를 띄우는 쪽이라, Pod로 뜰 수 없습니다. 노드 안에서 **일반 프로그램(systemd 서비스)**으로 돕니다. 단계 5에서 직접 확인합니다.

### 단계 5 — 노드 안으로 들어가 보기

노드는 컨테이너이니 `docker exec`로 들어갈 수 있습니다(진짜 서버라면 SSH).

```bash
docker exec devmart-worker systemctl is-active kubelet
docker exec devmart-worker crictl pods
```

- `systemctl is-active kubelet` : kubelet 서비스가 돌고 있는가
- `crictl` : 노드 안에서 containerd에 직접 묻는 도구. 노드에는 `docker`가 없다(3교시)

> **🟢 확인: 보이는 것 (ID는 생략)**
>
> ```text
> active
> ```
> ```text
> POD ID   CREATED         STATE   NAME               NAMESPACE     ATTEMPT   RUNTIME
> …        6 minutes ago   Ready   kindnet-4tq8w      kube-system   0         (default)
> …        6 minutes ago   Ready   kube-proxy-v8wcd   kube-system   0         (default)
> ```
> 단계 4의 목록에서 `NODE`가 `devmart-worker`였던 두 Pod가 정확히 여기 있습니다. **kubectl(본부 장부)과 crictl(현장)이 같은 것을 보고 있습니다.**

### 단계 6 — 컨트롤 플레인 부품은 누가 띄웠나

apiserver가 Pod로 떠 있다면, 그 Pod는 누가 만들었을까요? apiserver가 뜨기 전에는 Pod를 만들 수 없는데요.

```bash
docker exec devmart-control-plane ls /etc/kubernetes/manifests
```

> **🟢 확인: 보이는 것**
>
> ```text
> etcd.yaml
> kube-apiserver.yaml
> kube-controller-manager.yaml
> kube-scheduler.yaml
> ```

> **📖 용어 — 정적 Pod (static Pod)**
>
> 컨트롤 플레인 노드의 kubelet은 apiserver를 거치지 않고, **이 폴더의 매니페스트를 직접 읽어** 네 부품을 띄웁니다. 이것을 **정적 Pod**라고 합니다. 닭이 먼저냐 달걀이 먼저냐 문제를 푸는 방법입니다. kubectl에 보이는 `kube-apiserver-devmart-control-plane`은 kubelet이 "이런 Pod를 띄웠다"고 apiserver에 알려 둔 **거울 사본**(mirror Pod)입니다.

### 단계 7 — 앱 Pod는 왜 컨트롤 플레인에 안 가나

```bash
kubectl describe node devmart-control-plane | grep Taints
kubectl describe node devmart-worker | grep Taints
```

> **🟢 확인: 보이는 것**
>
> ```text
> Taints:             node-role.kubernetes.io/control-plane:NoSchedule
> Taints:             <none>
> ```
> **테인트**(taint, 얼룩)는 노드에 붙이는 "출입 제한" 표시입니다. 컨트롤 플레인에는 `NoSchedule` — "일반 Pod는 여기 놓지 마"가 붙어 있습니다. 본부 건물에 창고 짐을 쌓지 않는 것과 같습니다. 2교시의 스케줄러가 '거르기' 단계에서 이 노드를 뺍니다. 그래서 내일 만들 DevMart Pod는 워커 두 대에만 놓입니다. (`coredns` · `kindnet`처럼 "괜찮다"는 **톨러레이션**(toleration)을 가진 시스템 Pod는 예외입니다.)

### 단계 8 — 어떤 종류의 리소스가 있나

```bash
kubectl api-resources --api-group=apps
```

> **🟢 확인: 보이는 것**
>
> ```text
> NAME                  SHORTNAMES   APIVERSION   NAMESPACED   KIND
> controllerrevisions                apps/v1      true         ControllerRevision
> daemonsets            ds           apps/v1      true         DaemonSet
> deployments           deploy       apps/v1      true         Deployment
> replicasets           rs           apps/v1      true         ReplicaSet
> statefulsets          sts          apps/v1      true         StatefulSet
> ```
> 4교시 매니페스트의 `apiVersion: apps/v1` · `kind: Deployment`가 바로 이 줄입니다. 그리고 단계 4에서 **모든 노드에 하나씩** 있던 `kube-proxy` · `kindnet`은 **DaemonSet**("노드마다 하나씩"을 지키는 컨트롤러)이 만든 것입니다. `kubectl get daemonsets -n kube-system`으로 확인해 보세요.

> [!TIP]
> **정리 스크립트**
>
> 단계 1~6의 읽기 명령은 `cluster-tour.sh`에 모아 두었습니다. 내일 아침 클러스터 상태를 확인할 때 `bash cluster-tour.sh`로 한 번에 봅니다.

## 실습 12 · 지우고, 끄고, 멈추기

> **🧪 실습: 실습 목표**
>
> reconcile과 노드 장애를 직접 일으켜 봅니다. 실험마다 **"누가 고쳤나(또는 왜 못 고쳤나)"**를 기록합니다.

> [!WARNING]
> **실험 순서를 지킵니다**
>
> 실험 3(컨트롤 플레인 멈추기)을 먼저 하면 실험 1 · 2가 동작하지 않습니다. 반드시 1 → 2 → 3 순서로, 실험이 끝날 때마다 원래대로 되돌린 뒤 넘어갑니다.

### 실험 1 — 시스템 Pod를 지우면

```bash
kubectl -n kube-system get deployment coredns
kubectl -n kube-system delete pod -l k8s-app=kube-dns
kubectl -n kube-system get pods -l k8s-app=kube-dns
```

- `-l k8s-app=kube-dns` : 이 **라벨**이 붙은 Pod들 (4교시의 라벨 · 셀렉터)

> **🟢 확인: 보이는 것**
>
> ```text
> NAME      READY   UP-TO-DATE   AVAILABLE   AGE
> coredns   2/2     2            2           12m
> ```
> ```text
> pod "coredns-5d4b8c7f9d-7hx2p" deleted
> pod "coredns-5d4b8c7f9d-qm9vt" deleted
> ```
> ```text
> NAME                       READY   STATUS    RESTARTS   AGE
> coredns-5d4b8c7f9d-c2wfn   1/1     Running   0          6s
> coredns-5d4b8c7f9d-j8kxr   1/1     Running   0          6s
> ```
> - 지운 지 몇 초 만에 **이름이 다른** 새 Pod 두 개가 생겼습니다 (3교시: Pod는 소모품, 바뀌면 이름도 바뀐다).
> - 누가? `coredns` Deployment가 "2개"를 선언해 두었고, **ReplicaSet 컨트롤러**가 0개를 보고 2개를 만들었습니다(4교시의 반복).

### 실험 2 — 워커 노드를 끄면

```bash
docker stop devmart-worker2
kubectl get nodes -w
```

- `docker stop` : 노드 컨테이너를 끈다 = 서버 전원이 나간 것과 같다
- `-w` : 바뀔 때마다 한 줄씩 계속 보여 준다 (watch). 멈추려면 **Ctrl+C**

> **🟢 확인: 1분 안쪽에 이렇게 바뀝니다**
>
> ```text
> NAME                    STATUS     ROLES           AGE   VERSION
> devmart-control-plane   Ready      control-plane   14m   v1.37.0
> devmart-worker          Ready      <none>          13m   v1.37.0
> devmart-worker2         Ready      <none>          13m   v1.37.0
> devmart-worker2         NotReady   <none>          14m   v1.37.0
> ```
> 바로 바뀌지 않습니다. worker2의 kubelet은 주기적으로 "나 살아 있다"(heartbeat)를 보내는데, 그것이 **일정 시간 끊겨야** Node 컨트롤러가 `NotReady`로 바꿉니다. 네트워크가 잠깐 흔들린 것과 진짜 장애를 구분하기 위한 기다림입니다.

Ctrl+C로 멈추고 테인트를 봅니다.

```bash
kubectl describe node devmart-worker2 | grep -A1 Taints
```

> **🟢 확인: 보이는 것**
>
> ```text
> Taints:             node.kubernetes.io/unreachable:NoExecute
>                     node.kubernetes.io/unreachable:NoSchedule
> ```
> Node 컨트롤러가 worker2에 **"연락 안 됨"** 얼룩을 붙였습니다. `NoSchedule` — 새 Pod를 놓지 마라. `NoExecute` — 있던 Pod도 (기본 5분 뒤) 다른 곳으로 옮겨라. 내일 앱 Pod를 올린 뒤 같은 실험을 하면, 5분 뒤 worker2의 앱 Pod가 worker로 **옮겨 가는** 것을 볼 수 있습니다.

되돌립니다.

```bash
docker start devmart-worker2
kubectl get nodes -w
```

> **🟢 확인: 다시 Ready**
>
> 30초~1분 안에 `devmart-worker2   Ready`로 돌아옵니다. 테인트도 사라집니다. Ctrl+C로 멈춥니다.

### 실험 3 — 컨트롤 플레인을 멈추면

```bash
docker stop devmart-control-plane
kubectl get nodes
```

> **🟢 확인: 이 오류가 나야 정상**
>
> ```text
> The connection to the server 127.0.0.1:41235 was refused - did you specify the right host or port?
> ```
> 6교시 단계 6의 오류와 같은 모양입니다. 이번엔 주소가 `localhost:8080`이 아니라 **kubeconfig에 적힌 진짜 주소**입니다. "주소는 맞는데 apiserver가 대답을 안 한다"는 뜻입니다. 같은 오류 문장이라도 **어느 주소인지**가 진단의 열쇠입니다.

> **📘 예시 — 지금 워커들은?**
>
> ```bash
> docker exec devmart-worker crictl pods --state ready | head -3
> ```
> 워커의 Pod(`kube-proxy`, `kindnet`)는 **그대로 돌고 있습니다.** 2교시 예시 표의 "본부가 멈춰도 현장은 하던 일을 계속한다"가 이것입니다. 다만 지금 워커의 Pod가 죽으면 아무도 새로 만들어 주지 않습니다.

되돌립니다.

```bash
docker start devmart-control-plane
sleep 30
kubectl get nodes
```

> **🟢 확인: 다시 응답**
>
> 처음 몇 번은 `connection refused`나 `the server is currently unable to handle the request`가 날 수 있습니다. apiserver와 etcd가 다시 뜨는 중입니다. 30초~1분 뒤 세 노드가 모두 `Ready`로 보이면 끝입니다.

> **🛠️ 막혔다면: 몇 분이 지나도 돌아오지 않는다**
>
> kind 클러스터는 노드 컨테이너를 껐다 켜는 것을 대부분 견디지만, 노트북 메모리가 부족하거나 Docker Desktop 자체를 재시작하면 가끔 망가집니다. 망가진 kind 클러스터는 **고치지 않고 새로 만드는 것**이 원칙입니다 — 5교시에서 kind를 고른 이유입니다.
> ```bash
> kind delete cluster --name devmart
> kind create cluster --config kind-devmart.yaml
> ```
> ```text
> Deleting cluster "devmart" ...
> Deleted nodes: ["devmart-worker2" "devmart-control-plane" "devmart-worker"]
> ```

## 실습 13 · 1교시 표 완성

1교시에 만든 표의 오른쪽 칸을 채웁니다. 오늘 직접 본 것을 근거로 적습니다.

> **🟢 확인: 예시 답**
>
> | 1~2일차에 내가 손으로 한 일 | Kubernetes에서는 누가? |
> |---|---|
> | `--scale order-worker=3` | Deployment의 `replicas: 3` → ReplicaSet 컨트롤러가 개수를 맞춘다 (실험 1) |
> | `restart:` 정책이 다시 띄움 | 같은 노드에서는 kubelet이 컨테이너를 다시 시작, Pod가 사라지면 컨트롤러가 새로 만든다 |
> | 컴퓨터가 꺼지면 손으로 다시 | Node 컨트롤러가 NotReady 표시 + 테인트 → 5분 뒤 다른 노드에 다시 (실험 2) |
> | 서비스 이름으로 찾아가기 (Compose DNS) | CoreDNS + Service (내일) |
> | 헬스 체크 | kubelet이 probe로 직접 묻는다 (5일차) |

> **✅ 확인 문제**
>
> 1. kubectl은 어떤 파일을 보고 접속할 apiserver 주소를 아나요?
> 2. kubelet이 `kubectl get pods -n kube-system` 목록에 없는 이유는?
> 3. 컨트롤 플레인 부품 네 개는 apiserver 없이 어떻게 뜨나요?
> 4. 일반 앱 Pod가 컨트롤 플레인 노드에 놓이지 않는 이유는?
> 5. 워커 노드를 꺼도 바로 `NotReady`가 되지 않는 이유는?
> 6. `connection … refused` 오류에서 주소가 `localhost:8080`일 때와 `127.0.0.1:41235`일 때 원인은 각각?
>
> <details><summary>정답</summary>
>
> 1. kubeconfig (`~/.kube/config`)의 현재 컨텍스트
> 2. kubelet은 Pod를 띄우는 쪽이라 노드에서 일반 서비스(systemd)로 돈다
> 3. 정적 Pod — kubelet이 `/etc/kubernetes/manifests`의 파일을 직접 읽어 띄운다
> 4. 컨트롤 플레인 노드에 `NoSchedule` 테인트가 있어 스케줄러가 거른다
> 5. 하트비트가 일정 시간 끊겨야 장애로 판단한다 (잠깐의 네트워크 흔들림과 구분)
> 6. `localhost:8080` — kubeconfig가 없다(어디로 갈지 모름). `127.0.0.1:41235` — 주소는 맞는데 apiserver가 응답하지 않는다(컨트롤 플레인이 멈춤)
>
> </details>

## 참고 문헌

- kind. *Quick Start* · *Configuration* · *Known Issues*. kind.sigs.k8s.io/docs
- Kubernetes Docs. *Organizing Cluster Access Using kubeconfig Files*. kubernetes.io/docs/concepts/configuration
- Kubernetes Docs. *Create static Pods* · *Taints and Tolerations* · *Node Status — Heartbeats*. kubernetes.io/docs
- Kubernetes Docs. *Debugging Kubernetes nodes with crictl*. kubernetes.io/docs/tasks/debug
- Kubernetes Docs. *DaemonSet*. kubernetes.io/docs/concepts/workloads/controllers/daemonset

---

| 이전 | 목차 | 다음 |
|:--|:--:|--:|
| ⬅️ [6교시 · kubectl과 kind 설치](lesson-06.md) | [⬆️ 3일차 목차](README.md) | [8교시 · API 서버와 etcd 들여다보기 — 클러스터의 기억과 감시](lesson-08.md) ➡️ |
