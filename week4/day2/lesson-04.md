<sub>[🏠 과정 목차](../../README.md) › [4주차](../README.md) › [2일차](README.md) › 4/8교시</sub>

# 4교시 · Grafana 대시보드

> [!NOTE]
> **이번 시간에 할 일**
>
> - Grafana에 로그인하고, **Explore**로 3교시의 PromQL을 다시 그려 봅니다.
> - 차트에 들어 있는 **기본 대시보드**로 DevMart의 자원 사용을 봅니다.
> - 패널 하나를 손으로 만들어 보고, 대시보드를 **코드(ConfigMap)**로 관리하는 이유를 이해합니다.
> - 좋은 대시보드의 원칙을 압니다.

## 실습 6 · 로그인과 Explore

```bash
kubectl port-forward -n monitoring service/kps-grafana 3000:80
```

브라우저에서 **http://localhost:3000**. 사용자 `admin`, 비밀번호는 2교시 단계 1에서 본 16자리입니다. 잊었다면:

```bash
kubectl get secret grafana-admin -n monitoring -o jsonpath='{.data.admin-password}' | base64 -d; echo
```

> **🟢 확인: 로그인되면**
>
> Grafana 홈 화면이 열립니다. 왼쪽 메뉴의 **Connections → Data sources**에 **Prometheus**가 이미 연결되어 있습니다 — 차트가 사이드카로 데이터 소스까지 넣어 두었습니다.

왼쪽 메뉴 **Explore**에서 데이터 소스 Prometheus를 고르고, 3교시 단계 3의 쿼리를 붙여 넣어 실행합니다.

```promql
sum by (envoy_cluster_name) (rate(envoy_cluster_upstream_rq_total{envoy_cluster_name=~"httproute/devmart/.*"}[1m]))
```

> [!TIP]
> **Explore는 '물어보는 곳', 대시보드는 '늘 보는 곳'**
>
> 장애 중에 처음 떠오른 질문은 **Explore**에서 이것저것 쿼리를 바꿔 가며 찾습니다(1교시의 관찰 가능성). 그러다 "이건 매번 보게 되겠다" 싶은 것만 **대시보드**로 옮깁니다. 대시보드에 모든 것을 넣으면 아무것도 안 보입니다.

## 실습 7 · 기본 대시보드

왼쪽 메뉴 **Dashboards** → 폴더 안의 목록에서 고릅니다.

| 대시보드 | 볼 것 |
|---|---|
| **Kubernetes / Compute Resources / Namespace (Pods)** | 위쪽 `namespace` 선택을 **devmart**로 → Pod별 CPU · 메모리 사용과 **requests · limits 대비 비율** |
| **Kubernetes / Compute Resources / Node (Pods)** | 노드마다 어떤 Pod가 자원을 쓰나 |
| **Node Exporter / Nodes** | 노드의 CPU · 메모리 · 디스크 · 네트워크 |

> **🟢 확인: 확인할 것**
>
> Namespace (Pods) 대시보드에서 **Memory Usage** 표의 `Memory Requests %` 칸을 봅니다. 3주차 5일차 4교시에 정한 requests(catalog-api 64Mi)에 비해 실제로 얼마를 쓰고 있나요? 100%를 크게 넘거나 훨씬 밑돌면 requests를 다시 정할 근거가 됩니다 — 3주차 5일차의 "재 보고 정한다"를 지금 할 수 있게 되었습니다.

> [!TIP]
> **기본 대시보드는 출발점**
>
> kube-prometheus-stack에 딸린 대시보드는 **클러스터와 자원(USE)** 중심입니다. "주문이 잘 되고 있나" 같은 **서비스(RED)** 관점은 들어 있지 않습니다. 그것은 우리가 만듭니다.

## 실습 8 · 패널 하나 손으로

1. 왼쪽 메뉴 **Dashboards → New → New dashboard → Add visualization** → 데이터 소스 **Prometheus**.
2. 아래 쿼리 칸(Code 모드)에 3교시 단계 5의 p95 쿼리를 붙여 넣는다.
3. 오른쪽 설정에서 **Title**: `p95 응답 시간`, **Standard options → Unit**: `Time / milliseconds (ms)`.
4. **Legend** 칸(쿼리 아래 Options)에 `{{envoy_cluster_name}}`.
5. 오른쪽 위 **Save dashboard** → 이름 `내 첫 대시보드`.

> **🟢 확인: 보이는 것**
>
> 라우트마다 한 줄씩 응답 시간 선이 그려집니다. 범례가 `httproute/devmart/catalog/rule/0` 같은 이름으로 보입니다.

이 대시보드는 **Grafana의 DB 안에만** 있습니다. Grafana Pod가 새로 뜨면(그리고 DB가 PVC에 없으면) 사라질 수 있고, 누가 언제 무엇을 바꿨는지 알 수 없고, 다른 클러스터에 똑같이 만들려면 다시 클릭해야 합니다. 3주차 4일차의 `kubectl scale`처럼 **손으로 바꾼 상태**입니다.

## 실습 9 · 대시보드를 코드로

```bash
cd ~/devops-lab/k8s/w4d2
head -12 monitoring/devmart-dashboard.yaml
grep '"title"' monitoring/devmart-dashboard.yaml
```

> **🟢 확인: 보이는 것**
>
> ```yaml
> apiVersion: v1
> kind: ConfigMap
> metadata:
>   name: devmart-dashboard
>   namespace: devmart
>   labels:
>     grafana_dashboard: "1"
> data:
>   devmart-red.json: |
>     {
>       "uid": "devmart-red",
>       "title": "DevMart — RED + 자원",
> ```
> ```text
>   "title": "DevMart — RED + 자원",
>       "title": "요청 수 (초당) — Rate",
>       "title": "5xx 비율 — Errors",
>       "title": "p95 응답 시간 — Duration",
>       "title": "Pod CPU 사용 — Utilization",
>       "title": "Pod 메모리 사용",
>       "title": "재시작 횟수 (15분) — Saturation의 끝",
> ```
> 대시보드 전체가 **JSON 하나**이고, 그것을 ConfigMap에 넣었습니다. 라벨 `grafana_dashboard: "1"`이 붙은 ConfigMap을 Grafana의 **사이드카**가 찾아 대시보드로 만듭니다(2교시 values의 `sidecar.dashboards`).

```bash
kubectl apply -f monitoring/devmart-dashboard.yaml
```

1분쯤 뒤 Grafana **Dashboards**에서 `DevMart — RED + 자원`을 엽니다.

> **🟢 확인: 보이는 것**
>
> 여섯 칸 — 위 줄에 R · E, 가운데 D와 CPU, 아래 메모리와 재시작. 왼쪽 위가 1교시의 '주문이 초당 몇 건?'에 답합니다. 3교시 요청 루프를 멈췄다면 요청 수는 0 근처입니다(5교시에 부하를 겁니다).

| | 손으로 만든 대시보드 (실습 8) | 코드로 만든 대시보드 (실습 9) |
|---|---|---|
| 저장 위치 | Grafana 내부 DB | **ConfigMap → Git** |
| 바꾼 이력 | 없음 (Grafana 버전 기록뿐) | Git 커밋 · PR 리뷰 |
| 다른 클러스터에 | 다시 클릭 | `kubectl apply` (5주차 EKS에도 그대로) |
| 화면에서 고치면 | 저장된다 | 저장이 막힌다(Provisioned) — **JSON을 고쳐 apply**한다 |

> [!TIP]
> **화면에서 다듬고, 코드로 굳힌다**
>
> JSON을 처음부터 손으로 쓰는 사람은 없습니다. 화면에서 패널을 다듬은 뒤 **Share → Export → Save to file**(또는 Edit → JSON model)로 JSON을 받아, 그것을 ConfigMap에 넣고 Git에 올립니다. 내일 Argo CD가 이 ConfigMap도 Git에서 자동으로 맞춥니다.

## 좋은 대시보드의 원칙

> [!IMPORTANT]
> **대시보드는 질문에 답하는 순서대로**
>
> 1. **위에서 아래로, 바깥에서 안으로** — 맨 위는 사용자 관점(RED), 아래로 갈수록 자원(USE) · 세부. 3주차 5일차 6교시의 진단 순서와 같다.
> 2. **한 패널 = 한 질문** — 제목이 질문이 되게("p95 응답 시간"보다 "느린 쪽 5%는 몇 ms?"도 좋다).
> 3. **단위와 기준선** — 단위가 없는 숫자는 읽을 수 없다. SLO(7교시) 같은 기준선을 함께 그린다.
> 4. **색은 의미가 있을 때만** — 빨강은 '나쁨'에만.
> 5. **적게** — 아무도 안 보는 패널은 지운다.

> **🎓 학술 노트 — 정보 시각화의 원칙**
>
> Edward Tufte의 *The Visual Display of Quantitative Information*(1983)은 그래프의 잉크 중 **데이터를 나타내는 잉크의 비율**(data-ink ratio)을 높이라고 했습니다 — 장식 · 3D 효과 · 쓸데없는 격자선을 줄이라는 뜻입니다. 운영 대시보드에 대해서는 Stephen Few의 *Information Dashboard Design*(2006)이 "한 화면에서 **한눈에** 상태를 파악할 수 있어야 한다"는 원칙을 세웠습니다. 장애 중에 대시보드를 보는 사람은 긴장해 있습니다. 읽기 쉬운 대시보드가 진단 시간을 줄입니다.

> **📈 트렌드 2026 — 대시보드도 Git으로, 그리고 자동 제안**
>
> Grafana 12~13에서 **Git Sync**(대시보드를 Git 저장소와 직접 동기화)가 정식 기능이 되었고, 13에서는 연결한 데이터 소스를 보고 **대시보드를 자동으로 제안**하는 기능이 들어왔습니다(2026년 4월). 오늘의 ConfigMap 방식은 그 가장 기본형입니다. 어떤 방식이든 "대시보드는 코드다"라는 방향은 같습니다.

> **✅ 확인 문제**
>
> 1. Explore와 대시보드는 각각 언제 쓰나요?
> 2. 기본 대시보드만으로 부족한 것은 무엇인가요?
> 3. ConfigMap으로 만든 대시보드를 Grafana가 어떻게 찾나요?
> 4. 대시보드를 코드로 관리할 때 얻는 것 두 가지는?
> 5. 대시보드 패널의 위 · 아래 순서를 어떻게 정하나요?
>
> <details><summary>정답</summary>
>
> 1. Explore — 장애 중 처음 떠오른 질문을 이것저것 물어볼 때. 대시보드 — 매번 보게 될 질문을 늘 보여 줄 때
> 2. 서비스 관점(RED) — 주문 · 상품 같은 우리 서비스의 요청 수 · 오류 · 시간
> 3. 라벨 `grafana_dashboard: "1"`이 붙은 ConfigMap을 Grafana 사이드카가 찾아 대시보드로 만든다
> 4. 바꾼 이력(Git · 리뷰), 다른 클러스터에 그대로 재현, 손으로 바꾼 상태가 사라지지 않음 중 둘
> 5. 위는 사용자 관점(RED), 아래로 갈수록 자원(USE) · 세부 — 바깥에서 안으로
>
> </details>

## 참고 문헌

- Grafana Docs. *Explore* · *Dashboards — Build and manage* · *Provision Grafana — Dashboards*. grafana.com/docs/grafana
- Grafana Helm Chart. *Sidecar for dashboards*. github.com/grafana/helm-charts
- Tufte, E. R. (1983). *The Visual Display of Quantitative Information*. Graphics Press.
- Few, S. (2006). *Information Dashboard Design*. O'Reilly.
- Grafana Labs (2026-04-21). *Grafana 13 release*. grafana.com/blog

---

| 이전 | 목차 | 다음 |
|:--|:--:|--:|
| ⬅️ [3교시 · 타깃과 PromQL](lesson-03.md) | [⬆️ 2일차 목차](README.md) | [5교시 · k6 부하 테스트](lesson-05.md) ➡️ |
