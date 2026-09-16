# Week 4 Day4: Kubernetes Security - RBAC과 Kyverno

## Overview
W4D4는 Kubernetes 운영에서 "누가 무엇을 할 수 있는가"와 "무엇을 배포할 수 있는가"를 분리해서 다룬다. W4D1~D3에서 workload, traffic, observability를 확인했다면, 오늘은 RBAC으로 API 권한을 제한하고 Kyverno로 admission 단계에서 위험한 manifest를 차단한다.

실습 cluster는 kind 기준으로 진행한다. Kyverno는 Helm으로 설치하며, RBAC은 Kubernetes 기본 object인 ServiceAccount, Role, RoleBinding을 직접 작성한다.

## Learning Goals
- Kubernetes 권한 모델에서 user, group, ServiceAccount, Role, ClusterRole, RoleBinding을 구분한다.
- `kubectl auth can-i`로 권한을 확인하고 `forbidden` 오류를 읽는다.
- default ServiceAccount와 workload 전용 ServiceAccount의 차이를 설명한다.
- automountServiceAccountToken이 왜 중요한지 확인한다.
- Kyverno를 Helm으로 설치하고 admission controller/webhook Pod를 확인한다.
- Audit 정책과 Enforce 정책의 차이를 설명한다.
- `latest` image tag, owner label 누락, privileged container, hostPath를 정책으로 다룬다.
- RBAC forbidden과 Kyverno admission deny를 분리해서 troubleshooting note를 작성한다.

## Lesson Index
| 교시 | 주제 | 핵심 확인 |
|---|---|---|
| 1교시 | Day3 요약 + Kubernetes 권한 모델 | subject, verb, resource, scope |
| 2교시 | RBAC 최소 권한 실습 | ServiceAccount, Role, RoleBinding, forbidden |
| 3교시 | app Pod와 ServiceAccount | default SA, token mount, workload identity preview |
| 4교시 | Kyverno Helm 설치 | Kyverno admission/webhook/CRD 필수; External Secrets Operator는 선택 읽을거리 |
| 5교시 | Kyverno policy 1 | latest tag 금지, required label, Audit/Enforce |
| 6교시 | Kyverno policy 2 | privileged, hostPath 제한과 admission deny |
| 7교시 | 권한/정책 장애 분석 | RBAC forbidden vs Kyverno deny |
| 8교시 | 구름 EXP 배움일기 | security evidence와 다음 운영 질문 |

## Practice Files
| 자료 | 용도 |
|---|---|
| `hands-on-lab.md` | 전체 실습 순서 |
| `academic-foundations.md` | RBAC/admission/Kyverno 개념 정리 |
| `labs/rbac/` | namespace, ServiceAccount, Role, RoleBinding, workload |
| `labs/kyverno/values.yaml` | Kyverno Helm values |
| `labs/kyverno/*policy*.yaml` | 수업용 Kyverno 정책 |
| `labs/kyverno/bad-*.yaml` | 정책 위반 manifest |
| `labs/kyverno/good-pod.yaml` | 정책 통과 manifest |

## Verified Baseline
검증 기준:
```text
kind cluster Ready
RBAC can-i yes/no 확인 가능
Kyverno admission controller Running
bad-latest Pod는 admission denied
bad-privileged-hostpath Pod는 admission denied
good-versioned-owner Pod는 Running 또는 Completed 전 단계까지 생성
```

## Official References
| Topic | Reference |
|---|---|
| Kubernetes RBAC | https://kubernetes.io/docs/reference/access-authn-authz/rbac/ |
| Service Accounts | https://kubernetes.io/docs/concepts/security/service-accounts/ |
| Admission Controllers | https://kubernetes.io/docs/reference/access-authn-authz/admission-controllers/ |
| Kyverno Installation | https://kyverno.io/docs/installation/ |
| Kyverno Policies | https://kyverno.io/policies/ |

## 학습 제어: 회상·핵심·복구

### 시작 5분 회상
W4D3의 logs/events/metrics 차이를 자료 없이 구분하고, 각 증거가 답하지 못하는 질문도 하나씩 적는다.

### 오늘 반드시 가져갈 것
1. RBAC은 API 요청의 주체·동사·resource·scope를 제한한다.
2. Kyverno는 admission 단계에서 manifest를 허용하거나 거부한다.
3. `forbidden`과 `admission denied`는 서로 다른 실패 계층이다.

### 최소 복구 경로
`kubectl auth can-i` → 대상 ServiceAccount/Role/Binding 확인 → manifest 정책 위반 여부 확인 → admission/controller 로그 확인 순서로 복구한다. 다음 날로 넘어가기 전 권한 실패와 정책 실패의 첫 확인 위치를 각각 말할 수 있어야 한다.