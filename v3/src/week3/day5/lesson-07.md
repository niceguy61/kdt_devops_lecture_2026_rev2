# 7교시 · HPA — 부하에 따라 늘어나고 줄어들기

!!! goal "이번 시간에 할 일"
    - Pod의 CPU · 메모리 사용량을 모으는 **metrics-server**를 설치하고 `kubectl top`으로 봅니다.
    - **HorizontalPodAutoscaler(HPA)**로 `catalog-api`가 바쁘면 늘고, 한가하면 줄게 합니다.
    - HPA가 **4교시의 requests를 기준으로** 계산한다는 것을 확인합니다.
    - 부하를 걸어 늘어나는 것, 멈춰서 **천천히** 줄어드는 것을 지켜봅니다.
    - `replicas`를 매니페스트에 적어 둔 채 `apply`하면 HPA와 **싸운다**는 것을 보고, 피하는 법을 압니다.

!!! key "4일차의 `replicas: 3`은 사람이 정한 숫자였다"
    4일차부터 `replicas`를 손으로 정했습니다. 그런데 DevMart의 손님은 낮에 많고 새벽에 적습니다. 낮 기준으로 정하면 새벽에 돈이 새고, 새벽 기준으로 정하면 낮에 느려집니다. HPA는 **숫자 대신 목표**("CPU를 평균 50%쯤 쓰게")를 적으면, 컨트롤러가 그 목표에 맞게 `replicas`를 바꿔 줍니다. 3일차 4교시의 reconcile이 **사람이 정한 값**이 아니라 **측정한 값**을 보고 돈다는 점이 다릅니다.

## 실습 18 · metrics-server 설치와 `kubectl top`

### 단계 1 — 설치

```bash
cd ~/devops-lab/k8s/day5
kubectl apply -f https://github.com/kubernetes-sigs/metrics-server/releases/download/v0.9.1/components.yaml
kubectl -n kube-system patch deployment metrics-server --type=json \
  -p '[{"op":"add","path":"/spec/template/spec/containers/0/args/-","value":"--kubelet-insecure-tls"}]'
kubectl -n kube-system rollout status deployment metrics-server
```

- metrics-server는 각 노드의 kubelet에게 "지금 Pod들이 CPU · 메모리를 얼마나 쓰나"를 **15초마다** 물어 모아 둡니다
- `--kubelet-insecure-tls` : kind의 kubelet 인증서는 정식 인증 기관이 서명한 것이 아니라서, 실습 클러스터에서만 검사를 끕니다. **운영(EKS)에서는 쓰지 않습니다** — 5주차 4일차의 EKS 애드온은 이 옵션 없이 동작합니다

!!! warn "다른 사람의 매니페스트를 URL로 바로 적용한다는 것"
    `kubectl apply -f https://…`는 인터넷에 있는 YAML을 **읽지 않고** 내 클러스터에 넣는 일입니다. 오늘은 Kubernetes 공식 프로젝트(SIG Instrumentation)의 **버전을 고정한** 릴리스 파일이라 씁니다. 처음 보는 주소라면 `curl -sL 주소 | less`로 먼저 읽습니다(2주차 1일차 "받아서, 읽고, 실행").

### 단계 2 — 숫자 보기

1분쯤 기다린 뒤:

```bash
kubectl top nodes
kubectl top pods -n devmart
```

!!! check "이렇게 나오면 성공 (숫자는 다름)"
    ```text
    NAME                    CPU(cores)   CPU(%)   MEMORY(bytes)   MEMORY(%)
    devmart-control-plane   182m         2%       812Mi           10%
    devmart-worker          64m          0%       402Mi           5%
    …
    NAME                            CPU(cores)   MEMORY(bytes)
    catalog-api-7d9c…-4xk2p         2m           48Mi
    catalog-api-7d9c…-9qz7w         2m           47Mi
    db-6b8f…-x2lzq                  6m           38Mi
    …
    ```
    `m`은 1000분의 1 코어입니다. `catalog-api`는 지금 거의 놀고 있습니다(2m). `error: Metrics API not available`이 나오면 아직 첫 수집 전이니 30초 더 기다립니다.

## 실습 19 · HPA 걸고 부하 주기

### 단계 1 — HPA 만들기

```bash
code hpa-catalog.yaml
```

```yaml
apiVersion: autoscaling/v2
kind: HorizontalPodAutoscaler
metadata:
  name: catalog-api
  namespace: devmart
spec:
  scaleTargetRef:                 # 무엇을 늘리고 줄이나
    apiVersion: apps/v1
    kind: Deployment
    name: catalog-api
  minReplicas: 2                  # 아무리 한가해도 2개 (한 대가 죽어도 버티게)
  maxReplicas: 6                  # 아무리 바빠도 6개 (노트북과 지갑을 지킨다)
  metrics:
    - type: Resource
      resource:
        name: cpu
        target:
          type: Utilization
          averageUtilization: 50  # requests의 50%를 목표로
  behavior:
    scaleDown:
      stabilizationWindowSeconds: 60   # 실습용: 기본 300초 → 60초
```

```bash
kubectl apply -f hpa-catalog.yaml
kubectl get hpa -n devmart
```

!!! check "이렇게 나오면 성공"
    ```text
    NAME          REFERENCE                TARGETS       MINPODS   MAXPODS   REPLICAS   AGE
    catalog-api   Deployment/catalog-api   cpu: 4%/50%   2         6         2          20s
    ```
    `4%/50%` — **지금 / 목표**입니다. 4%는 `requests.cpu: 50m`의 4%(2m)라는 뜻입니다. 4교시에 requests를 적지 않았다면 여기에 `<unknown>`이 뜨고 HPA는 아무것도 하지 못합니다.

!!! key "HPA의 계산은 한 줄"
    **원하는 개수 = 올림( 지금 개수 × 지금 사용률 ÷ 목표 사용률 )**

    지금 2개가 평균 150%를 쓰면 → 2 × 150 ÷ 50 = **6개**. 평균 30%로 떨어지면 → 6 × 30 ÷ 50 = 3.6 → **4개**. 목표와 비슷하면(기본 ±10%) 바꾸지 않습니다 — 숫자가 조금 흔들릴 때마다 Pod를 늘렸다 줄였다 하지 않게.

### 단계 2 — 지켜볼 창

**터미널 A**:

```bash
kubectl get hpa -n devmart -w
```

### 단계 3 — 부하 걸기

**터미널 B** — 클러스터 안에서 상품 목록을 쉬지 않고 부르는 Pod 세 개를 띄웁니다.

```bash
kubectl create deployment load -n devmart --image=busybox:1.37 --replicas=3 -- \
  sh -c 'while true; do wget -q -O /dev/null http://catalog-api:8000/api/products; done'
```

!!! check "1~3분 안에 터미널 A가 이렇게 바뀝니다"
    ```text
    catalog-api   Deployment/catalog-api   cpu: 4%/50%     2   6   2
    catalog-api   Deployment/catalog-api   cpu: 186%/50%   2   6   2
    catalog-api   Deployment/catalog-api   cpu: 186%/50%   2   6   6
    catalog-api   Deployment/catalog-api   cpu: 71%/50%    2   6   6
    ```
    사용률이 목표를 넘자 **최대 6개**까지 늘었고, 일을 나눠 가지자 사용률이 내려왔습니다. `kubectl get pods -n devmart -l app=catalog-api`로 새 Pod들을 확인합니다. 새 Pod는 readiness probe(3교시)를 통과해야 Service에 들어갑니다.

!!! tip "6개로도 목표를 못 맞추면"
    `maxReplicas`에 막혀 사용률이 계속 높게 남습니다. 이때는 최대치를 올리거나, **노드가 모자라 Pending**이 생기면 노드를 늘려야 합니다. Pod를 늘리는 것은 HPA, **노드**를 늘리는 것은 클러스터 오토스케일러 · Karpenter(5주차 4일차)의 일입니다.

### 단계 4 — 부하 멈추기와 천천히 줄기

```bash
kubectl delete deployment load -n devmart
```

!!! check "터미널 A — 1분쯤 지나서"
    ```text
    catalog-api   Deployment/catalog-api   cpu: 3%/50%     2   6   6
    catalog-api   Deployment/catalog-api   cpu: 3%/50%     2   6   2
    ```
    사용률은 바로 떨어졌는데 **Pod는 1분을 기다렸다** 줄었습니다. `stabilizationWindowSeconds` 동안 "정말 한가해졌나"를 지켜본 것입니다. 기본값 5분은 잠깐 조용했다가 다시 몰리는 트래픽에 Pod를 줄였다 늘렸다 **출렁이지(flapping)** 않게 하려는 것입니다. **늘리기는 빠르게, 줄이기는 천천히**가 원칙입니다.

## 실습 20 · HPA와 `apply`가 싸운다

부하를 다시 걸어 6개로 늘려 둔 상태에서, 4교시처럼 매니페스트 전체를 다시 적용해 봅니다.

```bash
kubectl create deployment load -n devmart --image=busybox:1.37 --replicas=3 -- \
  sh -c 'while true; do wget -q -O /dev/null http://catalog-api:8000/api/products; done'
sleep 120
kubectl get deploy catalog-api -n devmart
kubectl apply -k devmart/ | grep catalog-api
kubectl get deploy catalog-api -n devmart
```

!!! check "이렇게 나옵니다"
    ```text
    catalog-api   6/6     6            6           …
    deployment.apps/catalog-api configured
    catalog-api   2/6     6            2           …
    ```
    매니페스트의 `replicas: 2`가 HPA가 늘린 **6을 2로 되돌렸습니다.** 잠시 뒤 HPA가 다시 6으로 늘리지만, 그사이 Pod 넷이 사라졌다 다시 생깁니다 — 손님이 가장 많을 때 배포했다면 장애입니다.

!!! key "HPA를 쓰면 `replicas`를 매니페스트에서 뺀다"
    개수를 정하는 주인은 **하나**여야 합니다. HPA가 붙은 Deployment는 매니페스트에서 `replicas:` 줄을 지우고, 개수는 HPA의 `minReplicas`/`maxReplicas`로만 정합니다. 4주차 3일차 GitOps에서 Argo CD의 자동 되돌리기(selfHeal)가 같은 이유로 HPA와 싸우는 장면을 다시 봅니다.

!!! cleanup "정리"
    ```bash
    kubectl delete deployment load -n devmart
    kubectl delete -f hpa-catalog.yaml
    kubectl apply -k devmart/          # replicas: 2로 돌아온다
    kubectl get deploy catalog-api -n devmart
    ```
    metrics-server는 **남겨 둡니다**(4주차에도 `kubectl top`을 씁니다). `hpa-catalog.yaml`은 `kustomization.yaml`에 넣지 **않습니다** — 4주차 매니페스트는 강의 저장소에서 새로 받고, HPA는 그 매니페스트에 맞춰 다시 붙입니다.

!!! academic "학술 노트 — 자동 확장은 피드백 제어다"
    HPA의 한 줄 공식은 제어 공학의 **피드백 루프**입니다. 목표(set point)와 측정값의 차이를 보고 조절 장치(replicas)를 움직입니다. 제어 이론은 이런 루프가 **너무 민감하면 출렁이고(진동), 너무 둔하면 늦는다**는 것을 오래전부터 다뤄 왔습니다. 헬러스타인(Hellerstein) 등은 『Feedback Control of Computing Systems』(2004)에서 웹 서버 · DB의 자원 조절을 제어 이론으로 분석하며, 측정의 **지연**(metrics-server의 15초 수집, Pod가 준비되는 시간)이 클수록 루프가 불안정해진다고 보였습니다. HPA의 **허용 범위(±10%)**와 **줄이기 안정화 창(5분)**은 바로 이 진동을 막는 장치입니다.

    - Hellerstein, J. L., Diao, Y., Parekh, S., & Tilbury, D. M. (2004). *Feedback Control of Computing Systems*. Wiley-IEEE Press.

!!! trend "트렌드 — CPU 말고 '일의 양'으로 늘리기"
    CPU 사용률은 늦게 반응하는 지표입니다. 큐에 주문이 쌓이는 `order-worker`라면 **큐의 길이**로 늘리는 게 더 정확합니다. **KEDA**(CNCF 졸업 프로젝트)는 Redis 큐 길이, Kafka 지연, 초당 요청 수 같은 **이벤트 지표**로 HPA를 움직이고, 일이 없으면 **0개까지** 줄입니다. Kubernetes 자체도 Pod를 다시 만들지 않고 CPU · 메모리를 바꾸는 **제자리 크기 조정(in-place resize)**을 정식 기능으로 만들어, "개수(가로)"와 "크기(세로)"를 함께 조절하는 방향으로 가고 있습니다.

## 정리

- **metrics-server**가 사용량을 모으고, `kubectl top`과 HPA가 그것을 씁니다.
- HPA는 **requests 대비 사용률**로 계산합니다. requests가 없으면 `<unknown>` — 4교시가 전제입니다.
- 원하는 개수 = 올림(지금 개수 × 지금 ÷ 목표). **늘리기는 빠르게, 줄이기는 천천히**(안정화 창).
- HPA를 붙이면 매니페스트에서 `replicas`를 뺍니다. 개수의 주인은 하나.
- Pod를 늘리는 것은 HPA, 노드를 늘리는 것은 클러스터 오토스케일러 · Karpenter.

!!! quiz "확인 문제"
    1. `kubectl get hpa`의 TARGETS가 `<unknown>/50%`입니다. 가장 먼저 확인할 두 가지는?
    2. Pod 3개가 평균 CPU 100%를 쓰고 목표가 50%입니다. HPA는 몇 개로 늘리나요? (최대치는 충분)
    3. 부하가 끝났는데 Pod가 바로 줄지 않습니다. 고장인가요?
    4. HPA를 붙인 뒤 `kubectl apply -k`를 할 때마다 Pod가 줄었다 늘어납니다. 원인과 해결은?
    5. 큐에 쌓인 주문 수로 `order-worker`를 늘리고 싶습니다. 어떤 도구를 찾아보나요?

    ??? answer "정답"
        1. metrics-server가 동작하는지(`kubectl top pods`), 대상 컨테이너에 `requests.cpu`가 있는지
        2. 올림(3 × 100 ÷ 50) = 6개
        3. 아닙니다. 줄이기 안정화 창(기본 5분, 오늘 60초) 동안 기다리는 것입니다.
        4. 매니페스트의 `replicas`가 HPA가 정한 개수를 덮어씁니다. 매니페스트에서 `replicas`를 지웁니다.
        5. KEDA (이벤트 기반 오토스케일링)

## 참고 문헌

- Hellerstein, J. L., Diao, Y., Parekh, S., & Tilbury, D. M. (2004). *Feedback Control of Computing Systems*. Wiley-IEEE Press.
- Kubernetes Documentation. *Horizontal Pod Autoscaling* — algorithm details, stabilization window; *HorizontalPodAutoscaler Walkthrough*; *Resize CPU and Memory Resources assigned to Containers*.
- Kubernetes SIGs. *metrics-server* v0.9 — Requirements, `--kubelet-insecure-tls`. github.com/kubernetes-sigs/metrics-server
- KEDA. *Kubernetes Event-driven Autoscaling*. keda.sh
