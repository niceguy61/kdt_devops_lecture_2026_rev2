# 8교시 · 메시 문제 해결 — istioctl로 진단하기

!!! goal "이번 시간에 할 일"
    - 배포 저장소와 상관없는 **연습용 네임스페이스**(`mesh-lab`)에서 메시 장애를 마음껏 만들고 고칩니다.
    - **등록 누락 · 아무 데도 안 걸린 정책 · 신원 오타** 세 가지 장애를 서로 다른 증상으로 구분합니다.
    - `istioctl analyze`(설정 검사), `ztunnel-config`(누가 메시 안인가), ztunnel 로그(누가 누구를 거절했나), `waypoint list` · `proxy-status`(L7 프록시 상태)를 쓰는 순서를 익힙니다.
    - 메시 때문인지 아닌지 가를 때 쓰는 **"잠깐 빼 보기"**를 연습합니다.

!!! key "메시 장애가 어려운 이유"
    메시는 요청을 **코드 밖에서** 가로챕니다. 그래서 앱 로그에는 아무것도 없는데 요청이 끊기거나(`Connection reset`), 정책을 썼는데 아무 일도 안 일어납니다. 오늘의 규칙은 하나입니다. **"메시가 무엇을 보고 있는지 메시에게 물어본다."**

!!! warn "devmart에서는 하지 않는다"
    devmart의 메시 설정은 Argo CD가 배포 저장소대로 지킵니다(3일차). `kubectl`로 고쳐도 되돌아가고, 잘못 건드리면 사이트가 멈춥니다. 오늘 장애는 모두 **`mesh-lab`**에서 만듭니다.

## 실습 21 · 연습장 만들기

```bash
kubectl create namespace mesh-lab
kubectl label namespace mesh-lab istio.io/dataplane-mode=ambient
kubectl create serviceaccount client -n mesh-lab
kubectl create deployment server -n mesh-lab --image=ghcr.io/stefanprodan/podinfo:6.14.0 --port=9898
kubectl expose deployment server -n mesh-lab --port=9898
kubectl run client -n mesh-lab --image=nicolaka/netshoot:v0.17 \
  --overrides='{"spec":{"serviceAccountName":"client"}}' -- sleep infinity
kubectl wait -n mesh-lab --for=condition=Available deploy/server --timeout=90s
kubectl wait -n mesh-lab --for=condition=Ready pod/client --timeout=90s
kubectl exec -n mesh-lab client -- curl -s -m 3 -o /dev/null -w '%{http_code}\n' server:9898/
istioctl ztunnel-config workloads | grep -E "NAMESPACE|mesh-lab"
```

!!! check "이렇게 나오면 성공"
    ```text
    200
    NAMESPACE  POD NAME                  ADDRESS      NODE            WAYPOINT  PROTOCOL
    mesh-lab   client                    10.244.1.21  devmart-worker  None      HBONE
    mesh-lab   server-6c8f…-x2k9p        10.244.2.30  devmart-worker2 None      HBONE
    ```
    `HBONE` = ztunnel이 mTLS로 감싸 주는 **메시 안**입니다(2교시).

## 실습 22 · 장애 세 가지

### 장애 A — 등록이 빠졌다

```bash
kubectl label namespace mesh-lab istio.io/dataplane-mode-
sleep 5
istioctl ztunnel-config workloads | grep -E "NAMESPACE|mesh-lab"
kubectl exec -n mesh-lab client -- curl -s -m 3 -o /dev/null -w '%{http_code}\n' server:9898/
```

!!! check "증상"
    ```text
    mesh-lab   client               …  None   TCP
    mesh-lab   server-6c8f…-x2k9p   …  None   TCP
    200
    ```
    **요청은 된다**가 함정입니다. `PROTOCOL`이 `TCP` — 암호화도 신원도 없는 **평문**으로 돌고 있습니다. 6교시처럼 상대가 STRICT라면 그때 가서야 끊깁니다. "메시에 들어 있다고 믿었는데 아니었다"는 `ztunnel-config workloads`로만 보입니다.

```bash
kubectl label namespace mesh-lab istio.io/dataplane-mode=ambient
sleep 5 && istioctl ztunnel-config workloads | grep mesh-lab | awk '{print $2, $NF}'
```

### 장애 B — 정책이 아무 데도 안 걸렸다

"`server`는 `client`만 부를 수 있다"는 허가 규칙을 씁니다. 그런데 라벨에 오타가 있습니다.

```bash
cat <<'EOF' | kubectl apply -f -
apiVersion: security.istio.io/v1
kind: AuthorizationPolicy
metadata:
  name: server-allow-client
  namespace: mesh-lab
spec:
  selector:
    matchLabels:
      app: sever                      # 오타! (server)
  action: ALLOW
  rules:
    - from:
        - source:
            principals: ["cluster.local/ns/mesh-lab/sa/client"]
EOF
kubectl run stranger -n mesh-lab --image=nicolaka/netshoot:v0.17 --restart=Never -- sleep 300
kubectl wait -n mesh-lab --for=condition=Ready pod/stranger --timeout=60s
kubectl exec -n mesh-lab stranger -- curl -s -m 3 -o /dev/null -w '%{http_code}\n' server:9898/
```

!!! check "증상"
    ```text
    200
    ```
    `client`만 허락했는데 **낯선 Pod(`stranger`, sa/default)도 들어옵니다.** 에러도 없습니다 — 정책이 **아무 Pod에도 걸리지 않았기** 때문입니다.

```bash
istioctl analyze -n mesh-lab
```

!!! check "메시에게 물어보면"
    ```text
    Warning [IST0127] (AuthorizationPolicy mesh-lab/server-allow-client) No matching workloads for this resource with the following labels: app=sever
    ```
    `analyze`는 클러스터의 Istio 설정을 읽고 **말이 안 되는 곳**을 찾아 줍니다. 고칩니다.

```bash
kubectl patch authorizationpolicy server-allow-client -n mesh-lab --type=merge \
  -p '{"spec":{"selector":{"matchLabels":{"app":"server"}}}}'
istioctl analyze -n mesh-lab
kubectl exec -n mesh-lab stranger -- curl -s -m 3 -o /dev/null -w '%{http_code}\n' server:9898/; echo "종료 코드: $?"
kubectl exec -n mesh-lab client   -- curl -s -m 3 -o /dev/null -w '%{http_code}\n' server:9898/
```

!!! check "이렇게 나오면 성공"
    ```text
    ✔ No validation issues found when analyzing namespace: mesh-lab.
    000
    종료 코드: 56
    200
    ```
    낯선 Pod는 **연결이 끊기고**(`56` = 받다가 끊김), `client`만 들어갑니다. ztunnel이 L4에서 신원을 보고 거절했습니다.

### 장애 C — 신원 오타: 아무도 못 들어온다

이번에는 허가할 신원에 오타를 넣습니다(`client` → `clinet`).

```bash
kubectl patch authorizationpolicy server-allow-client -n mesh-lab --type=json \
  -p '[{"op":"replace","path":"/spec/rules/0/from/0/source/principals/0","value":"cluster.local/ns/mesh-lab/sa/clinet"}]'
kubectl exec -n mesh-lab client -- curl -s -m 3 -o /dev/null -w '%{http_code}\n' server:9898/
istioctl analyze -n mesh-lab
kubectl logs -n istio-system -l app=ztunnel --since=1m --tail=-1 | grep -i "mesh-lab" | grep -iE "deny|denied|reject" | tail -2
```

!!! check "증상"
    ```text
    000
    ✔ No validation issues found when analyzing namespace: mesh-lab.
    … error="connection closed due to policy rejection" src.identity="spiffe://cluster.local/ns/mesh-lab/sa/client" dst.workload="server-6c8f…" …
    ```
    - 이번엔 `analyze`도 조용합니다 — `clinet`이라는 신원이 **없다는 것**까지는 알 수 없기 때문입니다
    - **ztunnel 로그**가 답입니다. 들어온 쪽의 신원은 `sa/client`인데 정책은 다른 이름을 기다렸습니다. 3교시에 SPIFFE ID를 읽어 둔 이유입니다

```bash
kubectl patch authorizationpolicy server-allow-client -n mesh-lab --type=json \
  -p '[{"op":"replace","path":"/spec/rules/0/from/0/source/principals/0","value":"cluster.local/ns/mesh-lab/sa/client"}]'
kubectl exec -n mesh-lab client -- curl -s -m 3 -o /dev/null -w '%{http_code}\n' server:9898/
```

## 실습 23 · L7 프록시 상태 보기 (devmart, 읽기만)

```bash
istioctl waypoint list -n devmart
istioctl proxy-status
istioctl analyze -n devmart
```

!!! check "보이는 것 (이름 뒷부분은 다름)"
    ```text
    NAME       REVISION   PROGRAMMED
    waypoint   default    True
    NAME                                  CLUSTER      ISTIOD                VERSION   SUBSCRIBED TYPES
    waypoint-7f9c…-k2x8p.devmart          Kubernetes   istiod-6b8d…-m4n7p    1.31.0    4 (CDS,LDS,EDS,RDS)
    ✔ No validation issues found when analyzing namespace: devmart.
    ```
    - `proxy-status`는 istiod가 설정을 보내 주는 **Envoy들**(waypoint)의 목록입니다. ztunnel은 다른 방식(노드 단위)으로 설정을 받으므로 여기 없고, `ztunnel-config`로 봅니다
    - 4교시의 90/10 나누기나 5교시의 장애 주입이 "적용이 안 된 것 같다"면, 먼저 **waypoint가 PROGRAMMED인지**, 서비스에 `istio.io/use-waypoint` 라벨이 있는지 봅니다

## 진단 순서 — 한 장

| 증상 | 먼저 | 그다음 |
|---|---|---|
| 되긴 하는데 메시가 안 하는 것 같다 | `ztunnel-config workloads` — `HBONE`인가 `TCP`인가 | 네임스페이스 · Pod 라벨 |
| 정책을 썼는데 아무 변화 없음 | `istioctl analyze` — IST0127 같은 경고 | 셀렉터 · `targetRefs` 오타 |
| `Connection reset` · 000 · 56 | ztunnel 로그의 `policy rejection` · `src.identity` | 정책의 principals · namespaces |
| L7 규칙(나누기 · 재시도 · 장애 주입)이 안 먹음 | `waypoint list` · `proxy-status` | `istio.io/use-waypoint` 라벨 |
| 메시 때문인지조차 모르겠다 | **잠깐 빼 보기** — 연습장에서 라벨을 빼고 재현 | 운영은 Git에서 라벨을 되돌리는 커밋(2교시) |

!!! cleanup "정리"
    ```bash
    kubectl delete namespace mesh-lab
    ```
    devmart의 메시는 그대로 둡니다(7교시의 "남긴다" 표).

!!! academic "학술 노트 — 분산 시스템 디버깅은 '보이게 하기'다 (Beschastnikh 외, 2016)"
    워싱턴대 등 연구진은 CACM에 실은 「Debugging Distributed Systems」(2016)에서, 분산 시스템의 버그가 어려운 이유를 **동시성 · 부분 실패 · 관찰의 어려움**으로 정리하고, 실무에서 쓰는 방법을 로그 분석 · 추적 · 모델 검사 · **설정 검증** 등으로 나눠 비교했습니다. 결론은 어느 하나로 충분하지 않고, 시스템이 **스스로 자기 상태를 말하게** 만드는 도구를 겹쳐 써야 한다는 것이었습니다. 오늘의 네 도구가 정확히 그 겹침입니다 — `analyze`(설정 검증), `ztunnel-config`(실제 상태), ztunnel 로그(사건 기록), `proxy-status`(설정 배포 상태).

    - Beschastnikh, I., Wang, P., Brun, Y., & Ernst, M. D. (2016). Debugging distributed systems. *Communications of the ACM*, 59(8), 32–37.

!!! trend "트렌드 — 메시 진단도 노드 단위로"
    사이드카 시절에는 Pod마다 Envoy가 있어 `istioctl proxy-config`로 Pod 하나하나의 설정을 열어 봤습니다. ambient에서는 L4가 **노드의 ztunnel**로 모였기 때문에 진단도 `ztunnel-config`처럼 **노드 단위**로 바뀌었습니다. Kiali도 ztunnel · waypoint를 따로 그리고, 정책 오타를 경고해 주는 방향으로 바뀌고 있습니다. 2교시의 "되돌리기 쉬운 것이 ambient의 장점"은 진단에서도 마찬가지입니다 — 라벨 하나로 넣고 빼며 **메시 때문인지 아닌지**를 가를 수 있습니다.

## 정리

- 메시 장애는 앱 로그에 안 남습니다. **메시에게 물어봅니다.**
- `ztunnel-config workloads` — 누가 메시 안(`HBONE`)인가. `TCP`면 등록이 빠진 것.
- `istioctl analyze` — 말이 안 되는 설정(아무 데도 안 걸린 정책 등). 단, **신원 오타는 못 잡습니다.**
- ztunnel 로그의 `policy rejection` · `src.identity` — 누가 누구에게 거절당했나.
- `waypoint list` · `proxy-status` — L7 규칙이 실제로 갈 프록시가 준비됐나.

!!! quiz "확인 문제"
    1. 요청은 잘 되는데 `ztunnel-config workloads`에서 PROTOCOL이 `TCP`입니다. 무엇이 문제인가요?
    2. ALLOW 정책을 썼는데 낯선 Pod도 들어옵니다. 가장 먼저 칠 명령과 의심할 곳은?
    3. `istioctl analyze`가 깨끗한데 `client`가 `000`으로 끊깁니다. 다음에 볼 곳은?
    4. 90/10 나누기가 적용되지 않는 것 같습니다. 무엇을 확인하나요?
    5. 운영 네임스페이스에서 "메시 때문인지" 가르려고 라벨을 뺄 때, 왜 `kubectl`이 아니라 Git 커밋으로 하나요?

    ??? answer "정답"
        1. 메시에 등록되지 않아 평문으로 돌고 있습니다 — 네임스페이스 · Pod의 `istio.io/dataplane-mode` 라벨
        2. `istioctl analyze` — 정책의 `selector` · `targetRefs`가 아무 워크로드에도 안 맞는지(IST0127)
        3. ztunnel 로그의 `policy rejection`과 `src.identity` — 정책의 principals와 실제 신원 비교
        4. `istioctl waypoint list`(PROGRAMMED), 서비스의 `istio.io/use-waypoint` 라벨, `proxy-status`
        5. Argo CD의 selfHeal이 kubectl 변경을 되돌리고, Git에 남아야 무엇을 언제 바꿨는지 기록되기 때문

!!! diary "오늘의 배움일기 — 수업 뒤 각자"
    - 남북과 동서를 DevMart의 예로 한 문장씩, 각각 무엇이 다루나
    - ztunnel 로그에서 본 신원(SPIFFE ID)을 그대로 옮겨 적고, 각 부분의 뜻
    - 3초 지연을 넣었을 때 products와 orders가 다르게 반응한 이유
    - STRICT를 켰을 때의 사고 — 무엇을 먼저 셌어야 했나?
    - 오늘 잰 메시 비용(메모리)과, DevMart에 메시가 정말 필요한지 내 판단
    - 내일 전에 궁금한 것: 오늘 허가 규칙은 "네임스페이스 단위"였다. DevMart의 Pod들이 **모두 같은 신원(sa/default)**인데, 서비스마다 · 사람마다 할 수 있는 일을 어떻게 나눌까? 그리고 "이미지 태그 latest 금지" 같은 규칙은 누가 지키게 할까?

## 참고 문헌

- Beschastnikh, I., Wang, P., Brun, Y., & Ernst, M. D. (2016). Debugging distributed systems. *Communications of the ACM*, 59(8).
- Istio Documentation. *Diagnostic Tools — istioctl analyze; Configuration Analysis Messages (IST0127)*; *Ambient mode — Troubleshoot connectivity issues with ztunnel*; *Troubleshoot issues with waypoints*. istio.io
- Istio Documentation. *istioctl reference — ztunnel-config, waypoint, proxy-status*.
