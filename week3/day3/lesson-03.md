# 3교시: 인프라 엔지니어의 GitHub 관리 전략

![Week 3 Day 3 Lesson 3](./assets/lesson-03-infra-github-governance.png)

## 수업 목표
- 인프라 엔지니어가 GitHub를 코드 저장소 이상으로 사용하는 방식을 설명한다.
- IaC, workflow, secret, protected branch, audit trail을 연결한다.
- GitHub 관리 전략이 배포 사고를 줄이는 방식을 이해한다.

## 개발자와 인프라 엔지니어의 관점 차이
| 관점 | 개발자 | 인프라 엔지니어 |
|---|---|---|
| 주요 변경 | application code | workflow, Dockerfile, IaC, manifest |
| 주요 위험 | 기능 버그 | 배포 실패, secret 노출, 잘못된 리소스 변경 |
| 주요 gate | test, review | plan, policy, approval, environment |
| 주요 evidence | test result | workflow log, artifact, image tag, audit |

## 인프라 GitHub 관리 대상
| 대상 | 관리 포인트 |
|---|---|
| `.github/workflows` | 누가 어떤 자동화를 실행하는가 |
| Dockerfile | build context, secret 포함 여부, image size |
| Terraform | plan/apply 승인, state 보호 |
| Kubernetes manifest | namespace, image tag, secret 참조 |
| branch protection | main/prod 직접 변경 차단 |
| repository secrets | token 권한과 노출 방지 |

## Protected branch 기준
| 설정 | 목적 |
|---|---|
| require pull request | 직접 push 방지 |
| require approvals | 사람 검토 |
| require status checks | CI 통과 강제 |
| restrict who can push | 운영 branch 보호 |
| require conversation resolved | 미해결 리뷰 방치 방지 |

## Secret 관리
Docker Hub push에 필요한 값:

| Secret | 설명 |
|---|---|
| `DOCKERHUB_USERNAME` | Docker Hub namespace |
| `DOCKERHUB_TOKEN` | password 대신 access token |

주의:

```text
workflow에서 echo로 secret 출력 금지
Dockerfile에 secret COPY 금지
.env commit 금지
```

## 핵심 포인트
인프라 엔지니어에게 GitHub는 배포 통제면이다. 누가 어떤 변경을 어떤 검증을 거쳐 어느 환경에 반영했는지 남겨야 한다.

## Evidence Note
```markdown
# W3D3S3 Infra GitHub Strategy
- protected branch:
- required checks:
- secrets:
- workflow owner:
- audit evidence:
```


## 학습 제어
### 시작 3분 회상
- PR의 review와 status check는 각각 무엇을 증명하는가?
- IaC/workflow/secret/protected branch 중 Git 기준 상태를 보호하는 것은 무엇인가?
### 오늘 반드시 가져갈 것
- GitHub 운영은 코드뿐 아니라 workflow·manifest·secret 접근·audit trail의 책임을 관리한다.
- secret은 값이 아니라 권한과 노출 경로까지 통제해야 하는 증거다.
### 최소 복구 경로
- 보호 branch와 workflow를 확인한다 → secret이 로그에 없는지 확인한다 → PR check 실패를 기록한다.
- 성공 판정은 변경 권한·검증 gate·감사 증거를 분리해 설명하는 것이다. 첫 실패는 check log와 repository settings에서 찾는다.
- 다음 lesson 진입 조건은 기준 상태가 우회되지 않는 이유를 말하는 것이다.

### W3D3 필수 흐름
`branch/PR → CI 실패 증거 → 로컬 수정 → 재실행 → 통과 기록`을 필수로 연결한다. SAST/DAST·tag·rebase는 기본 흐름 완료 후 선택 심화로 확인한다.