# Week 4: Kubernetes 운영 확장

Week 4는 W3D4~W3D5에서 시작한 Kubernetes 기본 흐름을 운영 가능한 MSA 배포 기준으로 확장한다. 모든 add-on 설치는 Helm을 기본 표준으로 사용하고, 설치 명령마다 release name, namespace, values file, 검증 명령, 제거 명령을 함께 남긴다.

## Cluster Safety Rule
매일 1교시는 오늘 사용할 kind cluster를 만들고 context를 고정하는 것으로 시작한다. 매일 8교시는 cluster를 유지할지 삭제할지 명시하고 evidence를 남기는 것으로 끝낸다.

```bash
bash week4/scripts/create-kind-cluster.sh paperclip-w4d2
bash week4/scripts/ensure-kind-context.sh paperclip-w4d2
```

수업 중 새 manifest를 적용하기 전에는 `ensure-kind-context.sh`를 반복한다. context 확인을 생략하면 다른 local Kubernetes cluster에 Helm chart나 manifest를 적용할 수 있다.

종료 시 삭제하는 경우:
```bash
bash week4/scripts/delete-kind-cluster.sh paperclip-w4d2
```

## Day Index
| 일차 | 주제 | 핵심 산출물 |
|---|---|---|
| Day1 | 운영 가능한 workload와 resource 관찰 | Helm 설치 루프, ConfigMap/Secret, probe, resource, metrics-server |
| Day2 | Service, DNS, Gateway API, 외부 traffic | Envoy Gateway Helm 설치, Gateway/HTTPRoute routing |
| Day3 | 장애와 성능 관찰 | kube-prometheus-stack, Prometheus target, Grafana dashboard |
| Day4 | 권한과 정책 | RBAC, Kyverno admission policy |
| Day5 | GitOps와 mesh preview | Argo CD, Istio, Kiali preview |
