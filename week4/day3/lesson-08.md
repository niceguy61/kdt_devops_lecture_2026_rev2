<sub>[🏠 과정 목차](../../README.md) › [4주차](../README.md) › [3일차](README.md) › 8/8교시</sub>

# 8교시 · 플랫폼도 Git으로 — App of Apps

> [!NOTE]
> **이번 시간에 할 일**
>
> - 4교시의 `devmart-app.yaml`처럼 **손으로 `kubectl apply`한 Application**도 Git에 둡니다.
> - 그 Application들을 관리하는 **루트 Application 하나**(App of Apps)를 만들어, 손으로 넣는 것을 **한 줄**로 줄입니다.
> - 2일차의 대시보드 · 알림 규칙, 1일차 8교시의 인증서 설정처럼 **흩어져 있던 플랫폼 설정**을 배포 저장소로 모읍니다.
> - 자식 Application을 지웠을 때 **리소스까지 지울지 남길지**를 finalizer로 정합니다.

> [!IMPORTANT]
> **지금 클러스터에서 Git에 없는 것**
>
> 7교시까지 DevMart 앱은 Git대로 섰습니다. 그런데 이 클러스터에는 **아직 손으로 넣은 것**이 남아 있습니다.
>
> | 무엇 | 언제 손으로 넣었나 |
> |---|---|
> | Argo CD의 `devmart` Application | 4 · 6교시 `kubectl apply -f argocd/…` |
> | Grafana 대시보드 · 알림 규칙 · PodMonitor | 2일차 `kubectl apply -f monitoring/…` |
> | Loki 데이터 소스 | 2일차 8교시 `cat <<EOF \| kubectl apply` |
> | 사설 CA · DevMart 인증서 | 1일차 8교시 `kubectl apply -f tls/…` |
>
> 새 클러스터를 만들면 이것들을 **기억해서** 다시 넣어야 합니다. 오늘은 이 목록을 Git으로 옮깁니다.

## App of Apps — 목록을 관리하는 Application

```text
root (손으로 넣는 유일한 것)
 └─ 배포 저장소의 apps/ 폴더를 본다
     ├─ apps/devmart.yaml        → Application devmart        → devmart/ 폴더 (앱)
     ├─ apps/observability.yaml  → Application observability  → observability/ 폴더
     └─ apps/tls.yaml            → Application tls            → tls/ 폴더
```

Application도 결국 Kubernetes 리소스(YAML)이므로, **다른 Application이 그것을 Git대로 맞출 수 있습니다.** 루트 하나만 넣으면, 루트가 자식 Application들을 만들고, 자식들이 각자의 폴더를 맞춥니다.

## 실습 20 · 플랫폼 설정을 배포 저장소로

### 단계 1 — 폴더 만들고 파일 모으기

```bash
cd ~/devmart-deploy && git pull
mkdir -p apps observability tls
cp ~/devops-lab/k8s/w4d2/monitoring/{devmart-dashboard,devmart-rules,envoy-podmonitor}.yaml observability/
cp ~/devops-lab/k8s/w4d1/tls/{issuers,devmart-cert}.yaml tls/
ls observability tls
```

2일차 8교시에 `cat <<EOF`로 바로 넣었던 Loki 데이터 소스는 이번에 **파일로** 남깁니다(Loki를 지웠다면 이 파일은 건너뜁니다).

```bash
kubectl get configmap loki-datasource -n monitoring -o yaml \
  | grep -vE '^\s+(uid|resourceVersion|creationTimestamp):|kubectl.kubernetes.io/last-applied' \
  > observability/loki-datasource.yaml
head -8 observability/loki-datasource.yaml
```

> [!TIP]
> **클러스터에서 YAML을 꺼낼 때는 '상태 칸'을 뺀다**
>
> `kubectl get -o yaml`에는 `uid`, `resourceVersion`, `creationTimestamp`처럼 **클러스터가 채운 칸**(3주차 3일차 8교시)이 섞여 나옵니다. Git에 둘 원하는 상태에는 필요 없으므로 지웁니다. 손으로 쓰는 편이 더 깔끔한 경우가 많습니다.

### 단계 2 — 자식 Application 세 개

```bash
ID=$(gh api user --jq .login)
cp ~/devops-lab/k8s/w4d3/argocd/devmart-app-auto.yaml apps/devmart.yaml
code apps/observability.yaml
```

```yaml
apiVersion: argoproj.io/v1alpha1
kind: Application
metadata:
  name: observability
  namespace: argocd
spec:
  project: default
  source:
    repoURL: https://github.com/YOUR_ID/devmart-deploy.git
    targetRevision: main
    path: observability            # 그냥 YAML이 든 폴더 (kustomization 없이도 된다)
  destination:
    server: https://kubernetes.default.svc
    namespace: monitoring          # 파일에 namespace가 없을 때만 쓰는 기본값
  syncPolicy:
    automated: { prune: true, selfHeal: true }
```

같은 모양으로 `apps/tls.yaml`을 만듭니다. 바뀌는 곳은 세 줄입니다.

```yaml
  name: tls
  …
    path: tls
  …
    namespace: cert-manager
```

```bash
sed -i "s/YOUR_ID/$ID/" apps/*.yaml          # Mac: sed -i ''
grep -H "path:" apps/*.yaml
```

> **🟢 확인: 이렇게 나오면 성공**
>
> ```text
> apps/devmart.yaml:    path: devmart
> apps/observability.yaml:    path: observability
> apps/tls.yaml:    path: tls
> ```

### 단계 3 — 루트 Application

```bash
code root.yaml
```

```yaml
# 새 클러스터에서 손으로 넣는 유일한 Application
apiVersion: argoproj.io/v1alpha1
kind: Application
metadata:
  name: root
  namespace: argocd
spec:
  project: default
  source:
    repoURL: https://github.com/YOUR_ID/devmart-deploy.git
    targetRevision: main
    path: apps                     # 자식 Application들의 YAML이 든 폴더
  destination:
    server: https://kubernetes.default.svc
    namespace: argocd              # Application은 argocd 네임스페이스에 산다
  syncPolicy:
    automated: { prune: true, selfHeal: true }
```

```bash
sed -i "s/YOUR_ID/$ID/" root.yaml
git add apps observability tls root.yaml
git commit -m "플랫폼 설정도 Git으로: app of apps (devmart · observability · tls)"
git push
```

## 실습 21 · 루트 하나 넣기

```bash
kubectl apply -f root.yaml
sleep 20
argocd app list | awk '{print $1, $5, $6}' | column -t
```

`argocd` CLI의 로그인이 풀렸다면 3교시처럼 port-forward와 `argocd login`을 다시 합니다.

> **🟢 확인: 이렇게 나오면 성공**
>
> ```text
> NAME                  STATUS  HEALTH
> argocd/devmart        Synced  Healthy
> argocd/observability  Synced  Healthy
> argocd/root           Synced  Healthy
> argocd/tls            Synced  Healthy
> ```
> - `devmart`는 이미 있던 Application입니다. 루트가 **같은 이름·같은 내용**을 Git에서 가져와 덮었으므로 아무 일도 일어나지 않고, 이제 **루트가 관리**합니다
> - `observability` · `tls`는 손으로 넣었던 리소스를 **그대로 넘겨받았습니다**(Argo CD가 추적 표시만 붙임)

웹 UI(3교시)에서 `root`를 열면 자식 Application 세 개가 **나무 모양**으로 보입니다.

### 손으로 지워 보기 — 루트가 되살린다

```bash
kubectl delete application observability -n argocd
sleep 15
kubectl get application -n argocd
kubectl get configmap devmart-dashboard -n devmart
```

> **🟢 확인: 이렇게 나오면 성공**
>
> ```text
> NAME            SYNC STATUS   HEALTH STATUS
> devmart         Synced        Healthy
> observability   Synced        Healthy
> root            Synced        Healthy
> tls             Synced        Healthy
> NAME                DATA   AGE
> devmart-dashboard   1      2d
> ```
> - 루트의 `selfHeal`이 지워진 `observability` Application을 **다시 만들었습니다**(6교시와 같은 일, 대상이 Application일 뿐)
> - 대시보드 ConfigMap은 **나이(AGE)가 그대로** — Application을 지워도 그 아래 리소스는 지워지지 않았습니다. 이유는 다음 단계

## 실습 22 · 지울 때 리소스까지? — finalizer

| 자식 Application에 | Application이 지워지면 |
|---|---|
| finalizer **없음**(오늘) | Application만 사라지고, 리소스는 **남는다**(주인 없이) |
| `resources-finalizer.argocd.argoproj.io` | Application이 리소스를 **먼저 다 지운 뒤** 사라진다 |

플랫폼 설정처럼 **실수로 지우면 아픈 것**은 finalizer 없이 두는 편이 안전합니다. 반대로 실습용 앱처럼 깨끗이 치워야 하는 것에는 붙입니다.

```yaml
metadata:
  name: devmart
  namespace: argocd
  finalizers:
    - resources-finalizer.argocd.argoproj.io
```

> [!WARNING]
> **루트에 finalizer를 붙이면**
>
> 루트를 지우는 순간 **자식 Application → 그 아래 모든 리소스**가 줄줄이 지워집니다. 루트에는 붙이지 않습니다. `prune: true`인 루트에서 `apps/` 파일 하나를 지우는 커밋도 같은 효과를 낼 수 있으므로, `apps/` 폴더의 변경은 **PR과 리뷰**로 받습니다.

> **📘 새 클러스터에서 '5분 복구'가 이렇게 줄어든다**
>
> | 순서 | 어제까지 | 오늘부터 |
> |---|---|---|
> | 1 | Secret 손으로 | Secret 손으로 (5주차에 외부 금고로) |
> | 2 | kps · Envoy Gateway · cert-manager · Loki · Argo CD `helm install` | 같음 |
> | 3 | Application · 대시보드 · 규칙 · 데이터 소스 · 인증서 `kubectl apply` 여러 번 | **`kubectl apply -f root.yaml` 한 번** |
>
> 2번의 `helm install`까지 Argo CD Application(Helm 소스)으로 옮기면 Argo CD 하나만 손으로 설치하면 됩니다. 5주차 4일차의 EKS에서 그 방향을 다시 봅니다.

> **🧹 정리: 정리**
>
> 아무것도 지우지 않습니다. 이제 `root`가 DevMart와 플랫폼 설정을 함께 관리합니다. **4 · 5일차에 DevMart를 바꿀 때는 지금처럼 배포 저장소에 커밋합니다.**

> **🎓 학술 노트 — 시스템을 처음부터 다시 세울 수 있는가**
>
> 마크 버제스(Mark Burgess)는 CFEngine을 만들며 1990년대부터 **수렴(convergence)**이라는 생각을 연구했습니다. 시스템을 "지금 무엇을 실행하라"가 아니라 "이런 상태여야 한다"로 적어 두고, 에이전트가 어디서 시작하든 **그 상태로 수렴**하게 하면 몇 번을 돌려도 결과가 같다는 것입니다(Burgess, 1995). 운영 분야는 이것을 "**서버를 고치지 말고, 처음부터 다시 세울 수 있게 하라**"는 원칙으로 받아들였습니다. App of Apps는 클러스터 수준에서 그 원칙을 지키는 장치입니다 — 클러스터를 잃어도 **루트 하나**에서 전체가 수렴합니다.
>
> - Burgess, M. (1995). A site configuration engine. *Computing Systems*, 8(2), 309–337.

> **📈 트렌드 — 플랫폼 팀의 '셀프서비스'**
>
> 회사가 커지면 클러스터마다 깔아야 하는 것(관측, 인증서, 정책, 게이트웨이)을 **플랫폼 팀**이 하나의 저장소로 묶어 제공하고, 앱 팀은 자기 앱 폴더만 고칩니다. Argo CD의 **ApplicationSet**은 "클러스터 목록 × 폴더 규칙"으로 자식 Application을 **자동으로 찍어 내어** App of Apps를 수십 개 클러스터로 넓힙니다(5주차 4일차). 같은 Git 저장소에서 클러스터 수십 개가 수렴하는 것 — 2026년 플랫폼 엔지니어링의 기본 모습입니다.

## 정리

- Application도 YAML입니다. **Application들을 관리하는 Application**(루트)을 하나 두면, 손으로 넣을 것은 그 하나뿐입니다.
- 흩어진 플랫폼 설정(대시보드 · 규칙 · 데이터 소스 · 인증서)을 배포 저장소의 폴더로 모으고, 폴더마다 자식 Application을 둡니다.
- 루트의 `selfHeal`은 **Application이 지워져도** 되살립니다.
- finalizer가 없으면 Application을 지워도 리소스는 남고, 있으면 함께 지워집니다. **루트에는 붙이지 않습니다.**

> **✅ 확인 문제**
>
> 1. App of Apps에서 새 클러스터에 손으로 넣는 것은 무엇인가요?
> 2. 이미 있던 `devmart` Application을 루트가 가져갈 때 앱이 다시 배포되지 않은 이유는?
> 3. 자식 Application을 `kubectl delete`했는데 다시 생겼습니다. 누가 만들었나요?
> 4. `resources-finalizer.argocd.argoproj.io`를 루트에 붙이면 생길 수 있는 사고는?
> 5. 클러스터에서 꺼낸 YAML을 Git에 넣기 전에 지우는 칸 두 가지는?
>
> <details><summary>정답</summary>
>
> 1. Argo CD 설치(Helm)와 루트 Application 하나 (+ 아직은 Secret)
> 2. Git의 내용이 지금 클러스터의 Application과 같아서 바꿀 것이 없었기 때문
> 3. 루트 Application의 selfHeal — `apps/`의 YAML대로 다시 맞췄다
> 4. 루트를 지우는 순간 자식 Application과 그 아래 모든 리소스가 함께 지워진다
> 5. `uid`, `resourceVersion`, `creationTimestamp`, `last-applied` 주석 중 둘 이상
>
> </details>

> [!NOTE]
> **오늘의 배움일기 — 수업 뒤 각자**
>
> - push 배포와 pull 배포를 한 문장씩, 3주차에 내가 한 배포를 예로
> - 5교시에 본 어긋남 세 방향(A · B · C)을 각각 Sync · Health 두 단어로
> - selfHeal이 되돌린 손 수정 중 가장 인상 깊었던 것, 그리고 selfHeal이 **방해가 될** 상황 하나
> - 오늘 잰 숫자: PR 합치기 → 운영 반영까지 몇 분? revert → 반영까지 몇 분?
> - CI가 가진 권한과 Argo CD가 가진 권한을 각각 적고, 어느 쪽이 털리면 더 위험한지
> - 내일 전에 궁금한 것: 오늘까지 서비스 사이의 호출(order-api → catalog-api)은 **아무 검사 없이** 오갔다. 누가 누구를 부를 수 있는지, 그 통신이 암호화되는지는 어떻게 정할까?

## 참고 문헌

- Argo CD Documentation. *Cluster Bootstrapping — App Of Apps Pattern*; *App Deletion — Finalizers*; *ApplicationSet*. argo-cd.readthedocs.io
- Burgess, M. (1995). A site configuration engine. *Computing Systems*, 8(2), 309–337.
- OpenGitOps. *GitOps Principles v1.0.0*. opengitops.dev

---

| 이전 | 목차 | 다음 |
|:--|:--:|--:|
| ⬅️ [7교시 · Actions → Argo CD 전체 파이프라인](lesson-07.md) | [⬆️ 3일차 목차](README.md) | [4주차 4일차 목차](../day4/README.md) ➡️ |
