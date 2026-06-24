# Week 3 Day3: Git/GitHub 전략과 GitHub Actions Docker 배포

## Overview
Day 3는 Git 명령만 배우는 날이 아니다. 개발자가 매일 쓰는 GitHub 협업 방식과, 인프라 엔지니어가 GitHub를 운영/배포 통제 지점으로 쓰는 방식을 함께 다룬다.

오늘의 흐름:

```text
Git 이론
  -> 개발자가 주로 쓰는 GitHub 협업
  -> 인프라 엔지니어의 GitHub 관리 전략
  -> dev/stage/prod branch 전략
  -> PR/merge/revert/tag 운영
  -> unit test / SAST / DAST gate
  -> GitHub Secrets로 registry 인증
  -> GitHub Actions로 Docker image build/push
  -> Docker Hub image 확인
  -> 로컬에서 pull/run 검증
```

## Learning Goals
- Git object, commit, branch, remote, tag의 의미를 설명한다.
- 개발자가 GitHub에서 issue, branch, commit, PR, review를 어떻게 쓰는지 설명한다.
- 인프라 엔지니어가 GitHub를 IaC, CI/CD, 정책, secret, audit 관점으로 어떻게 관리하는지 설명한다.
- `dev`, `stage`, `prod` branch/environment 전략의 장단점을 비교한다.
- PR, merge, squash, rebase, revert, tag 기준을 운영 관점으로 설명한다.
- unit test, SAST, DAST가 CI/CD gate에서 맡는 역할을 설명한다.
- GitHub Secrets의 장점과 단점을 설명한다.
- GitHub Actions workflow의 event, job, step, runner, secret을 읽고 작성한다.
- Docker image를 로컬에서 build/run하고, Actions로 Docker Hub에 push하는 흐름을 설명한다.
- Docker Hub에서 생성된 image를 확인하고 로컬에서 pull/run하는 검증 절차를 작성한다.

## Lesson Index
| 교시 | 주제 | 핵심 실습 |
|---|---|---|
| 1교시 | Git 이론과 변경 이력 모델 | commit/branch/remote/tag 개념 정리 |
| 2교시 | 개발자가 많이 쓰는 GitHub 흐름 | issue, branch, PR, review, code owner |
| 3교시 | 인프라 엔지니어의 GitHub 관리 전략 | IaC repo, protected branch, required check, secret 정책 |
| 4교시 | Branch 전략: dev/stage/prod | environment branch와 promotion 전략 비교 |
| 5교시 | PR, merge, rebase, revert, tag 운영 | sandbox conflict/revert/tag |
| 6교시 | GitHub Actions 1: 코드, workflow, 품질 gate | unit test, SAST, DAST, `.gitignore`, `.dockerignore`, local build |
| 7교시 | GitHub Actions 2: Secrets, Docker Hub push, 대체 도구 | secrets, buildx, push, Docker Hub 확인, Jenkins/TeamCity/CodePipeline |
| 8교시 | 개인 repo Docker Hub push 회고 | workflow 작성, step 시간 분석, 보강 포인트 정리 |

## Practice Files
| 자료 | 용도 |
|---|---|
| `labs/git-sandbox/setup.sh` | 안전한 Git conflict/revert/tag sandbox |
| `labs/dockerhub-app/` | Docker Hub push용 sample app |
| `labs/quality-gates/` | unit test, SAST, DAST local gate |
| `labs/github-actions/dockerhub-publish.yml` | Docker Hub publish workflow |
| `labs/ci-gate-demo/` | local CI gate 간단 검증 |
| `hands-on-lab.md` | 전체 실습 순서 |

## Secret Policy
Docker Hub push에는 GitHub repository secrets가 필요하다. Docker Hub repository를 private으로 만들었다면 pull하는 PC나 서버에서도 Docker Hub 인증이 필요하다.

| Secret | 용도 |
|---|---|
| `DOCKERHUB_USERNAME` | Docker Hub namespace |
| `DOCKERHUB_TOKEN` | Docker Hub access token |

절대 workflow log에 token을 출력하지 않는다.

Private image pull 예시:

```bash
docker login -u DOCKERHUB_USERNAME
docker pull DOCKERHUB_USERNAME/w3d3-dockerhub-app:0.1.0
docker logout
```

수업에서는 password 대신 Docker Hub access token을 사용하도록 안내한다.

## CI/CD Gate 비용
자동화 gate가 추가되면 배포는 느려질 수 있다. 하지만 수동 배포의 실수와 추적 비용을 줄인다.

| Gate | 늘어나는 시간 | 줄이는 위험 |
|---|---|---|
| unit test | 수 초~수 분 | 기본 동작 회귀 |
| SAST/secret scan | 수 초~수 분 | 위험 코드, secret 노출 |
| Docker build | 수십 초~수 분 | build 실패, Dockerfile 오류 |
| DAST smoke check | 수 초~수 분 | 실행 후 health 실패 |
| Docker Hub push | network 시간 | registry artifact 누락 |

## End-Of-Day Checklist
- [ ] 개발자 GitHub 흐름과 인프라 GitHub 흐름의 차이를 설명했다.
- [ ] dev/stage/prod branch 전략의 장단점을 설명했다.
- [ ] protected branch와 required status check의 목적을 설명했다.
- [ ] GitHub Actions workflow에서 event/job/step/runner/secret을 찾았다.
- [ ] unit test, SAST, DAST의 차이를 설명했다.
- [ ] GitHub Secrets의 장단점을 설명했다.
- [ ] sample app을 로컬에서 Docker build/run 했다.
- [ ] Docker Hub push workflow의 secrets와 image tag 기준을 설명했다.
- [ ] Docker Hub에서 image를 확인하고 pull/run하는 절차를 작성했다.
- [ ] private Docker Hub image는 pull 전 `docker login`이 필요하다는 점을 설명했다.
- [ ] 본인 GitHub repo에서 Actions step별 실행 시간을 확인했다.
- [ ] unit test, SAST, DAST, build, push 중 시간이 많이 걸린 단계를 분석했다.
