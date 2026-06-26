# Academic Foundations: W4D3 Observability

## 1. Observability의 네 가지 증거
Kubernetes 운영에서는 하나의 명령으로 장애를 끝내기 어렵다.

| 증거 | 예시 | 잘 보이는 것 |
|---|---|---|
| logs | `kubectl logs` | app process가 남긴 메시지 |
| events | `kubectl describe pod` | scheduling, probe, image pull, kill reason |
| metrics | Prometheus, `kubectl top` | 시간에 따른 CPU/memory/restart/latency |
| traces | OpenTelemetry 등 | 요청이 여러 서비스로 흐르는 경로 |

W4D3는 metrics 중심이다. logs와 events는 “왜 지금 실패했는가”를 잘 보여주고, metrics는 “언제부터, 얼마나 자주, 얼마나 심하게”를 보여준다.

## 2. kube-prometheus-stack
`kube-prometheus-stack`은 Prometheus Operator 기반의 Kubernetes monitoring bundle이다.

| 구성요소 | 역할 |
|---|---|
| Prometheus Operator | Prometheus, Alertmanager, ServiceMonitor 같은 CRD reconcile |
| Prometheus | metric scrape, 저장, PromQL query |
| Grafana | dashboard 시각화 |
| Alertmanager | alert routing, grouping, silence |
| node-exporter | node level metric |
| kube-state-metrics | Kubernetes object 상태 metric |

## 3. ServiceMonitor와 PodMonitor
Prometheus Operator 환경에서는 scrape 설정을 직접 prometheus.yml에 쓰기보다 Kubernetes custom resource로 선언한다.

| 리소스 | 기준 |
|---|---|
| ServiceMonitor | Service와 Endpoint를 기준으로 scrape |
| PodMonitor | Pod label과 Pod endpoint를 기준으로 scrape |
| PrometheusRule | alert/recording rule 선언 |

ServiceMonitor는 Service selector, namespace selector, endpoint port 이름이 맞아야 target을 만든다.

## 4. Dashboard는 답이 아니라 지도다
Grafana dashboard는 장애를 자동으로 고쳐주지 않는다. 하지만 다음 질문의 출발점을 준다.

```text
언제부터 CPU가 올랐는가?
어느 namespace가 memory를 많이 쓰는가?
restart가 늘어난 Pod는 무엇인가?
readiness 실패와 ingress 5xx가 같은 시점인가?
node 전체 압박인가, 특정 workload 문제인가?
```

## 5. Alert는 너무 민감해도 문제다
threshold가 낮으면 alert가 자주 울리고, 팀은 alert를 무시하게 된다. 좋은 alert는 “지금 사람이 개입해야 하는가”와 연결되어야 한다.

| 나쁜 alert | 더 나은 방향 |
|---|---|
| CPU 60% 1분 초과 | 10분 이상 지속 + latency/restart 영향 |
| Pod restart 1회 | 짧은 시간 반복 restart |
| target down 즉시 알림 | critical target, 지속 시간, 영향 범위 포함 |

