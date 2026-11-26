<sub>[🏠 과정 목차](../../README.md) › [4주차](../README.md) › [1일차](README.md) › 2/7교시</sub>

# 2교시 · Helm 설치 루프

> [!NOTE]
> **이번 시간에 할 일**
>
> - 연습용 앱 **podinfo** 차트로 Helm의 한 바퀴 — **살펴보기 → 렌더링해 보기 → 설치 → 확인 → 바꾸기 → 망가뜨리기 → 되돌리기 → 지우기** — 를 돕니다.
> - 릴리스 이력이 클러스터 **어디에** 남는지 확인합니다.
> - 3주차 4일차 `rollout undo`와 `helm rollback`의 차이를 구분합니다.

> **📖 용어 — podinfo**
>
> Flux(GitOps 도구) 개발자 Stefan Prodan이 만든 **연습용 웹 앱**입니다. 접속하면 자기 Pod 이름 · 버전 · 설정한 메시지와 색을 보여 주고, Helm 차트가 잘 관리되어 있어 Kubernetes 교육과 도구 시험에 널리 쓰입니다. 오늘 이 차트로 Helm을 익히고, 6교시에 Gateway 실습의 두 번째 앱으로도 씁니다.

## 실습 2 · 설치 전에 살펴보기

### 단계 1 — 실습 파일

```bash
mkdir -p ~/devops-lab/k8s/w4d1
cp -r ~/course/labs/week4/day1/* ~/devops-lab/k8s/w4d1/
cd ~/devops-lab/k8s/w4d1 && ls helm gateway
```

> **🟢 확인: 보이는 것**
>
> ```text
> gateway:
> devmart-routes.yaml  envoy-gateway-values.yaml  envoyproxy.yaml  gateway.yaml  gatewayclass.yaml  podinfo-route.yaml  podinfo-split.yaml
>
> helm:
> podinfo-canary-values.yaml  podinfo-values.yaml
> ```

### 단계 2 — 차트의 이름표

```bash
CHART=oci://ghcr.io/stefanprodan/charts/podinfo
helm show chart $CHART --version 6.14.0
```

- `oci://…` : 차트가 **컨테이너 레지스트리**(2주차의 GHCR)에 있다. `helm repo add` 없이 주소로 바로 쓴다
- `--version 6.14.0` : 차트 버전을 **고정**한다 — 이미지 태그를 SHA로 고정한 것과 같은 이유

> **🟢 확인: 보이는 것**
>
> ```text
> Pulled: ghcr.io/stefanprodan/charts/podinfo:6.14.0
> Digest: sha256:…
> apiVersion: v2
> appVersion: 6.14.0
> description: Podinfo Helm chart for Kubernetes
> ...
> name: podinfo
> version: 6.14.0
> ```
> **`version`은 차트의 버전, `appVersion`은 차트가 설치하는 앱의 버전**입니다. podinfo는 둘이 같지만, 많은 차트는 다릅니다(차트만 고쳐 새로 낸 경우 등). 5교시 Envoy Gateway도 둘을 함께 봅니다.

### 단계 3 — 바꿀 수 있는 값

```bash
helm show values $CHART --version 6.14.0 | head -30
cat helm/podinfo-values.yaml
```

> **🟢 확인: 보이는 것 (앞부분)**
>
> ```text
> # Default values for podinfo.
>
> replicaCount: 1
> logLevel: info
> host: #0.0.0.0
> backend: #http://backend-podinfo:9898/echo
> backends: []
>
> ui:
>   color: "#34577c"
>   message: ""
>   logo: ""
> ...
> ```
> ```yaml
> replicaCount: 2
> ui:
>   color: "#0E7C86"
>   message: "DevMart 4주차 — Helm으로 설치했습니다"
> resources:
>   requests: { cpu: 10m, memory: 32Mi }
>   limits: { memory: 128Mi }
> ```
> 차트의 기본값은 수백 줄이지만, **내 values 파일에는 바꾸는 것만** 적습니다. 나머지는 차트를 믿습니다. 차트를 새 버전으로 올려도 내 파일은 이 몇 줄이 전부입니다.

### 단계 4 — 설치하지 않고 렌더링만

```bash
helm template podinfo $CHART --version 6.14.0 -f helm/podinfo-values.yaml > /tmp/podinfo.yaml
grep -E '^kind:' /tmp/podinfo.yaml
grep -E 'replicas:|PODINFO_UI_COLOR|PODINFO_UI_MESSAGE' -A1 /tmp/podinfo.yaml | head -8
```

- `helm template` : 클러스터에 보내지 않고 **완성된 YAML만** 만든다

> **🟢 확인: 보이는 것**
>
> ```text
> kind: Service
> kind: Deployment
> ```
> ```text
>   replicas: 2
> --
>         - name: PODINFO_UI_COLOR
>           value: "#0E7C86"
>         - name: PODINFO_UI_MESSAGE
>           value: "DevMart 4주차 — Helm으로 설치했습니다"
> ```
> 내 values의 `ui.message`가 Deployment의 **환경 변수**가 되었습니다(3주차 5일차의 `env:`). 이렇게 "values의 어느 값이 어느 리소스의 어느 칸이 되는가"를 확인하는 것이 `helm template`의 쓸모입니다. 설치 전에 항상 한 번 봅니다.

## 실습 3 · 설치하고 확인하기

### 단계 1 — 설치

```bash
helm install podinfo $CHART --version 6.14.0 -f helm/podinfo-values.yaml --wait
```

- `podinfo` (첫 번째) : **릴리스 이름**. 같은 차트를 다른 이름으로 여러 번 설치할 수 있다 (6교시)
- `-f 파일` : 내 values
- `--wait` : 리소스가 **준비될 때까지** 기다렸다가 끝낸다 (3주차 4일차의 `rollout status`를 대신)

> **🟢 확인: 보이는 것**
>
> ```text
> Pulled: ghcr.io/stefanprodan/charts/podinfo:6.14.0
> Digest: sha256:…
> NAME: podinfo
> LAST DEPLOYED: Mon Nov 30 10:12:03 2026
> NAMESPACE: default
> STATUS: deployed
> REVISION: 1
> ...
> NOTES:
> 1. Get the application URL by running these commands:
>   echo "Visit http://127.0.0.1:8080 to use your application"
>   kubectl -n default port-forward deploy/podinfo 8080:9898
> ```
> **NOTES**는 차트 제작자가 남긴 사용 안내입니다. 처음 쓰는 차트라면 꼭 읽습니다.

### 단계 2 — Helm 쪽에서 보기

```bash
helm list
helm status podinfo | head -6
helm get values podinfo
```

> **🟢 확인: 보이는 것**
>
> ```text
> NAME     NAMESPACE  REVISION  UPDATED                                 STATUS    CHART           APP VERSION
> podinfo  default    1         2026-11-30 10:12:03.48 +0900 KST        deployed  podinfo-6.14.0  6.14.0
> ```
> ```text
> USER-SUPPLIED VALUES:
> replicaCount: 2
> resources: …
> ui:
>   color: '#0E7C86'
>   message: DevMart 4주차 — Helm으로 설치했습니다
> ```
> `helm get values`는 **내가 준 값만** 보여 줍니다. 차트 기본값까지 모두 보려면 `--all`.

### 단계 3 — Kubernetes 쪽에서 보기

```bash
kubectl get deployment,service,pod -l app.kubernetes.io/name=podinfo
kubectl get secret -l owner=helm
```

> **🟢 확인: 보이는 것**
>
> ```text
> NAME                      READY   UP-TO-DATE   AVAILABLE   AGE
> deployment.apps/podinfo   2/2     2            2           40s
>
> NAME              TYPE        CLUSTER-IP     EXTERNAL-IP   PORT(S)             AGE
> service/podinfo   ClusterIP   10.96.51.9     <none>        9898/TCP,9999/TCP   40s
> ...
> NAME                            TYPE                 DATA   AGE
> sh.helm.release.v1.podinfo.v1   helm.sh/release.v1   1      40s
> ```
> - 만들어진 것은 3주차에 손으로 쓰던 **Deployment와 Service**입니다.
> - 릴리스 이력은 **Secret**으로 클러스터에 저장됩니다(`.v1` = revision 1). Helm 실행 파일은 상태를 따로 갖지 않습니다 — 다른 사람이 다른 노트북에서 `helm list`를 해도 같은 것이 보이는 이유입니다.
> - 라벨 `app.kubernetes.io/name`은 Kubernetes가 권하는 **공통 라벨**입니다. 잘 만든 차트는 이 라벨을 붙입니다.

### 단계 4 — 접속

```bash
kubectl port-forward service/podinfo 9898:9898
```

```bash
# 다른 터미널
curl -s localhost:9898 | grep -E '"(hostname|version|message|color)"'
```

> **🟢 확인: 보이는 것**
>
> ```text
>   "hostname": "podinfo-7b9c8d6f5-k2x8p",
>   "version": "6.14.0",
>   "color": "#0E7C86",
>   "message": "DevMart 4주차 — Helm으로 설치했습니다",
> ```
> 브라우저로 **http://localhost:9898** 을 열면 청록색 화면에 메시지가 보입니다. 확인 후 port-forward는 Ctrl+C.

## 실습 4 · 바꾸기 · 망가뜨리기 · 되돌리기

### 단계 1 — values 파일을 고쳐 업그레이드

```bash
sed -i 's/replicaCount: 2/replicaCount: 3/; s/Helm으로 설치했습니다/upgrade로 바꿨습니다/' helm/podinfo-values.yaml   # Mac: sed -i ''
helm upgrade podinfo $CHART --version 6.14.0 -f helm/podinfo-values.yaml --wait
helm history podinfo
```

> **🟢 확인: 보이는 것**
>
> ```text
> Release "podinfo" has been upgraded. Happy Helming!
> NAME: podinfo
> ...
> REVISION: 2
> ```
> ```text
> REVISION  UPDATED                   STATUS      CHART           APP VERSION  DESCRIPTION
> 1         Mon Nov 30 10:12:03 2026  superseded  podinfo-6.14.0  6.14.0       Install complete
> 2         Mon Nov 30 10:20:41 2026  deployed    podinfo-6.14.0  6.14.0       Upgrade complete
> ```
> Deployment의 템플릿(환경 변수)이 바뀌었으니, 그 아래에서는 3주차 4일차의 **롤링 업데이트**가 일어났습니다.

> [!TIP]
> **업그레이드 전에 차이 보기**
>
> `helm upgrade`가 정확히 무엇을 바꿀지 미리 보고 싶으면 **helm-diff 플러그인**(`helm diff upgrade …`)을 씁니다. 실무에서는 거의 필수입니다.

### 단계 2 — 망가진 업그레이드

이미지 태그를 없는 값으로 바꿔 업그레이드합니다. 이번엔 파일이 아니라 `--set`으로 — **일부러 나쁜 습관으로** 합니다.

```bash
helm upgrade podinfo $CHART --version 6.14.0 -f helm/podinfo-values.yaml \
  --set image.tag=0.0.0-nope --wait --timeout 60s
```

- `--set 키=값` : 이번 한 번만 값을 덮어쓴다 — 파일에 남지 않는다
- `--timeout 60s` : `--wait`가 기다릴 최대 시간

> **🟢 확인: 60초 뒤**
>
> ```text
> Error: UPGRADE FAILED: … not ready … context deadline exceeded
> ```

```bash
helm history podinfo
kubectl get pods -l app.kubernetes.io/name=podinfo
```

> **🟢 확인: 보이는 것**
>
> ```text
> REVISION  …  STATUS      …  DESCRIPTION
> 1         …  superseded  …  Install complete
> 2         …  superseded  …  Upgrade complete
> 3         …  failed      …  Upgrade "podinfo" failed: … context deadline exceeded
> ```
> ```text
> NAME                        READY   STATUS             RESTARTS   AGE
> podinfo-6d8f9c7b5-xq2kt     0/1     ImagePullBackOff   0          65s
> podinfo-7c5b9d8f4-2m9wz     1/1     Running            0          5m
> podinfo-7c5b9d8f4-h7v4c     1/1     Running            0          5m
> podinfo-7c5b9d8f4-r8n3s     1/1     Running            0          5m
> ```
> Helm은 **실패**를 기록했지만, 클러스터는 3주차 4일차 7교시의 **'멈춘 배포'** 상태입니다. 옛 Pod 셋이 계속 일하고 있습니다. Helm의 실패 = 서비스 장애는 아닙니다.

### 단계 3 — 되돌리기

```bash
helm rollback podinfo 2 --wait
helm history podinfo | tail -2
kubectl get pods -l app.kubernetes.io/name=podinfo
```

> **🟢 확인: 보이는 것**
>
> ```text
> Rollback was a success! Happy Helming!
> 3         …  failed      …  Upgrade "podinfo" failed: …
> 4         …  deployed    …  Rollback to 2
> ```
> 망가진 Pod가 사라지고 3개가 남습니다. 되돌리기도 **새 revision(4)**으로 기록됩니다 — 3주차 4일차의 `rollout undo`와 같은 방식입니다.

| | `kubectl rollout undo` (3주차 4일차) | `helm rollback` |
|---|---|---|
| 되돌리는 범위 | Deployment **하나**의 Pod 템플릿 | 릴리스에 속한 **모든 리소스** (Service · ConfigMap · Deployment …) |
| 기록 위치 | 옛 ReplicaSet | Helm 릴리스 Secret |
| 이번처럼 Deployment만 바뀐 경우 | 똑같이 된다 | 똑같이 된다 |
| ConfigMap도 함께 바뀐 경우 | ConfigMap은 그대로 | 함께 되돌린다 |

> [!WARNING]
> **--set으로 망가뜨린 값은 어디에?**
>
> revision 3의 `image.tag=0.0.0-nope`는 values **파일에 없습니다.** 다음 사람이 파일로 `helm upgrade`를 하면 문제없이 올라가겠지만, "3번은 왜 실패했지?"를 파일에서 찾을 수 없습니다. `helm get values podinfo --revision 3`으로만 보입니다. 운영에서 `--set`을 쓰지 않는 이유입니다.

### 단계 4 — 지우기 연습

같은 차트를 다른 이름으로 하나 더 설치하고 지워 봅니다. **podinfo 릴리스는 6교시에 쓰니 남겨 둡니다.**

```bash
helm install tmp $CHART --version 6.14.0 --set replicaCount=1 --wait
helm list
helm uninstall tmp
helm list
kubectl get secret -l owner=helm,name=tmp
```

> **🟢 확인: 보이는 것**
>
> ```text
> NAME     NAMESPACE  REVISION  …  STATUS    CHART
> podinfo  default    4         …  deployed  podinfo-6.14.0
> tmp      default    1         …  deployed  podinfo-6.14.0
> release "tmp" uninstalled
> NAME     NAMESPACE  REVISION  …
> podinfo  default    4         …
> No resources found in default namespace.
> ```
> `helm uninstall`은 릴리스가 만든 리소스와 **이력 Secret까지** 지웁니다. 이력을 남기고 싶으면 `--keep-history`.

> **🎓 학술 노트 — 변경은 원자적이어야 하는가**
>
> 데이터베이스의 **트랜잭션**은 여러 변경을 '모두 되거나, 하나도 안 되거나'(원자성, atomicity)로 묶습니다(Gray & Reuter, *Transaction Processing*, 1992). Helm의 업그레이드는 그렇지 않습니다 — 리소스 열 개 중 셋이 바뀐 뒤 실패하면 **중간 상태**로 남습니다. 오늘 revision 3이 그랬습니다. Helm 4의 `--rollback-on-failure`(옛 `--atomic`)는 실패하면 자동으로 되돌려 원자성을 **흉내** 내지만, 되돌리는 동안의 중간 상태는 피할 수 없습니다. 분산 시스템에서 진짜 원자적 배포는 매우 어렵고, 그래서 실무는 "작게 바꾸고, 실패를 빨리 감지하고, 되돌릴 수 있게"(3주차 4일차 학술 노트)로 접근합니다.

> **📈 트렌드 2026 — 차트도 서명하고 검증한다**
>
> podinfo 차트는 **Sigstore cosign으로 서명**되어 GHCR에 올라갑니다. `cosign verify ghcr.io/stefanprodan/charts/podinfo:6.14.0 …`로 "정말 그 제작자가 GitHub Actions에서 만든 차트인가"를 확인할 수 있습니다(2주차 2일차의 SLSA · 출처 증명과 같은 흐름). 또, 2025년 Bitnami가 무료 차트 · 이미지 정책을 바꾸면서 많은 회사가 "어떤 차트 저장소를 믿을지"를 다시 정했습니다. 차트도 **남의 코드**라는 2주차 2일차의 교훈이 그대로 적용됩니다.

> **✅ 확인 문제**
>
> 1. `helm template`과 `helm install`의 차이는?
> 2. 차트의 `version`과 `appVersion`은 각각 무엇의 버전인가요?
> 3. Helm 릴리스 이력은 어디에 저장되나요? 그래서 생기는 장점은?
> 4. 업그레이드가 실패했는데 서비스가 멀쩡했던 이유는?
> 5. `--set`으로 바꾼 값의 문제점은?
>
> <details><summary>정답</summary>
>
> 1. `template`은 완성된 YAML을 만들기만 하고, `install`은 그것을 클러스터에 보내고 릴리스를 기록한다
> 2. `version` — 차트 자체, `appVersion` — 차트가 설치하는 앱
> 3. 그 네임스페이스의 Secret (`sh.helm.release.v1.이름.vN`). 누가 어디서 helm을 실행해도 같은 이력을 본다
> 4. 새 Pod가 준비되지 않아 롤링 업데이트가 멈췄고, 옛 Pod가 계속 일했다 (3주차 4일차 '멈춘 배포')
> 5. 파일에 남지 않아, 다음 업그레이드에서 사라지거나 왜 그렇게 했는지 추적할 수 없다
>
> </details>

## 참고 문헌

- Helm Docs. *Helm Commands — install · upgrade · rollback · history · template · uninstall*. helm.sh/docs/helm
- Helm Docs. *Use OCI-based registries*. helm.sh/docs/topics/registries
- Kubernetes Docs. *Recommended Labels*. kubernetes.io/docs/concepts/overview/working-with-objects/common-labels
- Prodan, S. *podinfo*. github.com/stefanprodan/podinfo
- Gray, J., & Reuter, A. (1992). *Transaction Processing: Concepts and Techniques*. Morgan Kaufmann.

---

| 이전 | 목차 | 다음 |
|:--|:--:|--:|
| ⬅️ [1교시 · 3주차 요약 + Helm 개념](lesson-01.md) | [⬆️ 1일차 목차](README.md) | [3교시 · Ingress의 역사와 ingress-nginx 은퇴](lesson-03.md) ➡️ |
