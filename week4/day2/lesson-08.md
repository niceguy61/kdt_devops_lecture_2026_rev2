# 8교시: 구름 EXP 배움일기

![Week 4 Day 2 Lesson 8](./assets/lesson-08-traffic-evidence-journal.png)

## 수업 목표
- Service, DNS, Ingress, Endpoint의 차이를 evidence 중심으로 정리한다.
- traffic 장애를 404/503/connection refused/timeout으로 나누어 기록한다.
- W4D3 observability로 이어질 질문을 남긴다.

## 오늘 배운 내용 요약
| 주제 | 핵심 문장 |
|---|---|
| Service | Pod IP 변화를 가리는 안정적인 내부 진입점 |
| Endpoint | 실제 traffic을 받을 Ready Pod IP 목록 |
| DNS | Service 이름을 ClusterIP로 해석 |
| Ingress | host/path rule로 외부 요청을 Service에 연결 |
| ingress-nginx | Ingress rule을 실제 NGINX proxy 설정으로 반영 |
| NetworkPolicy | 누가 누구에게 갈 수 있는지 제한 |
| rollout | Ready Pod 교체가 외부 응답으로 드러남 |

## 배움일기 작성 표
| 항목 | 기록 |
|---|---|
| ingress-nginx release/namespace |  |
| IngressClass 이름 |  |
| frontend Service port/endpoint |  |
| api Service port/endpoint |  |
| `/` 응답 확인 |  |
| `/api` 응답 확인 |  |
| 가장 헷갈린 장애 |  |
| 404 원인 후보 |  |
| 503 원인 후보 |  |
| connection refused 원인 후보 |  |
| NetworkPolicy에서 DNS가 필요한 이유 |  |
| rollout 전/후 API 응답 |  |

## 작성 예시
| 항목 | 기록 예시 |
|---|---|
| ingress-nginx release/namespace | `ingress-nginx` / `ingress-nginx` |
| IngressClass 이름 | `nginx` |
| frontend Service port/endpoint | `80 -> 10.244.x.x:80` |
| api Service port/endpoint | `80 -> 10.244.x.x:8080` |
| `/` 응답 확인 | frontend HTML 확인 |
| `/api` 응답 확인 | `{"service":"api","version":"v1","status":"ok"}` |
| 가장 헷갈린 장애 | Service는 있는데 endpoint가 `<none>`인 상황 |
| 404 원인 후보 | host/path 불일치, class 처리 안 됨 |
| 503 원인 후보 | endpoint 없음, readiness 실패 |
| connection refused 원인 후보 | port-forward/controller Service 문제 |
| NetworkPolicy에서 DNS가 필요한 이유 | Service 이름 해석에 kube-dns가 필요 |
| rollout 전/후 API 응답 | v1 -> v2 -> rollback v1 |

## Traffic 장애 기록 템플릿
```markdown
## 증상
- 요청:
- 응답 코드/메시지:

## Ingress
- host:
- path:
- ingressClassName:
- backend service/port:

## Service/Endpoint
- service port:
- targetPort:
- endpoint:

## Pod
- READY:
- logs/event:

## 판단
- 가장 가능성 높은 원인:
- 다음 확인:
```

## 오늘의 evidence 명령
```bash
helm list -n ingress-nginx
kubectl get ingressclass
kubectl -n ingress-nginx get deploy,pod,svc
kubectl -n week4 get ingress
kubectl -n week4 describe ingress paperclip
kubectl -n week4 get svc,endpoints -o wide
curl -H "Host: paperclip.local" http://localhost:8080/
curl -H "Host: paperclip.local" http://localhost:8080/api
kubectl -n week4 rollout history deploy/api
```

## 장애별 한 줄 판별법
| 증상 | 한 줄 판별 |
|---|---|
| 404 | Ingress host/path/class부터 본다 |
| 503 | Service endpoint와 Pod readiness부터 본다 |
| connection refused | port-forward 또는 controller Service 접근부터 본다 |
| DNS failure | Service 이름, namespace, CoreDNS, NetworkPolicy DNS egress를 본다 |
| v1/v2 응답 혼재 | rollout 중 endpoint와 ReplicaSet을 본다 |

## 좋은 기록과 아쉬운 기록
| 아쉬운 기록 | 좋은 기록 |
|---|---|
| Ingress가 안 됐다 | `curl -H Host... /api`가 503, `endpoints/api <none>` 확인 |
| DNS 문제였다 | `nslookup api` 실패, CoreDNS와 NetworkPolicy DNS egress 확인 |
| 배포했다 | `rollout status deploy/api` 성공, `/api` 응답 v1 -> v2 확인 |
| 헷갈렸다 | Service port 80과 targetPort 8080을 혼동했다고 기록 |

## W4D3로 이어지는 질문
내일은 observability로 넘어간다. 오늘 남겨야 할 질문은 다음이다.

| 질문 | W4D3 연결 |
|---|---|
| 503이 늘어났는지 어떻게 알 수 있는가 | ingress/controller metric |
| endpoint가 줄어든 순간을 dashboard로 볼 수 있는가 | Pod readiness/restart metric |
| CPU/memory 증가와 latency를 같이 볼 수 있는가 | Prometheus/Grafana |
| target down은 어디서 확인하는가 | Prometheus target |
| 운영팀에 어떤 정보를 전달해야 하는가 | runbook과 dashboard 링크 |

## W4D3 준비 메모
W4D3에서는 같은 traffic을 dashboard와 metric으로 본다. 오늘의 evidence가 있어야 내일 metric을 해석할 수 있다.

| 오늘 증거 | 내일 연결 |
|---|---|
| endpoint `<none>` | ready replica, endpoint, ingress 5xx |
| rollout v1 -> v2 | deployment revision, restart, latency 변화 |
| controller log | ingress-nginx metric과 log |
| NetworkPolicy preview | policy로 인한 timeout 해석 |
| Service DNS | CoreDNS와 target discovery |

## 오늘의 runbook 초안
```markdown
## External traffic runbook

1. 사용자가 본 URL과 status code를 확인한다.
2. Ingress host/path/class가 맞는지 확인한다.
3. backend Service 이름과 port가 맞는지 확인한다.
4. Endpoint가 비어 있지 않은지 확인한다.
5. Pod READY와 event를 확인한다.
6. ingress-nginx controller log를 확인한다.
7. rollout 직후라면 ReplicaSet과 endpoint 변화를 확인한다.
8. NetworkPolicy가 있다면 DNS egress와 backend 허용선을 확인한다.
```

## 스스로 점검할 질문
| 질문 | 답 |
|---|---|
| Ingress는 Pod로 직접 보내는가 | 아니오, Service로 보낸다 |
| Endpoint는 무엇을 의미하는가 | Ready Pod IP와 port 목록 |
| Service port와 targetPort는 같은가 | 같을 수도 있지만 다를 수 있다 |
| Host header가 왜 중요한가 | Ingress host rule과 매칭되기 때문이다 |
| 503이면 어디부터 보는가 | Service endpoint와 Pod readiness |
| NetworkPolicy에서 DNS를 왜 여는가 | Service 이름 해석이 필요하기 때문이다 |

## 최종 한 문단
```markdown
오늘은 frontend/api/db 구조를 Service DNS로 연결하고, ingress-nginx를 Helm으로 설치해 `/`와 `/api`를 외부 경로로 노출했다. Service가 있어도 Endpoint가 비면 traffic은 갈 곳이 없고, Ingress 장애는 host/path/class/service/endpoint/readiness 순서로 좁혀야 한다. NetworkPolicy는 routing이 아니라 허용선이며 DNS egress를 잊으면 Service 이름 해석부터 실패할 수 있다. rollout은 Ready endpoint를 통해 외부 응답에 반영된다.
```

## 다음 수업 전 체크
W4D3에서 observability를 진행하기 전에 아래 상태를 확인한다.

| 확인 | 명령 |
|---|---|
| ingress-nginx 유지 여부 | `helm list -n ingress-nginx` |
| app namespace 유지 여부 | `kubectl get ns week4` |
| Ingress rule | `kubectl -n week4 get ingress` |
| API 응답 | `curl -H "Host: paperclip.local" http://localhost:8080/api` |
| metrics-server 유지 여부 | `helm list -n kube-system` |

Ingress와 app을 삭제했다면 W4D3 초반에 다시 올리고 관찰 stack을 붙인다.

## Evidence Note
```markdown
# W4D2S8 final journal
- 오늘 확인한 정상 경로:
- 가장 이해가 어려웠던 계층:
- 내가 본 장애 출력:
- 그 출력의 원인 후보:
- W4D3에서 dashboard로 보고 싶은 지표:
- 내 runbook의 첫 번째 확인 명령:
```

## 한 줄 요약
```text
W4D2의 핵심은 외부 traffic을 Ingress에서 Pod endpoint까지 층별 증거로 추적하는 것이다.
```
