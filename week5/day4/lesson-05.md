[🏠 과정 목차](../../README.md) › [5주차](../README.md) › [4일차](README.md)

# 5교시 · 같은 배포 저장소를 EKS에

> [!NOTE]
> **이번 시간에 할 일**
>
> - 배포 저장소에 **`eks/` 폴더 하나**를 더해, 4주차 `devmart/`를 그대로 쓰면서 EKS에 없는 것만 뺍니다.
> - Secret을 만들고, EKS의 Argo CD에 Application을 넣습니다.
> - **인터넷 주소로** DevMart를 열고, 주문까지 해 봅니다.

## 무엇을 빼야 하나

4주차 4 · 5일차에 배포 저장소에는 **Istio**(waypoint · VirtualService · PeerAuthentication · AuthorizationPolicy)와 **Prometheus Operator**(PrometheusRule) 리소스가 들어갔습니다. EKS에는 오늘 그 CRD가 없습니다(4교시 표). CRD가 없는 리소스가 하나라도 있으면 Argo CD의 Sync가 **통째로 실패**합니다.

| 방법 | 장단 |
|---|---|
| devmart/에서 지운다 | kind 쪽이 망가진다 ✗ |
| eks/ 폴더에 **복사** | 두 벌을 따로 고쳐야 한다 — 3일차 6교시의 "복사해서 붙이기" ✗ |
| eks/ 폴더가 devmart/를 **참조**하고 **빼기만** | 원본은 하나, 차이만 적는다 ✓ — kustomize **오버레이** |

```bash
cat ~/devops-lab/aws/w5d4/deploy/kustomization.yaml
head -8 ~/devops-lab/aws/w5d4/deploy/remove-mesh-and-monitoring.yaml
```

```yaml
# eks/kustomization.yaml
resources:
  - ../devmart                        # 4주차 그대로
patches:
  - path: remove-mesh-and-monitoring.yaml
---
# remove-mesh-and-monitoring.yaml
$patch: delete                        # 펼친 결과에서 이 리소스를 지운다
apiVersion: gateway.networking.k8s.io/v1
kind: Gateway
metadata:
  name: waypoint
  namespace: devmart
---
…                                     # VirtualService · PeerAuthentication · AuthorizationPolicy 둘 · PrometheusRule
```

> **📖 오버레이 (overlay)**
>
> kustomize에서 **바탕**(base, 여기서는 `devmart/`)을 참조하고 **환경마다 다른 점만** 덧붙이는 폴더입니다. 3주차 5일차의 `configMapGenerator`, 4주차 3일차의 `images:`와 함께 kustomize의 세 번째 핵심 기능입니다. 실무에서는 `base/` + `overlays/dev · staging · prod`가 흔한 모양입니다.

## 실습 6 · eks/ 폴더 (커밋)

```bash
cd ~/devmart-deploy && git pull
mkdir -p eks
cp ~/devops-lab/aws/w5d4/deploy/*.yaml eks/
kubectl kustomize devmart | grep -E '^kind:' | sort | uniq -c > /tmp/kind.txt
kubectl kustomize eks     | grep -E '^kind:' | sort | uniq -c > /tmp/eks.txt
diff /tmp/kind.txt /tmp/eks.txt
```

> **🟢 확인: 확인**
>
> ```text
> < 2 kind: AuthorizationPolicy
> < 1 kind: Gateway
> < 1 kind: PeerAuthentication
> < 1 kind: PrometheusRule
> < 1 kind: VirtualService
> ```
> 빼려던 것만 사라졌는지 확인합니다. 배포 저장소의 상태(4주차에 어디까지 커밋했나)에 따라 줄 수가 조금 다릅니다. **없는 리소스를 빼려 하면** kustomize가 오류를 냅니다 — 그 줄은 remove 파일에서 지웁니다.

```bash
git add eks && git commit -m "EKS 오버레이: Istio · Prometheus Operator 리소스 제외" && git push
```

## 실습 7 · Secret과 Application

```bash
kubectl create secret generic devmart-db -n devmart \
  --from-literal=DB_PASSWORD="$(openssl rand -hex 12)"
ID=$(gh api user -q .login)
sed "s/YOUR_ID/$ID/" ~/devops-lab/aws/w5d4/argocd/devmart-eks-app.yaml | kubectl apply -f -
kubectl get application -n argocd
```

> **🟢 확인: 확인**
>
> ```text
> secret/devmart-db created
> application.argoproj.io/devmart created
> NAME      SYNC STATUS   HEALTH STATUS
> devmart   Synced        Progressing
> ```
> Secret은 3주차 5일차와 같이 **Git 밖에서** 손으로 만듭니다(4주차 3일차의 빈칸 — 내일 이야기).

```bash
kubectl get pods -n devmart -w
```

> **🟢 확인: 확인 (2~3분)**
>
> ```text
> NAME                            READY   STATUS              RESTARTS   AGE
> db-6b7f8c9d5-q4w2e              0/1     Pending             0          5s
> db-6b7f8c9d5-q4w2e              0/1     ContainerCreating   0          25s
> catalog-api-7c9d8b6f4-m2k8q     0/1     Running             2          50s
> …
> db-6b7f8c9d5-q4w2e              1/1     Running             0          70s
> catalog-api-7c9d8b6f4-m2k8q     1/1     Running             2          95s
> …
> ```
> - db가 잠깐 **Pending** — PVC가 생기고 EBS CSI가 **EBS 볼륨을 만들어 붙이는** 시간입니다(6교시).
> - catalog-api가 db를 기다리며 재시작하는 것은 3주차 5일차와 같습니다(probe가 지켜 준다).
> `Ctrl+C`.

## 실습 8 · 인터넷에서 열기

```bash
NLB=$(kubectl get gateway devmart -n devmart -o jsonpath='{.status.addresses[0].value}')
echo "http://$NLB/"
for p in / /api/products /api/info; do printf '%-15s ' $p; curl -s -o /dev/null -w '%{http_code}\n' http://$NLB$p; done
curl -s -X POST http://$NLB/api/orders -H 'content-type: application/json' -d '{"product_id":1,"quantity":1}'; echo
```

> **🟢 확인: 확인**
>
> ```text
> http://k8s-envoygat-envoydev-0a1b2c3d4e-0f1e2d3c4b5a6978.elb.ap-northeast-2.amazonaws.com/
> /               200
> /api/products   200
> /api/info       200
> {"order_id":1,"request_id":"…","status":"pending","total_price":59000}
> ```
> **휴대폰**(Wi-Fi를 끄고 LTE로)에서도 이 주소를 열어 봅니다. 3주차부터 노트북 안에만 있던 DevMart가 처음으로 **인터넷에** 나왔습니다. 짝의 주소도 열어 봅니다.

> [!IMPORTANT]
> **바뀐 것과 바뀌지 않은 것**
>
> 이 배포에서 **앱 쪽 파일은 한 줄도 바뀌지 않았습니다** — 이미지(GHCR), Deployment, Service, HTTPRoute, ConfigMap, kustomization의 `images:`. 바뀐 것은 ① **플랫폼**(4교시: StorageClass · LBC · EnvoyProxy), ② **오버레이 한 폴더**(CRD가 없는 것 빼기)뿐입니다. 4주차 3일차의 "destination만 바꾼다"가 이렇게 실현되었습니다.

> [!TIP]
> **Argo CD 화면**
>
> `kubectl port-forward -n argocd svc/argocd-server 8080:80 &` → <http://localhost:8080>. 비밀번호는 4주차 3일차처럼 `argocd-initial-admin-secret`에서. kind의 Argo CD와 **같은 모양의 나무**가 보입니다 — 다만 PVC 아래에 EBS 볼륨 이름이, Service 아래에 NLB 주소가 있습니다.

> **❓ 오해 — 클라우드로 옮기려면 앱을 다시 짜야 한다**
>
> 앱이 12-Factor(3주차 1일차)를 지키고 — 설정은 환경 변수, 상태는 밖에, 로그는 표준 출력 — 컨테이너 이미지와 선언적 매니페스트로 배포된다면, 옮기는 일은 대부분 **플랫폼의 일**입니다. 오늘 DevMart가 그 증거입니다. 옮기기 어려운 것은 대개 **데이터**(DB)입니다 — 내일 EBS의 AZ 문제로 봅니다.

> **🎓 학술 노트 — 환경 간 차이의 관리**
>
> Humble과 Farley(2010, 4주차 3일차)는 배포 파이프라인에서 환경 간 차이를 **설정으로만** 두고 산출물은 같게 하라고 했습니다. kustomize 오버레이 · Helm values 파일은 그 '설정 차이'를 **선언적 diff**로 표현하는 도구입니다. Sayagh 외의 *Software Configuration Engineering in Practice*(IEEE TSE, 2020)는 실무에서 설정 오류의 큰 원인이 **환경마다 복사된 설정이 서로 어긋나는 것**임을 보였습니다 — 오버레이가 복사 대신 참조를 쓰는 이유입니다.

> **📈 트렌드 2026 — 한 저장소, 여러 클러스터**
>
> Argo CD의 **ApplicationSet**은 "클러스터 목록 × 폴더 규칙"으로 Application을 자동으로 찍어 냅니다 — 클러스터를 더하면 배포가 따라옵니다. 오늘 손으로 만든 '같은 저장소, 다른 폴더, 다른 클러스터'를 수십 개 클러스터로 넓히는 표준 방법입니다. 그리고 Argo CD 3.x의 Source Hydrator(4주차 3일차)는 오버레이를 펼친 결과를 커밋해 "EKS에 실제로 무엇이 가나"를 PR에서 보이게 합니다.

> **✅ 확인 문제**
>
> 1. EKS용으로 devmart/를 복사하지 않고 오버레이를 쓴 이유는?
> 2. `$patch: delete`가 하는 일은?
> 3. db가 잠깐 Pending이었던 이유는?
> 4. 오늘 EKS로 옮기면서 바뀌지 않은 앱 쪽 파일 넷은?
>
> <details><summary>정답</summary>
>
> 1. 원본을 하나로 두고 차이만 적기 위해 — 복사하면 두 벌이 어긋난다
> 2. 펼친 결과에서 그 리소스를 지운다 (원본 파일은 그대로)
> 3. PVC가 생긴 뒤 EBS CSI가 EBS 볼륨을 만들어 노드에 붙이는 시간
> 4. 이미지(GHCR), Deployment, Service, HTTPRoute (ConfigMap, images: 등)
>
> </details>

## 참고 문헌

- Kubernetes Docs. *Kustomize — Bases and Overlays*, *Strategic merge patch $patch: delete*. kubernetes.io/docs
- Argo CD Docs. *ApplicationSet*. argo-cd.readthedocs.io
- Sayagh, M. 외 (2020). *Software Configuration Engineering in Practice: Interviews, Survey, and Systematic Literature Review*. IEEE TSE 46(6).

---

⬅️ 이전: [4교시 · 플랫폼 올리기](lesson-04.md) &nbsp;|&nbsp; [⬆️ 4일차 목차](README.md) &nbsp;|&nbsp; 다음: [6교시 · 클라우드에서 달라진 것](lesson-06.md) ➡️
