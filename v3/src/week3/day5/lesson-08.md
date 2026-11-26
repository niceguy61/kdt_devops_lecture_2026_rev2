# 8교시 · 3주차 회고

!!! goal "이번 시간에 할 일"
    - 3주차 닷새를 **한 장의 지도**로 되짚습니다.
    - Compose ↔ Kubernetes 대응표를 **내 말로** 채웁니다.
    - KPT로 한 주를 회고하고, 4주차에 가져갈 것을 정합니다.
    - 다음 주를 위해 클러스터 상태를 정리합니다.

## 한 주의 지도

| 날 | 한 일 | 핵심 한 줄 | 남은 것 |
|---|---|---|---|
| 1일차 | 모놀리식 → MSA, Compose로 여섯 서비스 | 나누면 독립적으로 배포 · 확장할 수 있지만, **연결이 새 장애 지점**이 된다 | `devmart-msa/` |
| 2일차 | 장애 전파 · 타임아웃 · 재시도 · 큐 유실, GitHub Actions CI | 느린 것이 죽은 것보다 무섭다. 사람 대신 **CI가 매번 똑같이** 검사 · 빌드 | GHCR의 세 이미지 |
| 3일차 | Kubernetes 구조, kind 클러스터 | 여러 대를 한 대처럼 + **원하는 상태를 계속 지킨다**(reconcile) | `devmart` 클러스터 |
| 4일차 | Pod · Deployment · Service, 롤링 업데이트 | **라벨**로 이어진 리소스들, 되돌릴 수 있는 배포 | — |
| 5일차 | ConfigMap · Secret · probe · 자원, MSA 전체 배포, 장애 연습 | 같은 이미지가 운영 모델만 바꿔 클러스터에 — **probe가 장애의 번짐을 정한다** | `devmart` 네임스페이스 |

!!! key "이번 주를 한 문장으로"
    **"여러 서비스로 나뉜 앱을, 사람 대신 기계가 검증하고(CI), 사람 대신 클러스터가 지키게(Kubernetes) 만들었다."** 1주차 5일차에 그림으로만 본 파이프라인의 ①~③, ⑤ 칸과 그 결과물이 도는 자리까지 손으로 만들었습니다. 남은 칸(④ 보안 검사, ⑥ 자동 배포, ⑦ 모니터링)이 4주차입니다.

## 실습 21 · 회고

!!! lab "실습 목표"
    `retro-week3.md`를 채웁니다. 혼자 10분, 짝과 10분 나눕니다.

```bash
cd ~/devops-lab/k8s/day5
cp retro-week3.md ~/devops-lab/retro-week3.md
```

### 1 — 이번 주에 만든 것 체크

양식 맨 위의 다섯 칸을 확인합니다. 체크하지 못한 칸이 있으면 어디서 막혔는지 한 줄 적습니다. 그것이 Problem 칸의 첫 줄이 됩니다.

### 2 — Compose ↔ Kubernetes 대응표

5교시 끝의 대응표를 보지 않고 **내 말로** '차이' 칸을 채웁니다.

!!! example "예시 — 이렇게 쓰면 좋다"
    | Compose | Kubernetes | 내 말로 차이 |
    |---|---|---|
    | `healthcheck:` | readiness · liveness probe | Compose는 표시만, Kubernetes는 **행동**한다 — 목록에서 빼거나 재시작 |
    | `restart: unless-stopped` | kubelet 재시작 + ReplicaSet | Compose는 그 컴퓨터 안에서만, Kubernetes는 **다른 노드에** 새로 만든다 |

### 3 — KPT

| 칸 | 묻는 것 | 예 |
|---|---|---|
| **Keep** | 잘 됐고 계속할 것 | "describe의 Events를 맨 아래부터 읽는 습관" |
| **Problem** | 막혔거나 아쉬웠던 것 — **사실**로 | "장애 3을 15분 안에 못 찾았다. get pods만 봤다" |
| **Try** | 다음 주에 **구체적으로** 해 볼 것 | "장애 진단은 항상 사용자 증상(curl)부터 시작한다" |

!!! tip "좋은 Try의 조건"
    "더 열심히 하자"는 Try가 아닙니다. **다음 주 언제, 무엇을 하면 지켰는지 알 수 있는** 문장이어야 합니다. 예: "4주차 매일 아침 `bash cluster-tour.sh`로 클러스터 상태를 먼저 본다."

### 4 — 장애 연습 기록

6교시에 맡았던 장애와 **원인을 찾은 명령**, 걸린 시간을 적습니다. 짝과 비교해, 같은 장애를 다른 명령으로 찾았다면 그것도 적습니다.

## 4주차 미리 보기

| 4주차 | 이번 주에서 이어지는 것 |
|---|---|
| 1일차 Helm + Gateway API | 오늘의 매니페스트 여덟 개를 **차트**로 묶는다 · NodePort 대신 도메인 · 경로로 들어오는 표준 입구 |
| 2일차 Observability | 오늘 손으로 센 FAIL · `kubectl logs | grep $RID`를 **메트릭 · 로그 · 트레이스** 도구로 |
| 3일차 GitOps — Argo CD | 장애 3의 드리프트를 **화면에 보여 주고 되돌린다** · CI(2일차) → CD 완성 |
| 4일차 Service Mesh — Istio | 2일차의 타임아웃 · 재시도를 **코드 밖에서** · 카나리 배포 |
| 5일차 보안 + 종합 | 누가 `kubectl scale`을 할 수 있었나(RBAC) · "requests 없으면 거절"(Kyverno) |

!!! warn "주말 동안 — 클러스터는 지우지 않는다"
    `devmart` 클러스터와 네임스페이스는 **4주차 1일차에 그대로** 씁니다. 노트북을 꺼도 됩니다. 월요일 아침에는 Docker Desktop을 켜고 노드 셋을 켭니다.
    ```bash
    docker start devmart-control-plane devmart-worker devmart-worker2
    sleep 40 && kubectl get pods -n devmart
    ```
    망가져 있으면 `kind delete cluster --name devmart` → 다시 만들고 → 2교시의 Secret을 다시 만든 뒤 → `kubectl apply -k devmart/`. 이 순서를 지금 회고 노트에 적어 두세요. **5분이면 처음부터 되살릴 수 있다**는 것이 이번 주에 만든 것의 진짜 가치입니다.

디스크가 부족하면 이번 주에 쌓인 것 중 안 쓰는 이미지만 정리합니다.

```bash
docker system df
docker image prune
```

- `docker image prune` : 태그 없는 이미지(`<none>`)만 지운다. kind 노드 이미지와 실행 중인 것은 지우지 않는다

!!! academic "학술 노트 — 회고의 기본 지침"
    애자일 회고는 Kerth의 *Project Retrospectives*(2001)와 Derby & Larsen의 *Agile Retrospectives*(2006)가 틀을 잡았습니다. Kerth가 회고를 시작할 때 읽으라고 제안한 **기본 지침**(Prime Directive)은 이렇습니다 — "무엇을 발견하든, 우리는 모두가 그때 알던 것, 가진 기술과 능력, 주어진 자원과 상황에서 할 수 있는 최선을 다했다고 믿고 이해한다." 6교시의 '비난 없는 사후 검토'와 같은 정신입니다. 회고는 잘못한 사람을 찾는 자리가 아니라, **다음에 더 나은 선택을 하게 해 줄 조건**을 찾는 자리입니다.

!!! trend "트렌드 2026 — 4주차 도구들의 지금"
    4주차는 '요즘 표준'을 기준으로 합니다. 외부 트래픽 입구로 오래 쓰인 **ingress-nginx는 2026년 3월 은퇴**했고, 그 자리를 **Gateway API**가 이어받았습니다. GitOps 도구 Argo CD와 서비스 메시 Istio는 CNCF 졸업 프로젝트로 널리 쓰이고, Istio는 Pod마다 프록시를 붙이지 않는 **ambient 모드**를 정식으로 내놓았습니다. 이번 주에 익힌 Pod · Service · 라벨 · reconcile이 이 모든 도구가 서 있는 바닥입니다.

!!! quiz "3주차 종합 확인 문제"
    1. MSA로 나눴을 때 얻는 것 하나와, 새로 생기는 장애 지점 하나는?
    2. 2일차 CI가 PR에서는 하지 않고 main에서만 하는 일은?
    3. reconcile 반복의 세 단계는?
    4. Service가 Pod를 찾는 방법과, 찾은 목록을 담는 리소스는?
    5. readiness와 liveness가 실패했을 때 각각 일어나는 일은?
    6. 메모리 limit을 넘으면? CPU limit을 넘으면?
    7. `kubectl set env`로 넣은 값이 `kubectl apply -k`로 지워지지 않는 이유는?

    ??? answer "정답"
        1. 얻는 것 — 서비스별 독립 배포 · 확장 · 장애 격리 중 하나. 새 장애 지점 — 서비스 사이의 네트워크 호출(타임아웃 · 연결 오류), 큐 유실 등
        2. GHCR 로그인 후 이미지 push (PR에서는 빌드만)
        3. 관찰 → 비교 → 행동
        4. 라벨 셀렉터, EndpointSlice
        5. readiness — Service 목록에서 뺀다(죽이지 않음). liveness — 컨테이너를 다시 시작한다
        6. 메모리 — OOMKilled(Exit 137), CPU — 느려진다(throttling)
        7. apply는 지난번 자기가 적용한 기록과 비교해 바꾸므로, 기록에 없는 칸(명령형으로 들어온 값)은 남의 것으로 보고 건드리지 않는다

!!! diary "오늘의 배움일기 (3주차 마무리)"
    - ConfigMap과 Secret을 나눈 이유를, 2주차 `.env`와 비교해 한 문단으로
    - probe를 넣기 전과 후의 FAIL 숫자, 그리고 그 차이를 만든 세 조각
    - OOMKilled를 직접 보고 든 생각 — 내가 만든 앱이라면 limit을 어떻게 정할지
    - DevMart가 Kubernetes에서 처음 주문을 처리했을 때의 기분 (진심으로)
    - 장애 연습에서 가장 오래 걸린 단계와, 다음엔 무엇부터 볼지
    - 3주차 전체에서 **가장 크게 바뀐 생각** 하나
    - 4주차 전에 궁금한 것: 매니페스트 여덟 개를 서비스 50개로 늘리면? 누가 언제 무엇을 바꿨는지 어떻게 남길까?

## 참고 문헌

- Kerth, N. L. (2001). *Project Retrospectives: A Handbook for Team Reviews*. Dorset House.
- Derby, E., & Larsen, D. (2006). *Agile Retrospectives: Making Good Teams Great*. Pragmatic Bookshelf.
- Kubernetes Blog (2025). *Ingress NGINX Retirement: What You Need to Know*. kubernetes.io/blog
- kind. *Known Issues — Docker Desktop restart*. kind.sigs.k8s.io/docs/user/known-issues
