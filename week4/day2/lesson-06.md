# 6교시: NetworkPolicy Preview

![Week 4 Day 2 Lesson 6](./assets/lesson-06-networkpolicy-preview.png)

## 수업 목표
- frontend -> api -> db traffic 허용선을 설계한다.
- NetworkPolicy가 왜 DNS egress를 고려해야 하는지 설명한다.
- kind 기본 CNI에서는 NetworkPolicy가 강제되지 않을 수 있음을 명확히 구분한다.

## 왜 NetworkPolicy가 필요한가
Service와 Ingress는 “어디로 보낼 것인가”를 다룬다. NetworkPolicy는 “누가 누구에게 갈 수 있는가”를 다룬다.

운영 기준:
```text
사용자 -> Ingress -> frontend/api
frontend -> api 허용
api -> db 허용
frontend -> db 차단
알 수 없는 Pod -> db 차단
DNS egress 허용
```

host에서 db에 직접 접근하는 구조는 만들지 않는다. db는 내부 backend dependency로 남겨둔다.

## 오늘 manifest 보기
```bash
cat week4/day2/labs/traffic-routing/networkpolicy-preview.yaml
```

적용:
```bash
kubectl apply -f week4/day2/labs/traffic-routing/networkpolicy-preview.yaml
kubectl -n week4 get networkpolicy
```

예상 출력:
```text
NAME                           POD-SELECTOR   AGE
default-deny-all               <none>         5s
allow-dns-egress               <none>         5s
allow-frontend-to-api          app=api        5s
allow-frontend-egress-to-api   app=frontend   5s
allow-api-to-db                app=postgres   5s
allow-api-egress-to-db         app=api        5s
```

`default-deny-all`과 `allow-dns-egress`의 `podSelector: {}`는 namespace 안 모든 Pod를 대상으로 한다. 그 위에 역할별 허용 policy를 추가해 필요한 통신만 열어준다.

## CNI 주의
NetworkPolicy는 Kubernetes API object지만, 실제 packet 차단은 CNI plugin이 수행한다.

| 환경 | 주의 |
|---|---|
| kind 기본 CNI | NetworkPolicy enforcement가 기대처럼 동작하지 않을 수 있음 |
| Calico/Cilium | NetworkPolicy enforcement 가능 |
| cloud managed cluster | provider/CNI 설정 확인 필요 |

따라서 오늘은 정책 강제 실험보다 “어떤 traffic을 허용해야 하는가”를 preview로 본다.

## DNS egress를 빼먹으면 생기는 문제
Service 이름 호출은 DNS가 필요하다.

```bash
curl http://api
```

이 요청은 먼저 `api.week4.svc.cluster.local`을 DNS로 해석한다. egress policy에서 kube-dns/CoreDNS로 가는 53번 UDP/TCP를 막으면 Service 이름이 풀리지 않는다.

대표 증상:
```text
Could not resolve host: api
```

이때 app이 죽은 것이 아니라 DNS egress가 막혔을 수 있다.

## traffic matrix
| Source | Destination | 허용 여부 | 이유 |
|---|---|---|---|
| frontend | api | 허용 | 사용자 기능 호출 |
| api | postgres | 허용 | 데이터 접근 |
| frontend | postgres | 차단 의도 | db 직접 접근 방지 |
| unknown Pod | postgres | 차단 의도 | lateral movement 방지 |
| app Pod | kube-dns | 허용 | Service DNS 필요 |

## 정책별 의미
| Policy | 대상 | 의미 |
|---|---|---|
| `default-deny-all` | 모든 Pod | 기본 ingress/egress 차단 |
| `allow-dns-egress` | 모든 Pod | kube-dns 53번 허용 |
| `allow-frontend-to-api` | api Pod ingress | frontend에서 api로 들어오는 traffic 허용 |
| `allow-frontend-egress-to-api` | frontend Pod egress | frontend가 api로 나가는 traffic 허용 |
| `allow-api-to-db` | postgres Pod ingress | api에서 db로 들어오는 traffic 허용 |
| `allow-api-egress-to-db` | api Pod egress | api가 db로 나가는 traffic 허용 |

NetworkPolicy는 ingress와 egress 양쪽을 나누어 생각해야 한다. egress default deny가 걸려 있으면 source Pod에서 나가는 것도 열어야 한다.

## NetworkPolicy와 Ingress는 다른 문제다
Ingress는 외부 요청을 Service로 보낸다. NetworkPolicy는 Pod 간 network path를 제한한다.

```text
Ingress 정상
Service 정상
Endpoint 정상
NetworkPolicy가 backend traffic 차단
  -> timeout 또는 connection 문제
```

즉 Ingress rule이 맞아도 NetworkPolicy 때문에 backend 연결이 안 될 수 있다.

## 강제되지 않는 환경에서의 확인법
kind 기본 CNI처럼 policy가 강제되지 않는 환경에서는 정책을 적용해도 통신이 계속 될 수 있다.

```bash
kubectl -n week4 get networkpolicy
kubectl -n week4 describe networkpolicy allow-frontend-to-api
```

이 경우 오늘의 목표는 “차단 결과”가 아니라 “어떤 label과 port를 기준으로 정책을 작성하는가”다. 실제 차단 효과는 Calico/Cilium 같은 CNI 환경에서 확인하는 것이 맞다.

## 확인 명령
```bash
kubectl -n week4 describe networkpolicy default-deny-all
kubectl -n week4 describe networkpolicy allow-frontend-to-api
kubectl -n week4 describe networkpolicy allow-api-to-db
kubectl -n week4 get pod --show-labels
kubectl -n kube-system get pod -l k8s-app=kube-dns --show-labels
```

확인할 것:
| 확인 | 이유 |
|---|---|
| Pod label | policy selector가 label 기반 |
| kube-dns label | DNS egress rule 대상 |
| namespace label | `kubernetes.io/metadata.name` 사용 여부 |

## 운영에서 더 나은 구성
오늘 manifest도 역할별로 나누어 둔다. 운영에서는 여기에 namespace, ServiceAccount, app tier, environment label을 더해 정책을 세분화한다.

| Policy | 목적 |
|---|---|
| `allow-frontend-to-api` | frontend가 api 호출 |
| `allow-api-to-db` | api가 db 호출 |
| `allow-dns-egress` | DNS 해석 허용 |
| `default-deny` | 나머지 기본 차단 |

## label이 정책의 API다
NetworkPolicy는 Pod 이름이 아니라 label을 본다. 그래서 label 설계가 곧 network policy 설계가 된다.

```bash
kubectl -n week4 get pod --show-labels
```

예상 출력:
```text
frontend-xxxxx   app=frontend,tier=web
api-yyyyy        app=api,tier=api
postgres-zzzzz   app=postgres,tier=db
```

정책은 이 label을 기준으로 source와 destination을 고른다. label이 부정확하면 정책도 부정확해진다.

## 잘못된 policy의 흔한 결과
| 실수 | 증상 |
|---|---|
| DNS egress 누락 | `Could not resolve host: api` |
| egress만 열고 ingress를 안 엶 | source는 나가려 하지만 destination이 거부 |
| ingress만 열고 egress를 안 엶 | source Pod에서 나가는 traffic이 차단 |
| port를 Service port로 착각 | 실제 Pod port 기준과 불일치 |
| label 오타 | policy가 기대한 Pod에 적용되지 않음 |

NetworkPolicy의 port는 일반적으로 Pod가 실제로 받는 port를 기준으로 생각해야 한다. Service port와 targetPort가 다른 경우 특히 주의한다.

## 오늘은 차단 실험보다 설계 실험이다
강제 가능한 CNI가 있는 환경이라면 다음을 테스트할 수 있다.

```bash
frontend -> api 성공
frontend -> postgres 실패
api -> postgres 성공
unknown pod -> api/db 실패
```

하지만 kind 기본 CNI에서는 결과가 다를 수 있으므로, 오늘은 manifest를 읽고 traffic matrix를 설명하는 것을 성공 기준으로 둔다.

## Evidence Note
```markdown
# W4D2S6 NetworkPolicy preview
- default deny policy:
- DNS egress policy:
- frontend -> api policy:
- api -> db policy:
- kind 기본 CNI 주의:
- DNS egress를 빼먹으면 생기는 증상:
- label이 틀리면 생기는 문제:
```

## 한 줄 요약
```text
NetworkPolicy는 routing이 아니라 허용선을 정하는 정책이며, DNS egress를 빼먹으면 Service 이름부터 깨질 수 있다.
```
