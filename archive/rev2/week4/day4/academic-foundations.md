# Academic Foundations: W4D4 RBAC과 Policy

## 권한과 정책은 다르다
Kubernetes 보안에서 RBAC과 admission policy는 서로 다른 질문에 답한다.

| 영역 | 질문 | 예시 |
|---|---|---|
| RBAC | 이 주체가 이 API 동작을 할 수 있는가 | `readonly-viewer`가 Pod를 delete할 수 있는가 |
| Admission Policy | 이 object를 cluster에 받아도 되는가 | `nginx:latest` Pod를 생성해도 되는가 |

RBAC은 API 요청자의 권한을 판단하고, Kyverno 같은 admission controller는 요청된 manifest의 내용을 판단한다.

## RBAC 구성요소
| 요소 | 의미 |
|---|---|
| Subject | user, group, ServiceAccount |
| Verb | get, list, watch, create, update, delete 등 |
| Resource | pods, deployments, services 같은 API resource |
| Role | namespace scope 권한 규칙 |
| ClusterRole | cluster scope 또는 여러 namespace에 재사용 가능한 권한 규칙 |
| RoleBinding | subject와 Role/ClusterRole을 namespace에서 연결 |
| ClusterRoleBinding | subject와 ClusterRole을 cluster 전체에 연결 |

권한은 "누구에게", "어떤 resource에", "어떤 동작을", "어떤 scope에서" 허용할지로 읽는다.

## ServiceAccount
사람은 보통 kubeconfig의 user로 API를 호출하지만, Pod 안의 application은 ServiceAccount로 API를 호출한다. 그래서 workload에 적절한 ServiceAccount를 지정하지 않으면 default ServiceAccount가 사용된다.

| 선택 | 운영 영향 |
|---|---|
| default ServiceAccount 사용 | 어떤 권한/토큰 설정인지 추적이 어려움 |
| app 전용 ServiceAccount | workload identity를 명확히 분리 |
| automount token false | 앱이 Kubernetes API를 쓰지 않을 때 공격면 감소 |
| automount token true | API 호출이 필요한 controller/operator에만 제한적으로 사용 |

## Admission 흐름
Kubernetes API 요청은 대략 다음 단계를 지난다.

```text
kubectl / controller / CI
  -> authentication
  -> authorization(RBAC)
  -> admission
  -> persistence(etcd)
```

RBAC에서 거절되면 `forbidden`이 나오고, admission에서 거절되면 webhook 또는 policy 이름이 포함된 deny 메시지가 나온다.

## Kyverno
Kyverno는 Kubernetes resource를 Kubernetes resource로 검증하는 policy engine이다. 별도 언어를 많이 배우기보다 YAML 기반으로 validate/mutate/generate 정책을 작성할 수 있다.

오늘은 validate에 집중한다.

| 정책 | 목적 |
|---|---|
| required label | 소유자/팀/비용 기준 누락 방지 |
| disallow latest | 재현 불가능한 배포 tag 방지 |
| disallow privileged | container 탈출 위험 감소 |
| disallow hostPath | node filesystem 접근 위험 감소 |

## Audit과 Enforce
| 모드 | 동작 |
|---|---|
| Audit | 위반을 기록하지만 생성은 허용 |
| Enforce | 위반 object 생성을 거절 |

운영에서는 새 정책을 바로 Enforce로 넣기보다 Audit으로 영향 범위를 확인하고, 예외와 migration 계획을 세운 뒤 Enforce로 전환하는 경우가 많다.

## 수업 범위
오늘은 PSP, PSA, OPA Gatekeeper, cloud IAM 연동을 깊게 다루지 않는다. 대신 학생들이 장애 상황에서 "권한 문제인지, 정책 문제인지"를 빠르게 구분하는 것을 목표로 한다.
