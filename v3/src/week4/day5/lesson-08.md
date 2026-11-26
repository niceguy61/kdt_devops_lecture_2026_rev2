# 8교시 · 4주차 회고 + 보안 점검표

!!! goal "이번 시간에 할 일"
    - 4주차에 만든 것을 **한 장의 그림**으로 정리합니다.
    - **보안 점검표**를 채우고 빈 곳을 Try로 옮깁니다.
    - KPT로 회고하고, 숫자로 한 주를 봅니다.
    - 5주차(AWS)로 무엇을 가져가는지 정리합니다.

## 정리 먼저

```bash
kubectl delete pod client -n devmart
kubectl delete namespace outsider
kubectl delete pod plain -n default --ignore-not-found
```

## 4주차 한 장 — 요청 하나와 변경 하나

| | 요청 하나 (손님이 주문) | 변경 하나 (개발자가 2.1.0 배포) |
|---|---|---|
| 1 | 입구 **Gateway**(1일차) — /api/orders → order-api | PR → CI 테스트 · 검문 · 빌드 · **서명** → GHCR (3주차 · 3일차 · 오늘) |
| 2 | ztunnel이 **mTLS**로 감싸 order-api로 (4일차) | CI 봇이 배포 저장소에 태그 커밋 (3일차) |
| 3 | order-api → catalog-api: waypoint가 **order-api인지** 확인, 타임아웃 · 재시도 (4 · 5일차) | Argo CD가 당겨 와 apiserver로 (3일차) |
| 4 | ztunnel(L4)이 waypoint인지 확인 → catalog-api (5일차) | **RBAC**: Argo CD SA는 쓸 수 있다 (5일차) |
| 5 | Envoy · waypoint가 요청 수 · 오류 · 시간을 남긴다 → **Prometheus · Grafana · Loki · 알림** (2일차) | **Kyverno**: latest가 아닌가, limits는, **우리 CI가 서명했나** (5일차) |
| 6 | 이상하면 런북 (2일차) | 롤링 업데이트, 문제면 `git revert` (3일차) |

1일차의 Helm이 이 모든 도구(Envoy Gateway · kube-prometheus-stack · Argo CD · Istio · Kiali · Kyverno)를 설치한 방법이었습니다.

## 실습 17 · 보안 점검표

```bash
cd ~/devops-lab/k8s/w4d5
cat security-checklist.md
```

각 줄의 **근거** 칸에 적힌 명령으로 직접 확인하고 `지금` 칸에 ✓ · △ · ✗를 적습니다.

```bash
kubectl auth can-i create deployments -n devmart --as=jane --as-group=devmart-devs
grep -rniE "password|secret_key|token" ~/devmart-deploy/devmart --include=*.yaml | grep -v secretKeyRef | grep -v "^.*#" || echo "비밀 값 없음"
kubectl get sa -n devmart
kubectl get peerauthentication,authorizationpolicy -n devmart
kubectl get policyreport -n devmart -o wide
kubectl get imagevalidatingpolicy
```

!!! check "대표적인 결과"
    | 항목 | 지금 |
    |---|---|
    | latest 금지 | ✓ Deny |
    | root 금지 | △ Audit — 6개 모두 FAIL |
    | 사람은 읽기만 | ✓ (`no`) |
    | 비밀 값은 Git에 없다 | ✓ |
    | 서비스마다 SA | △ 셋만 (db · redis · web은 default) |
    | mTLS STRICT · catalog-api 허가 | ✓ — 다른 서비스(db · redis)는 허가 규칙 없음 △ |
    | 이미지는 우리 CI가 서명한 것만 | ✓ Deny (7교시) |
    | 입구 TLS | △ HTTPS 리스너는 있지만(1일차 8교시) 30080은 여전히 http |

△ · ✗ 줄이 Try 후보입니다. 모두 고칠 필요는 없습니다 — **무엇이 비어 있는지 알고 있다**는 것이 점검표의 목적입니다.

## 실습 18 · KPT 회고

```bash
cat retro-week4.md
```

3주차 5일차와 같은 방법입니다. 혼자 5분 적고 → 짝과 5분 나누고 → 반 전체에서 Try 하나씩.

"숫자로 본 한 주"는 지난 사흘의 배움일기에서 옮깁니다 — 합치기 → 반영 시간, revert → 복구 시간, 오늘 훈련에서 알아채기까지의 시간, 클러스터 전체 메모리(Grafana의 Nodes 대시보드).

!!! tip "좋은 Try의 모양"
    "보안을 더 신경 쓴다"는 Try가 아닙니다. "**db · redis에 ServiceAccount와 L4 허가 규칙을 커밋한다 — catalog-l4.yaml을 본떠서**"처럼 다음 주에 **한 번에 끝낼 수 있는 행동**이어야 합니다(3주차 5일차).

## '5분 복구' — 4주차 최종판

클러스터가 통째로 사라졌을 때의 순서입니다. 각자의 `~/devops-lab/k8s/RECOVERY.md`에 옮겨 적습니다.

| 순서 | 명령 | 출처 |
|---|---|---|
| 1 | `kind create cluster --config kind-devmart.yaml` | 3주차 3일차 |
| 2 | Secret: `devmart-db`, `grafana-admin` (`kubectl create secret`) | 3주차 5일차 · 2일차 |
| 3 | `helm install` — Envoy Gateway → cert-manager → kps · Loki · Alloy → Istio 네 차트 → Kiali → Kyverno → Argo CD (VERSIONS.txt의 버전으로) | 1~5일차 |
| 4 | 플랫폼 `apply` — GatewayClass · EnvoyProxy · Gateway, RBAC, Kyverno 정책, envoy-gateway-system 라벨 (대시보드 · 규칙 · PodMonitor · 인증서는 루트가) | `platform-changes.md` |
| 5 | `kubectl apply -f root.yaml` — 루트 하나 | 3일차 8교시 |
| 6 | 나머지(DevMart · 관측 설정 · 인증서)는 Argo CD가 배포 저장소에서 | |

!!! warn "4번이 가장 길다"
    루트 Application 덕분에 앱과 관측 설정은 한 줄(5번)이지만, **플랫폼 설치(3번)와 나머지 설정(4번)은 여전히 손으로** 여러 줄입니다. 3 · 4번도 루트 아래의 Application(Helm 소스)으로 옮기는 것 — 3일차 8교시의 다음 걸음 — 이 실무 플랫폼 팀의 일입니다. 5주차에는 **Terraform**으로 1번(클러스터 자체)까지 코드로 만듭니다.

## 5주차로 가져가는 것

| 4주차 (kind) | 5주차 (AWS) |
|---|---|
| kind 클러스터 — 내 노트북 | **EKS** — 각자의 AWS 계정, 실습 당일 만들고 당일 지운다 |
| NodePort 30080 | **ALB** (AWS 로드 밸런서) |
| PVC — 노드 디스크 | EBS · RDS |
| 클러스터를 손으로 만든다 | **Terraform** — 네트워크 · 클러스터를 코드로 |
| SA 토큰 · SPIFFE | **IAM 역할**과 Pod Identity |
| 배포 저장소 + Argo CD | 그대로 — **destination만 EKS로** |

마지막 줄이 4주차의 핵심입니다. 앱의 원하는 상태(배포 저장소)는 클러스터가 바뀌어도 그대로 갑니다.

!!! academic "학술 노트 — 보안은 성질이 아니라 과정"
    Schneier는 *Secrets and Lies*(2000)에서 "보안은 제품이 아니라 **과정**"이라고 썼습니다. 오늘의 점검표가 ✓로 가득 차도, 내일 새 서비스가 들어오면 다시 빈 곳이 생깁니다. 그래서 4주차의 장치들 — 정책을 Audit로 넣어 **보고서로 계속 보기**, 변경을 **PR로 리뷰하기**, 장애 훈련을 **반복하기** — 은 상태가 아니라 과정을 만드는 도구입니다. NIST의 Cybersecurity Framework 2.0(2024)이 '식별 · 보호 · 탐지 · 대응 · 복구'에 '**거버넌스**'를 더한 것도 같은 이유입니다.

!!! trend "트렌드 2026 — 공급망 보안"
    2026년 보안 논의의 중심은 "내 클러스터에 들어오는 이미지가 **정말 내 CI가 만든 것인가**"입니다. 이미지 서명(Sigstore cosign)과 빌드 증명(SLSA provenance)을 CI에서 만들고, Kyverno의 `ImageValidatingPolicy`로 **서명이 없는 이미지는 입장 거절**하는 구성이 표준이 되어 가고 있습니다. 오늘 7교시에 서명과 입장 거절까지 했으니, 다음 걸음은 **빌드 증명(SLSA provenance)**을 붙이고 정책이 그것까지 확인하게 하는 것입니다.

!!! quiz "확인 문제"
    1. 손님의 주문 요청 하나가 4주차의 어느 장치들을 지나가나요? 셋 이상.
    2. 변경 하나(2.1.0 배포)를 막을 수 있는 관문 셋은?
    3. '5분 복구'에서 가장 긴 단계와 그것을 줄이는 방법은?
    4. 5주차에 EKS로 옮겨도 그대로 가져가는 것은?

    ??? answer "정답"
        1. Gateway, ztunnel(mTLS · L4 허가), waypoint(L7 허가 · 타임아웃 · 재시도), Prometheus · Grafana · 알림 중 셋 이상
        2. PR 리뷰 · CI 테스트, apiserver RBAC, Kyverno 입장 제어
        3. 플랫폼 설치 · apply 단계. 플랫폼도 Git과 Argo CD(app of apps)로, 클러스터는 Terraform으로
        4. 배포 저장소(원하는 상태)와 Argo CD 방식 — destination만 바꾼다

!!! diary "오늘의 배움일기 — 4주차 마지막"
    - 세 관문(인증 · 인가 · 입장 제어)을 오늘 본 메시지 하나씩과 함께
    - 3교시에 order-api에서 사라진 토큰 — 그것이 있었을 때 무엇이 위험했나
    - L7 규칙과 L4 규칙이 각각 막은 것
    - 종합 훈련에서 내가 맡은 장애: 알아채기까지 · 복구까지 걸린 시간, 그리고 '누가 거절했나'
    - 4주차 전체에서 가장 "운영을 바꿨다"고 느낀 하루와 그 이유
    - 다음 주 전에 궁금한 것: 지금까지 클러스터는 내 노트북 안에 있었다. **클라우드의 클러스터는 누가, 어떤 네트워크 위에, 얼마의 비용으로** 만드는가?

## 참고 문헌

- Schneier, B. (2000). *Secrets and Lies: Digital Security in a Networked World*. Wiley.
- NIST (2024). *The NIST Cybersecurity Framework (CSF) 2.0*. NIST CSWP 29.
- Sigstore Docs. *cosign*, SLSA. *Supply-chain Levels for Software Artifacts v1.1*. slsa.dev
- Kyverno Docs. *ImageValidatingPolicy*. kyverno.io/docs
