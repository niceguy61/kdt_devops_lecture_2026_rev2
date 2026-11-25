# 누가 거절했나 — 거절 메시지 지도 (6교시)

| 메시지 (예) | 누가 | 어디서 보나 | 고치는 곳 |
|---|---|---|---|
| `Error from server (Forbidden): … cannot list resource "secrets" …` | apiserver **RBAC** | kubectl 출력 | Role · RoleBinding (플랫폼) |
| `admission webhook "…kyverno…" denied the request: …` | **Kyverno** (입장 제어) | kubectl 출력, Argo CD Sync 오류 | 매니페스트를 정책에 맞게, 또는 정책 |
| `RBAC: access denied` (HTTP 403) | **Istio waypoint** (AuthorizationPolicy) | curl 응답, waypoint 로그, Kiali | AuthorizationPolicy (배포 저장소) |
| curl `000` · `Connection reset by peer` | **ztunnel** (STRICT · L4 정책) | ztunnel 로그 | PeerAuthentication · L4 정책 |
| HTTP `504` · 로그의 `UT` | **waypoint 타임아웃** | waypoint 로그 | VirtualService (배포 저장소) |
| HTTP `500` · `no healthy upstream` | **Envoy Gateway** (백엔드 없음) | HTTPRoute status | HTTPRoute (배포 저장소) |
| `ImagePullBackOff` | **kubelet** | `kubectl describe pod` · events | 이미지 이름 · 태그 · 공개 여부 |
