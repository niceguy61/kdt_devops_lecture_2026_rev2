[🏠 과정 목차](../../README.md) › [4주차](../README.md) › [4일차](README.md)

# 2교시 · Istio 설치와 메시 등록

> [!NOTE]
> **이번 시간에 할 일**
>
> - `istioctl`을 설치하고, 클러스터가 Istio를 받을 준비가 되었는지 검사합니다.
> - ambient에 필요한 **네 차트**(base · istiod · cni · ztunnel)를 순서대로 설치합니다.
> - DevMart 네임스페이스에 **라벨 하나를 커밋**해서 메시에 넣습니다.
> - Pod가 **재시작 없이** 메시에 들어간 것을 확인합니다.

## 무엇을 설치하나

| 차트 | 만들어지는 것 | 하는 일 |
|---|---|---|
| `base` | CRD (VirtualService · AuthorizationPolicy · PeerAuthentication …) | Istio의 "말"을 Kubernetes에 가르친다 |
| `istiod` | Deployment `istiod` | **두뇌** — 설정을 프록시들에 나눠 주고(xDS), 인증서를 발급(CA) |
| `cni` | DaemonSet `istio-cni-node` | 메시에 넣은 Pod의 트래픽을 ztunnel로 **돌려 놓는다** |
| `ztunnel` | DaemonSet `ztunnel` | 노드마다 하나 — L4 프록시, mTLS |

Gateway API CRD는 1일차 Envoy Gateway 설치 때 이미 들어 있습니다 — Istio도 같은 CRD를 씁니다(4교시 waypoint).

## 실습 1 · istioctl과 사전 검사

```bash
mkdir -p ~/devops-lab/k8s/w4d4 && cp -r ~/course/labs/week4/day4/* ~/devops-lab/k8s/w4d4/
cd ~/devops-lab/k8s/w4d4
ISTIO=1.31.0          # 그날의 최신 1.31.x를 github.com/istio/istio/releases 에서 확인해 바꾼다
echo "istio $ISTIO" | tee -a VERSIONS.txt
```

**Linux · WSL2 Ubuntu (bash)**

```bash
curl -sL https://istio.io/downloadIstio | ISTIO_VERSION=$ISTIO TARGET_ARCH=x86_64 sh -
sudo install -m 555 istio-$ISTIO/bin/istioctl /usr/local/bin/istioctl
```

**Mac (터미널 · Homebrew)** — brew는 그날의 최신 istioctl을 깝니다. 버전을 맞추려면 위 Linux 명령에서 `TARGET_ARCH=arm64`(Apple Silicon)로 바꿔 씁니다.

```bash
brew install istioctl
```

**확인 (공통)**

```bash
istioctl version --remote=false
istioctl x precheck
```

> [!TIP]
> **다른 설치 방법 — winget · 직접 다운로드**
>
> | 방법 | 어디서 | 명령 · 주소 |
> |---|---|---|
> | winget | Windows PowerShell | 없음 — winget의 `Istio.Istio`는 1.17에서 멈춤 |
> | 직접 다운로드 | 브라우저 | [github.com/istio/istio/releases](https://github.com/istio/istio/releases) — `istioctl-1.31.x-win.zip` · `-osx-arm64.tar.gz` |
>
> winget은 **Windows 쪽**에 설치하므로 PowerShell에서만 보입니다. 수업 명령은 WSL Ubuntu(bash)에서 치므로, Windows 사용자도 위의 **WSL 방법**으로 설치합니다. 전체 목록은 **부록 A · 도구 설치 가이드**.

> **🟢 확인: 확인**
>
> ```text
> client version: 1.31.0
> ✔ No issues found when checking the cluster. Istio is safe to install or upgrade!
> ```

> [!WARNING]
> **Kubernetes 버전 경고가 나온다면**
>
> Istio 1.31이 **공식 지원하는 Kubernetes는 1.32~1.36**입니다. 우리 kind는 1.37(3주차 3일차)이라 precheck가 "지원 범위 밖"을 경고할 수 있습니다. Istio는 새 Kubernetes 버전에서 대개 동작하지만 **시험을 거치지 않았다**는 뜻입니다. 실습은 진행하고, 운영이라면 **Istio가 지원하는 버전까지만** 클러스터를 올립니다 — 메시처럼 클러스터 깊숙이 들어가는 도구가 업그레이드 순서를 정합니다(7교시).

## 실습 2 · 네 차트 설치

순서가 중요합니다 — CRD(base) → 두뇌(istiod) → 트래픽 돌리기(cni) → 프록시(ztunnel).

```bash
cat istio/istiod-values.yaml
CH=oci://ghcr.io/istio/release/charts
helm install istio-base $CH/base    -n istio-system --create-namespace --version $ISTIO --wait
helm install istiod     $CH/istiod  -n istio-system --version $ISTIO -f istio/istiod-values.yaml --wait
helm install istio-cni  $CH/cni     -n istio-system --version $ISTIO -f istio/cni-values.yaml --wait
helm install ztunnel    $CH/ztunnel -n istio-system --version $ISTIO -f istio/ztunnel-values.yaml --wait
kubectl get pods -n istio-system -o wide
```

> **🟢 확인: 확인 (3~4분)**
>
> ```text
> NAME                      READY   STATUS    RESTARTS   AGE   IP           NODE
> istio-cni-node-5qk2m      1/1     Running   0          1m    172.18.0.3   devmart-worker
> istio-cni-node-8wz7d      1/1     Running   0          1m    172.18.0.4   devmart-worker2
> istio-cni-node-r2x9t      1/1     Running   0          1m    172.18.0.2   devmart-control-plane
> istiod-7c8b9d6f5-m4q8p    1/1     Running   0          2m    10.244.1.21  devmart-worker
> ztunnel-4hn7s             1/1     Running   0          40s   10.244.2.30  devmart-worker2
> ztunnel-9kq2w             1/1     Running   0          40s   10.244.1.22  devmart-worker
> ztunnel-tq6m3             1/1     Running   0          40s   10.244.0.9   devmart-control-plane
> ```
> cni와 ztunnel이 **노드마다 하나**(DaemonSet, 3주차 3일차)입니다. cni의 IP가 노드 IP와 같은 것은 `hostNetwork`로 노드에 직접 붙어 일하기 때문입니다.

| values에서 바꾼 것 | 이유 |
|---|---|
| `profile: ambient` (istiod · cni) | ambient에 맞는 기본값 묶음 — 이것이 없으면 sidecar 모드로 설치된다 |
| `pilot.resources` | istiod 기본 요청이 커서 kind에 맞게 줄였다 |
| `meshConfig.accessLogFile` | 프록시가 요청마다 한 줄씩 로그를 남긴다 (5교시) |

> [!TIP]
> **OCI 차트 주소**
>
> Istio는 1.31부터 차트 · 이미지를 구글 클라우드 저장소에서 옮겼습니다. 오래된 블로그의 `https://istio-release.storage.googleapis.com/charts`는 2026년 12월 이후 동작하지 않습니다. 공식 문서의 `oci://ghcr.io/istio/release/charts`를 씁니다(1일차 podinfo와 같은 OCI 방식).

## 실습 3 · DevMart를 메시에 — 커밋 하나

메시에 넣는 방법은 **네임스페이스에 라벨 하나**입니다. 네임스페이스는 배포 저장소의 `namespace.yaml`이 관리하므로, 그 파일을 바꿔 커밋합니다.

```bash
kubectl get pods -n devmart -o custom-columns=NAME:.metadata.name,AGE:.metadata.creationTimestamp > /tmp/before.txt
cd ~/devmart-deploy
cp ~/devops-lab/k8s/w4d4/deploy/namespace.yaml devmart/namespace.yaml
git diff
git commit -am "devmart를 Istio ambient 메시에 등록"
git push
```

> **🟢 확인: git diff**
>
> ```diff
>  metadata:
>    name: devmart
> +  labels:
> +    istio.io/dataplane-mode: ambient     # 이 네임스페이스의 Pod를 메시에 넣는다
> +    # istio.io/use-waypoint: waypoint    # 4교시에 앞의 # 를 지운다 — L7 기능은 waypoint를 거친다
> ```

1분 안에 Argo CD가 반영합니다. 확인합니다.

```bash
sleep 60
kubectl get ns devmart --show-labels
istioctl ztunnel-config workloads | grep -E "NAMESPACE|devmart"
diff /tmp/before.txt <(kubectl get pods -n devmart -o custom-columns=NAME:.metadata.name,AGE:.metadata.creationTimestamp) && echo "재시작 없음"
```

> **🟢 확인: 확인**
>
> ```text
> NAME      STATUS   AGE   LABELS
> devmart   Active   9d    istio.io/dataplane-mode=ambient,kubernetes.io/metadata.name=devmart
> NAMESPACE  POD NAME                       ADDRESS      NODE             WAYPOINT  PROTOCOL
> devmart    catalog-api-5d8c7b9f6-2xkq4    10.244.1.15  devmart-worker   None      HBONE
> devmart    catalog-api-5d8c7b9f6-8wm3p    10.244.2.17  devmart-worker2  None      HBONE
> devmart    db-6b7f8c9d5-q4w2e             10.244.1.12  devmart-worker   None      HBONE
> devmart    order-api-…                    …            …                None      HBONE
> …
> 재시작 없음
> ```
> - **PROTOCOL HBONE** — 이 Pod로 오가는 트래픽은 이제 ztunnel이 mTLS 터널(HBONE)로 감쌉니다.
> - **WAYPOINT None** — 아직 L7 프록시는 없습니다(4교시).
> - Pod 이름과 생성 시각이 그대로입니다. sidecar 모드였다면 모든 Pod가 다시 만들어졌을 것입니다.

```bash
curl -s -o /dev/null -w '%{http_code}\n' localhost:30080/api/products
curl -s -X POST localhost:30080/api/orders -H 'content-type: application/json' -d '{"product_id":1,"quantity":1}'; echo
```

> **🟢 확인: 확인**
>
> `200`, 그리고 `{"order_id":…,"status":"pending",…}`. 손님 쪽에서는 **아무것도 바뀌지 않았습니다.** 그래야 정상입니다.

> **🛠️ 막혔다면: 주문이 503이라면**
>
> `kubectl logs -n istio-system ds/istio-cni-node | tail`에 오류가 있는지, `istioctl ztunnel-config workloads`에서 devmart Pod가 `HBONE`인지 봅니다. 급하면 **Git에서 라벨을 되돌립니다**(`git revert HEAD && git push`) — 라벨을 빼면 Pod는 재시작 없이 메시 밖으로 나옵니다. 되돌리기 쉬운 것이 ambient의 장점입니다.

> **🎓 학술 노트 — 데이터 평면과 제어 평면**
>
> 네트워크 장비는 오래전부터 **데이터 평면**(패킷을 실제로 나르는 곳)과 **제어 평면**(어디로 나를지 정하는 곳)을 나눠 설계되었습니다. 이것을 소프트웨어로 완전히 떼어 낸 것이 **SDN**(Software-Defined Networking)이고, McKeown 외의 *OpenFlow*(SIGCOMM CCR, 2008)가 그 출발점입니다. Istio에서 istiod가 제어 평면, ztunnel · waypoint가 데이터 평면입니다. istiod가 잠시 죽어도 이미 받은 설정으로 트래픽은 계속 흐릅니다 — 3주차 3일차에 "컨트롤 플레인이 죽어도 Pod는 산다"와 같은 원리입니다.

> **📈 트렌드 2026 — 메시를 '켜는' 것이 쉬워졌다**
>
> ambient 이전에는 메시 도입이 "모든 Pod 재시작 + 사이드카 메모리 + 앱마다 호환성 확인"이라는 큰 공사였습니다. 이제는 라벨 하나로 넣고 빼므로, **보안팀이 mTLS만 먼저 켜고**(L4) L7은 필요한 팀만 나중에 붙이는 단계적 도입이 흔해졌습니다. AWS · GKE · AKS 모두 ambient를 지원하는 관리형 메시 선택지를 내놓았습니다.

> **✅ 확인 문제**
>
> 1. 네 차트의 설치 순서와 그 이유는?
> 2. 메시에 넣는 방법과, 그것을 kubectl이 아니라 커밋으로 한 이유는?
> 3. `PROTOCOL HBONE`의 뜻은?
> 4. 메시 등록 뒤 문제가 생기면 가장 빨리 되돌리는 방법은?
>
> <details><summary>정답</summary>
>
> 1. base(CRD) → istiod(두뇌) → cni(트래픽 돌리기) → ztunnel(프록시). 앞의 것이 있어야 뒤의 것이 동작한다
> 2. 네임스페이스에 `istio.io/dataplane-mode=ambient` 라벨. 네임스페이스를 Argo CD(배포 저장소)가 관리하므로
> 3. 그 Pod로 오가는 트래픽을 ztunnel이 mTLS 터널(HTTP/2 CONNECT)로 감싼다
> 4. 배포 저장소에서 라벨 커밋을 revert — Pod 재시작 없이 메시 밖으로 나온다
>
> </details>

## 참고 문헌

- Istio Docs. *Install with Helm (ambient)*, *Platform-Specific Prerequisites — kind*. istio.io/latest/docs/ambient/install
- Istio Docs. *Supported Releases*. istio.io/latest/docs/releases/supported-releases
- McKeown, N. 외 (2008). *OpenFlow: Enabling Innovation in Campus Networks*. ACM SIGCOMM CCR 38(2).

---

⬅️ 이전: [1교시 · 3일차 요약 + 서비스 메시](lesson-01.md) &nbsp;|&nbsp; [⬆️ 4일차 목차](README.md) &nbsp;|&nbsp; 다음: [3교시 · mTLS 확인과 Kiali](lesson-03.md) ➡️
