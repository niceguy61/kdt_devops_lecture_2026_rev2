# Week 3 Day 3 Hands-on Lab: GitHub Strategy and Docker Hub Actions

## Phase 1. Git 상태와 이론 연결
```bash
cd /mnt/d/paperclip
git status -sb
git branch --show-current
git log --oneline -5
git remote -v
```

기록:

| Evidence | 값 |
|---|---|
| current branch | |
| remote origin | |
| modified files | |
| latest commit | |

## Phase 2. Git Sandbox로 conflict/revert/tag
```bash
week3/day3/labs/git-sandbox/setup.sh
cd /tmp/w3d3-git-sandbox
git log --oneline --graph --decorate --all
```

Conflict:

```bash
git switch feature/change-message
git rebase main
git status
cat app.txt
git rebase --abort
```

Revert and tag:

```bash
git switch main
git revert HEAD --no-edit
git tag v0.1.0
git log --oneline --graph --decorate -6
git tag --list
```

## Phase 3. Branch 전략 설계
다음 중 하나를 선택해 이유를 적는다.

| 전략 | 선택 기준 |
|---|---|
| GitHub Flow | 작고 자주 배포하는 웹 서비스 |
| dev/stage/prod branch | 환경별 승인과 배포 gate가 필요한 조직 |
| trunk-based + environment | main 중심, 배포 환경은 GitHub Environment로 분리 |
| Git Flow | release/hotfix branch가 필요한 버전 릴리스 조직 |

## Phase 4. `.gitignore`와 `.dockerignore` 확인
```bash
cd /mnt/d/paperclip
cat .gitignore
cat week3/day3/labs/dockerhub-app/.dockerignore
```

확인:

| 파일 | 막아야 할 것 |
|---|---|
| `.gitignore` | `.env`, `node_modules`, temp, private |
| `.dockerignore` | `.git`, `.env`, cache, build output |

## Phase 5. Demo App 로컬 실행
```bash
python3 week3/day3/labs/dockerhub-app/app.py
```

별도 터미널에서:

```bash
curl -s http://localhost:8080/health
```

수업에서는 오래 켜두지 않고 Ctrl+C로 종료한다.

## Phase 6. Docker Build and Local Run
```bash
cd /mnt/d/paperclip
week3/day3/labs/quality-gates/unit-test.sh
week3/day3/labs/quality-gates/sast-scan.sh

docker build \
  --build-arg APP_VERSION=0.1.0 \
  -t w3d3-dockerhub-app:0.1.0 \
  week3/day3/labs/dockerhub-app

docker rm -f w3d3-dockerhub-app 2>/dev/null || true
docker run -d --name w3d3-dockerhub-app -p 18088:8080 w3d3-dockerhub-app:0.1.0
curl -s http://localhost:18088/health
docker logs --tail=20 w3d3-dockerhub-app
docker rm -f w3d3-dockerhub-app
```

DAST smoke check:

```bash
week3/day3/labs/quality-gates/dast-health-check.sh
```

한 번에 실행:

```bash
week3/day3/labs/quality-gates/run-all-local.sh
```

## Phase 7. GitHub Actions Workflow 읽기
```bash
cat week3/day3/labs/github-actions/dockerhub-publish.yml
```

확인:

| 항목 | 의미 |
|---|---|
| `workflow_dispatch` | 수동 실행 |
| `push.tags` | `v0.1.0` 같은 tag push 시 실행 |
| `DOCKERHUB_USERNAME` | Docker Hub namespace secret |
| `DOCKERHUB_TOKEN` | Docker Hub token secret |
| `docker/build-push-action` | image build/push |
| unit test step | 코드 단위 검증 |
| SAST step | 위험 코드/secret scan |
| DAST step | container 실행 후 health 검증 |

## Phase 8. GitHub에서 Actions 동작 확인
GitHub UI에서 확인한다.

| 위치 | 확인할 것 |
|---|---|
| Repository Settings > Secrets and variables > Actions | Docker Hub secrets 존재 여부 |
| Actions tab | workflow run 성공/실패 |
| Job log | failed step, build output, pushed tag |
| Docker Hub repository | image tag 생성 여부 |

## Phase 8-0. Step 실행 시간 분석
Actions run 화면에서 각 step의 실행 시간을 기록한다.

| Step | 실행 시간 | 느려지는 이유 후보 | 보강 아이디어 |
|---|---:|---|---|
| Checkout repository |  | repository 크기, submodule | 필요 파일만 checkout |
| Unit test |  | test 수, fixture 준비 | 빠른 test와 느린 test 분리 |
| SAST and secret scan |  | scan 범위, rule 수 | scan 대상 경로 제한 |
| Docker build |  | base image pull, cache miss | cache, `.dockerignore`, 작은 base image |
| DAST health check |  | container boot, health retry | 명확한 health endpoint |
| Docker Hub login/push |  | network, image size | image 최적화, tag 정책 정리 |

시간이 길어진다는 것은 무조건 나쁜 것이 아니다. 어떤 위험을 줄이기 위해 시간이 늘어났는지 설명할 수 있어야 한다.

## Phase 8-1. 수동 배포와 자동화 비교
| 수동 배포 | GitHub Actions |
|---|---|
| 로컬에서 build 명령 직접 실행 | runner에서 같은 명령 반복 |
| Docker Hub login을 사람이 수행 | GitHub Secrets로 login |
| test 누락 가능 | workflow step으로 강제 |
| 누가 언제 push했는지 흐림 | Actions run log가 남음 |
| 실수하면 재현이 어려움 | YAML로 절차 재현 |

## Phase 9. Docker Hub Image Pull/Run
Actions push가 성공한 뒤 실행한다.

Public repository라면 바로 pull할 수 있다.

```bash
docker pull DOCKERHUB_USERNAME/w3d3-dockerhub-app:0.1.0
docker run -d --name w3d3-dockerhub-app -p 18088:8080 DOCKERHUB_USERNAME/w3d3-dockerhub-app:0.1.0
curl -s http://localhost:18088/health
docker rm -f w3d3-dockerhub-app
```

`DOCKERHUB_USERNAME`은 실제 Docker Hub 계정으로 바꾼다.

Private repository라면 pull 전에 Docker Hub 인증이 필요하다.

```bash
docker login -u DOCKERHUB_USERNAME
docker pull DOCKERHUB_USERNAME/w3d3-dockerhub-app:0.1.0
docker run -d --name w3d3-dockerhub-app -p 18088:8080 DOCKERHUB_USERNAME/w3d3-dockerhub-app:0.1.0
curl -s http://localhost:18088/health
docker rm -f w3d3-dockerhub-app
docker logout
```

비밀번호를 직접 입력하지 않고 Docker Hub access token을 입력한다. token은 terminal 화면, shell history, 문서, screenshot에 남기지 않는다.

## Evidence Note
```markdown
# W3D3 Evidence
- Git strategy:
- branch/environment strategy:
- PR gate:
- local docker build:
- local docker run result:
- workflow file:
- required secrets:
- unit test:
- unit test time:
- SAST:
- SAST time:
- DAST:
- DAST time:
- slowest step:
- improvement idea:
- Docker Hub image:
- Docker Hub visibility: public/private
- private pull auth result:
- pull/run result:
```
