# 4교시: Deployment가 필요한 이유

![Week 3 Day 5 Lesson 4](./assets/lesson-04-deployment-self-healing.png)

## 수업 목표
- 직접 만든 Pod와 Deployment의 차이를 운영 관점으로 설명한다.
- Deployment, ReplicaSet, Pod의 소유 관계를 확인한다.
- Pod를 삭제했을 때 Deployment가 replica 수를 다시 맞추는 self-healing을 관찰한다.

## 직접 Pod에서 생기는 운영 문제
2교시에서 만든 `hello-pod`는 학습용으로는 좋지만 운영 배포 단위로는 부족하다.

| 운영 요구 | 직접 Pod의 한계 |
|---|---|
| 같은 앱을 2개 이상 띄우기 | Pod manifest를 여러 개 직접 관리해야 함 |
| 죽은 Pod 복구 | Pod를 다시 만들어 줄 controller가 없음 |
| image 교체 | rollout/history/undo 흐름이 약함 |
| 서비스 연결 | label과 endpoint 관리가 불안정 |
| 배포 상태 확인 | `rollout status` 같은 배포 단위 상태가 없음 |

Deployment는 이 문제를 해결하기 위해 Pod template과 replica 수를 선언한다.

```text
Deployment
  -> ReplicaSet
    -> Pod 1
    -> Pod 2
```

## Deployment와 ReplicaSet count가 둘 다 보이는 이유
처음 Kubernetes를 볼 때 가장 헷갈리는 지점이 여기다. `Deployment`에도 replica 수가 있고, 그 아래 `ReplicaSet`에도 replica 수가 있다. 둘 중 하나가 node별 count를 의미하는 것은 아니다.

| 항목 | count가 의미하는 것 | node와의 관계 |
|---|---|---|
| Deployment `spec.replicas` | 이 application version을 최종적으로 몇 개 유지할지 선언 | node를 직접 고르지 않음 |
| ReplicaSet `spec.replicas` | 특정 Pod template으로 Pod를 몇 개 유지할지 실행 | node를 직접 고르지 않음 |
| Scheduler | 만들어진 Pod를 어느 node에 둘지 결정 | node 배치 담당 |
| DaemonSet | 보통 node마다 Pod 1개씩 유지 | node 수와 강하게 연결 |

Deployment는 "앱 배포 단위"다. ReplicaSet은 Deployment가 만든 "특정 Pod template의 Pod 집합"이다. node별 배치는 ReplicaSet이 아니라 Scheduler가 한다.

```text
Deployment: hello-web v1을 2개 유지해
  -> ReplicaSet: 이 Pod template으로 2개 유지해
    -> Pod 2개 생성
      -> Scheduler: 각 Pod를 어느 node에 둘지 결정
```

따라서 아래처럼 설명한다.

```text
Deployment의 replica count = 운영자가 원하는 앱 전체 개수
ReplicaSet의 replica count = 현재 Pod template을 기준으로 유지해야 하는 Pod 개수
node별 count = ReplicaSet이 아니라 Scheduler/DaemonSet/scheduling 정책의 영역
```

rolling update 때 ReplicaSet count가 더 중요하게 보인다. 새 template이 생기면 새 ReplicaSet이 만들어지고, Deployment는 새 ReplicaSet의 count를 늘리면서 기존 ReplicaSet의 count를 줄인다.

```text
Deployment desired replicas = 2
old ReplicaSet replicas: 2 -> 1 -> 0
new ReplicaSet replicas: 0 -> 1 -> 2
```

## Deployment 배포
```bash
export NS=week3
export LAB=week3/day5/labs/k8s-first-app

kubectl apply -f "$LAB/deployment.yaml"
kubectl -n "$NS" rollout status deployment/hello-web
kubectl -n "$NS" get deploy,rs,pod -l app=hello-web -o wide
```

예상 패턴:
```text
deployment.apps/hello-web successfully rolled out
deployment.apps/hello-web   2/2
replicaset.apps/hello-web-...
pod/hello-web-...           Running
pod/hello-web-...           Running
```

Deployment와 ReplicaSet의 count를 나란히 본다.

```bash
kubectl -n "$NS" get deploy hello-web
kubectl -n "$NS" get rs -l app=hello-web
```

읽는 법:

| 출력 | 해석 |
|---|---|
| Deployment `READY 2/2` | Deployment가 원하는 전체 앱 replica 2개 중 2개가 Ready |
| ReplicaSet `DESIRED 2` | 현재 Pod template을 가진 ReplicaSet이 Pod 2개를 유지해야 함 |
| Pod `NODE` | Scheduler가 각 Pod를 어느 node에 배치했는지 보여줌 |

kind 단일 node 실습에서는 Pod가 같은 node에 몰려 보일 수 있다. 이것은 ReplicaSet이 node별로 배치했다는 뜻이 아니라, cluster에 node가 하나뿐이라 Scheduler가 선택할 node가 하나뿐인 것이다.

노드마다 1개씩 떠야 하는 예시는 Deployment/ReplicaSet이 아니라 DaemonSet이다.

```text
로그 수집 agent
node exporter
CNI agent
storage CSI node plugin
```

이런 workload는 "앱 replica 수"보다 "node마다 agent가 있어야 한다"는 목적이 강하다.

## Deployment가 유지하는 상태
manifest에서 가장 중요한 부분은 replica 수와 Pod template이다.

```yaml
spec:
  replicas: 2
  selector:
    matchLabels:
      app: hello-web
  template:
    metadata:
      labels:
        app: hello-web
    spec:
      containers:
        - name: nginx
          image: nginx:1.27
```

| 필드 | 의미 |
|---|---|
| `replicas: 2` | Ready Pod 2개를 유지하고 싶다 |
| `selector.matchLabels` | Deployment가 관리할 Pod를 찾는 기준 |
| `template.metadata.labels` | 새로 만들 Pod에 붙일 label |
| `template.spec.containers` | Pod 안 container spec |

selector와 template label이 맞지 않으면 Deployment는 Pod를 제대로 소유할 수 없다. 이 부분은 Week4 Ingress/Service 장애에서도 계속 등장한다.

## Self-healing 확인
Pod 하나를 삭제해도 Deployment가 replica 수를 다시 맞춘다.

```bash
POD_NAME=$(kubectl -n "$NS" get pod -l app=hello-web -o jsonpath='{.items[0].metadata.name}')
kubectl -n "$NS" delete pod "$POD_NAME"
kubectl -n "$NS" get pod -l app=hello-web -w
```

관찰 포인트:
```text
삭제된 Pod는 Terminating이 된다.
새 Pod가 생성된다.
최종적으로 Running Pod가 다시 2개가 된다.
```

`-w`는 watch 모드다. 흐름을 확인한 뒤 `Ctrl+C`로 종료한다.

## owner 관계 확인
```bash
kubectl -n "$NS" get pod -l app=hello-web -o jsonpath='{range .items[*]}{.metadata.name}{" <- "}{.metadata.ownerReferences[0].kind}{"/"}{.metadata.ownerReferences[0].name}{"\n"}{end}'
```

예상:
```text
hello-web-xxxxx <- ReplicaSet/hello-web-xxxxx
```

Deployment가 직접 Pod를 붙잡는 것처럼 보이지만 중간에 ReplicaSet이 있다. rollout 때 새 ReplicaSet과 기존 ReplicaSet의 replica 수를 조정하는 것도 이 구조 때문이다.

## 한 줄 요약
```text
Deployment는 Pod를 직접 실행하는 방법이 아니라,
Pod template과 replica 수를 원하는 상태로 유지하는 controller 단위다.
```

## Evidence Note
```markdown
# W3D5S4 Deployment
- deployment READY:
- replica count:
- ReplicaSet name:
- deleted Pod:
- newly created Pod:
- self-healing evidence:
```
