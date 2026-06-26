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

macOS에서 `sed: ... command a expects \ followed by text`가 나오면 권한 문제가 아니라 BSD sed와 GNU sed의 `-i` 옵션 차이다. 최신 `setup.sh`는 portable 방식으로 수정되어 있으므로 자료를 갱신한 뒤 다시 실행한다.

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

## Phase 7. GitHub Actions Workflow 작성
개인 repository에서는 다음 경로에 workflow 파일을 만든다.

```bash
mkdir -p .github/workflows
```

8교시에서 기본으로 복사할 파일은 workflow YAML 하나다.

```bash
COURSE_REPO=/mnt/d/paperclip
MY_REPO=/path/to/my/w3d3-github-actions-dockerhub

cd "$MY_REPO"
mkdir -p .github/workflows

cp "$COURSE_REPO/week3/day3/labs/github-actions/dockerhub-publish.yml" .github/workflows/dockerhub-publish.yml
```

복사되는 파일:

| 원본 | 대상 |
|---|---|
| `week3/day3/labs/github-actions/dockerhub-publish.yml` | `.github/workflows/dockerhub-publish.yml` |

복사 후 확인:

```bash
ls -al .github/workflows
sed -n '1,220p' .github/workflows/dockerhub-publish.yml
```

전제 조건:

| 필요 파일 | 이유 |
|---|---|
| `week3/day3/labs/dockerhub-app/` | Docker build context |
| `week3/day3/labs/quality-gates/` | unit/SAST/DAST step 실행 |

앞 실습에서 위 파일을 이미 개인 repository에 넣었다면 workflow YAML만 복사하면 된다. 파일이 없다면 다음 보조 명령으로 샘플도 함께 가져온다.

```bash
mkdir -p week3/day3/labs
cp -R "$COURSE_REPO/week3/day3/labs/dockerhub-app" week3/day3/labs/
cp -R "$COURSE_REPO/week3/day3/labs/quality-gates" week3/day3/labs/
```

`APP_DIR`를 바꾸지 않으려면 app은 `week3/day3/labs/dockerhub-app` 경로에 둔다.

최소 workflow로 먼저 구조를 확인한다.

```yaml
name: w3d3-first-action

on:
  workflow_dispatch:

jobs:
  hello:
    runs-on: ubuntu-latest
    steps:
      - name: Print runner info
        run: |
          pwd
          uname -a
          echo "hello github actions"
```

작성 포인트:

| YAML | 의미 |
|---|---|
| `name` | Actions 화면에 보이는 workflow 이름 |
| `on` | 실행 조건 |
| `workflow_dispatch` | 수동 실행 버튼 |
| `jobs` | 실행할 작업 묶음 |
| `runs-on` | runner 종류 |
| `steps` | job 내부 실행 단계 |
| `uses` | 외부 action 사용 |
| `run` | shell 명령 실행 |
| `cache-from` | 이전 build cache 사용 |
| `cache-to` | 다음 실행을 위한 cache 저장 |

최소 workflow가 실행되면 Docker Hub publish workflow로 확장한다.

```bash
cat week3/day3/labs/github-actions/dockerhub-publish.yml
```

개인 repo에 복사할 때는 다음 값을 확인한다.

| 항목 | 의미 |
|---|---|
| `.github/workflows/dockerhub-publish.yml` | workflow 파일 위치 |
| `workflow_dispatch` | 수동 실행 |
| `push.tags` | `v0.1.0` 같은 tag push 시 실행 |
| `env.IMAGE_NAME` | Docker Hub repository 이름 |
| `env.APP_DIR` | Docker build context 경로 |
| `DOCKERHUB_USERNAME` | Docker Hub namespace secret |
| `DOCKERHUB_TOKEN` | Docker Hub token secret |
| `docker/build-push-action` | image build/push |
| `cache-from: type=gha` | GitHub Actions cache에서 Docker layer 복원 |
| `cache-to: type=gha,mode=max` | Docker layer cache 저장 |
| unit test step | 코드 단위 검증 |
| SAST step | 위험 코드/secret scan |
| DAST step | container 실행 후 health 검증 |

작성 순서:

| 순서 | Step | 설명 |
|---|---|---|
| 1 | Checkout repository | runner가 코드를 가져온다 |
| 2 | Prepare image metadata | tag/version을 만든다 |
| 3 | Run unit test | 코드 단위 검증 |
| 4 | Run SAST and secret scan | 위험 코드와 secret 노출 검사 |
| 5 | Set up Docker Buildx | Docker build 환경 준비 |
| 6 | Build local image for DAST | push 전 image build, GHA cache 사용 |
| 7 | Run DAST health check | 실행 중인 container 검증 |
| 8 | Login to Docker Hub | secret으로 registry 인증 |
| 9 | Build and push image | Docker Hub에 image 업로드 |
| 10 | Show pull command | 검증 명령 출력 |

주의:

| 주의 | 이유 |
|---|---|
| `secrets.DOCKERHUB_TOKEN`을 출력하지 않는다 | token 노출 방지 |
| `APP_DIR` 경로가 실제 repo 구조와 맞아야 한다 | build context 오류 방지 |
| step을 하나로 합치지 않는다 | 실패 위치와 실행 시간 확인 |
| tag trigger를 쓸 때 `v0.1.0` 형식을 맞춘다 | `v*.*.*` 조건과 일치 |
| cache가 항상 빨라지는 것은 아니다 | restore/save 비용과 cache miss 가능성 |

## Phase 8. GitHub에서 Actions 동작 확인
GitHub UI에서 확인한다.

| 위치 | 확인할 것 |
|---|---|
| Repository Settings > Secrets and variables > Actions | Docker Hub secrets 존재 여부 |
| Actions tab | workflow run 성공/실패 |
| Job log | failed step, build output, pushed tag |
| Docker Hub repository | image tag 생성 여부 |

## Phase 8-0. Runner Computing 확인
Actions job detail에서 runner와 cache 관련 log를 확인한다.

| 확인 항목 | 의미 |
|---|---|
| `runs-on: ubuntu-latest` | GitHub-hosted runner 사용 |
| runner image 정보 | 매 실행마다 새 환경으로 시작한다고 가정 |
| Docker build cache log | cache hit/miss 확인 |
| `cache-from: type=gha` | 이전 Actions cache를 읽는지 확인 |
| `cache-to: type=gha` | 다음 실행을 위해 cache를 저장하는지 확인 |

같은 workflow를 두 번 실행해서 첫 실행과 두 번째 실행의 Docker build 시간을 비교한다. 첫 실행은 cold build, 두 번째 실행은 warm build로 기록한다.

## Phase 8-1. Step 실행 시간 분석
Actions run 화면에서 각 step의 실행 시간을 기록한다.

| Step | 실행 시간 | 느려지는 이유 후보 | 보강 아이디어 |
|---|---:|---|---|
| Checkout repository |  | repository 크기, submodule | 필요 파일만 checkout |
| Unit test |  | test 수, fixture 준비 | 빠른 test와 느린 test 분리 |
| SAST and secret scan |  | scan 범위, rule 수 | scan 대상 경로 제한 |
| Docker build |  | base image pull, cache miss | `type=gha` cache, `.dockerignore`, 작은 base image |
| Cache restore/save |  | cache size, network | cache 대상 조정 |
| DAST health check |  | container boot, health retry | 명확한 health endpoint |
| Docker Hub login/push |  | network, image size | image 최적화, tag 정책 정리 |

시간이 길어진다는 것은 무조건 나쁜 것이 아니다. 어떤 위험을 줄이기 위해 시간이 늘어났는지 설명할 수 있어야 한다.

## Phase 8-2. GitHub-Hosted Runner와 Self-Hosted Runner 비교
| 구분 | GitHub-hosted runner | Self-hosted runner |
|---|---|---|
| 운영 | GitHub가 관리 | 직접 관리 |
| cache | 명시적 cache 설정 필요 | 로컬 disk cache 유지 가능 |
| 속도 | 편하지만 cold start 영향 | 장비/네트워크에 따라 빠를 수 있음 |
| 보안 | 격리된 일회성 환경에 가까움 | workspace 정리와 secret 보호 책임 |
| 내부망 접근 | 제한적 | 사내망/내부 registry 접근 가능 |

수업에서는 GitHub-hosted runner를 기본으로 쓰고, 회사에서는 private registry, 내부망, 대형 build 자원 요구가 있을 때 self-hosted runner를 검토한다.

## Phase 8-3. 수동 배포와 자동화 비교
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
