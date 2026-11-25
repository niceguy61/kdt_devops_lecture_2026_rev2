# DevMart 보안 점검표 — 4주차 끝

| 층 | 항목 | 지금 | 근거 |
|---|---|---|---|
| 코드 · 이미지 | 이미지 태그를 고정한다 (latest 금지) | | Kyverno disallow-latest-tag |
| | 컨테이너가 root가 아니다 | | Kyverno 보고서 (Audit) |
| 클러스터 접근 | 사람은 devmart를 읽기만 | | `kubectl auth can-i --as` |
| | 비밀 값은 Git에 없다 | | `grep -r password ~/devmart-deploy` |
| | CI는 클러스터 열쇠가 없다 | | 3일차 구조 |
| 워크로드 신원 | 서비스마다 ServiceAccount | | `kubectl get sa -n devmart` |
| | API를 안 부르는 Pod에는 토큰이 없다 | | automountServiceAccountToken: false |
| 서비스 사이 | mTLS STRICT | | PeerAuthentication |
| | catalog-api는 order-api만 | | AuthorizationPolicy (L7 + L4) |
| 관찰 | 거절이 기록된다 | | waypoint · ztunnel 로그, PolicyReport |
