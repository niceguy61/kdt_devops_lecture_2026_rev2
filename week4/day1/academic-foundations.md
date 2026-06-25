# Academic Foundations: W4D1 운영 가능한 Kubernetes Workload

## 1. Kubernetes 기본 실행에서 운영 기준으로
W3D5까지의 핵심 질문은 “Pod, Deployment, Service가 어떻게 실행되는가”였다. W4D1부터의 질문은 달라진다.

```text
이 workload는 운영 환경에서 설정을 바꿀 수 있는가?
민감정보를 image 안에 넣지 않았는가?
죽었는지, 준비됐는지 Kubernetes가 판단할 수 있는가?
얼마나 많은 CPU/memory를 요구하는지 선언되어 있는가?
관찰 가능한 metric이 있는가?
```

Deployment가 정상 Running이어도 운영 가능한 상태라고 단정할 수 없다. readiness가 실패하면 사용자 traffic을 받으면 안 되고, memory limit을 넘으면 OOMKilled가 발생하며, metric이 없으면 HPA나 capacity 판단도 어렵다.

## 2. Helm이 필요한 이유
Kubernetes add-on은 보통 하나의 YAML 파일로 끝나지 않는다. Deployment, ServiceAccount, ClusterRole, ClusterRoleBinding, Service, ValidatingWebhookConfiguration, ConfigMap 같은 리소스가 묶여 들어간다.

Helm은 이 묶음을 chart로 관리한다.

| 용어 | 의미 | 실무 질문 |
|---|---|---|
| Chart | 설치 가능한 Kubernetes 리소스 패키지 | 무엇을 설치하는가 |
| Repository | chart 저장소 | 어디서 가져오는가 |
| Release | cluster에 설치된 chart instance | 어떤 이름으로 설치됐는가 |
| Values | chart template에 넣는 설정 | 우리 환경에 맞게 무엇을 바꾸는가 |
| Upgrade | release를 새 chart/values로 갱신 | 어떻게 변경하는가 |
| Rollback | 이전 revision으로 되돌림 | 잘못된 변경을 어떻게 되돌리는가 |
| Uninstall | release 제거 | 실습 후 어떻게 정리하는가 |

수업 표준은 다음이다.

```bash
helm repo add <repo-name> <repo-url>
helm repo update
helm upgrade --install <release> <repo/chart> \
  --namespace <namespace> \
  --create-namespace \
  -f <values-file>
helm status <release> -n <namespace>
helm list -n <namespace>
```

긴 `--set` 명령은 빠른 확인용으로만 사용한다. 강의에서는 values file을 repo 안에 남겨 어떤 설정으로 설치했는지 추적 가능하게 만든다.

## 3. ConfigMap과 Secret
ConfigMap은 민감하지 않은 설정을 image 밖으로 분리한다. Secret은 password, token, key처럼 민감한 값을 Kubernetes object로 분리한다.

중요한 점은 Secret이 “자동으로 안전해진 비밀 저장소”가 아니라는 것이다. Kubernetes Secret의 값은 기본적으로 base64 인코딩된 형태다. base64는 암호화가 아니며, RBAC, etcd encryption, external secret manager, Git secret scanning 같은 보완책이 필요하다.

| 구분 | ConfigMap | Secret |
|---|---|---|
| 용도 | endpoint, feature flag, log level | password, token, API key |
| 기본 표현 | plain text | base64 인코딩 |
| Git 저장 | 가능하지만 환경별 주의 필요 | 실제 값은 저장 금지 |
| Pod 주입 | env, envFrom, volume | env, envFrom, volume |

Docker에서 `.env.dev`, `.env.staging`, `.env.prod`로 환경을 나누던 감각은 Kubernetes에서도 이어진다. 다만 Kubernetes에서는 그 파일을 그대로 운영 secret으로 commit하지 않고, 환경별 ConfigMap/Secret 또는 이후 Terraform/Secret Manager 흐름으로 연결한다.

## 4. Probe
Probe는 Kubernetes가 container의 상태를 판단하는 질문이다.

| Probe | 질문 | 실패 시 영향 |
|---|---|---|
| startupProbe | 애플리케이션이 시작을 완료했는가 | 성공 전까지 liveness/readiness 판단 지연 |
| readinessProbe | 지금 traffic을 받아도 되는가 | Service endpoint에서 제외 |
| livenessProbe | process를 재시작해야 하는가 | container restart |

readiness 실패는 애플리케이션 bug가 아니어도 사용자 장애가 될 수 있다. 예를 들어 backend가 DB migration 중이라 `/ready`가 실패하면 Pod는 Running이어도 Service endpoint에서 빠져야 한다.

## 5. Resource Requests/Limits
Kubernetes scheduler는 resource request를 보고 Pod를 배치한다. Limit은 container가 사용할 수 있는 상한을 만든다.

| 설정 | 의미 | 없을 때 생기는 문제 |
|---|---|---|
| `requests.cpu` | 필요한 CPU 최소량 | scheduling과 capacity 계획이 불명확 |
| `requests.memory` | 필요한 memory 최소량 | node overcommit 판단 어려움 |
| `limits.cpu` | CPU 사용 상한 | 과도한 CPU 사용 통제 어려움 |
| `limits.memory` | memory 사용 상한 | 초과 시 OOMKilled 기준 없음 |

Memory limit 초과는 OOMKilled로 이어질 수 있고, CPU limit은 throttling으로 latency를 늘릴 수 있다. 그래서 requests/limits는 “넣으면 좋은 옵션”이 아니라 운영 용량 계획의 언어다.

## 6. Metrics Server
metrics-server는 kubelet에서 resource metric을 수집해 Kubernetes Metrics API로 제공한다. `kubectl top node`, `kubectl top pod`는 이 API를 사용한다.

metrics-server는 Prometheus/Grafana를 대체하지 않는다. 목적이 다르다.

| 도구 | 주 용도 |
|---|---|
| metrics-server | CPU/memory 현재 사용량, HPA/VPA의 기본 resource metric |
| Prometheus | 시계열 metric 저장, query, alerting |
| Grafana | dashboard 시각화 |

kind/local 실습에서는 kubelet certificate 검증 문제 때문에 `--kubelet-insecure-tls`가 필요할 수 있다. 이 설정은 로컬 실습 편의용이며 운영 환경의 기본값으로 가져가면 안 된다.

