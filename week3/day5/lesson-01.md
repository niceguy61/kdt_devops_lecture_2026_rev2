<sub>[🏠 과정 목차](../../README.md) › [3주차](../README.md) › [5일차](README.md) › 1/7교시</sub>

# 1교시 · 4일차 요약 + Namespace

> [!NOTE]
> **이번 시간에 할 일**
>
> - 어제 만든 catalog-api를 정리하며 4일차를 손으로 복습합니다.
> - 오늘 쓸 **세 이미지**의 SHA 태그를 확인하고 실습 파일을 준비합니다.
> - **Namespace**가 무엇이고 무엇이 **아닌지** 이해하고, `devmart` 네임스페이스를 만듭니다.

## 4일차 요약 — 정리하며 복습

```bash
kubectl get deployment,replicaset,pod,service -l app=catalog-api
kubectl get service
```

> **🟢 확인: 보이는 것 (요약)**
>
> ```text
> deployment.apps/catalog-api   3/3   3   3   1d
> replicaset.apps/catalog-api-6b8f7c9d5c   0   0   0   1d
> replicaset.apps/catalog-api-7d9c4b8f6a   3   3   3   1d
> pod/catalog-api-7d9c4b8f6a-…   1/1   Running   0   1d
> ...
> NAME              TYPE        CLUSTER-IP     EXTERNAL-IP   PORT(S)        AGE
> catalog-api       ClusterIP   10.96.142.87   <none>        80/TCP         1d
> catalog-api-web   NodePort    10.96.77.201   <none>        80:30080/TCP   1d
> kubernetes        ClusterIP   10.96.0.1      <none>        443/TCP        2d
> ```

짝에게 한 줄씩 설명해 봅니다. 막히는 줄이 있으면 4일차 해당 교시를 다시 봅니다.

| 보이는 것 | 설명할 것 | 4일차 |
|---|---|---|
| ReplicaSet 두 개, 하나는 0 | 롤링 업데이트가 남긴 옛 ReplicaSet — 되돌리기의 재료 | 7교시 |
| Pod 이름의 가운데 해시 | 템플릿 해시 — 템플릿이 바뀌면 새 ReplicaSet | 4교시 |
| `catalog-api` ClusterIP | 바뀌지 않는 이름과 가상 IP, 셀렉터로 Pod를 찾는다 | 6교시 |
| `80:30080/TCP` | NodePort — kind의 포트 통로로 `localhost:30080` | 6교시 |

오늘 DevMart 전체가 **30080**을 씁니다. 어제 것을 지웁니다. 파일로 만든 것은 파일로 지웁니다.

```bash
cd ~/devops-lab/k8s/day4
kubectl delete -f service-nodeport.yaml -f service.yaml -f deployment.yaml
kubectl get all
```

> **🟢 확인: 보이는 것**
>
> ```text
> service "catalog-api-web" deleted
> service "catalog-api" deleted
> deployment.apps "catalog-api" deleted
> NAME                 TYPE        CLUSTER-IP   EXTERNAL-IP   PORT(S)   AGE
> service/kubernetes   ClusterIP   10.96.0.1    <none>        443/TCP   2d
> ```
> Deployment 하나를 지웠는데 ReplicaSet과 Pod도 함께 사라졌습니다 — 4일차 4교시의 **주인-딸린 관계**(가비지 컬렉션)입니다.

> [!TIP]
> **`kubectl get all`의 'all'은 모두가 아니다**
>
> `all`은 Pod · Service · Deployment · ReplicaSet 등 **자주 쓰는 몇 종류**만 뜻합니다. ConfigMap · Secret · PVC는 빠집니다. 오늘 그것들을 만들 때는 따로 `kubectl get configmap,secret,pvc`로 봅니다.

## 실습 1 · 세 이미지 확인과 파일 준비

### 단계 1 — 세 이미지의 태그

```bash
GH=$(gh api user --jq .login | tr 'A-Z' 'a-z')
for s in catalog-api order-api order-worker; do
  printf '%-14s ' $s
  gh api /user/packages/container/devmart-$s/versions --jq '.[0].metadata.container.tags'
done
```

> **🟢 확인: 이렇게 나오면 성공**
>
> ```text
> catalog-api    ["sha-7f3c2e1","latest"]
> order-api      ["sha-7f3c2e1","latest"]
> order-worker   ["sha-7f3c2e1","latest"]
> ```
> 세 SHA가 **같아야** 합니다. 2일차 CI의 build 잡은 main에 병합될 때 세 서비스를 **같은 커밋으로** 한꺼번에 빌드했습니다.

> **🛠️ 막혔다면: SHA가 서로 다르다**
>
> 2일차 이후 한 서비스만 고쳐 다시 병합했다면, 그 서비스만 새 SHA가 있을 수 있습니다. 문제는 아닙니다. 서비스마다 자기 최신 SHA를 쓰면 됩니다 — 단계 3의 `sed`를 서비스별로 나눠 합니다. MSA에서 **서비스마다 버전이 따로 가는 것**이 오히려 정상입니다(1일차 1교시).

### 단계 2 — 실습 파일 복사

```bash
mkdir -p ~/devops-lab/k8s/day5
cp -r ~/course/labs/week3/day5/* ~/devops-lab/k8s/day5/
cd ~/devops-lab/k8s/day5 && ls
ls devmart steps
```

> **🟢 확인: 보이는 것**
>
> ```text
> README.md  break.sh  devmart  fix.sh  incident-report-template.md  retro-week3.md  steps
> devmart:
> catalog-api.yaml  config.yaml  db.yaml  files  kustomization.yaml  namespace.yaml  order-api.yaml  order-worker.yaml  redis.yaml  web.yaml
>
> steps:
> catalog-v1.yaml  catalog-v2.yaml  oom.yaml
> ```

### 단계 3 — 이미지 주소 채우기

```bash
SHA=sha-7f3c2e1      # 단계 1의 내 값
grep -rl YOUR_ID . | xargs sed -i "s/YOUR_ID/$GH/g; s/YOUR_SHA/$SHA/g"     # Mac: sed -i ''
grep -rh 'image: ghcr' . | sort | uniq -c
```

- `grep -rl` : 이 글자가 든 **파일 이름**만 모두 찾는다 → `xargs`로 sed에 넘긴다

> **🟢 확인: 보이는 것**
>
> ```text
>       3       image: ghcr.io/niceguy61/devmart-catalog-api:sha-7f3c2e1
>       1       image: ghcr.io/niceguy61/devmart-order-api:sha-7f3c2e1
>       1       image: ghcr.io/niceguy61/devmart-order-worker:sha-7f3c2e1
> ```
> catalog-api가 3번인 것은 `steps/`의 단계별 파일 두 개 + 최종본 하나라서입니다.

## Namespace — 클러스터 안의 칸막이

지금까지 우리는 모든 것을 `default` 네임스페이스에 만들었습니다. 3일차 7교시에 본 `kube-system`처럼, 클러스터는 **네임스페이스**라는 칸으로 나눌 수 있습니다.

> **🧩 비유 — 공유 오피스의 호실**
>
> 한 건물(클러스터)을 여러 회사(팀)가 씁니다. 회사마다 **호실**(네임스페이스)이 있어, 같은 이름의 '회의실'(`catalog-api`)이 호실마다 따로 있어도 헷갈리지 않습니다. 호실마다 쓸 수 있는 전기 용량(ResourceQuota)과 출입 카드(RBAC)를 정할 수 있습니다. 하지만 **벽이 방음벽은 아닙니다** — 기본으로는 옆 호실 소리(네트워크)가 다 들립니다.

| 네임스페이스가 하는 것 | 네임스페이스가 하지 **않는** 것 |
|---|---|
| **이름의 범위** — 같은 이름을 칸마다 따로 쓸 수 있다 | 네트워크 차단 — 다른 칸의 Pod도 `서비스.칸이름`으로 부를 수 있다 (막으려면 NetworkPolicy) |
| 한꺼번에 지우기 — 칸을 지우면 안의 것이 다 지워진다 | 노드 나누기 — 모든 칸의 Pod가 같은 노드들에 섞여 뜬다 |
| 칸 단위 권한(RBAC) · 자원 한도(ResourceQuota)의 단위 | 그 자체로 보안 경계 — RBAC · 정책을 함께 써야 의미가 있다 (4주차 5일차) |

> **📖 용어 — 네임스페이스에 속하는 것과 속하지 않는 것**
>
> Pod · Deployment · Service · ConfigMap · Secret · PVC는 **네임스페이스 안**에 있습니다. Node · Namespace 자신 · PersistentVolume · StorageClass는 **클러스터 전체**의 것입니다. 3일차 7교시의 `kubectl api-resources` 출력에서 `NAMESPACED` 칸이 이것을 알려 줍니다.

## 실습 2 · devmart 네임스페이스

### 단계 1 — 만들기

```bash
cd ~/devops-lab/k8s/day5
cat devmart/namespace.yaml
kubectl apply -f devmart/namespace.yaml
kubectl get namespaces
```

> **🟢 확인: 보이는 것**
>
> ```text
> apiVersion: v1
> kind: Namespace
> metadata:
>   name: devmart
> namespace/devmart created
> NAME                 STATUS   AGE
> default              Active   2d
> devmart              Active   1s
> ...
> ```

### 단계 2 — 기본 네임스페이스 바꾸기 (선택)

매번 `-n devmart`를 치기 번거로우면, 지금 컨텍스트의 기본 네임스페이스를 바꿉니다.

```bash
kubectl config set-context --current --namespace=devmart
kubectl config get-contexts
```

> **🟢 확인: 보이는 것**
>
> ```text
> Context "kind-devmart" modified.
> CURRENT   NAME           CLUSTER        AUTHINFO       NAMESPACE
> *         kind-devmart   kind-devmart   kind-devmart   devmart
> ```

> [!WARNING]
> **교재는 계속 `-n devmart`를 쓴다**
>
> 기본 네임스페이스는 **보이지 않는 설정**이라, 다음 날 잊고 `kubectl delete`를 쳤다가 엉뚱한 칸을 지우는 일이 생깁니다. 교재 명령에는 계속 `-n devmart`를 붙입니다. 바꿨다면 나중에 `kubectl config set-context --current --namespace=default`로 되돌릴 수 있습니다.

> **🎓 학술 노트 — 다중 사용 클러스터와 '시끄러운 이웃'**
>
> 여러 팀이 한 클러스터를 나눠 쓰는 것을 **멀티 테넌시**(multi-tenancy)라고 합니다. 자원을 모아 쓰면 효율이 오르지만(3일차 1교시의 Borg 논문이 보인 서버 절약), 한 팀의 폭주가 다른 팀을 느리게 만드는 **시끄러운 이웃**(noisy neighbor) 문제가 생깁니다. Borg 논문(Verma 외, 2015)은 이를 우선순위 · 할당량(quota) · 자원 격리로 다뤘고, Kubernetes의 Namespace + ResourceQuota + requests/limits(4교시)가 같은 계보입니다. Kubernetes 다중 테넌시 작업 그룹은 네임스페이스만으로는 **약한 격리**이고, 강한 격리가 필요하면 클러스터를 나누라고 권합니다.

> **📈 트렌드 2026 — 네임스페이스와 클러스터 사이**
>
> "팀마다 클러스터를 따로"는 비싸고, "네임스페이스만"은 약합니다. 그 사이로 **가상 클러스터**(vCluster 등) — 한 클러스터 안에 팀마다 자기 apiserver를 가진 것처럼 보이게 하는 방식 — 와 플랫폼 팀이 네임스페이스 · 권한 · 할당량을 묶어 셀프서비스로 내주는 방식(3일차 5교시의 플랫폼 엔지니어링)이 널리 쓰입니다. 어느 쪽이든 오늘 배우는 네임스페이스가 기본 단위입니다.

> **✅ 확인 문제**
>
> 1. Deployment를 지웠는데 ReplicaSet과 Pod도 사라진 이유는?
> 2. `devmart` 칸의 Pod가 `default` 칸의 `catalog-api` Service를 부를 수 있나요? 부른다면 이름은?
> 3. 네임스페이스에 속하지 **않는** 리소스 두 가지는?
> 4. 오늘 세 이미지의 SHA가 같아야 하나요?
>
> <details><summary>정답</summary>
>
> 1. ReplicaSet과 Pod의 주인(ownerReferences)이 Deployment라서, 주인이 지워지면 함께 지워진다 (가비지 컬렉션)
> 2. 부를 수 있다 — 네임스페이스는 기본으로 네트워크를 막지 않는다. `catalog-api.default`
> 3. Node, Namespace, PersistentVolume, StorageClass 중 둘
> 4. 꼭 같을 필요는 없다. 서비스마다 자기 최신 SHA를 쓰면 된다 (MSA는 서비스마다 버전이 따로 간다)
>
> </details>

## 참고 문헌

- Kubernetes Docs. *Namespaces* · *Resource Quotas*. kubernetes.io/docs/concepts
- Kubernetes Docs. *Multi-tenancy*. kubernetes.io/docs/concepts/security/multi-tenancy
- Verma, A. 외 (2015). Large-scale cluster management at Google with Borg. *EuroSys '15*.
- kubectl Reference. *kubectl config set-context*. kubernetes.io/docs/reference/kubectl

---

| 이전 | 목차 | 다음 |
|:--|:--:|--:|
| ⬅️ [3주차 5일차 목차](README.md) | [⬆️ 5일차 목차](README.md) | [2교시 · ConfigMap과 Secret](lesson-02.md) ➡️ |
