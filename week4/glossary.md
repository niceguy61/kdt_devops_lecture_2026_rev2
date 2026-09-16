# Week 4 Glossary: Kubernetes 운영 확장 용어

이 용어집은 정의 암기보다 **어떤 질문에 답하고 어떤 증거로 확인하는가**를 회복하기 위한 자료다. 먼저 한 줄 뜻을 가리고 설명한 뒤 확인 명령이나 화면을 찾아본다.

## Workload와 상태

### Running
- 한 줄 뜻: container process가 실행 중인 상태에 가까운 workload 상태
- 답하는 질문: process가 실행되고 있는가?
- 혼동 주의: traffic을 받을 준비가 되었다는 뜻은 아니다.
- 확인: `kubectl get pods`

### Ready
- 한 줄 뜻: readiness 기준을 통과해 traffic을 받을 수 있는 상태
- 답하는 질문: Service가 이 Pod를 endpoint로 사용할 수 있는가?
- 확인: `kubectl get pods`, `kubectl get endpoints`

### Readiness Probe
- 한 줄 뜻: Pod를 traffic에 포함할지 판단하는 검사
- 혼동 주의: 실패해도 process가 바로 재시작되는 것은 아니다.
- 확인: `kubectl describe pod`

### Liveness Probe
- 한 줄 뜻: process가 계속 살아 있는지 판단하는 검사
- 혼동 주의: 잘못 설정하면 정상적으로 시작 중인 앱을 재시작할 수 있다.
- 확인: Pod events와 restart count

### Resource Request / Limit
- 한 줄 뜻: 배치에 필요한 최소 자원과 사용할 수 있는 상한
- 답하는 질문: 어디에 배치할 수 있고 자원 압박 시 어떤 일이 생기는가?
- 확인: `kubectl describe pod`, `kubectl top pod`

## Traffic

### Service
- 한 줄 뜻: 변하는 Pod를 안정적인 DNS와 virtual IP 뒤에 묶는 Kubernetes object
- 혼동 주의: 외부 Gateway나 application health 자체와 같은 계층이 아니다.
- 확인: `kubectl get svc,endpointslice`

### EndpointSlice
- 한 줄 뜻: Service가 실제로 전달할 대상 endpoint 목록
- 답하는 질문: 현재 traffic을 받을 Pod가 무엇인가?
- 확인: `kubectl get endpointslice`

### Gateway
- 한 줄 뜻: 외부 traffic 진입과 listener 기준을 표현하는 API object
- 혼동 주의: Gateway만 만들어도 backend route가 자동으로 완성되지 않는다.
- 확인: `kubectl get gateway,gatewayclass`

### HTTPRoute
- 한 줄 뜻: host/path 요청을 어떤 Service로 보낼지 선언하는 route
- 확인: `kubectl get httproute`

## 관찰과 권한

### Logs
- 한 줄 뜻: process가 남긴 사건의 텍스트 증거
- 강점: 특정 오류 메시지와 실행 흐름
- 한계: 시간 추세와 전체 영향 범위를 혼자 보여주지 못함

### Events
- 한 줄 뜻: Kubernetes가 resource를 처리하며 남긴 상태 변화 이유
- 강점: scheduling, probe, image pull, admission 단서
- 확인: `kubectl describe`, `kubectl get events`

### Metrics
- 한 줄 뜻: 시간에 따른 수치 관찰 데이터
- 강점: 추세, 비율, 증가량
- 한계: metric 하나만으로 원인을 확정하지 못함

### Prometheus Target
- 한 줄 뜻: metric 수집 대상과 현재 scrape 상태
- 혼동 주의: target이 DOWN이면 Grafana 화면보다 먼저 수집 경계를 확인한다.
- 확인: Prometheus Targets 화면

### RBAC
- 한 줄 뜻: 주체가 특정 범위의 API 작업을 할 수 있는지 제한하는 권한 모델
- 확인: `kubectl auth can-i`

### Admission Deny
- 한 줄 뜻: API에 들어온 manifest가 정책을 위반해 생성·변경이 거부된 상태
- 혼동 주의: RBAC의 `forbidden`과 같은 오류 계층이 아니다.
- 확인: kubectl 오류, Kyverno policy/report/controller log

## GitOps와 Mesh

### Git Desired State
- 한 줄 뜻: Git repository에 선언된 운영 기준 상태
- 확인: commit, manifest, path, revision

### Sync
- 한 줄 뜻: Git desired state를 cluster object에 반영하는 작업
- 혼동 주의: Sync 성공은 application이 Healthy라는 뜻과 다르다.
- 확인: Argo CD Application의 Sync/Health

### Drift
- 한 줄 뜻: Git 기준과 cluster 실제 상태가 달라진 상태
- 확인: Argo CD diff, OutOfSync

### Sidecar
- 한 줄 뜻: 주 application container와 같은 Pod에 함께 실행되는 보조 container
- 확인: `kubectl get pod`의 `READY` 수, container 목록

### Data Plane / Control Plane
- Data plane: 실제 service-to-service 요청을 처리하는 proxy 계층
- Control plane: proxy 설정과 정책을 배포·관리하는 계층
- 혼동 주의: control plane이 실제 application request를 직접 처리한다고 보지 않는다.

## 회상 카드

1. Pod가 `Running`인데 `Ready`가 아니면 먼저 무엇을 확인하는가?
2. Service에 endpoint가 없을 때 Gateway와 application log 중 어디까지 확인해야 하는가?
3. `forbidden`과 `admission denied`를 어떻게 구분하는가?
4. Argo CD의 `Synced`와 `Healthy`가 다를 수 있는 이유는 무엇인가?
5. Logs, Events, Metrics가 각각 답하는 질문은 무엇인가?
