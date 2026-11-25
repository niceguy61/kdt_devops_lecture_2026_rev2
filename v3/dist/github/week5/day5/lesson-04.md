# 4교시 · 클라우드 장애 훈련 — 노드와 AZ

> [!NOTE]
> **이번 시간에 할 일**
>
> - EC2 콘솔에서 **노드 하나를 종료**하고, Kubernetes와 AWS가 각각 무엇을 하는지 봅니다.
> - db의 **데이터가 살아남는지** 주문 수로 확인합니다.
> - **AZ 하나를 못 쓰게** 만들어, 상태 있는 Pod가 왜 회복하지 못하는지 봅니다.
> - 장애 기록을 한 장 씁니다.

## 준비 — 손님과 기준선

```bash
kubectl config use-context eks-devmart
NLB=$(kubectl get gateway devmart -n devmart -o jsonpath='{.status.addresses[0].value}')
for i in $(seq 5); do curl -s -o /dev/null -X POST http://$NLB/api/orders -H 'content-type: application/json' -d '{"product_id":1,"quantity":1}'; done
curl -s http://$NLB/api/orders | grep -o '"id":[0-9]*' | head -1
kubectl get pods -n devmart -o wide | awk '{print $1, $7}' | column -t
kubectl get nodes -L topology.kubernetes.io/zone
```

> **🟢 확인: 확인 — 기록해 둔다**
>
> ```text
> "id":7                       ← 가장 최근 주문 번호
> NAME                          NODE
> catalog-api-…                 ip-10-0-131-52…
> db-6b7f8c9d5-q4w2e            ip-10-0-131-52…      ← db가 있는 노드
> …
> NAME                STATUS   ROLES    AGE   VERSION   ZONE
> ip-10-0-131-52…     Ready    <none>   40m   v1.36.○   ap-northeast-2a
> ip-10-0-150-17…     Ready    <none>   40m   v1.36.○   ap-northeast-2c
> ```
> **db가 있는 노드**와 그 AZ를 적어 둡니다(대개 2a — 4일차 6교시의 PV가 2a였다면).

터미널 A — 손님 루프(2일차 6교시와 같은 모양):

```bash
while true; do
  printf '%s products=%s orders=%s\n' "$(date +%T)" \
    "$(curl -s -m 3 -o /dev/null -w '%{http_code}' http://$NLB/api/products)" \
    "$(curl -s -m 3 -o /dev/null -w '%{http_code}' -X POST http://$NLB/api/orders -H 'content-type: application/json' -d '{"product_id":1,"quantity":1}')"
  sleep 2
done
```

## 훈련 1 · db가 있는 노드를 종료

EC2 콘솔 → 인스턴스 → 위에서 적은 노드(이름 `default`, 사설 IP `10.0.131.52`) → **인스턴스 상태 → 인스턴스 종료**.

터미널 B:

```bash
kubectl get nodes -w &
kubectl get pods -n devmart -o wide -w
```

> **🟢 확인: 확인 — 시간 순서 (예)**
>
> | 시각 | 손님 | Kubernetes | AWS |
> |---|---|---|---|
> | +0:00 | | | 인스턴스 종료 시작 |
> | +0:30 | products 일부 503 · **orders 503** | 노드 `NotReady` → 그 노드의 Pod 삭제 | |
> | +0:40 | products 200 (2c의 catalog가 받음) | catalog-api는 2c 노드에 새로 | |
> | +0:40 | orders 503 계속 | **db Pending** — `volume node affinity conflict` | |
> | +1:30 | | | 노드 그룹(ASG)이 **2a에** 새 인스턴스 |
> | +3:30 | | 새 노드 `Ready` → db가 그 노드로 · EBS **다시 붙음** | EBS 볼륨이 새 인스턴스에 attach |
> | +4:30 | **orders 202** | db Running · order-api 준비 | |

```bash
curl -s http://$NLB/api/orders | grep -o '"id":[0-9]*' | head -3
```

> **🟢 확인: 확인**
>
> 주문 번호가 기준선(7)보다 **크고 이어져** 있습니다 — 종료된 노드에 붙어 있던 **EBS 볼륨이 살아남아** 새 노드로 옮겨 붙었습니다. 노드의 **루트 디스크**는 사라졌지만(2일차 6교시), PVC의 볼륨은 노드와 **수명이 따로**입니다.

| 회복한 것 | 누가 | 걸린 시간 |
|---|---|---|
| catalog-api · order-api (상태 없음) | **Kubernetes** (다른 노드로) | 몇십 초 |
| 노드 수 2 | **AWS** (노드 그룹 = Auto Scaling 그룹) | 몇 분 |
| db (상태 있음) | 둘이 함께 — **같은 AZ**에 노드가 다시 생길 때까지 | 몇 분 |

> [!IMPORTANT]
> **운이 좋았던 부분**
>
> db가 돌아온 것은 노드 그룹이 AZ 균형을 맞추려고 **2a에** 새 노드를 띄웠기 때문입니다. 그 AZ 자체에 문제가 있다면? — 훈련 2.

## 훈련 2 · AZ 하나를 못 쓰게

AZ 장애를 흉내 내려고, db가 있는 AZ의 노드를 **스케줄 금지 + 비우기**합니다.

```bash
AZ=$(kubectl get pv $(kubectl get pvc db-data -n devmart -o jsonpath='{.spec.volumeName}') -o jsonpath='{.spec.nodeAffinity.required.nodeSelectorTerms[0].matchExpressions[0].values[0]}'); echo "db 볼륨의 AZ: $AZ"
for n in $(kubectl get nodes -l topology.kubernetes.io/zone=$AZ -o name); do
  kubectl cordon $n
  kubectl drain $n --ignore-daemonsets --delete-emptydir-data --timeout=2m
done
sleep 30
kubectl get pods -n devmart -o wide | grep -E "NAME|db-"
kubectl describe pod -n devmart -l app=db | grep -A3 Events: | tail -2
```

> **🟢 확인: 확인**
>
> ```text
> db 볼륨의 AZ: ap-northeast-2a
> node/ip-10-0-133-77… cordoned
> evicting pod devmart/db-6b7f8c9d5-…
> …
> NAME                  READY   STATUS    RESTARTS   AGE   IP       NODE
> db-6b7f8c9d5-z9x8w    0/1     Pending   0          35s   <none>   <none>
>   Warning  FailedScheduling  … 0/2 nodes are available: 1 node(s) had volume node affinity conflict, 1 node(s) were unschedulable. …
> ```
> - 2c에 **빈 노드가 있는데도** db는 Pending입니다. 데이터(EBS)가 2a에 있고, EBS는 다른 AZ의 노드에 **붙을 수 없기** 때문입니다(4일차 6교시).
> - 터미널 A: products는 200(catalog-api는 2c에서), **orders는 503** — 주문이 멈췄습니다.
> - 이 상태는 **기다려도 저절로 낫지 않습니다.** 2a가 돌아오거나, 데이터를 다른 AZ로 옮겨야(스냅샷 → 2c에 새 볼륨) 합니다.

되돌립니다.

```bash
for n in $(kubectl get nodes -l topology.kubernetes.io/zone=$AZ -o name); do kubectl uncordon $n; done
kubectl get pods -n devmart -l app=db -w
```

`Running`이 되면 `Ctrl+C`. 터미널 A의 orders가 202로 돌아옵니다. 터미널 A도 `Ctrl+C`.

![노드 하나가 죽으면 같은 AZ에 새 노드가 생겨 db가 같은 볼륨으로 돌아오지만, AZ 전체를 못 쓰면 db는 다른 AZ에서 뜰 수 없다](../../assets/week5/day5/w5d5-az.png)

> [!IMPORTANT]
> **상태 있는 것의 자리**
>
> | 선택지 | AZ 장애 때 | 비용 · 운영 |
> |---|---|---|
> | Pod + EBS (오늘) | **멈춘다** — 그 AZ가 돌아올 때까지 | 싸다 · 백업 · 업그레이드 모두 내 몫 |
> | Pod + 여러 AZ 복제 (StatefulSet + 복제 DB 오퍼레이터) | 다른 AZ의 복제본이 이어받는다 | 복잡하다 |
> | **RDS Multi-AZ** (관리형) | AWS가 다른 AZ의 대기 DB로 **자동 전환**(1~2분) | 비싸다 · 운영은 AWS가 |
>
> 3주차 1일차부터 "상태는 서비스 밖에"라고 했던 것의 끝이 여기입니다. 실무의 DevMart라면 db는 **RDS**, redis는 **ElastiCache**, 파일은 **S3**에 두고, Kubernetes에는 상태 없는 서비스만 둡니다. 그러면 오늘의 훈련 2에서도 주문이 멈추지 않습니다.

## 장애 기록

3 · 4주차의 장애 보고서 틀(`~/devops-lab/k8s/w4d5/drills/incident-report-w4.md`)로 **훈련 2**를 한 장 씁니다. "다음에는" 칸에 무엇을 적을지가 오늘의 핵심입니다.

> **❓ 오해 — 여러 AZ에 노드를 두면 고가용성이다**
>
> 노드가 여러 AZ에 있어도, **데이터가 한 AZ에 있으면** 그 데이터에 기대는 서비스는 한 AZ짜리입니다. 고가용성은 가장 약한 고리 — 대개 상태 있는 것 — 가 정합니다. 오늘 2c의 노드는 멀쩡했지만 주문은 멈췄습니다.

> **🎓 학술 노트 — CAP와 가용 영역**
>
> Brewer의 CAP 추측(PODC 2000 기조연설; Gilbert & Lynch 2002 증명)은 네트워크가 갈라졌을 때(P) **일관성(C)과 가용성(A)** 중 하나를 포기해야 한다고 말합니다. AZ 장애는 실제로 일어나는 '갈라짐'입니다. RDS Multi-AZ는 **동기 복제**로 일관성을 지키고 전환 동안 잠깐 가용성을 잃는 쪽을, 여러 리전의 비동기 복제는 가용성을 지키고 최근 쓰기 일부를 잃을 수 있는 쪽을 택합니다. 오늘의 Pod + EBS는 갈라진 쪽의 데이터를 쓸 수 없어 **가용성을 잃은** 경우입니다.

> **📈 트렌드 2026 — 장애 주입을 클라우드에서**
>
> AWS **Fault Injection Service**는 "이 AZ의 네트워크를 끊어라", "EKS 노드 그룹의 30%를 종료하라" 같은 실험을 안전장치(멈춤 조건 · 대상 태그)와 함께 제공하고, AWS는 **AZ 장애 대비 훈련**을 Well-Architected의 신뢰성 기둥에서 권합니다. 오늘 손으로 한 두 훈련이 그 실험의 원형입니다(4주차 4일차의 카오스 공학).

> **✅ 확인 문제**
>
> 1. 노드를 종료했을 때 상태 없는 서비스와 db가 회복한 시간이 달랐던 이유는?
> 2. 종료된 노드의 데이터 중 사라진 것과 살아남은 것은?
> 3. 2c 노드가 비어 있는데 db가 Pending이었던 이유는?
> 4. 훈련 2에서도 주문이 멈추지 않게 하려면?
>
> <details><summary>정답</summary>
>
> 1. 상태 없는 것은 아무 노드에서나 다시 뜨지만, db는 볼륨이 있는 AZ에 노드가 다시 생길 때까지 기다려야 했다
> 2. 루트 디스크는 사라지고, PVC의 EBS 볼륨은 살아남아 새 노드에 다시 붙었다
> 3. EBS 볼륨이 2a에 있어 다른 AZ 노드에 붙을 수 없기 때문 (volume node affinity conflict)
> 4. db를 여러 AZ에 복제되는 저장소(RDS Multi-AZ 등)로 옮긴다
>
> </details>

## 참고 문헌

- AWS Docs. *Amazon RDS Multi-AZ deployments*, *AWS Fault Injection Service — EKS actions*. docs.aws.amazon.com
- AWS. *Well-Architected Framework — Reliability Pillar: Use fault isolation to protect your workload*. docs.aws.amazon.com/wellarchitected
- Gilbert, S. & Lynch, N. (2002). *Brewer's Conjecture and the Feasibility of Consistent, Available, Partition-Tolerant Web Services*. ACM SIGACT News 33(2).
