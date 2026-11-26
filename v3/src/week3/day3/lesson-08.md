# 8교시 · API 서버와 etcd 들여다보기 — 클러스터의 기억과 감시

!!! goal "이번 시간에 할 일"
    - kubectl 없이 `curl`로 apiserver를 불러, **kubectl = REST API 클라이언트**임을 확인합니다.
    - apiserver가 변화를 **실시간으로 흘려보내는 감시(watch)**를 눈으로 보고, 컨트롤러가 어떻게 일을 알아채는지 이해합니다.
    - etcd 안에 Pod와 Secret이 **어떤 열쇠로, 어떤 모양으로** 저장되는지 직접 꺼내 봅니다.
    - 2교시에 말로만 들은 "Secret은 기본적으로 암호화가 아니다"를 **증거로** 확인합니다.
    - `resourceVersion`으로 두 사람이 동시에 고칠 때 생기는 충돌을 Kubernetes가 어떻게 막는지 봅니다.

!!! warn "오늘은 들여다보기만 합니다"
    etcd에 **직접 쓰는 것은 절대 하지 않습니다.** etcd에 쓰는 것은 apiserver뿐이어야 합니다(2교시). 오늘은 읽기 명령만 씁니다. 회사 클러스터에서 etcd에 접속할 일은 백업 · 복구 말고는 거의 없습니다.

## 실습 14 · curl로 apiserver 부르기

### 단계 1 — 통로 열기

```bash
cd ~/devops-lab/k8s
kubectl proxy --port 8001 > /tmp/proxy.log 2>&1 &
sleep 1
curl -s http://localhost:8001/version | jq '.gitVersion'
```

- `kubectl proxy` : 내 kubeconfig의 열쇠로 apiserver에 **대신 로그인**해 주는 작은 중계기를 노트북의 8001번에 띄운다. 그래서 `curl`에 인증서를 붙일 필요가 없다
- 맨 끝 `&` : 터미널을 붙잡지 않고 **뒤에서** 실행

!!! check "이렇게 나오면 성공"
    ```text
    "v1.37.0"
    ```

### 단계 2 — 같은 질문, 두 가지 방법

```bash
kubectl get pods -n kube-system -o name | head -3
curl -s http://localhost:8001/api/v1/namespaces/kube-system/pods | jq -r '.items[].metadata.name' | head -3
```

두 줄의 결과가 같습니다. `kubectl get pods -n kube-system`은 `GET /api/v1/namespaces/kube-system/pods`입니다. 7교시에 `-v=6`으로 본 그 주소를 이번에는 직접 불렀습니다.

| kubectl | HTTP |
|---|---|
| `get pods -n X` | `GET /api/v1/namespaces/X/pods` |
| `get deployment Y -n X` | `GET /apis/apps/v1/namespaces/X/deployments/Y` |
| `apply -f …` | `PATCH …` (없으면 `POST`) |
| `delete pod Z` | `DELETE /api/v1/namespaces/default/pods/Z` |

!!! tip "주소에 `/api`와 `/apis`가 섞인 이유"
    Pod · Service 같은 **처음부터 있던** 리소스는 `/api/v1`(코어 그룹)에, Deployment 같은 나중에 생긴 리소스는 `/apis/<그룹>/<버전>`에 있습니다. 4교시 매니페스트의 `apiVersion: apps/v1`이 바로 그 `<그룹>/<버전>`입니다. `kubectl api-versions`로 이 클러스터의 그룹 목록을 볼 수 있습니다.

## 실습 15 · 감시(watch) — 변화가 흘러온다

!!! lab "실습 목표"
    apiserver에 "default 네임스페이스의 Pod가 바뀌면 알려 줘"라고 걸어 두고, 다른 터미널에서 Pod를 만들고 지우며 알림이 오는 것을 봅니다.

**터미널 A** — 감시를 겁니다.

```bash
curl -sN "http://localhost:8001/api/v1/namespaces/default/pods?watch=true" \
  | jq -r --unbuffered '"\(.type)\t\(.object.metadata.name)\t\(.object.status.phase // "-")"'
```

- `?watch=true` : 응답을 끝내지 않고 **바뀔 때마다 한 줄씩** 계속 보내 달라
- `curl -N` : 받는 즉시 보여 줌(버퍼에 모으지 않음)

**터미널 B** — Pod 하나를 만들고 지웁니다.

```bash
kubectl run watch-me --image=nginx:1.30-alpine
kubectl wait --for=condition=Ready pod/watch-me --timeout=60s
kubectl delete pod watch-me
```

!!! check "터미널 A에 이렇게 흘러옵니다"
    ```text
    ADDED      watch-me   Pending
    MODIFIED   watch-me   Pending
    MODIFIED   watch-me   Pending
    MODIFIED   watch-me   Running
    MODIFIED   watch-me   Running
    MODIFIED   watch-me   Running
    DELETED    watch-me   Running
    ```
    줄 수는 조금 다를 수 있습니다. **Pending → Running**은 4교시의 그림 그대로입니다. 스케줄러가 노드를 적고(`MODIFIED`), kubelet이 컨테이너를 띄워 상태를 적을 때마다(`MODIFIED`) 알림이 왔습니다.

!!! key "컨트롤러는 이렇게 일을 안다"
    스케줄러 · 컨트롤러 매니저 · kubelet은 apiserver에 **오늘 터미널 A처럼 감시를 걸어 두고** 기다립니다. "자리 없는 Pod가 생겼다"는 알림이 오면 스케줄러가 움직이고, "내 노드에 배정된 Pod가 생겼다"는 알림이 오면 kubelet이 움직입니다. 서로 직접 부르지 않고 **apiserver를 게시판처럼** 씁니다. 그래서 부품 하나가 잠깐 멈췄다 돌아와도, 다시 목록을 읽고(list) 감시를 걸면(watch) 놓친 것 없이 따라잡습니다(4교시 reconcile).

터미널 A는 `Ctrl` + `C`로 멈춥니다.

## 실습 16 · etcd 안을 들여다보기

### 단계 1 — etcd에 묻는 준비

etcd도 정적 Pod로 떠 있습니다(7교시). 그 Pod 안의 `etcdctl`을 빌려 씁니다. etcd는 인증서로만 대화하므로 열쇠 세 개를 붙입니다.

```bash
ETCD="kubectl -n kube-system exec etcd-devmart-control-plane -- etcdctl \
  --endpoints=https://127.0.0.1:2379 \
  --cacert=/etc/kubernetes/pki/etcd/ca.crt \
  --cert=/etc/kubernetes/pki/etcd/server.crt \
  --key=/etc/kubernetes/pki/etcd/server.key"
$ETCD endpoint status -w table
```

!!! check "이렇게 나오면 성공"
    ```text
    ENDPOINT                 VERSION   DB SIZE   IN USE   IS LEADER
    https://127.0.0.1:2379   3.6.x     4.1 MB    2.3 MB   true
    ```
    실제 표에는 테두리와 칸이 더 있습니다. 클러스터 **전체의 기억**이 몇 MB 파일 하나에 들어 있습니다. kind는 컨트롤 플레인이 1대라 etcd도 1대입니다(운영은 3대 · 5대).

### 단계 2 — 열쇠 이름 보기

```bash
$ETCD get /registry --prefix --keys-only | grep -v '^$' | awk -F/ '{print $3}' | sort | uniq -c | sort -rn | head -8
$ETCD get /registry/pods/kube-system --prefix --keys-only | grep -v '^$' | head -3
```

!!! check "보이는 것 (예)"
    ```text
         70 events
         45 clusterroles
         …
          9 pods
    /registry/pods/kube-system/coredns-…
    /registry/pods/kube-system/etcd-devmart-control-plane
    /registry/pods/kube-system/kindnet-…
    ```
    모든 것이 `/registry/<종류>/<네임스페이스>/<이름>` 열쇠 아래 있습니다. 1주차 2일차 8교시의 `cut | sort | uniq -c`가 여기서도 쓰였습니다.

### 단계 3 — Secret은 정말 그대로 있나

```bash
kubectl create secret generic etcd-demo --from-literal=password='devmart-demo-pw-1234'
kubectl get secret etcd-demo -o jsonpath='{.data.password}'; echo
$ETCD get /registry/secrets/default/etcd-demo --print-value-only | grep -a -o 'devmart-demo-pw-[0-9]*'
```

!!! check "증거"
    ```text
    ZGV2bWFydC1kZW1vLXB3LTEyMzQ=
    devmart-demo-pw-1234
    ```
    `kubectl`이 보여 준 값은 base64이고, **etcd에 저장된 값은 원문 그대로** 들어 있습니다(Kubernetes의 이진 형식 안에). etcd 파일이나 그 **백업 파일을 손에 넣은 사람은 모든 Secret을 읽을 수 있다**는 뜻입니다. 그래서:

    | 대책 | 어디서 |
    |---|---|
    | etcd **저장 시 암호화**(EncryptionConfiguration, KMS) | 운영 클러스터 필수. EKS는 기본으로 켜져 있다(5주차) |
    | etcd 백업 파일도 Secret처럼 보관 | 2주차 4일차 8교시 — 백업은 고객 데이터 |
    | Secret 읽기 권한(RBAC)을 좁게 | 4주차 5일차 |

```bash
kubectl delete secret etcd-demo
```

### 단계 4 — 동시에 고치면 누가 이기나 — `resourceVersion`

```bash
kubectl create configmap rv-demo --from-literal=color=blue
kubectl get configmap rv-demo -o yaml > /tmp/rv-a.yaml          # 사람 A가 받아 둔 사본
kubectl patch configmap rv-demo -p '{"data":{"color":"green"}}'  # 그사이 사람 B가 고침
sed -i 's/color: blue/color: red/' /tmp/rv-a.yaml                # A가 옛 사본을 고쳐서
kubectl replace -f /tmp/rv-a.yaml                                # 덮어쓰려 하면
```

!!! check "충돌로 거절됩니다"
    ```text
    Error from server (Conflict): error when replacing "/tmp/rv-a.yaml": Operation cannot be fulfilled
    on configmaps "rv-demo": the object has been modified; please apply your changes to the latest version and try again
    ```
    A의 사본에는 받을 때의 `resourceVersion`이 적혀 있고, B가 고치면서 그 번호가 올라갔습니다. apiserver는 **번호가 다르면 거절**해서, B의 변경을 A가 모르고 덮어쓰는 사고를 막습니다. (Mac은 `sed -i ''`)

```bash
kubectl get configmap rv-demo -o jsonpath='{.data.color} {.metadata.resourceVersion}'; echo
kubectl delete configmap rv-demo
```

!!! cleanup "정리"
    ```bash
    kill %1 2>/dev/null || pkill -f "kubectl proxy --port 8001"
    kubectl get pods,secrets,configmaps -n default
    ```
    `default`에 오늘 만든 것이 남아 있지 않으면 됩니다. 클러스터는 **내일도 쓰므로 그대로** 둡니다.

!!! academic "학술 노트 — 게시판 하나를 모두가 본다 (Omega, 2013)"
    구글은 Borg(1주차 2일차) 다음 세대 연구 시스템 **Omega**를 EuroSys 2013 논문으로 발표했습니다(Schwarzkopf 외). Borg는 한가운데의 스케줄러 하나가 모든 결정을 내렸는데, 일의 종류가 많아지자 그 한 곳이 병목이 됐습니다. Omega는 **클러스터 상태 전체를 공유 장부 하나**에 두고, 여러 스케줄러가 각자 사본을 보고 결정한 뒤 장부에 쓰되, **그사이 누가 먼저 바꿨으면 거절하고 다시 시도**하게 했습니다(낙관적 동시성 제어). 오늘 본 **apiserver + etcd(공유 장부), watch(변화 알림), resourceVersion 충돌(낙관적 동시성)**이 그 설계를 Kubernetes가 물려받은 모습입니다.

    - Schwarzkopf, M., Konwinski, A., Abd-El-Malek, M., & Wilkes, J. (2013). Omega: flexible, scalable schedulers for large compute clusters. *EuroSys '13*.

!!! trend "트렌드 — etcd를 넘어서는 큰 클러스터"
    etcd는 수천 노드까지는 잘 버티지만, 그 이상에서는 장부 하나가 한계가 됩니다. 그래서 관리형 서비스는 etcd의 **속을 바꾸고** 있습니다. AWS는 2025년 EKS에서 **노드 10만 대** 클러스터를 지원한다고 발표하면서, etcd의 합의 부분을 내부 분산 기록 시스템으로 옮기고 데이터는 메모리 위에 두는 방식으로 바꿨다고 설명했습니다. 반대쪽 끝에서는 k3s 같은 작은 배포판이 etcd 대신 SQLite · PostgreSQL을 쓰기도 합니다(kine). **apiserver의 API는 그대로이고 뒤의 장부만 바뀐다** — 오늘 curl로 본 그 API가 표준인 이유입니다.

## 정리

- kubectl은 apiserver의 **REST API**를 부르는 클라이언트입니다(`kubectl proxy` + `curl`로 확인).
- `?watch=true`로 apiserver는 **변화를 흘려보냅니다.** 모든 컨트롤러는 이 list-watch로 일을 압니다.
- etcd에는 모든 것이 `/registry/<종류>/<네임스페이스>/<이름>`으로 저장됩니다. **Secret도 원문으로** — 저장 시 암호화와 백업 보호가 필요합니다.
- `resourceVersion`이 다르면 apiserver가 **거절**해서, 동시에 고칠 때의 덮어쓰기 사고를 막습니다.

!!! quiz "확인 문제"
    1. `kubectl get deployments -n shop`은 어떤 HTTP 요청인가요?
    2. 스케줄러는 "자리 없는 Pod가 생겼다"는 것을 어떻게 아나요?
    3. etcd 백업 파일을 Secret처럼 보관해야 하는 이유는?
    4. `Operation cannot be fulfilled … the object has been modified`는 무슨 뜻이고, 어떻게 하나요?
    5. etcd에 직접 값을 써서 고치면 안 되는 이유는?

    ??? answer "정답"
        1. `GET /apis/apps/v1/namespaces/shop/deployments`
        2. apiserver에 Pod 감시(watch)를 걸어 두고, `nodeName`이 비어 있는 Pod의 알림을 받습니다.
        3. 저장 시 암호화를 켜지 않았다면 모든 Secret이 원문으로 들어 있기 때문입니다.
        4. 내가 받아 둔 뒤 누군가 먼저 고쳐 `resourceVersion`이 바뀌었다는 뜻입니다. 최신을 다시 받아 내 변경을 다시 적용합니다.
        5. apiserver의 검사(문법 · 권한 · 정책)와 감시 알림을 모두 건너뛰어, 컨트롤러가 변화를 모르고 클러스터가 어긋나기 때문입니다.

!!! diary "오늘의 배움일기 — 수업 뒤 각자"
    - Kubernetes를 친구에게 **한 문장**으로 설명한다면
    - 컨트롤 플레인 네 부품 중 하나가 멈춘다면, 내가 가장 먼저 눈치챌 증상은 무엇일까 (부품 하나를 골라)
    - 명령형과 선언형 — 1~2주차에 내가 한 일 중 '사실은 선언형이었던 것' 하나
    - 실험 1 · 2 · 3에서 **고친 주체**를 각각 한 단어로
    - DevMart에 Kubernetes가 정말 필요한지, 5교시 판단표를 바탕으로 내 의견
    - 내일 전에 궁금한 것: Pod의 IP가 매번 바뀐다면, `order-api`는 `catalog-api`를 **어떻게** 찾아갈까?

## 참고 문헌

- Schwarzkopf, M., Konwinski, A., Abd-El-Malek, M., & Wilkes, J. (2013). Omega: flexible, scalable schedulers for large compute clusters. *Proceedings of EuroSys '13*.
- Kubernetes Documentation. *The Kubernetes API*; *API Concepts — Efficient detection of changes (watch), Resource versions*; *Encrypting Confidential Data at Rest*.
- etcd Documentation. *etcdctl — get, endpoint status*. etcd.io/docs
- Kubernetes Documentation. *kubectl proxy*.
- AWS Containers Blog (2025). *Amazon EKS enables ultra scale AI/ML workloads with support for 100K nodes per cluster*.
