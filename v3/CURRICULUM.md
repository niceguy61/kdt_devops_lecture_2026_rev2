# Cloud Native DevOps 기초 이론 과정 — 커리큘럼 v3

> 이 문서는 `docs/plan.md`(2026 상반기판)를 대체하는 v3 기준 문서입니다.
> 강의 원고(이북 PDF), 강의 슬라이드(PPTX), GitHub 안내 문서는 모두 이 표를 기준으로 만듭니다.

## 1. 과정 개요

| 항목 | 내용 |
|---|---|
| 기간 | 5주, 주 5일, 하루 8시간 (주 40시간, 총 200시간) |
| 시간 단위 | 1교시 = 50분 수업 + 10분 휴식, 매 정시 시작 |
| 매일 8교시 | 배움일기 (오늘 이해한 개념, 막힌 지점, 다시 해볼 것, 질문) |
| 1주차 1일차 | 과정 OT 포함 5시간 운영 (12:00~18:00, 점심 13:00~14:00) |
| 대상 | 전공 막학기 학생, 비전공 취업준비생, 클라우드 직군 전환 희망 개발자 |
| 목표 직무 | DevOps 엔지니어, 클라우드 엔지니어, SRE/플랫폼 엔지니어 주니어 |

### 난이도 곡선

| 주차 | 난이도 | 운영 원칙 |
|---|---|---|
| 1주차 | ★☆☆☆☆ | **핸즈온 없음.** 개념, 그림, 강사 시연만. 용어와 큰 그림을 잡는다 |
| 2주차 | ★★☆☆☆ | 첫 핸즈온. A to Z 101 스타일로 한 단계씩, 실패해도 되돌아올 수 있게 |
| 3주차 | ★★★☆☆ | MSA와 Kubernetes 입문. 개념 → 실습 → 장애 확인 순서 |
| 4주차 | ★★★★☆ | Kubernetes 운영 도구. 어려워도 하루 한 도구에 집중 |
| 5주차 | ★★★★★ | AWS + Terraform + EKS. 수강생 본인 계정에서 직접 생성하고 당일 삭제 |

### 과정을 관통하는 한 줄

**"앱 하나의 여행"** — 같은 MSA 앱 하나가 5주 동안 이렇게 이동한다.

```
내 노트북(1주) → Docker 컨테이너(2주) → Compose MSA(3주) → Kubernetes(3~4주)
→ Argo CD/Istio(4주) → AWS + Terraform(5주) → EKS 위 GitOps 배포(5주 마지막 날)
```

## 2. 주차별 요약

| 주차 | 주제 | Day1 | Day2 | Day3 | Day4 | Day5 |
|---|---|---|---|---|---|---|
| 1 | 클라우드·컴퓨팅 기초 이론 | OT + 클라우드란 무엇인가 | 컴퓨터와 운영체제, 가상화 | 네트워크 기초 | 현대 애플리케이션 구조 | DevOps 문화와 협업 커뮤니케이션 |
| 2 | Docker + Git 첫 실습 | 개발환경 세팅 + Git/GitHub 첫걸음 | Docker 기본 | 이미지와 Dockerfile | Volume·Network·환경변수 | Compose + GitHub 협업 |
| 3 | MSA + Kubernetes 입문 | MSA 개념과 Compose 실행 | MSA 장애 분석 + GitHub Actions CI | Kubernetes 아키텍처 + kind | Pod·Deployment·Service | 설정·헬스체크·리소스 + MSA 배포 |
| 4 | Kubernetes 운영 | Helm + Gateway API | Observability (Prometheus/Grafana) | GitOps — Argo CD | Service Mesh — Istio | 보안(RBAC·Kyverno) + 종합 트러블슈팅 |
| 5 | AWS + IaC + EKS | AWS 계정 보안·리전·VPC | EC2·ALB·S3 콘솔 실습 | Terraform 기초 | Terraform으로 VPC·ECR·EKS | EKS 위 GitOps 통합 + 정리 |

## 3. 일차별 상세

### 1주차 — 클라우드·컴퓨팅 기초 이론 (핸즈온 없음)

**Day 1 — OT와 클라우드의 큰 그림** (5시간)

| 교시 | 주제 | 핵심 |
|---|---|---|
| 1 | 과정 OT | 과정 목표, 5주 구조, 수업 리듬, 질문하는 법, 계정·보안 규칙 |
| 2 | 5주 로드맵과 DevOps 직무 | "앱 하나의 여행", DevOps/SRE/클라우드/플랫폼 엔지니어가 하는 일 |
| 3 | AI 시대의 DevOps 마인드셋 | 작은 앱 vs 운영 가능한 서비스, 서비스화 체크리스트 8가지 |
| 4 | 데이터센터에서 클라우드까지 | 서버·데이터센터, 가상화, 클라우드 5대 특성(NIST) |
| 5 | 서비스 모델·공유 책임·비용 | IaaS/PaaS/SaaS, 공유 책임 모델, CAPEX/OPEX/TCO, 리전/AZ 미리보기 |

**Day 2 — 컴퓨터와 운영체제, 가상화**

| 교시 | 주제 | 핵심 |
|---|---|---|
| 1 | 컴퓨터는 무엇으로 이루어져 있나 | CPU, 메모리, 디스크, 네트워크 카드, 서버 vs PC |
| 2 | 운영체제가 하는 일 | 커널, 사용자 영역, 시스템 콜, 왜 서버는 Linux인가 |
| 3 | 프로그램·프로세스·스레드 | 실행 단위, PID, 종료 코드, 포그라운드/백그라운드 |
| 4 | 파일과 저장소 | 파일시스템, 경로, 권한(rwx), 영속 데이터 vs 임시 데이터 |
| 5 | Linux 명령어 맛보기 (강사 시연) | pwd, ls, cd, cat, ps, 환경변수 — 읽는 법만 |
| 6 | 가상화와 하이퍼바이저 | VM 원리, Type 1/2, 클라우드 인스턴스의 정체 |
| 7 | VM에서 컨테이너로 (예고) | 컨테이너는 격리된 프로세스, VM과 비교 |
| 8 | 배움일기 | |

**Day 3 — 네트워크 기초**

| 교시 | 주제 | 핵심 |
|---|---|---|
| 1 | 네트워크 큰 그림 | 계층 모델을 "택배"로 이해하기 (TCP/IP 4계층 중심) |
| 2 | IP 주소와 서브넷 | 공인/사설 IP, CIDR 읽기 (VPC 설계 예고) |
| 3 | 포트와 프로토콜 | TCP/UDP, 잘 알려진 포트, localhost |
| 4 | DNS | 도메인 → IP, 레코드 종류, 캐시 |
| 5 | HTTP와 HTTPS | 요청/응답, 메서드, 상태 코드, TLS 인증서 |
| 6 | 서비스로 가는 길 | 브라우저 → DNS → 로드밸런서 → 서버 → DB 전체 흐름 |
| 7 | 네트워크 장비의 역할 | 라우터, 방화벽, NAT, 프록시, 로드밸런서 |
| 8 | 배움일기 | |

**Day 4 — 현대 애플리케이션 구조**

| 교시 | 주제 | 핵심 |
|---|---|---|
| 1 | 웹 서비스의 구성요소 | 프론트엔드, 백엔드, API, DB, 캐시, 큐 |
| 2 | 3-Tier 아키텍처 | 계층 분리 이유, 요청 흐름 |
| 3 | 확장성과 가용성 | Scale up/out, 단일 장애점, 이중화 |
| 4 | 데이터 저장 선택 | RDB, NoSQL, 캐시, 객체 스토리지 |
| 5 | 비동기와 메시지 큐 | 동기 호출의 위험, 큐/이벤트 |
| 6 | 국내 기업 사례로 보기 | 커머스·핀테크·배달 서비스 구조 (공개 기술 블로그 기반) |
| 7 | 모놀리식과 MSA 맛보기 | 배포 단위, 장애 범위 (3주차 예고) |
| 8 | 배움일기 | |

**Day 5 — DevOps 문화와 협업 커뮤니케이션**

| 교시 | 주제 | 핵심 |
|---|---|---|
| 1 | DevOps란 무엇인가 | 등장 배경, 문화·자동화·측정·공유, DORA 지표 소개 |
| 2 | 소프트웨어 전달 과정 | SDLC, 빌드·테스트·배포·운영, CI/CD 개념 |
| 3 | 버전 관리와 Git/GitHub (강사 시연) | 커밋, 브랜치, PR, 리뷰 — 개념 중심 |
| 4 | 타 부서와 일하는 법 | 개발·QA·보안·기획·CS와의 접점, 요구사항 받기, 일정·리스크 말하기 |
| 5 | 장애 커뮤니케이션과 포스트모템 | 장애 공지, 타임라인, 비난 없는 회고, runbook |
| 6 | 문서로 일하기 | README, 티켓, 변경 요청서, 좋은 질문 템플릿 |
| 7 | 왜 Docker인가 + 2주차 준비 | "내 PC에선 되는데" 문제, 설치 전 체크리스트 |
| 8 | 배움일기 | |

### 2주차 — Docker + Git 첫 실습

| Day | 주제 | 교시 구성 (1~7교시) |
|---|---|---|
| 1 | 개발환경 세팅 + Git 첫걸음 | WSL2/macOS 터미널 → VS Code → Git 설치·설정 → GitHub 계정·PAT → 첫 repo·commit·push → Docker Desktop 설치 → 설치 점검 |
| 2 | Docker 기본 | 이미지와 컨테이너 → hello-world → nginx 실행 → 포트 연결 → logs/exec → stop/rm/cleanup → 실패 사례 |
| 3 | 이미지와 Dockerfile | 이미지 레이어 → Dockerfile 문법 → 첫 빌드 → .dockerignore → 캐시 → 태그·Docker Hub push → 멀티 스테이지 맛보기 |
| 4 | Volume·Network·환경변수 | 데이터가 사라지는 이유 → named volume → bind mount → bridge network → 컨테이너 이름 DNS → 환경변수·시크릿 → 장애 연습 |
| 5 | Compose + GitHub 협업 | compose.yaml 읽기 → web+api+db 실행 → logs/down → branch → PR → 리뷰·merge → 충돌 해결 |

### 3주차 — MSA + Kubernetes 입문

| Day | 주제 | 교시 구성 |
|---|---|---|
| 1 | MSA 개념과 실행 | 모놀리식 vs MSA → 서비스 경계 → 실습 앱 구조 → compose up → 서비스 간 통신 추적 → 장애 1 (URL/env 오류) |
| 2 | MSA 장애 + CI | 장애 전파 → 헬스체크·타임아웃·재시도 → 큐 적체 → GitHub Actions 개념 → 첫 workflow → 이미지 빌드·push 자동화 |
| 3 | Kubernetes 아키텍처 | 등장 배경 → Control Plane → Node → 선언형·reconcile → 장단점 → kind 설치 → 첫 클러스터 |
| 4 | Pod·Deployment·Service | kubectl 루프 → Pod → Pod 장애 읽기 → Deployment → ReplicaSet·self-healing → Service·DNS → rollout/undo |
| 5 | 운영 가능한 워크로드 | Namespace → ConfigMap/Secret → probe → requests/limits → MSA 앱 K8s 배포 → 장애 연습 |

### 4주차 — Kubernetes 운영

| Day | 주제 | 교시 구성 |
|---|---|---|
| 1 | Helm + Gateway API | Helm 개념 → 설치 루프 → Ingress 역사와 ingress-nginx 은퇴 → Gateway API 구조 → Envoy Gateway 설치 → HTTPRoute → 장애 분석 |
| 2 | Observability | 로그·메트릭·트레이스 → kube-prometheus-stack → target → Grafana 대시보드 → 부하 테스트(k6) → 알림 → 관찰 runbook |
| 3 | GitOps — Argo CD | GitOps 개념 → CI/CD 책임 분리 → Argo CD 설치 → Application → sync·drift → self-heal·prune → Actions → Argo CD 파이프라인 완성 |
| 4 | Service Mesh — Istio | 메시가 필요한 이유 → 사이드카와 ambient 모드 → 설치 → 트래픽 분할 → 장애 주입 → mTLS → Kiali 그래프 |
| 5 | 보안 + 종합 트러블슈팅 | 인증·인가 → RBAC → ServiceAccount → Kyverno 정책 → RBAC forbidden vs 정책 deny → 종합 장애 시나리오 → 주간 회고 |

### 5주차 — AWS + Terraform + EKS

| Day | 주제 | 교시 구성 |
|---|---|---|
| 1 | AWS 계정·리전·VPC | 계정 보안(root, MFA, IAM) → Budget 알림 → 리전/AZ → AWS 서비스 지도 → VPC·서브넷·라우팅 → 보안 그룹 → 콘솔로 VPC 생성 |
| 2 | EC2·ALB·S3 콘솔 실습 | EC2 생성 → user data 웹서버 → 보안 그룹 장애 → ALB·대상 그룹 → S3·퍼블릭 접근 차단 → RDS 개념 → 삭제 점검 |
| 3 | Terraform 기초 | 왜 IaC인가 → 설치 → provider·resource → plan/apply/destroy → state → variable/output → 어제 만든 VPC·EC2를 코드로 |
| 4 | Terraform으로 EKS | module → 원격 state → VPC module → EKS module → kubeconfig 연결 → ECR push → 비용·삭제 순서 |
| 5 | 통합 + 정리 | EKS에 Argo CD 설치 → MSA 앱 GitOps 배포 → 외부 노출 → CloudWatch 확인 → 비용 점검 → terraform destroy → 포트폴리오 정리 |

## 4. 운영 원칙

1. **1주차는 핸즈온이 없다.** 명령어는 강사 시연과 화면 캡처로만 보여준다.
2. **핸즈온은 101 스타일.** 한 단계 = 명령 1~2개 + 기대 결과 + 실패 시 대처. 단계를 건너뛰지 않는다.
3. **실습 앱은 하나로 이어진다.** W3 MSA 앱이 W5 EKS까지 간다.
4. **Kubernetes add-on은 Helm으로 설치한다.** `values.yaml` 파일 기반.
5. **외부 트래픽 표준은 Gateway API(Envoy Gateway)다.** ingress-nginx는 2026년 3월 은퇴한 프로젝트로 소개만 한다.
6. **AWS 리소스는 수강생 본인 계정에서 만들고 당일 삭제한다.** EKS·NAT Gateway·ALB는 켜져 있는 시간만큼 과금된다. 매일 마지막 교시 전에 삭제 점검을 한다.
7. **AWS 컨테이너 실행 서비스로 App Runner를 쓰지 않는다.** 2026-04-30부터 신규 고객을 받지 않는다. ECS/EKS를 기준으로 한다.
8. **같은 주의사항을 교시마다 반복하지 않는다.** 공통 원칙은 하루 개요에 한 번만 둔다.

## 5. 산출물 형식

| 형식 | 용도 | 원본 |
|---|---|---|
| PDF 이북 | 수강생 교재, 복습용 | `v3/src/week*/day*/` 원고 |
| PPTX | 강의 플랫폼 업로드, 강사 진행용 (발표자 노트 포함) | 같은 원고의 슬라이드 정의 |
| GitHub | 저장소 안내, 실습 코드, 목차 | 같은 원고에서 자동 생성 |

다이어그램은 `v3/diagrams/`의 코드로 생성한다. 그림의 화살표와 배치는 레이아웃 엔진이 계산하므로 수동 좌표로 그리지 않는다. AWS 아이콘은 `reference/icons`의 공식 패키지를 쓴다.
