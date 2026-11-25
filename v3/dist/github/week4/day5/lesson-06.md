# 6교시 · 4주차 종합 장애 훈련

> [!NOTE]
> **이번 시간에 할 일**
>
> - 4주차에 쌓은 층 — 입구 · 관찰 · GitOps · 메시 · RBAC · 입장 제어 — 이 모두 섞인 장애를 **짝과** 풉니다.
> - 거절 메시지의 **모양**으로 "누가 거절했나"를 찾는 지도를 익힙니다.
> - 복구는 **Git으로** 하고, 장애 보고서를 씁니다.

## 거절의 지도

![클러스터를 바꿀 때는 apiserver RBAC · Kyverno · kubelet이, 요청이 오갈 때는 Envoy Gateway · waypoint · ztunnel이 거절하고, 메시지 모양이 다르다](../../assets/week4/day5/w4d5-who-refused.png)

```bash
cat ~/devops-lab/k8s/w4d5/drills/who-refused.md
```

| 메시지 | 누가 | 고치는 곳 |
|---|---|---|
| `Forbidden: … cannot list resource …` | apiserver RBAC | Role · RoleBinding |
| `admission webhook … denied the request` | Kyverno | 매니페스트 또는 정책 |
| `RBAC: access denied` (HTTP 403) | waypoint | AuthorizationPolicy (L7) |
| curl `000` · `Connection reset` | ztunnel | PeerAuthentication · L4 규칙 |
| HTTP `504` · 로그의 `UT` | waypoint 타임아웃 | VirtualService |
| HTTP `500` · `no healthy upstream` | Envoy Gateway | HTTPRoute · Service |
| `ImagePullBackOff` | kubelet | 이미지 이름 · 태그 · 공개 여부 |

> [!IMPORTANT]
> **Istio의 'RBAC'와 Kubernetes의 'RBAC'**
>
> 둘 다 RBAC라는 말을 쓰지만 **전혀 다른 곳**입니다. `Forbidden`은 **apiserver**가 "클러스터를 바꾸려는 사람 · 프로그램"을 거절한 것이고, `RBAC: access denied`는 **waypoint**가 "서비스를 부른 쪽"을 거절한 것입니다. 메시지 전체 모양(kubectl 오류인가, HTTP 응답인가)으로 구분합니다.

## 훈련 방법

3주차 5일차의 장애 훈련과 같은 짝 방식입니다.

1. **A**가 짝의 화면을 보지 않고 `break-w4.sh random`을 실행합니다. A는 결과 번호를 모릅니다(`/tmp/.w4-break`에만 적힌다).
2. **B**(짝)는 "무언가 이상하다"는 말만 듣고 **알아채기 → 좁히기 → 원인 → 복구**를 합니다. 15분 제한.
3. B는 `incident-report-w4.md`를 채웁니다. 끝나면 A가 번호를 알려 주고 역할을 바꿉니다.
4. 시간이 되는 만큼 **두세 판** 합니다.

```bash
cd ~/devops-lab/k8s/w4d5
cat drills/break-w4.sh | head -5          # 내용은 보지 않는다 — 사용법만
./drills/break-w4.sh random
```

> [!WARNING]
> **규칙**
>
> - 복구는 **원래 고치는 곳**에서 합니다 — 배포 저장소 문제는 `git revert`, 플랫폼 문제는 플랫폼 파일을 다시 `apply`. `kubectl edit`으로 devmart를 직접 고치면 selfHeal이 되돌리거나 기록이 남지 않습니다.
> - 손님 흉내 루프를 계속 돌려 둡니다(아래). 알아챈 시각을 적기 위해서입니다.

```bash
# 손님 — 장애 훈련 내내 켜 둔다
while true; do
  printf '%s products=%s orders=%s web=%s\n' "$(date +%T)" \
    "$(curl -s -o /dev/null -w '%{http_code}' localhost:30080/api/products)" \
    "$(curl -s -o /dev/null -w '%{http_code}' -X POST localhost:30080/api/orders -H 'content-type: application/json' -d '{"product_id":1,"quantity":1}')" \
    "$(curl -s -o /dev/null -w '%{http_code}' localhost:30080/)"
  sleep 2
done
```

## 조사의 순서 — 바깥에서 안으로

2일차 4교시 대시보드 원칙 그대로, **손님 → 입구 → 메시 → 배포 → 클러스터** 순서로 좁힙니다.

| 단계 | 볼 것 | 명령 · 화면 |
|---|---|---|
| 1. 손님 | 무엇이 실패하나 — products · orders · web 중 어느 것? 상태 코드는? | 손님 루프, 브라우저 |
| 2. 관찰 | 언제부터? 어느 라우트? 알림이 울렸나? | Grafana DevMart 대시보드, Alertmanager |
| 3. 최근 변경 | **방금 누가 무엇을 바꿨나** — 배포 저장소의 마지막 커밋들 | `cd ~/devmart-deploy && git pull && git log --oneline -5 && git show --stat HEAD` |
| 4. Argo CD | Sync는 성공했나? 실패했다면 메시지는? | `argocd app get devmart`, 웹 UI |
| 5. 메시 | 서비스 사이 403 · 504가 있나? | Kiali 지도, waypoint 로그 `--tail=20` |
| 6. 입구 | 라우트 상태 · 백엔드 | `kubectl get httproute -n devmart -o yaml | grep -A5 conditions` |
| 7. 플랫폼 | 사람의 권한은? (동료가 "로그가 안 보여요"라고 하면) | `kubectl auth can-i … --as` |

> [!TIP]
> **가장 빠른 질문: 무엇이 바뀌었나?**
>
> 운영 장애의 상당수는 **변경 직후**에 옵니다(2일차 7교시). GitOps 덕분에 "무엇이 바뀌었나"는 `git log` 한 줄로 답할 수 있습니다. 단, 플랫폼 쪽 변경(kubectl apply)은 Git에 없으니 `platform-changes.md`와 `kubectl get … --sort-by=.metadata.creationTimestamp`, events를 봅니다 — 플랫폼도 Git으로 관리해야 하는 이유입니다.

## 훈련 뒤 — 다섯 가지 정답 펼쳐 보기

모든 판이 끝난 뒤에 함께 봅니다.

<details><summary>1 · catalog-api 최신 이미지로</summary>

- 손님: **아무 이상 없음.** 하지만 "새 버전이 안 나간다"는 개발자의 문의.
- Argo CD: OutOfSync, Sync 실패 — `admission webhook … denied … disallow-latest-tag`.
- 거절한 주체: **Kyverno**. 복구: `git revert`. 교훈: 정책이 사고를 **막았다.** 막힌 것을 알아채려면 Argo CD의 Sync 실패도 알림으로 받아야 한다(Argo CD notifications, 3일차에 끈 것).

</details>

<details><summary>2 · 정책 정리</summary>

- 손님: **orders만 실패(5xx)**, products · web은 200.
- Kiali: order-api → catalog-api 선이 빨강, 403. waypoint 로그: `rbac_access_denied`.
- git show: `catalog-authz.yaml`의 `sa/order-api` → `sa/order-worker`.
- 거절한 주체: **waypoint**(L7 허가). 복구: `git revert`. 교훈: 허가 규칙의 PR에는 "누가 부르게 되고 누가 못 부르게 되나"를 적는다.

</details>

<details><summary>3 · 응답 시간 목표 조정</summary>

- 손님: **orders만 503**, 빠르게(0.0x초).
- waypoint 로그: `504 UT`(upstream timeout). Grafana: orders 오류율.
- git show: `catalog-timeout.yaml`의 `timeout: 1s` → `10ms`.
- 거절한 주체: **waypoint 타임아웃**. 복구: `git revert`. 교훈: 2와 증상이 같다 — **로그의 응답 코드 · 플래그**가 둘을 가른다.

</details>

<details><summary>4 · (커밋 없음)</summary>

- 손님: **아무 이상 없음.** 동료 jane: "devmart 로그가 갑자기 안 보여요."
- `kubectl logs … --as=jane --as-group=devmart-devs` → `Forbidden … cannot get resource "pods/log"`.
- 배포 저장소에는 변경이 없다 → **플랫폼 변경**. `kubectl get role devmart-developer -n devmart -o yaml`에서 `pods/log`가 빠짐.
- 거절한 주체: **apiserver RBAC**. 복구: `kubectl apply -f rbac/devmart-developer.yaml`. 교훈: 플랫폼 변경도 Git에 두지 않으면 "무엇이 바뀌었나"에 답할 수 없다.

</details>

<details><summary>5 · web 포트 정리</summary>

- 손님: **web만 500**(첫 화면), products · orders는 200.
- `kubectl get httproute web -n devmart -o yaml`의 status: `ResolvedRefs False` · `BackendNotFound`류. Envoy: `no healthy upstream`.
- git show: `devmart-routes.yaml`의 `port: 80` → `8080`.
- 거절한 주체: **Envoy Gateway**(갈 곳이 없다). 복구: `git revert`. 교훈: Argo CD는 **Synced · Healthy**였다 — Git대로 잘 배포된 '틀린 설정'(3일차 Synced + 틀림).

</details>

> **🎓 학술 노트 — 장애 조사의 인지 부하**
>
> Allspaw의 석사 논문 *Trade-offs Under Pressure*(Lund University, 2015)는 실제 장애 대응을 분석해, 숙련자가 모든 신호를 다 보지 않고 **"최근 무엇이 바뀌었나"와 "증상의 모양"으로 가설을 빨리 세우고 버리는** 방식으로 일한다는 것을 보였습니다. Woods의 *STELLA Report*(2017)는 이를 '선 위(사람의 이해)와 선 아래(시스템)' 사이의 간극으로 설명합니다. 오늘의 거절 지도는 그 '증상의 모양' 사전을 미리 만들어 두는 연습입니다.

> **📈 트렌드 2026 — AI와 함께 하는 장애 조사**
>
> 장애 채널에 붙은 AI 도우미가 최근 배포 · 알림 · 로그를 모아 "가장 의심되는 변경"을 제안하는 도구가 흔해졌습니다(Grafana Assistant, Datadog Bits AI, PagerDuty 등). 이 도구들도 결국 **Git 커밋 이력 · 구조화된 로그 · 의미 있는 알림**을 읽습니다 — 4주차에 만든 것이 그대로 AI의 입력이 됩니다. 마지막 판단과 복구 버튼은 여전히 사람의 몫입니다.

> **✅ 확인 문제**
>
> 1. `Forbidden`과 `RBAC: access denied`는 각각 누가 거절한 것인가요?
> 2. 증상이 같은 2번과 3번을 무엇으로 구별하나요?
> 3. 4번처럼 배포 저장소에 변경이 없을 때 볼 곳은?
> 4. 1번에서 손님은 아무 이상이 없었는데 왜 장애로 다뤄야 하나요?
>
> <details><summary>정답</summary>
>
> 1. Forbidden — apiserver의 RBAC(클러스터 변경 요청), RBAC: access denied — Istio waypoint의 AuthorizationPolicy(서비스 호출)
> 2. waypoint 로그의 응답 코드와 플래그 — 403 rbac_access_denied와 504 UT
> 3. 플랫폼 변경 — platform-changes.md, Role 등 플랫폼 리소스, events
> 4. 새 버전이 배포되지 못하고 있고(Sync 실패), 아무도 모르면 급한 수정도 나가지 못하기 때문
>
> </details>

## 참고 문헌

- Allspaw, J. (2015). *Trade-offs Under Pressure: Heuristics and Observations of Teams Resolving Internet Service Outages*. Lund University.
- Woods, D. D. (2017). *STELLA: Report from the SNAFUcatchers Workshop on Coping With Complexity*.
- Istio Docs. *Envoy response flags* (UT · DI · …). istio.io / envoyproxy.io
