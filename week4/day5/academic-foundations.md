# Academic Foundations: W4D5 GitOps와 Mesh

## CI와 CD 분리
GitHub Actions는 주로 code를 test/build/push하는 CI gate로 다뤘다. Argo CD는 Git에 선언된 Kubernetes manifest를 cluster에 반영하는 CD/GitOps 도구다.

| 영역 | 책임 |
|---|---|
| CI | test, scan, image build, registry push |
| CD/GitOps | Git manifest를 cluster desired state로 sync |
| Registry | versioned artifact 보관 |
| Kubernetes | desired/current state reconcile |

## GitOps
GitOps는 Git repository를 운영 desired state의 기준으로 삼는다. 사람이 cluster에서 직접 바꾼 값은 drift가 되고, Git과 cluster 상태 차이는 OutOfSync로 보인다.

```text
Git manifest
  -> Argo CD Application
  -> Kubernetes API
  -> cluster state
```

## Argo CD 핵심 요소
| 요소 | 의미 |
|---|---|
| Application | repo/path/revision/destination 정의 |
| Project | Application 권한/범위 묶음 |
| Sync | Git 상태를 cluster에 반영 |
| OutOfSync | Git과 cluster 상태가 다름 |
| Healthy | workload runtime 상태가 정상 |
| Prune | Git에서 사라진 리소스를 cluster에서도 삭제 |
| Self-heal | cluster drift를 자동 복구 |

## Namespace를 넘어 통신하고 관찰하는 원리
Kubernetes namespace는 이름과 권한 범위를 나누는 논리적 경계다. network가 기본적으로 namespace마다 완전히 끊어지는 것은 아니다. 별도 NetworkPolicy가 없다면 Pod는 다른 namespace의 Service로 통신할 수 있다.

```text
http://service-name.namespace-name.svc.cluster.local
```

하지만 "통신 가능"과 "API로 조회/변경 가능"은 다르다.

| 구분 | 기준 | 예시 |
|---|---|---|
| Service 통신 | Cluster DNS, Service, EndpointSlice, CNI | `argocd-server.argocd.svc`, `kiali.istio-system.svc` |
| Kubernetes API 접근 | ServiceAccount token, RBAC | Argo CD가 다른 namespace에 Deployment 생성 |
| Node/cluster metric 수집 | API aggregation, kubelet/API 권한 | metrics-server가 node metric 수집 |
| 관찰 도구의 namespace 조회 | ServiceMonitor/selector/RBAC | Prometheus/Kiali가 여러 namespace metric 조회 |

Helm chart가 `kube-system`, `monitoring`, `argocd`, `istio-system` 같은 system 영역에 설치되어도 다른 namespace를 볼 수 있는 이유는 보통 ServiceAccount와 ClusterRole/ClusterRoleBinding이 함께 설치되기 때문이다.

```text
Pod in argocd namespace
  -> ServiceAccount token
  -> Kubernetes API server
  -> RBAC check
  -> read/apply resources in target namespace
```

metrics-server도 application namespace에 들어가서 Pod를 뒤지는 방식이 아니다. `kube-system`에 설치된 뒤 Kubernetes API aggregation과 kubelet 통신을 통해 node/pod resource metric을 제공한다. 그래서 `kubectl top pod -n some-namespace`는 namespace의 app Pod가 metrics-server와 직접 통신해서 나오는 값이 아니라, API server를 통해 metrics API를 조회한 결과다.

Argo CD도 비슷하다. Argo CD component는 `argocd` namespace에 있지만, Application의 destination namespace에 리소스를 만들 수 있다. 이때 실제 판단 기준은 "argocd namespace에 있으니 자동으로 가능"이 아니라 "Argo CD controller ServiceAccount에 어떤 RBAC 권한이 부여되었는가"다.

## Service Mesh
Service mesh는 application code 밖에서 service-to-service traffic을 관찰하고 제어하는 계층이다. Istio는 Pod에 Envoy sidecar를 붙여 traffic을 가로채고 정책을 적용한다.

| 개념 | 의미 |
|---|---|
| sidecar | app container 옆의 proxy container |
| Envoy | data plane proxy |
| istiod | control plane |
| mTLS | service 간 암호화/identity |
| VirtualService | routing, retry, fault injection 등 traffic rule |
| Kiali | mesh graph와 config validation UI |

## 오늘의 범위
오늘은 mesh를 운영 수준으로 깊게 튜닝하지 않는다. 목표는 “왜 mesh가 필요한가”, “sidecar가 어떻게 보이는가”, “traffic graph와 delay preview를 어떻게 확인하는가”다.

## 주의
Argo CD, Istio, Kiali는 모두 가벼운 add-on이 아니다. kind local에서 resource가 부족하면 Pod Pending/OOM이 생길 수 있다. 수업 중에는 필요한 component만 Helm values로 작게 설치하고, cleanup 기준을 명확히 둔다.
