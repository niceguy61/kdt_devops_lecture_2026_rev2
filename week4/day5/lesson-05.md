<sub>[🏠 과정 목차](../../README.md) › [4주차](../README.md) › [5일차](README.md) › 5/8교시</sub>

# 5교시 · Kyverno 정책

> [!NOTE]
> **이번 시간에 할 일**
>
> - **입장 제어**(admission control)가 RBAC와 무엇이 다른지 이해합니다.
> - Kyverno를 Helm으로 설치합니다.
> - **Audit**로 정책을 넣어 지금 DevMart가 **얼마나 어기고 있는지** 보고서로 봅니다.
> - **Deny** 정책이 kubectl과 **Argo CD Sync**를 어떻게 막는지 봅니다.

## 입장 제어 — 내용을 보는 관문

RBAC는 "devmart에 deployments를 만들 수 있나"까지만 묻습니다. 입장 제어는 **그 Deployment의 내용**을 봅니다.

| 규칙 | 왜 | 오늘 |
|---|---|---|
| 이미지 태그에 `:latest` 금지 | 어떤 버전이 도는지 알 수 없고, 되돌릴 기준이 없다 (3일차 revert) | **Deny** |
| 메모리 limits 필수 | 한 Pod가 노드 메모리를 다 먹는 것을 막는다 (3주차 5일차 OOM) | Audit → Deny |
| root로 실행 금지 | 컨테이너가 뚫리면 노드까지 위험해진다 | **Audit** (지금은 많이 어긴다) |

Kubernetes에도 기본 입장 제어 — **Pod Security Admission**(privileged · baseline · restricted 세 단계)과 **ValidatingAdmissionPolicy**(CEL) — 가 있습니다. Kyverno는 그 위에 **보고서**(이미 있는 리소스가 어기는지), **예외 관리**, **CLI로 PR에서 미리 검사** 같은 운영 기능을 더합니다.

## 실습 10 · Kyverno 설치

```bash
cd ~/devops-lab/k8s/w4d5
helm repo add kyverno https://kyverno.github.io/kyverno/
helm repo update
helm search repo kyverno/kyverno
KYV=$(helm search repo kyverno/kyverno -o json | python3 -c "import sys,json; print([c for c in json.load(sys.stdin) if c['name']=='kyverno/kyverno'][0]['version'])")
echo "kyverno 차트 $KYV" | tee -a VERSIONS.txt
helm install kyverno kyverno/kyverno -n kyverno --create-namespace --version $KYV -f kyverno/kyverno-values.yaml --wait
kubectl get pods -n kyverno
```

> **🟢 확인: 확인**
>
> ```text
> NAME           CHART VERSION   APP VERSION   DESCRIPTION
> kyverno/kyverno   3.○.○          v1.○○.○      Kubernetes Native Policy Management
> …
> NAME                                             READY   STATUS    RESTARTS   AGE
> kyverno-admission-controller-6c9b8d7f5-q2m4x     1/1     Running   0          1m
> kyverno-background-controller-7d8c9b6f4-k8w2e    1/1     Running   0          1m
> kyverno-reports-controller-5f7b9c8d6-p3x7t       1/1     Running   0          1m
> ```
> APP VERSION이 **1.17 이상**이어야 오늘 쓰는 `ValidatingPolicy`(policies.kyverno.io/v1)가 있습니다. 옛 문서의 `ClusterPolicy`는 1.17에서 폐기 예정이 되었습니다.

## 정책 읽기

```bash
cat kyverno/disallow-latest.yaml
```

```yaml
apiVersion: policies.kyverno.io/v1
kind: ValidatingPolicy
metadata:
  name: disallow-latest-tag
spec:
  validationActions: [Deny]                 # 어기면 거절 (Audit = 보고만)
  matchConstraints:                         # 어디에 — devmart의 Deployment 만들기 · 고치기
    namespaceSelector:
      matchExpressions:
        - { key: kubernetes.io/metadata.name, operator: In, values: [devmart] }
    resourceRules:
      - apiGroups: [apps]
        apiVersions: [v1]
        operations: [CREATE, UPDATE]
        resources: [deployments]
  matchConditions:                          # 예외 — Istio가 만드는 waypoint
    - name: not-istio-managed
      expression: "!has(object.metadata.labels) || !('gateway.istio.io/managed' in object.metadata.labels)"
  validations:                              # 무엇을 — CEL 식이 참이어야 통과
    - expression: >-
        object.spec.template.spec.containers.all(c,
          c.image.contains(':') && !c.image.endsWith(':latest'))
      message: "이미지에 태그를 적어야 하고 ':latest'는 쓸 수 없습니다 — …"
```

| 칸 | 읽는 법 |
|---|---|
| `object` | 지금 들어오려는 리소스 (Deployment YAML 그대로) |
| `.all(c, …)` | 모든 컨테이너 `c`에 대해 … 가 참 — CEL의 목록 함수 |
| `matchConditions` | 이 정책을 **적용할지** 먼저 거르는 식. waypoint Deployment는 Istio가 관리하므로 제외 |

> [!WARNING]
> **시스템이 만드는 것을 먼저 생각한다**
>
> 정책을 devmart 네임스페이스 전체에 걸면, **사람이 아니라 컨트롤러**가 만드는 것(Istio의 waypoint)도 검사됩니다. 그것이 거절되면 istiod가 waypoint를 고치지 못해 메시가 망가집니다. 입장 제어 사고의 대부분이 이 경우입니다. 그래서 ① 네임스페이스를 좁히고, ② 컨트롤러가 만든 것은 예외로 두고, ③ **Audit부터** 넣습니다.

## 실습 11 · Audit — 지금 얼마나 어기나

```bash
kubectl apply -f kyverno/require-limits.yaml -f kyverno/require-non-root.yaml
echo "- $(date +%F) Kyverno 설치 · ValidatingPolicy require-memory-limits · require-run-as-non-root (Audit)" >> ~/devops-lab/k8s/w4d4/platform-changes.md
kubectl get validatingpolicy
sleep 60
kubectl get policyreport -n devmart -o wide
```

> **🟢 확인: 확인**
>
> ```text
> NAME                      ACTIONS     READY   AGE
> require-memory-limits     ["Audit"]   true    1m
> require-run-as-non-root   ["Audit"]   true    1m
> NAME                                   KIND         NAME           PASS   FAIL   WARN   ERROR   SKIP   AGE
> 0b1c…                                  Deployment   catalog-api    1      1      0      0       0      50s
> 3f9a…                                  Deployment   db             1      1      0      0       0      50s
> 7d2e…                                  Deployment   order-api      1      1      0      0       0      50s
> …
> ```
> 모든 Deployment가 **limits는 통과(PASS 1), root 규칙은 실패(FAIL 1)**입니다. 3주차 5일차에 limits는 정성껏 넣었지만, `runAsNonRoot`는 아무도 넣지 않았습니다. **Audit는 아무것도 막지 않고** 이 사실만 알려 줍니다.

```bash
kubectl get policyreport -n devmart -o jsonpath='{range .items[*]}{.scope.name}{"\t"}{range .results[?(@.result=="fail")]}{.policy}{" "}{end}{"\n"}{end}'
```

> [!IMPORTANT]
> **Audit → 고치기 → Deny**
>
> 정책을 처음부터 Deny로 넣으면, 다음 배포 때 **6개 서비스가 모두 막힙니다.** 그래서 순서는 ① Audit로 넣어 보고서를 본다 → ② 어기는 것을 **Git에서** 고친다(앱 팀의 PR) → ③ FAIL이 0이 되면 Deny로 바꾼다. root 규칙은 postgres · redis · nginx 이미지의 실행 사용자를 바꿔야 해서 오늘은 ①에서 멈춥니다 — 회고의 Try 후보입니다.

## 실습 12 · Deny — kubectl이 막힌다

```bash
kubectl apply -f kyverno/disallow-latest.yaml
kubectl create deployment try-latest -n devmart --image=nginx:latest
kubectl create deployment try-notag -n devmart --image=nginx
```

> **🟢 확인: 확인**
>
> ```text
> validatingpolicy.policies.kyverno.io/disallow-latest-tag created
> error: failed to create deployment: admission webhook "….kyverno.svc-fail" denied the request: Policy disallow-latest-tag failed: 이미지에 태그를 적어야 하고 ':latest'는 쓸 수 없습니다 — 어떤 버전이 도는지 알 수 없게 됩니다.
> error: failed to create deployment: admission webhook "….kyverno.svc-fail" denied the request: …
> ```
> 나는 **cluster-admin**인데도 막혔습니다. 입장 제어는 **누구인지와 상관없이** 내용을 봅니다 — RBAC와의 결정적인 차이입니다.

## 실습 13 · Deny — Argo CD도 막힌다

배포 저장소에서 catalog-api의 태그를 `latest`로 바꿔 봅니다(GHCR에는 `latest` 태그가 실제로 있습니다 — 3주차 2일차의 CI가 만든다).

```bash
cd ~/devmart-deploy
sed -i '/devmart-catalog-api/{n;s/newTag: .*/newTag: latest/;}' devmart/kustomization.yaml     # Mac: sed -i '' …
git commit -am "catalog-api latest로 (정책 시험)" && git push
sleep 60
argocd app get devmart | grep -E "Sync Status|Health|Message" | head -4
argocd app get devmart -o json | python3 -c "import sys,json; print(json.load(sys.stdin)['status']['operationState']['message'][:240])"
```

> **🟢 확인: 확인**
>
> ```text
> Sync Status:        OutOfSync from main (a4c2e9b)
> Health Status:      Healthy
> one or more objects failed to apply, reason: admission webhook "….kyverno.svc-fail" denied the request: Policy disallow-latest-tag failed: 이미지에 태그를 적어야 하고 …
> ```
> - Argo CD는 Git대로 하려 했지만 **apiserver의 관문에서** 막혔습니다. Sync 실패, OutOfSync가 남습니다.
> - 서비스는 **옛 버전 그대로** 돕니다(Healthy) — 잘못된 변경이 클러스터에 닿지 않았습니다.
> - 웹 UI의 devmart 화면 위쪽에 빨간 **SYNC FAILED** 표시와 같은 메시지가 보입니다.

되돌립니다.

```bash
git revert --no-edit HEAD && git push
sleep 60; argocd app get devmart | grep -E "Sync Status|Health"
```

> [!TIP]
> **PR 단계에서 먼저 막기**
>
> 오늘은 클러스터 관문에서 막았지만, 더 좋은 곳은 **PR 단계**입니다. `kyverno` CLI는 같은 정책을 매니페스트 파일에 돌려 볼 수 있습니다 — 배포 저장소에 CI를 두고 `kustomize build devmart | kyverno apply kyverno/ --resource -` 같은 단계를 넣으면, 합치기 전에 빨간 X가 뜹니다. 3일차 6교시 트렌드의 "PR 검사 + 입장 제어" 이중 구조입니다.

> **🎓 학술 노트 — 기준 감시기**
>
> Anderson의 *Computer Security Technology Planning Study*(1972)는 모든 접근을 검사하는 **기준 감시기**(reference monitor)의 조건으로 세 가지를 들었습니다 — **항상 불린다**(우회 불가), **변조할 수 없다**, **검증할 수 있을 만큼 작다**. apiserver의 입장 제어 단계는 클러스터 변경에 대한 기준 감시기 역할을 합니다. 모든 쓰기(kubectl이든 Argo CD든)가 지나가고(실습 12 · 13), 정책은 읽을 수 있는 짧은 CEL 식입니다. 단, 웹훅이 죽었을 때 '통과'시킬지 '거절'할지(failurePolicy)가 첫 번째 조건을 좌우합니다.

> **📈 트렌드 2026 — 정책 엔진의 정리**
>
> Kyverno는 2026년 3월 CNCF **졸업**(graduated) 프로젝트가 되었고, 1.17에서 CEL 기반 정책을 v1으로, 옛 ClusterPolicy를 폐기 예정으로 돌렸습니다. Kubernetes 자체의 ValidatingAdmissionPolicy와 같은 CEL을 쓰므로, 간단한 규칙은 웹훅 없이 apiserver 안에서, 보고서 · 예외 · 이미지 서명 검증 같은 운영 기능은 Kyverno가 맡는 분업이 자리 잡고 있습니다. OPA Gatekeeper(Rego 언어)도 여전히 널리 쓰이는 대안입니다.

> **✅ 확인 문제**
>
> 1. 입장 제어가 RBAC와 다른 점은?
> 2. 정책을 Audit로 먼저 넣는 이유는?
> 3. matchConditions로 waypoint를 뺀 이유는?
> 4. Argo CD의 Sync가 막혔을 때 서비스가 Healthy였던 이유는?
>
> <details><summary>정답</summary>
>
> 1. 누구인지가 아니라 요청의 내용(이미지 태그, limits 등)을 보고, cluster-admin도 막는다
> 2. 지금 얼마나 어기는지 먼저 보고 Git에서 고친 뒤 Deny로 바꿔야 배포가 한꺼번에 막히지 않기 때문
> 3. waypoint는 Istio(istiod)가 만들고 고치는 것이라, 막히면 메시가 망가지기 때문
> 4. 잘못된 변경이 apiserver에서 거절되어 클러스터에 닿지 않았고, 옛 버전이 그대로 돌았기 때문
>
> </details>

## 참고 문헌

- Kubernetes Docs. *Admission Control*, *Validating Admission Policy*, *Pod Security Admission*. kubernetes.io/docs
- Kyverno Docs. *ValidatingPolicy*, *Policy Reports*, *Kyverno CLI — apply*. kyverno.io/docs
- Anderson, J. P. (1972). *Computer Security Technology Planning Study* (ESD-TR-73-51). U.S. Air Force.
- CNCF (2026-03-24). *Cloud Native Computing Foundation Announces Kyverno's Graduation*. cncf.io

---

| 이전 | 목차 | 다음 |
|:--|:--:|--:|
| ⬅️ [4교시 · 서비스 신원으로 허가](lesson-04.md) | [⬆️ 5일차 목차](README.md) | [6교시 · 4주차 종합 장애 훈련](lesson-06.md) ➡️ |
