# Week 3 Day3 Academic Foundations

## 수업 기준
Day 3는 GitHub를 개발 협업 도구이자 인프라 운영 통제면으로 다룬다.

## 개발자가 GitHub를 쓰는 방식
| 기능 | 목적 |
|---|---|
| Issue | 작업 단위와 요구사항 기록 |
| Branch | 변경 격리 |
| Commit | 변경 이력 저장 |
| Pull Request | review와 merge gate |
| Review | 코드 품질과 의도 확인 |
| Status Check | 자동 검증 |
| Release/Tag | 배포 지점 기록 |

## 인프라 엔지니어가 GitHub를 쓰는 방식
| 영역 | 예 |
|---|---|
| IaC repository | Terraform, Kubernetes manifest |
| Environment policy | dev/stage/prod 승인 |
| Protected branch | main/prod branch 직접 push 방지 |
| Required check | plan/test/build 통과 전 merge 차단 |
| Secrets | cloud token, Docker Hub token 관리 |
| Audit trail | 누가 언제 어떤 인프라 변경을 했는지 추적 |
| Actions runner | build/deploy 실행 환경 관리 |

## Branch/Environment 전략
| 전략 | 장점 | 단점 |
|---|---|---|
| `dev -> stage -> prod` branch | 환경 승인이 명확함 | branch drift 위험 |
| main + GitHub Environment | 코드 이력 단순, 환경 gate 분리 | Actions/환경 설계 필요 |
| GitHub Flow | 단순하고 빠름 | 배포 승인 복잡한 조직에는 부족 |
| Git Flow | release/hotfix 분리 | 복잡하고 느릴 수 있음 |

## GitHub Actions 개념
| 개념 | 의미 |
|---|---|
| workflow | 자동화 정의 파일 |
| event | workflow 실행 조건 |
| job | runner에서 실행되는 작업 묶음 |
| step | job 안의 개별 작업 |
| runner | job이 실행되는 환경 |
| action | 재사용 가능한 step |
| secret | workflow에서 쓰는 민감정보 |
| artifact/image | build 결과물 |

## Quality/Security Gate
| Gate | 목적 | 예 |
|---|---|---|
| unit test | 코드 단위 동작 검증 | Python unittest |
| SAST | 소스 코드 정적 보안 검사 | 위험 함수, hardcoded secret 탐지 |
| DAST | 실행 중인 앱 동적 검사 | container 실행 후 `/health` 호출 |
| image build | 배포 artifact 생성 검증 | Docker build |
| registry push | 배포 artifact 저장 | Docker Hub push |

## GitHub Secrets 장단점
| 장점 | 단점 |
|---|---|
| repo에 token을 commit하지 않아도 됨 | 값 자체를 UI에서 다시 볼 수 없음 |
| Actions log에서 masking 지원 | 잘못 echo하면 구조나 일부 값이 노출될 수 있음 |
| 환경별 secret 분리 가능 | 권한/이름 관리가 복잡해질 수 있음 |
| rotation 가능 | 만료/교체 절차가 필요 |

## 수동 배포의 불편함
| 수동 배포 문제 | 자동화로 줄이는 것 |
|---|---|
| 사람마다 build 명령이 다름 | workflow에 명령 고정 |
| test 누락 | required check |
| image tag 실수 | tag 규칙 자동화 |
| Docker Hub login 실수 | secret 기반 login |
| 배포 증거 부족 | Actions log와 artifact 기록 |

## 유사 도구
| 도구 | 특징 |
|---|---|
| GitHub Actions | GitHub repo와 통합이 쉽고 marketplace가 큼 |
| Jenkins | 오래된 표준, 플러그인 풍부, 직접 운영 부담 |
| TeamCity | JetBrains 계열 CI/CD, 엔터프라이즈 기능 강함 |
| AWS CodePipeline | AWS 배포 흐름과 IAM 통합이 강함 |

## Docker Hub Push 원칙
- Docker Hub token은 GitHub secret으로만 사용한다.
- image tag는 app version/Git tag와 맞춘다.
- `latest`만 믿지 않는다.
- push 후 Docker Hub UI에서 tag를 확인한다.
- 로컬에서 `docker pull` 후 실행까지 확인해야 배포 artifact를 믿을 수 있다.
