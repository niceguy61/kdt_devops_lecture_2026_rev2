# 3교시 · ServiceAccount — 프로그램의 신원

> [!NOTE]
> **이번 시간에 할 일**
>
> - 모든 Pod에 **토큰이 자동으로** 들어 있다는 것을 확인합니다.
> - 그 토큰으로 Pod 안에서 apiserver를 불러 보고, 권한이 **신원에 따라** 달라지는 것을 봅니다.
> - DevMart 서비스마다 **자기 ServiceAccount**를 Git으로 만들고, 쓰지 않는 토큰을 뺍니다.
> - 메시의 신원(SPIFFE)이 함께 바뀌는 것을 확인합니다.

## Pod 안의 열쇠

```bash
kubectl exec -n devmart deploy/order-api -- ls /var/run/secrets/kubernetes.io/serviceaccount
kubectl get pod -n devmart -l app=order-api -o jsonpath='{.items[0].spec.serviceAccountName}'; echo
```

> **🟢 확인: 확인**
>
> ```text
> ca.crt
> namespace
> token
> default
> ```
> order-api는 Kubernetes API를 **한 번도 부르지 않는데**, Pod 안에 `default` ServiceAccount의 **토큰**이 들어 있습니다. Kubernetes가 모든 Pod에 기본으로 넣어 주기 때문입니다(`automountServiceAccountToken` 기본값 true). 누군가 order-api의 취약점으로 셸을 얻으면, 이 토큰을 들고 apiserver에 말을 걸 수 있습니다.

## 실습 5 · 토큰으로 apiserver 부르기

```bash
cd ~/devops-lab/k8s/w4d5
kubectl run sa-demo -n devmart --image=curlimages/curl:8.17.0 --restart=Never -- sleep 3600
kubectl wait -n devmart --for=condition=Ready pod/sa-demo
kubectl exec -n devmart sa-demo -- sh -c '
S=/var/run/secrets/kubernetes.io/serviceaccount
curl -s --cacert $S/ca.crt -H "Authorization: Bearer $(cat $S/token)" \
  https://kubernetes.default.svc/api/v1/namespaces/devmart/pods | head -12'
```

> **🟢 확인: 확인**
>
> ```text
> {
>   "kind": "Status",
>   "apiVersion": "v1",
>   "status": "Failure",
>   "message": "pods is forbidden: User \"system:serviceaccount:devmart:default\" cannot list resource \"pods\" in API group \"\" in the namespace \"devmart\"",
>   "reason": "Forbidden",
>   "code": 403
> }
> ```
> - ① 인증은 **통과**했습니다 — apiserver가 이 요청을 `system:serviceaccount:devmart:default`로 알아봤습니다(토큰 = 신분증).
> - ② 인가(RBAC)에서 **거절** — default SA에는 아무 권한도 없습니다. 다행이지만, 누가 실수로 default에 권한을 주면 **모든 Pod가** 그 권한을 갖게 됩니다.

이번에는 **Pod 목록만 읽을 수 있는** SA로 같은 일을 합니다.

```bash
cat test/pod-reader.yaml
kubectl apply -f test/pod-reader.yaml
kubectl run sa-demo2 -n devmart --image=curlimages/curl:8.17.0 --restart=Never \
  --overrides='{"spec":{"serviceAccountName":"pod-reader"}}' -- sleep 3600
kubectl wait -n devmart --for=condition=Ready pod/sa-demo2
kubectl exec -n devmart sa-demo2 -- sh -c '
S=/var/run/secrets/kubernetes.io/serviceaccount
curl -s --cacert $S/ca.crt -H "Authorization: Bearer $(cat $S/token)" \
  https://kubernetes.default.svc/api/v1/namespaces/devmart/pods | grep -o "\"name\": \"[a-z0-9-]*\"" | sort -u | head -5
echo; cut -d. -f2 $S/token | base64 -d 2>/dev/null | head -c 400'
```

> **🟢 확인: 확인**
>
> ```text
> "name": "catalog-api-5d8c7b9f6-2xkq4"
> "name": "db-6b7f8c9d5-q4w2e"
> …
> {"aud":["https://kubernetes.default.svc.cluster.local"],"exp":1795652…,"iat":1795648…,"iss":"https://kubernetes.default.svc.cluster.local","kubernetes.io":{"namespace":"devmart","pod":{"name":"sa-demo2",…},"serviceaccount":{"name":"pod-reader",…}},…,"sub":"system:serviceaccount:devmart:pod-reader"}
> ```
> - 같은 명령인데 **신원이 다르니 결과가 다릅니다.**
> - 토큰은 **JWT**입니다. 가운데 부분을 풀면 `sub`(누구), `exp`(만료), 그리고 **어느 Pod에 묶였는지**가 보입니다. Kubernetes 1.24 이후의 토큰은 **한 시간쯤 뒤 만료**되고 kubelet이 자동으로 바꿔 넣으며, **Pod가 사라지면 무효**가 됩니다(bound token). 예전처럼 Secret에 영구 토큰이 남지 않습니다.

> **📖 ServiceAccount**
>
> Pod 안에서 도는 **프로그램의 신원**입니다. 사람(User)과 달리 Kubernetes 안의 리소스이고, 네임스페이스에 속합니다. 이름은 `system:serviceaccount:<네임스페이스>:<이름>`. Pod의 `spec.serviceAccountName`으로 지정하고, 없으면 `default`입니다. 어제 본 메시의 SPIFFE ID(`…/ns/devmart/sa/default`)도 **이 ServiceAccount에서** 왔습니다.

## 실습 6 · 서비스마다 자기 신원 (커밋)

```bash
cat deploy/serviceaccounts.yaml deploy/kustomization-patches.yaml
```

두 가지를 합니다.
- **ServiceAccount 셋** — `automountServiceAccountToken: false`로 **토큰을 넣지 않습니다.** DevMart 앱은 Kubernetes API를 부르지 않기 때문입니다.
- **kustomize patches** — Deployment 파일을 고치지 않고, 묶음 단계에서 `serviceAccountName`을 끼워 넣습니다(2일차의 `images:`와 같은 생각).

```bash
cd ~/devmart-deploy
cp ~/devops-lab/k8s/w4d5/deploy/serviceaccounts.yaml devmart/
sed -i 's/^resources:$/resources:\n  - serviceaccounts.yaml/' devmart/kustomization.yaml      # Mac: 편집기로 resources 맨 앞에
cat ~/devops-lab/k8s/w4d5/deploy/kustomization-patches.yaml >> devmart/kustomization.yaml
kubectl kustomize devmart | grep -B2 -A1 "serviceAccountName"
git add . && git commit -m "서비스마다 ServiceAccount (토큰 없음)" && git push
```

> **🟢 확인: kustomize 결과**
>
> ```text
>     spec:
>       containers:
>       …
>       serviceAccountName: catalog-api
> …
>       serviceAccountName: order-api
> …
>       serviceAccountName: order-worker
> ```
> push 전에 펼쳐 본 결과로 확인했습니다(3일차 2교시). Argo CD도 똑같이 펼칩니다.

```bash
sleep 90
kubectl get pods -n devmart -o custom-columns=NAME:.metadata.name,SA:.spec.serviceAccountName | grep -v -E "sa-demo|client"
kubectl exec -n devmart deploy/order-api -- ls /var/run/secrets/kubernetes.io/serviceaccount
curl -s -o /dev/null -w '%{http_code}\n' -X POST localhost:30080/api/orders -H 'content-type: application/json' -d '{"product_id":1,"quantity":1}'
```

> **🟢 확인: 확인**
>
> ```text
> NAME                            SA
> catalog-api-7c9d8b6f4-m2k8q     catalog-api
> catalog-api-7c9d8b6f4-x4p7w     catalog-api
> db-6b7f8c9d5-q4w2e              default
> order-api-5b8c7d9f6-r2t5y       order-api
> order-worker-6d9f8c7b5-k3w9e    order-worker
> redis-…                         default
> waypoint-…                      waypoint
> web-…                           default
> ls: cannot access '/var/run/secrets/kubernetes.io/serviceaccount': No such file or directory
> 202
> ```
> - SA를 바꾼 세 Deployment는 **새 Pod**로 롤링되었습니다(Pod 템플릿이 바뀌었으니까 — 3주차 4일차).
> - order-api에서 토큰이 **사라졌고**, 주문은 그대로 됩니다 — 원래 쓰지 않던 열쇠였습니다.
> - waypoint는 Istio가 만든 자기 SA(`waypoint`)를 씁니다. 4교시에 씁니다.
> - db · redis · web은 아직 default — 같은 방법으로 나눌 수 있습니다(회고의 Try 후보).

## 메시의 신원도 바뀌었다

```bash
curl -s -o /dev/null -X POST localhost:30080/api/orders -H 'content-type: application/json' -d '{"product_id":2,"quantity":1}'
kubectl logs -n istio-system -l app=ztunnel --tail=300 | grep 'dst.workload="catalog-api' | tail -1 | grep -o 'src.identity="[^"]*"'
```

> **🟢 확인: 확인**
>
> ```text
> src.identity="spiffe://cluster.local/ns/devmart/sa/waypoint"
> ```
> order-api → catalog-api 호출은 **waypoint를 거쳐** catalog-api에 닿으므로, catalog-api 앞의 ztunnel이 보는 상대는 waypoint입니다. waypoint 쪽 로그(`kubectl logs -n devmart -l gateway.networking.k8s.io/gateway-name=waypoint --tail=5`)에는 원래 부른 쪽이 `sa/order-api`로 찍힙니다. 이 **두 겹의 신원**이 4교시의 열쇠입니다.

```bash
kubectl delete pod sa-demo sa-demo2 -n devmart
kubectl delete -f test/pod-reader.yaml
```

> **❓ 오해 — 토큰이 있어도 권한이 없으면 괜찮다**
>
> 지금은 default SA에 권한이 없어 괜찮습니다. 하지만 ① 누군가 나중에 default에 권한을 주면(Helm 차트가 그러기도 한다) **모든 Pod**가 그 권한을 갖고, ② 토큰은 apiserver의 **버전 · 리소스 목록**을 읽는 데 쓰여 공격의 정찰 단계를 돕습니다. 쓰지 않는 열쇠는 **애초에 주지 않는 것**이 최소 권한입니다.

> **🎓 학술 노트 — 혼동된 대리인**
>
> 권한을 가진 프로그램이 **다른 사람의 요청을 대신 처리하다가** 자기 권한을 잘못 쓰는 문제를 Hardy는 *The Confused Deputy*(ACM SIGOPS OSR, 1988)라 이름 붙였습니다. 강한 ServiceAccount를 가진 Pod(예: Argo CD 컨트롤러)가 바깥 입력(Git)에 따라 행동하는 구조는 이 문제와 닮았습니다. 그래서 그런 Pod의 입력 — 배포 저장소의 쓰기 권한 — 을 지키는 것이 Pod의 권한을 지키는 것과 같은 무게를 갖습니다.

> **📈 트렌드 2026 — 워크로드 신원 하나로**
>
> ServiceAccount 토큰(JWT)은 이제 클러스터 밖에서도 신분증으로 쓰입니다. EKS Pod Identity · IRSA는 SA 토큰을 AWS IAM 역할로 바꿔 주고, GitHub Actions의 OIDC 토큰도 같은 방식으로 클라우드 권한을 받습니다. "비밀 키를 넣지 말고 **신원을 증명해 짧은 권한을 받는다**"가 표준입니다 — 5주차 EKS에서 order-api가 S3에 접근할 때 직접 씁니다.

> **✅ 확인 문제**
>
> 1. order-api Pod에 토큰이 있었던 이유와 그것이 위험한 이유는?
> 2. sa-demo가 403을 받았을 때 인증은 통과했나요?
> 3. 요즘 SA 토큰이 예전보다 안전한 점 두 가지는?
> 4. Deployment 파일을 고치지 않고 serviceAccountName을 넣은 방법은?
>
> <details><summary>정답</summary>
>
> 1. automountServiceAccountToken 기본값이 true라서. 셸을 빼앗기면 그 토큰으로 apiserver에 말을 걸 수 있다
> 2. 통과했다 — system:serviceaccount:devmart:default로 알아봤고, 인가에서 거절됐다
> 3. 한 시간쯤 뒤 만료되고 자동 교체된다, Pod에 묶여 Pod가 사라지면 무효가 된다
> 4. kustomization의 patches (JSON patch로 /spec/template/spec/serviceAccountName 추가)
>
> </details>

## 참고 문헌

- Kubernetes Docs. *Service Accounts*, *Configure Service Accounts for Pods — Opt out of API credential automounting*. kubernetes.io/docs
- Kubernetes Docs. *Kustomize — patches*. kubernetes.io/docs/tasks/manage-kubernetes-objects/kustomization
- Hardy, N. (1988). *The Confused Deputy*. ACM SIGOPS Operating Systems Review 22(4).
- AWS Docs. *EKS Pod Identity*. docs.aws.amazon.com/eks
