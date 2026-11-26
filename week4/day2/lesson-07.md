<sub>[🏠 과정 목차](../../README.md) › [4주차](../README.md) › [2일차](README.md) › 7/7교시</sub>

# 7교시 · 관찰 런북과 SLO

> [!NOTE]
> **이번 시간에 할 일**
>
> - **SLI · SLO · SLA**를 구분하고, DevMart의 SLO를 정합니다.
> - **오류 예산**(error budget)을 계산해 봅니다.
> - 6교시 알림에 붙일 **런북**을 쓰고, 알림의 `runbook_url`과 연결합니다.

## SLI · SLO · SLA

5교시의 k6 합격 기준(`p(95)<500`, 실패 1% 미만)과 6교시의 알림 기준(5xx 5%)은 어디서 나온 숫자일까요? 지금까지는 '적당히' 정했습니다. 그 숫자의 근거를 정하는 틀이 **SLO**입니다.

| 낱말 | 뜻 | DevMart의 예 |
|---|---|---|
| **SLI** (Service Level Indicator, 지표) | 서비스가 잘 되고 있는지를 나타내는 **측정값** — 보통 '좋은 것 / 전체'의 비율 | 주문 요청 중 5xx가 아닌 비율 · 상품 요청 중 0.5초 안에 끝난 비율 |
| **SLO** (Objective, 목표) | SLI가 **기간 동안** 지켜야 할 목표 | "28일 동안 주문 성공률 **99.5%** 이상" |
| **SLA** (Agreement, 계약) | 고객과의 **약속**. 어기면 보상 · 위약금 | "월 99.0% 미만이면 요금 10% 환불" — SLO보다 느슨하게 둔다 |

> **🧩 비유 — 택배 회사**
>
> SLI는 "약속한 날 도착한 택배의 비율", SLO는 "이번 달 98% 이상을 목표로 한다"(회사 내부 목표), SLA는 "95% 미만이면 고객에게 배송비를 돌려준다"(계약)입니다. 내부 목표(SLO)를 계약(SLA)보다 **높게** 잡아야, 목표를 조금 놓쳐도 계약은 지킵니다.

> **❓ 오해 — 목표는 100%여야 한다**
>
> 100%는 불가능하고, 다가갈수록 **비용이 폭발**합니다. 99%에서 99.9%로 올리는 데 드는 노력은 대개 99%까지 오는 노력보다 큽니다. 그리고 사용자는 우리 서비스보다 **덜 믿을 만한 것들**(휴대폰 통신, 집 와이파이)을 거쳐 들어오므로, 그 이상은 느끼지도 못합니다. 구글 SRE 책은 "100%는 잘못된 목표"라고 못 박습니다.

### 오류 예산

SLO 99.5%는 뒤집으면 **0.5%는 실패해도 된다**는 뜻입니다. 이것이 **오류 예산**입니다.

> **📘 예시 — DevMart 주문의 오류 예산**
>
> - 5교시 k6처럼 주문이 초당 약 3.5건이라면, 28일 동안 약 **850만 건**.
> - 99.5% SLO → 실패해도 되는 주문은 약 **4만 2천 건**.
> - 오늘 5교시 장애(40초 동안 주문 대부분 실패, 초당 3.5건) → 약 **140건** 소모. 예산의 0.3%.
> - 시간으로 바꾸면 28일 × 0.5% ≈ **3시간 22분** — 이만큼 '완전히 멈춰도' 목표는 지킨다.

> [!IMPORTANT]
> **오류 예산은 '써도 되는 돈'**
>
> 예산이 **넉넉하면** 새 기능을 빨리 내보내고, 실험(카나리, 4주차 1일차)도 과감히 합니다. 예산을 **다 쓰면** 새 배포를 멈추고 안정성 작업에 집중합니다. 개발팀(빨리 내보내고 싶다)과 운영팀(안 깨뜨리고 싶다)의 오래된 다툼을 **숫자 하나로** 정리하는 장치입니다 — 1주차 5일차 DevOps의 '벽 허물기'의 구체적인 방법입니다.

### PromQL로 SLI 재기

```promql
# 최근 1시간 주문 성공률 (SLI)
1 - (
  sum(increase(envoy_cluster_upstream_rq_xx{envoy_response_code_class="5", envoy_cluster_name=~"httproute/devmart/orders/.*"}[1h]))
  /
  sum(increase(envoy_cluster_upstream_rq_total{envoy_cluster_name=~"httproute/devmart/orders/.*"}[1h]))
)
```

> **🟢 확인: Prometheus Query 탭에서**
>
> 오늘 5교시 · 6교시 장애가 1시간 안에 있었다면 1보다 조금 작은 값(예: `0.987`)이 나옵니다. 28일 창(`[28d]`)으로 바꾸면 SLO와 비교할 수 있지만, 우리 Prometheus는 2일만 보관합니다(2교시 values `retention: 2d`). 실무에서 28일 SLO를 재려면 원격 저장소가 필요합니다(2교시 트렌드).

## 런북

새벽 3시에 알림을 받은 사람은 **잠이 덜 깬 상태**이고, 이 서비스를 처음 맡았을 수도 있습니다. 그 사람이 따라 할 수 있는 문서가 **런북**(runbook)입니다. 6교시 알림의 `runbook_url`이 가리킬 곳입니다.

> [!IMPORTANT]
> **좋은 런북의 조건**
>
> 1. **알림 이름으로 바로 찾을 수 있다** — 파일 이름 = 알림 이름.
> 2. **추측이 아니라 명령** — "DB를 확인한다"가 아니라 `kubectl exec … psql …`.
> 3. **판단 기준이 있다** — "이 숫자가 0이면 → 3번으로".
> 4. **되돌리는 법이 함께 있다** — 조치마다.
> 5. **언제 도움을 부를지** — 15분 안에 못 찾으면 누구에게.
> 6. **장애가 끝날 때마다 고친다** — 틀린 곳, 빠진 곳.

## 실습 14 · DevMartHighErrorRate 런북

> **🧪 실습: 실습 목표**
>
> `runbook-template.md`를 채워 DevMartHighErrorRate의 런북을 씁니다. 3주차 5일차 6교시(장애 넷), 4주차 1일차 7교시(라우트 장애 넷), 오늘 5 · 6교시의 경험이 재료입니다.

### 단계 1 — 실습 저장소에 런북 자리 만들기

2주차부터 쓰는 내 실습 저장소 `~/devops-lab`(GitHub에 올라가 있는 것)에 둡니다.

```bash
cd ~/devops-lab
git switch -c docs/runbook-high-error-rate
mkdir -p runbooks
cp ~/devops-lab/k8s/w4d2/runbook-template.md runbooks/devmart-high-error-rate.md
```

### 단계 2 — 채우기

> **📘 예시 — 2번 '먼저 확인' 칸을 채운 모습**
>
> | 순서 | 볼 것 | 명령 · 대시보드 | 정상이면 | 이상이면 |
> |---|---|---|---|---|
> | 1 | 어느 라우트인가 | 알림의 `envoy_cluster_name` | — | catalog / orders / web 중 어느 것인지 적고 4로 |
> | 2 | Gateway · 라우트 상태 | `kubectl get gateway -n devmart` · `kubectl describe httproute <이름> -n devmart` | PROGRAMMED True, Accepted · ResolvedRefs True | 4주차 1일차 7교시 표: ResolvedRefs False면 backendRefs 확인 |
> | 3 | 서비스 뒤의 Pod | `kubectl get endpointslices -n devmart` · `kubectl get pods -n devmart` | 엔드포인트 있음, 모두 1/1 | 비었거나 0/1이면 3주차 5일차 6교시 진단 순서 |
> | 4 | 앱의 마지막 에러 | `kubectl logs -n devmart -l app=<서비스> --tail=20` | 오류 없음 | 메시지로 원인 분류 (DB · 큐 · 다른 서비스) |
> | 5 | 최근 변경 | `kubectl get events -n devmart --sort-by=.lastTimestamp \| tail` · `helm history` · Git 로그 | 최근 변경 없음 | 변경 직후라면 **되돌리기부터** (rollout undo · helm rollback) |

> [!TIP]
> **'최근 변경'을 먼저 의심한다**
>
> 3주차 3일차 학술 노트에서 본 것처럼 장애의 큰 몫은 **변경**에서 옵니다. 장애가 배포 직후에 시작했다면, 원인을 끝까지 찾기 전에 **되돌려서 손님부터 살리는** 것이 보통 옳습니다. 원인 분석은 그 뒤에 해도 됩니다. 런북의 3번 '흔한 원인' 표 맨 위에 "직전 배포 → 되돌리기"를 둡니다.

### 단계 3 — 알림과 연결하고 올리기

```bash
cd ~/devops-lab/k8s/w4d2
GH=$(gh api user --jq .login)
sed -i "s/YOUR_ID/$GH/" monitoring/devmart-rules.yaml        # Mac: sed -i ''
grep runbook_url monitoring/devmart-rules.yaml
kubectl apply -f monitoring/devmart-rules.yaml

cd ~/devops-lab
git add runbooks/
git commit -m "docs: DevMartHighErrorRate 런북"
git push -u origin docs/runbook-high-error-rate
gh pr create --fill
```

> **🟢 확인: 보이는 것**
>
> ```text
>         runbook_url: "https://github.com/niceguy61/devops-lab/blob/main/runbooks/devmart-high-error-rate.md"
> prometheusrule.monitoring.coreos.com/devmart configured
> ...
> https://github.com/niceguy61/devops-lab/pull/7
> ```
> PR을 병합하면, 다음에 알림이 울릴 때 Alertmanager 화면의 `runbook_url`을 눌러 **바로 이 문서**로 갑니다. 런북도 코드처럼 PR로 리뷰받습니다.

## 오늘 정리

> [!WARNING]
> **오늘 설치한 것은 지우지 않는다**
>
> kube-prometheus-stack · PodMonitor · 대시보드 · 규칙은 **내일과 그 뒤에도** 씁니다. 내일 Argo CD로 배포하는 과정을 이 대시보드로 지켜보고, 4일차 Istio의 장애 주입도 여기서 봅니다. 메모리가 빠듯하면 `helm uninstall podinfo-canary`만 해 둡니다. '5분 복구' 순서에 오늘 것을 덧붙입니다 — Secret → `helm install kps …` → PodMonitor · 대시보드 · 규칙 `apply`.

> **🎓 학술 노트 — SLO와 오류 예산의 기원**
>
> SLO와 오류 예산은 구글 SRE 책(Beyer 외, 2016) 3장 *Embracing Risk*와 4장 *Service Level Objectives*에서 체계화되었습니다. 핵심 주장은 "신뢰성은 **많을수록 좋은 것이 아니라 정해야 하는 제품 기능**"이라는 것입니다. 한편 Hidalgo의 *Implementing Service Level Objectives*(O'Reilly, 2020)는 SLO가 숫자보다 **조직의 대화 도구**라는 점을 강조합니다 — 개발 · 운영 · 제품 담당자가 "얼마나 믿을 만해야 하나"를 함께 정하는 과정 자체가 가치라는 것입니다.

> **📈 트렌드 2026 — 관찰 데이터를 읽는 AI**
>
> Grafana 13은 OSS · Enterprise 사용자에게도 **AI 도우미**(Assistant)를 열어, 대시보드를 만들고 쿼리를 쓰고 이상을 설명하는 일을 돕게 했습니다(2026년 4월). 장애 중에 "지난 30분 동안 무엇이 바뀌었나"를 요약하는 기능도 흔해졌습니다. 그러나 AI가 좋은 답을 내려면 오늘 만든 것들 — **의미 있는 라벨, 증상 기반 알림, 런북** — 이 먼저 있어야 합니다. 쓰레기가 들어가면 쓰레기가 나온다는 원칙은 그대로입니다.

> **✅ 확인 문제**
>
> 1. SLI · SLO · SLA를 DevMart 예로 하나씩?
> 2. SLO를 SLA보다 높게 잡는 이유는?
> 3. 오류 예산을 다 썼다면 팀은 무엇을 하나요?
> 4. 좋은 런북의 조건 세 가지는?
> 5. 장애가 배포 직후에 시작했다면 무엇부터 하나요?
>
> <details><summary>정답</summary>
>
> 1. SLI — 주문 요청 중 5xx가 아닌 비율, SLO — 28일 동안 99.5% 이상, SLA — 월 99.0% 미만이면 환불 (예)
> 2. 내부 목표를 조금 놓쳐도 고객과의 계약은 지키도록 여유를 두기 위해
> 3. 새 배포를 멈추고 안정성 개선에 집중한다
> 4. 알림 이름으로 찾을 수 있다, 명령과 판단 기준이 있다, 되돌리는 법이 있다, 도움을 부를 시점이 있다, 장애 후 고친다 중 셋
> 5. 원인을 끝까지 찾기 전에 되돌려서(rollout undo · helm rollback) 손님부터 살린다
>
> </details>

> [!NOTE]
> **오늘의 배움일기**
>
> - 로그 · 메트릭 · 트레이스를 각각 한 문장으로, DevMart 예와 함께
> - 오늘 만든 PromQL 중 가장 쓸모 있다고 느낀 것 하나와 그 이유
> - 5교시 장애에서 k6 · Grafana · events가 각각 알려 준 것
> - 알림이 Firing이 되기까지 걸린 시간 — 줄여야 할까, 늘려야 할까?
> - DevMart 주문의 SLO를 내가 정한다면 몇 %로? 근거는?
> - 내일 전에 궁금한 것: 런북 · 대시보드 · 규칙을 모두 Git에 올렸다. 그렇다면 **클러스터 자체도** Git에 있는 대로 맞춰지게 할 수는 없을까?

## 참고 문헌

- Beyer, B. 외 (2016). *Site Reliability Engineering*, Ch. 3 "Embracing Risk", Ch. 4 "Service Level Objectives". O'Reilly.
- Beyer, B. 외 (2018). *The Site Reliability Workbook*, Ch. 2 "Implementing SLOs". O'Reilly.
- Hidalgo, A. (2020). *Implementing Service Level Objectives*. O'Reilly.
- Grafana Labs (2026-04-21). *GrafanaCON 2026 announcements*. grafana.com/blog

---

| 이전 | 목차 | 다음 |
|:--|:--:|--:|
| ⬅️ [6교시 · 알림](lesson-06.md) | [⬆️ 2일차 목차](README.md) | [4주차 3일차 목차](../day3/README.md) ➡️ |
