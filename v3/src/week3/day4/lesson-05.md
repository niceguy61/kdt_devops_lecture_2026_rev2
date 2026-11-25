# 5교시 · ReplicaSet과 자가 치유

!!! goal "이번 시간에 할 일"
    - Pod를 지우고, 컨테이너를 죽이고, 라벨을 떼고, 노드를 끄며 **자가 치유**(self-healing)가 어떻게 일어나는지 봅니다.
    - **컨테이너 재시작**(kubelet)과 **Pod 교체**(ReplicaSet)의 차이를 구분합니다.
    - 노드 장애 때 Pod가 다른 노드로 옮겨 가는 과정과 그 **시간**을 잽니다.

!!! key "실험의 틀"
    실험마다 터미널 A에 `kubectl get pods -l app=catalog-api -o wide -w`를 띄워 두고, 터미널 B에서 망가뜨립니다. 기록할 것은 세 가지 — **무엇이 바뀌었나 · 누가 고쳤나 · 얼마나 걸렸나**.

```bash
# 터미널 A — 실험 내내 켜 둔다
kubectl get pods -l app=catalog-api -o wide -w
```

## 실험 1 · Pod 하나를 지우면

```bash
# 터미널 B
POD=$(kubectl get pod -l app=catalog-api -o jsonpath='{.items[0].metadata.name}')
kubectl delete pod $POD
```

!!! check "터미널 A"
    ```text
    catalog-api-6b8f7c9d5c-4xk2m   1/1     Terminating         0     12m   10.244.1.5   devmart-worker
    catalog-api-6b8f7c9d5c-r7n2k   0/1     Pending             0     0s    <none>       <none>
    catalog-api-6b8f7c9d5c-r7n2k   0/1     Pending             0     0s    <none>       devmart-worker2
    catalog-api-6b8f7c9d5c-r7n2k   0/1     ContainerCreating   0     0s    <none>       devmart-worker2
    catalog-api-6b8f7c9d5c-r7n2k   1/1     Running             0     2s    10.244.2.5   devmart-worker2
    ```
    - 지우는 순간 **새 이름, 새 IP**의 Pod가 생깁니다. 2초면 `Running`입니다(이미지가 이미 노드에 있으니까).
    - 고친 것은 **ReplicaSet 컨트롤러**입니다. 3개여야 하는데 2개가 된 차이를 보고 하나를 만들었습니다. 어제 4교시의 반복 그대로입니다.

## 실험 2 · 컨테이너만 죽으면

이번엔 Pod는 두고, 안의 프로세스만 끝냅니다.

```bash
POD=$(kubectl get pod -l app=catalog-api -o jsonpath='{.items[0].metadata.name}')
kubectl exec $POD -- python -c "import os, signal; os.kill(1, signal.SIGTERM)"
kubectl get pod $POD
```

- 컨테이너 안의 **PID 1**(gunicorn 주 프로세스)에게 '끝내라' 신호를 보낸다

!!! check "보이는 것"
    ```text
    NAME                           READY   STATUS    RESTARTS     AGE
    catalog-api-6b8f7c9d5c-9tq7w   1/1     Running   1 (3s ago)   14m
    ```
    **이름이 그대로**이고 **RESTARTS가 1**이 됐습니다. 새 Pod가 아니라 **같은 Pod 안에서 컨테이너만 다시 시작**했습니다. 고친 것은 그 노드의 **kubelet**입니다. Pod의 기본 재시작 정책 `restartPolicy: Always`에 따른 것으로, 2일차 Compose의 `restart: unless-stopped`와 같은 역할입니다.

| | 실험 1 — Pod 삭제 | 실험 2 — 컨테이너 종료 |
|---|---|---|
| 고친 주체 | ReplicaSet 컨트롤러 (컨트롤 플레인) | kubelet (노드) |
| 결과 | **새 Pod** — 이름 · IP 바뀜, 다른 노드일 수도 | **같은 Pod** — 이름 · IP 그대로, RESTARTS +1 |
| 범위 | 클러스터 어디든 | 그 노드 안에서만 |
| 계속 실패하면 | (Pod 자체는 잘 뜸) | CrashLoopBackOff (3교시) |

!!! myth "오해 — CrashLoopBackOff면 ReplicaSet이 새 Pod로 바꿔 주겠지"
    아닙니다. CrashLoopBackOff인 Pod도 **ReplicaSet 입장에서는 '있는' Pod**입니다. 개수는 맞으니 ReplicaSet은 아무것도 하지 않고, kubelet만 그 자리에서 계속 다시 시작합니다. 어차피 새 Pod를 만들어도 같은 설정이라 똑같이 죽습니다. 자가 치유는 **일시적인 고장**을 메워 줄 뿐, **틀린 설정**을 고쳐 주지 않습니다.

## 실험 3 · 라벨을 떼면

```bash
POD=$(kubectl get pod -l app=catalog-api -o jsonpath='{.items[0].metadata.name}')
kubectl label pod $POD app=debug --overwrite
kubectl get pods -L app
```

- `label … --overwrite` : 이미 있는 라벨 값을 바꾼다
- `-L app` : `app` 라벨 값을 칸으로 보여 준다

!!! check "보이는 것"
    ```text
    NAME                           READY   STATUS    RESTARTS   AGE   APP
    catalog-api-6b8f7c9d5c-9tq7w   1/1     Running   1          16m   debug
    catalog-api-6b8f7c9d5c-hz5rp   1/1     Running   0          16m   catalog-api
    catalog-api-6b8f7c9d5c-r7n2k   1/1     Running   0          4m    catalog-api
    catalog-api-6b8f7c9d5c-w5j9d   1/1     Running   0          2s    catalog-api
    ```
    - Pod가 **4개**가 됐습니다. 라벨을 뗀 Pod는 셀렉터(`app=catalog-api`)에 안 걸리니, ReplicaSet은 "2개뿐"이라고 보고 하나를 새로 만들었습니다.
    - 라벨을 뗀 Pod는 지워지지 않고 그대로 돕니다. 이제 **주인이 없는 Pod**입니다.

```bash
kubectl get pod $POD -o jsonpath='{.metadata.ownerReferences}{"\n"}'
```

!!! check "보이는 것"
    ```text

    ```
    빈 줄 — 주인(ownerReferences)이 사라졌습니다. ReplicaSet이 **놓아준** 것입니다.

!!! tip "실무에서 쓰는 기술 — 이상한 Pod를 격리하기"
    운영 중 Pod 하나가 이상하게 굴 때, 바로 지우면 증거도 사라집니다. 라벨을 바꿔 **떼어 놓으면**, ReplicaSet은 대신할 새 Pod를 만들고, 6교시의 Service도 이 Pod로 손님을 보내지 않게 됩니다. 떼어 놓은 Pod는 천천히 `logs` · `exec`로 조사한 뒤 지웁니다.

조사가 끝났다고 치고 지웁니다.

```bash
kubectl delete pod $POD
```

## 실험 4 · 노드를 끄면

어제 7교시 실험 2를, 이번엔 **앱 Pod가 있는 상태**에서 합니다.

### 단계 1 — 지금 배치 확인

```bash
kubectl get pods -l app=catalog-api -o wide
```

worker2에 Pod가 하나 이상 있는지 확인합니다. 없다면 실험 1을 한 번 더 해서 섞습니다.

### 단계 2 — worker2 끄기와 시간 재기

```bash
date +%T; docker stop devmart-worker2
kubectl get nodes -w
```

`NotReady`가 보이면 시각을 적고 Ctrl+C. 터미널 A를 봅니다.

!!! check "터미널 A — 1분 남짓 뒤"
    ```text
    catalog-api-6b8f7c9d5c-r7n2k   1/1     Terminating         0     10m   10.244.2.5   devmart-worker2
    catalog-api-6b8f7c9d5c-k8d4s   0/1     Pending             0     0s    <none>       devmart-worker
    catalog-api-6b8f7c9d5c-k8d4s   0/1     ContainerCreating   0     0s    <none>       devmart-worker
    catalog-api-6b8f7c9d5c-k8d4s   1/1     Running             0     2s    10.244.1.8   devmart-worker
    ```

걸린 시간은 두 단계를 더한 것입니다.

| 구간 | 누가 | 기본값 | 오늘 |
|---|---|---|---|
| 노드 끄기 → `NotReady` | Node 컨트롤러가 하트비트 끊김을 기다림 | 40~50초 안팎 | 같음 |
| `NotReady` → Pod 옮기기 | `unreachable` 테인트를 견디는 시간(toleration) | **300초** | **30초** (`deployment.yaml`의 `tolerations`) |

!!! warn "실습용으로 줄인 값"
    `deployment.yaml`에 `tolerationSeconds: 30`을 넣어 둔 것은 수업 시간 안에 보기 위해서입니다. 기본 5분은 **네트워크가 잠깐 끊긴 것**과 **진짜 장애**를 구분하려는 기다림입니다. 너무 짧으면 잠깐 흔들릴 때마다 Pod가 우르르 옮겨 가며 오히려 장애를 키웁니다. 운영 환경에서는 기본값을 두거나 신중하게 정합니다.

### 단계 3 — Terminating에서 멈춘 Pod

```bash
kubectl get pods -l app=catalog-api -o wide
```

!!! check "보이는 것"
    ```text
    NAME                           READY   STATUS        RESTARTS   AGE   IP           NODE
    catalog-api-6b8f7c9d5c-hz5rp   1/1     Running       0          20m   10.244.1.6   devmart-worker
    catalog-api-6b8f7c9d5c-k8d4s   1/1     Running       0          40s   10.244.1.8   devmart-worker
    catalog-api-6b8f7c9d5c-r7n2k   1/1     Terminating   0          12m   10.244.2.5   devmart-worker2
    catalog-api-6b8f7c9d5c-w5j9d   1/1     Running       0          8m    10.244.1.7   devmart-worker
    ```
    worker2의 Pod는 `Terminating`에서 **멈춰 있습니다.** 컨트롤 플레인은 "지워라"라고 적었지만, worker2의 kubelet이 연락이 안 되니 **정말 지워졌는지 확인할 수 없기** 때문입니다. 그래도 ReplicaSet은 이 Pod를 세지 않고 이미 대신할 Pod를 만들었습니다. 사용자 쪽에서는 `Running` 3개가 그대로입니다.

### 단계 4 — 되돌리기

```bash
docker start devmart-worker2
sleep 40
kubectl get nodes
kubectl get pods -l app=catalog-api -o wide
```

!!! check "보이는 것"
    worker2가 `Ready`로 돌아오고, `Terminating`이던 Pod는 kubelet이 확인한 뒤 사라집니다. 그런데 **Pod 세 개가 모두 worker에** 있습니다. worker2가 돌아왔다고 Pod가 다시 옮겨 가지는 않습니다.

!!! myth "오해 — Kubernetes는 Pod를 노드에 고르게 다시 나눠 준다"
    스케줄러는 **새 Pod를 놓을 때만** 결정합니다. 이미 도는 Pod를 옮기지는 않습니다. 그래서 장애 뒤에는 한쪽 노드에 몰린 상태가 남습니다. 다시 고르게 하려면 `kubectl rollout restart deployment/catalog-api`로 Pod를 새로 만들게 하거나(7교시), 몰린 Pod를 골라 내보내는 **Descheduler**(별도 프로젝트)를 씁니다. 같은 앱 Pod를 노드에 고루 퍼뜨리라는 규칙(topologySpreadConstraints)을 처음부터 매니페스트에 적어 두는 방법도 있습니다.

## 실습 9 · 자가 치유 관찰 기록

!!! lab "실습 목표"
    네 실험을 표 하나로 정리합니다.

| 실험 | 무엇이 바뀌었나 (이름 · IP · RESTARTS · 노드) | 누가 고쳤나 | 얼마나 걸렸나 |
|---|---|---|---|
| 1. Pod 삭제 | | | |
| 2. 컨테이너 종료 | | | |
| 3. 라벨 떼기 | | | |
| 4. 노드 끄기 | | | |

!!! academic "학술 노트 — 장애를 '견디는' 시스템과 'MTTR'"
    전통적인 운영은 고장 나지 않게(MTBF, 평균 고장 간격 늘리기) 하는 데 힘을 썼습니다. 클라우드 네이티브 운영은 **고장은 난다고 보고, 빨리 회복하게**(MTTR, 평균 회복 시간 줄이기) 하는 쪽으로 무게가 옮겨 왔습니다. 오늘 실험 1의 2초, 실험 4의 1분 남짓이 Kubernetes가 기계적으로 줄여 주는 MTTR입니다. 1주차 5일차의 **DORA 지표**에도 '장애 복구 시간'(failed deployment recovery time)이 들어 있습니다. 이 생각의 뿌리로 자주 인용되는 것이 Candea & Fox의 **크래시 전용 소프트웨어**(Crash-Only Software, HotOS 2003)입니다. "정상 종료와 비정상 종료를 구분하지 말고, 언제 죽어도 다시 시작하면 되게 만들라" — Pod가 소모품이 되려면 앱이 이렇게 만들어져야 합니다.

!!! trend "트렌드 2026 — 일부러 망가뜨려 보기"
    오늘 한 실험을 운영 환경에서 **정기적으로, 자동으로** 하는 것이 **카오스 엔지니어링**입니다(2일차 1교시 트렌드). Kubernetes용으로는 Chaos Mesh · LitmusChaos(둘 다 CNCF 프로젝트)가 Pod 삭제 · 노드 장애 · 네트워크 지연을 매니페스트로 일으킵니다. 실제 장애를 기다리지 않고, 자가 치유가 **정말 기대대로 동작하는지**와 **얼마나 걸리는지**를 미리 잽니다.

!!! quiz "확인 문제"
    1. Pod를 지웠을 때와 컨테이너가 죽었을 때, 고치는 주체는 각각?
    2. 라벨을 바꾼 Pod가 지워지지 않고 남는 이유는?
    3. 노드를 끈 뒤 Pod가 옮겨 가기까지의 시간은 어떤 두 구간의 합인가요?
    4. 노드가 돌아온 뒤에도 Pod가 한쪽에 몰려 있는 이유는?

    ??? answer "정답"
        1. Pod 삭제 — ReplicaSet 컨트롤러(새 Pod), 컨테이너 종료 — kubelet(같은 Pod에서 재시작)
        2. ReplicaSet은 셀렉터에 맞는 Pod만 자기 것으로 센다. 라벨이 바뀐 Pod는 놓아줄 뿐 지우지 않는다
        3. NotReady로 판단되기까지(하트비트 대기) + unreachable 테인트를 견디는 시간(tolerationSeconds, 기본 300초)
        4. 스케줄러는 새 Pod를 놓을 때만 결정하고, 이미 도는 Pod를 다시 나누지 않는다

## 참고 문헌

- Kubernetes Docs. *ReplicaSet* · *Pod Lifecycle — Container restart policy*. kubernetes.io/docs/concepts/workloads
- Kubernetes Docs. *Taints and Tolerations — Taint based Evictions*. kubernetes.io/docs/concepts/scheduling-eviction
- Kubernetes SIGs. *Descheduler*. github.com/kubernetes-sigs/descheduler
- Candea, G., & Fox, A. (2003). Crash-Only Software. *HotOS IX*.
