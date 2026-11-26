# 8교시 · HTTPS — cert-manager와 TLS Gateway

!!! goal "이번 시간에 할 일"
    - 인증서를 **사람이 손으로** 받고 갈아 끼우던 일을 **컨트롤러**에게 맡기는 이유를 압니다.
    - **cert-manager**를 Helm으로 설치하고, 실습용 **사설 인증 기관(CA)**을 클러스터 안에 만듭니다.
    - `Certificate` 리소스 하나로 DevMart의 인증서를 발급받고, 언제 **자동으로 갱신**되는지 읽습니다.
    - Gateway에 **443 리스너**를 더해 HTTPS로 DevMart를 열고, `curl`이 인증서를 믿게 만듭니다.

!!! key "1주차 3일차 5교시의 HTTPS가 운영의 일이 되는 순간"
    HTTPS는 **인증서**가 있어야 동작하고, 인증서에는 **만료일**이 있습니다. 인증서가 만료되면 브라우저는 사이트를 막고, API 클라이언트는 연결을 끊습니다. 큰 서비스들도 "인증서 갱신을 잊어서" 멈춘 사고를 반복해서 겪었습니다. 그래서 오늘의 핵심은 HTTPS를 켜는 것보다 **사람이 갱신을 기억하지 않아도 되게** 만드는 것입니다.

## 인증서를 자동으로 — 세 리소스

| 리소스 | 하는 일 | 비유 |
|---|---|---|
| `Issuer` / `ClusterIssuer` | **누가** 인증서를 서명해 주나 (Let's Encrypt, 회사 CA, 자체 서명 …) | 도장을 찍어 주는 기관 |
| `Certificate` | **어떤** 인증서가 필요한가 (도메인 · 기간 · 저장할 Secret 이름) | 신청서 |
| `Secret` (type `kubernetes.io/tls`) | 발급된 인증서와 **개인 키** | 받은 증명서 |

cert-manager 컨트롤러는 `Certificate`를 지켜보다가(3주차 3일차 8교시의 watch) 인증서가 없거나 **만료가 다가오면** 발급 기관에 다시 요청해 Secret을 바꿔 끼웁니다. Gateway는 그 Secret을 읽기만 합니다.

## 실습 15 · cert-manager 설치

```bash
cd ~/devops-lab/k8s/w4d1
CM=v1.21.3          # 그날의 최신 1.x는 github.com/cert-manager/cert-manager/releases
helm install cert-manager oci://quay.io/jetstack/charts/cert-manager --version $CM \
  -n cert-manager --create-namespace --set crds.enabled=true --wait
kubectl get pods -n cert-manager
kubectl api-resources --api-group=cert-manager.io
```

- `--set crds.enabled=true` : cert-manager의 **CRD**(Certificate 같은 새 리소스 종류)를 차트가 함께 설치한다. 5교시의 Envoy Gateway처럼 **API를 넓히는** 설치다

!!! check "이렇게 나오면 성공"
    ```text
    NAME                                       READY   STATUS    RESTARTS   AGE
    cert-manager-6c5f…                         1/1     Running   0          40s
    cert-manager-cainjector-7d9b…              1/1     Running   0          40s
    cert-manager-webhook-58c4…                 1/1     Running   0          40s
    NAME                  SHORTNAMES   APIVERSION                NAMESPACED   KIND
    certificaterequests   cr,crs       cert-manager.io/v1        true         CertificateRequest
    certificates          cert,certs   cert-manager.io/v1        true         Certificate
    clusterissuers        ciss         cert-manager.io/v1        false        ClusterIssuer
    issuers               iss          cert-manager.io/v1        true         Issuer
    ```

## 실습 16 · 실습용 CA와 DevMart 인증서

!!! warn "왜 Let's Encrypt가 아니라 사설 CA인가"
    Let's Encrypt 같은 공인 기관은 "이 도메인이 정말 당신 것인가"를 **인터넷에서 확인**합니다(내 서버에 특정 파일을 올리거나 DNS 레코드를 만들게 함). 노트북의 kind와 `devmart.localhost`는 인터넷에서 보이지 않으므로 확인을 통과할 수 없습니다. 그래서 오늘은 **클러스터 안에 작은 CA**를 만듭니다. 5주차 EKS에서 실제 도메인이 있다면 `ClusterIssuer`만 Let's Encrypt(ACME)로 바꾸면 되고, 나머지는 그대로입니다.

```bash
mkdir -p tls && code tls/issuers.yaml
```

```yaml
# ① 자기 자신이 서명하는 발급자 — CA를 만들 때 한 번만 쓴다
apiVersion: cert-manager.io/v1
kind: ClusterIssuer
metadata:
  name: selfsigned
spec:
  selfSigned: {}
---
# ② 실습용 루트 CA 인증서 (①이 서명)
apiVersion: cert-manager.io/v1
kind: Certificate
metadata:
  name: devmart-root-ca
  namespace: cert-manager
spec:
  isCA: true
  commonName: DevMart Lab Root CA
  secretName: devmart-root-ca
  duration: 8760h               # 1년
  privateKey:
    algorithm: ECDSA
    size: 256
  issuerRef:
    name: selfsigned
    kind: ClusterIssuer
---
# ③ 그 CA로 서명해 주는 발급자 — 앞으로 모든 인증서는 이걸로
apiVersion: cert-manager.io/v1
kind: ClusterIssuer
metadata:
  name: devmart-ca
spec:
  ca:
    secretName: devmart-root-ca
```

```bash
kubectl apply -f tls/issuers.yaml
kubectl get clusterissuer
```

!!! check "이렇게 나오면 성공"
    ```text
    NAME         READY   AGE
    devmart-ca   True    10s
    selfsigned   True    10s
    ```
    `devmart-ca`가 `False`면 ②의 Secret이 아직 안 생긴 것입니다. 몇 초 뒤 다시 봅니다.

이제 DevMart의 인증서를 **신청**합니다.

```bash
code tls/devmart-cert.yaml
```

```yaml
apiVersion: cert-manager.io/v1
kind: Certificate
metadata:
  name: devmart
  namespace: devmart
spec:
  secretName: devmart-tls
  dnsNames:
    - devmart.localhost
    - podinfo.localhost
  duration: 720h          # 30일
  renewBefore: 240h       # 만료 10일 전에 자동 갱신
  issuerRef:
    name: devmart-ca
    kind: ClusterIssuer
```

```bash
kubectl apply -f tls/devmart-cert.yaml
kubectl get certificate -n devmart
kubectl get certificate devmart -n devmart -o jsonpath='{.status.notAfter}{"  갱신 예정: "}{.status.renewalTime}{"\n"}'
kubectl get secret devmart-tls -n devmart -o jsonpath='{.data.tls\.crt}' | base64 -d \
  | openssl x509 -noout -subject -issuer -ext subjectAltName
```

!!! check "이렇게 나오면 성공"
    ```text
    NAME      READY   SECRET        AGE
    devmart   True    devmart-tls   5s
    2026-12-26T06:10:41Z  갱신 예정: 2026-12-16T06:10:41Z
    subject=
    issuer=CN=DevMart Lab Root CA
    X509v3 Subject Alternative Name:
        DNS:devmart.localhost, DNS:podinfo.localhost
    ```
    - `renewalTime` — cert-manager가 **스스로 다시 발급할 날**입니다. 사람이 달력에 적을 필요가 없습니다
    - 도메인은 이제 `subject`가 아니라 **SAN**(Subject Alternative Name) 칸에 적습니다. 브라우저도 이 칸만 봅니다

## 실습 17 · Gateway에 443 문 달기

`gateway/gateway.yaml`의 `listeners:` 아래에 HTTPS 리스너를 추가합니다(기존 `http`는 그대로).

```yaml
    - name: https
      protocol: HTTPS
      port: 443
      tls:
        mode: Terminate                 # Envoy에서 암호를 풀고 뒤로는 평문 HTTP
        certificateRefs:
          - name: devmart-tls           # cert-manager가 만든 Secret
      allowedRoutes:
        namespaces:
          from: All
```

```bash
kubectl apply -f gateway/gateway.yaml
kubectl get gateway devmart -n devmart -o jsonpath='{range .status.listeners[*]}{.name}{" "}{.attachedRoutes}{" "}{.conditions[?(@.type=="Programmed")].status}{"\n"}{end}'
```

!!! check "이렇게 나오면 성공"
    ```text
    http 4 True
    https 4 True
    ```
    6교시의 라우트 네 개는 `sectionName`을 정하지 않았으므로 **두 리스너 모두에** 붙었습니다.

kind는 노트북의 30080 하나만 클러스터로 열려 있으므로(3주차 3일차), 443은 `port-forward`로 엽니다.

```bash
SVC=$(kubectl get svc -n envoy-gateway-system \
  -l gateway.envoyproxy.io/owning-gateway-name=devmart -o jsonpath='{.items[0].metadata.name}')
kubectl port-forward -n envoy-gateway-system svc/$SVC 8443:443 > /tmp/pf.log 2>&1 &
sleep 2
curl -s -o /dev/null -w '%{http_code}\n' https://devmart.localhost:8443/api/products
```

!!! check "처음에는 거절"
    ```text
    000
    ```
    `curl -v`로 다시 보면 `SSL certificate problem: unable to get local issuer certificate`가 보입니다. 1주차 3일차 8교시의 TLS 층에서 멈췄습니다. **`curl`이 DevMart Lab Root CA를 모르기** 때문입니다.

```bash
kubectl get secret devmart-root-ca -n cert-manager -o jsonpath='{.data.ca\.crt}' | base64 -d > devmart-ca.crt
curl -s --cacert devmart-ca.crt -o /dev/null -w '%{http_code}\n' https://devmart.localhost:8443/api/products
curl -s --cacert devmart-ca.crt https://podinfo.localhost:8443/ | grep '"message"'
```

!!! check "이렇게 나오면 성공"
    ```text
    200
      "message": "upgrade로 바꿨습니다",
    ```
    podinfo의 메시지는 6교시 카나리 실습 상태에 따라 다를 수 있습니다.
    - `--cacert` : "이 CA가 서명한 인증서는 믿어라" — 회사 내부망에서 사내 CA를 PC에 설치하는 것과 같은 일입니다
    - `*.localhost`는 curl이 알아서 `127.0.0.1`로 보냅니다
    - Host에 따라 다른 앱으로 간 것은 6교시와 같습니다. 이제 **같은 문에서 암호화까지** 합니다

!!! tip "HTTP로 오면 HTTPS로 돌려보내기"
    운영에서는 80번으로 온 요청을 443으로 보내는 라우트를 둡니다.
    ```yaml
    spec:
      parentRefs:
        - name: devmart
          namespace: devmart
          sectionName: http          # http 리스너에만 붙는다
      rules:
        - filters:
            - type: RequestRedirect
              requestRedirect: { scheme: https, statusCode: 301 }
    ```
    오늘 kind에서는 HTTPS를 `port-forward`로만 열 수 있어 걸지 않습니다. 5주차 EKS에서 NLB가 443을 직접 받을 때 씁니다.

!!! cleanup "정리"
    ```bash
    kill %1 2>/dev/null || pkill -f "port-forward -n envoy-gateway-system"
    cd ~/devops-lab && git add k8s/w4d1/tls k8s/w4d1/gateway/gateway.yaml
    git commit -m "4주차 1일차: cert-manager 사설 CA + HTTPS 리스너" && git push
    ```
    개인 키가 든 Secret(`devmart-tls`, `devmart-root-ca`)은 파일로 꺼내지도, 커밋하지도 않습니다. cert-manager와 HTTPS 리스너는 **남겨 둡니다.** 내일부터의 실습은 그대로 30080(HTTP)을 씁니다.

!!! academic "학술 노트 — 웹 전체를 암호화한 자동화 (Aas 외, 2019)"
    2015년 이전에 HTTPS 인증서는 **돈을 내고, 서류를 내고, 사람이 손으로** 설치하는 물건이었습니다. 그래서 웹 페이지의 상당수가 평문 HTTP였습니다. 비영리 기관 ISRG가 만든 **Let's Encrypt**는 인증서를 **무료**로, 도메인 확인부터 발급 · 갱신까지 **완전 자동**으로 주는 CA입니다. 그 자동화 규약은 IETF 표준 **ACME**(RFC 8555, 2019)가 되었습니다. 운영진이 ACM CCS 2019에 발표한 논문은, 서비스 시작 4년 만에 Let's Encrypt가 세계 최대의 CA가 되었고 브라우저의 HTTPS 비율이 크게 올라간 과정을 보여 줍니다. 핵심 교훈은 **"보안이 수고로우면 사람들은 하지 않는다 — 기본값으로 만들어라"**였습니다. cert-manager는 그 ACME를 Kubernetes의 컨트롤러로 옮긴 것입니다.

    - Aas, J. et al. (2019). Let's Encrypt: An automated certificate authority to encrypt the entire web. *ACM CCS '19*, 2473–2487.
    - Barnes, R., Hoffman-Andrews, J., McCarney, D., & Kasten, J. (2019). *RFC 8555: Automatic Certificate Management Environment (ACME)*. IETF.

!!! trend "트렌드 — 인증서 수명이 47일로"
    인증서 규칙을 정하는 CA/브라우저 포럼은 2025년 4월, 공인 TLS 인증서의 최대 수명을 단계적으로 줄이기로 의결했습니다. **2026년 3월부터 200일**, 2027년 3월부터 100일, **2029년 3월부터 47일**입니다. 1년에 한 번 손으로 갈아 끼우던 일이 1년에 여덟 번이 되는 셈이라, 자동 갱신(ACME · cert-manager) 없이는 운영할 수 없게 됩니다. 오늘 `renewBefore` 한 줄이 그 대비입니다.

## 정리

- 인증서의 진짜 문제는 **만료**입니다. 갱신을 컨트롤러에게 맡깁니다.
- cert-manager: **Issuer**(누가 서명) + **Certificate**(무엇이 필요) → **Secret**(발급 결과). `renewalTime`에 스스로 갱신합니다.
- 공인 도메인이 없는 실습은 **사설 CA**로. 실제 도메인에서는 Issuer만 ACME(Let's Encrypt)로 바꿉니다.
- Gateway에 `protocol: HTTPS` 리스너 + `certificateRefs`로 TLS를 끝냅니다(Terminate). 라우트는 그대로 붙습니다.
- 사설 CA를 믿게 하려면 클라이언트에 CA 인증서를 줍니다(`--cacert`).

!!! quiz "확인 문제"
    1. Issuer, Certificate, Secret은 각각 무슨 역할인가요?
    2. kind 실습에서 Let's Encrypt를 쓰지 못하는 이유는?
    3. `renewBefore: 240h`는 무슨 뜻인가요?
    4. HTTPS 리스너를 더했는데 기존 HTTPRoute를 고치지 않아도 HTTPS로 동작한 이유는?
    5. `unable to get local issuer certificate` 에러는 어느 쪽의 문제이고, 오늘은 어떻게 풀었나요?

    ??? answer "정답"
        1. Issuer — 누가 서명하나. Certificate — 어떤 인증서가 필요한가(신청서). Secret — 발급된 인증서와 개인 키
        2. Let's Encrypt는 도메인 소유를 인터넷에서 확인하는데, 노트북의 kind와 `.localhost`는 밖에서 보이지 않기 때문
        3. 만료 10일 전에 cert-manager가 자동으로 다시 발급한다
        4. 라우트에 `sectionName`이 없어서 Gateway의 모든 리스너(http · https)에 붙기 때문
        5. 클라이언트가 서명한 CA를 모르는 문제 — `--cacert devmart-ca.crt`로 그 CA를 믿게 했다

!!! diary "오늘의 배움일기 — 수업 뒤 각자"
    - Helm을 친구에게 `apt`나 앱 스토어에 빗대어 한 문단으로
    - `helm rollback`과 `kubectl rollout undo`의 차이를 오늘 실제 상황으로
    - ingress-nginx 은퇴에서 가장 인상적이었던 점 — 기술 때문인가, 사람(유지보수) 때문인가
    - GatewayClass · Gateway · HTTPRoute를 회사의 세 사람에게 나눠 준다면 누구에게 무엇을
    - 오늘 장애 넷 중 응답 코드만 봤다면 놓쳤을 것과 그 이유
    - 내일 전에 궁금한 것: 오늘 50번 요청 중 카나리가 9번이었다. 하루 100만 번이라면 누가 세고, 오류가 늘었는지는 어떻게 알까?

## 참고 문헌

- Aas, J., Barnes, R., Case, B., Durumeric, Z., Eckersley, P., Flores-López, A., Halderman, J. A., Hoffman-Andrews, J., Kasten, J., Rescorla, E., Schoen, S., & Warren, B. (2019). Let's Encrypt: An automated certificate authority to encrypt the entire web. *ACM CCS '19*.
- Barnes, R. et al. (2019). *RFC 8555: Automatic Certificate Management Environment (ACME)*. IETF.
- cert-manager Documentation. *Installation with Helm (OCI)*; *CA Issuer*; *SelfSigned Issuer*; *Certificate resource — duration, renewBefore*; *Gateway API usage*. cert-manager.io/docs
- Kubernetes Gateway API. *TLS — Listener certificateRefs, HTTP redirects*. gateway-api.sigs.k8s.io
- CA/Browser Forum (2025). *Ballot SC-081: Introduce Schedule of Reducing Validity and Data Reuse Periods*.
