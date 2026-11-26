<sub>[🏠 과정 목차](../../README.md) › [4주차](../README.md) › [3일차](README.md) › 2/8교시</sub>

# 2교시 · CI와 CD 나누기 · 배포 저장소

> [!NOTE]
> **이번 시간에 할 일**
>
> - CI와 CD가 **각각 어디까지** 책임지는지 정합니다.
> - 코드 저장소와 **배포 저장소를 나누는 이유**를 이해합니다.
> - `devmart-deploy` 저장소를 만들고, 오늘까지의 매니페스트를 **한 묶음**으로 모읍니다.
> - kustomize의 `images:`로 **이미지 태그를 한 곳에서** 바꾸는 법을 익힙니다.

## CI는 어디까지, CD는 어디부터

3주차 2일차의 CI는 테스트 → 이미지 빌드 → GHCR push까지 했습니다. 그 이미지를 클러스터에 올린 것은 **사람**(`kubectl apply`)이었습니다. 오늘은 그 빈칸을 이렇게 채웁니다.

| 단계 | 누가 | 결과물 | 클러스터 열쇠 |
|---|---|---|---|
| 테스트 · 빌드 · push | CI (GitHub Actions) | GHCR의 이미지 `:sha-1a2b3c4` | 필요 없음 |
| "이 이미지를 쓰자"를 적기 | CI 봇 | 배포 저장소의 **커밋 한 개** | 필요 없음 (배포 저장소 쓰기 권한만) |
| 클러스터에 맞추기 | Argo CD | 롤링 업데이트 | 클러스터 **안에만** |

> [!IMPORTANT]
> **경계선 — CI는 Git에서 멈춘다**
>
> CI의 마지막 행동은 `kubectl apply`가 아니라 **`git push`**입니다. 그래서 CI는 클러스터에 접속할 정보가 전혀 없습니다. 클러스터가 몇 개든, 어디에 있든(오늘 kind, 5주차 EKS) CI는 바뀌지 않습니다.

## 왜 저장소를 둘로 나누나

같은 저장소의 `deploy/` 폴더에 두어도 Argo CD는 동작합니다. 그래도 Argo CD 공식 문서는 **매니페스트를 소스 코드와 다른 저장소에** 두기를 권합니다.

| 이유 | 같은 저장소라면 생기는 일 |
|---|---|
| **이력이 섞인다** | "로그 문구 고침"과 "운영 replicas 3→5"가 한 이력에 섞인다. 배포 이력만 보기 어렵다 |
| **CI가 자기 자신을 다시 깨운다** | CI 봇이 태그를 커밋 → 그 커밋이 또 CI를 돌린다 → 무한 반복을 막는 장치가 필요하다 |
| **보호 규칙과 부딪친다** | 2주차 5일차에 `main`에 "PR 필수" 규칙(ruleset)을 걸었다. CI 봇(`GITHUB_TOKEN`)은 이 규칙을 **건너뛸 수 없다** — 직접 push가 거절된다 |
| **권한이 섞인다** | 코드를 고칠 수 있는 사람 = 운영 설정을 고칠 수 있는 사람이 된다 |
| **설정만 바꿀 때도 CI가 돈다** | replicas 하나 바꾸려고 테스트 · 빌드를 다시 기다린다 |

> [!WARNING]
> **세 번째 이유는 실제로 막힌다**
>
> `GITHUB_TOKEN`으로 만든 push는 저장소 규칙의 우회(Bypass) 목록에 넣을 방법이 없습니다. "PR 필수"가 걸린 `main`에 CI 봇이 직접 커밋하려면 GitHub App이나 개인 토큰을 따로 만들어야 하고, 그러면 **"PR 필수"의 의미가 약해집니다.** 배포 저장소를 나누면 코드 저장소의 규칙은 그대로 두고, 배포 저장소 **하나만** 쓸 수 있는 토큰을 CI에 줄 수 있습니다(7교시).

## 실습 1 · 배포 저장소 만들기

```bash
cd ~
gh repo create devmart-deploy --public --clone --description "DevMart 배포 매니페스트 (GitOps)"
cd devmart-deploy
mkdir devmart
```

> **🟢 확인: 확인**
>
> ```text
> ✓ Created repository YOUR_ID/devmart-deploy on GitHub
>   https://github.com/YOUR_ID/devmart-deploy
> Cloning into 'devmart-deploy'...
> warning: You appear to have cloned an empty repository.
> ```
> 빈 저장소라는 경고는 정상입니다. **공개(public)** 저장소로 만들어 Argo CD가 로그인 없이 읽게 합니다. 회사라면 비공개로 두고 Argo CD에 읽기 전용 배포 키(deploy key)를 등록합니다.

## 실습 2 · 매니페스트 모으기

지난 사흘의 결과물을 한 폴더에 모읍니다.

```bash
cp -r ~/devops-lab/k8s/day5/devmart/* devmart/                         # 3주차 5일차 — 앱 전체 (web은 1일차에 ClusterIP로 바꾼 것)
cp ~/devops-lab/k8s/w4d1/gateway/devmart-routes.yaml devmart/           # 4주차 1일차 — 라우트
cp ~/devops-lab/k8s/w4d2/monitoring/devmart-dashboard.yaml devmart/     # 4주차 2일차 — 대시보드
cp ~/devops-lab/k8s/w4d2/monitoring/devmart-rules.yaml devmart/         # 4주차 2일차 — 알림 규칙
mkdir -p ~/devops-lab/k8s/w4d3 && cp -r ~/course/labs/week4/day3/* ~/devops-lab/k8s/w4d3/
cp ~/devops-lab/k8s/w4d3/deploy/kustomization.yaml devmart/kustomization.yaml   # 덮어쓴다
ls devmart
```

> **🟢 확인: 확인**
>
> ```text
> catalog-api.yaml  db.yaml                 devmart-routes.yaml  files               namespace.yaml  order-worker.yaml  web.yaml
> config.yaml       devmart-dashboard.yaml  devmart-rules.yaml   kustomization.yaml  order-api.yaml  redis.yaml
> ```

새 `kustomization.yaml`에서 3주차와 달라진 곳은 두 군데입니다.

```yaml
resources:
  # … 3주차 5일차의 8개 …
  - devmart-routes.yaml          # 4주차 1일차
  - devmart-dashboard.yaml       # 4주차 2일차
  - devmart-rules.yaml           # 4주차 2일차
# 7교시부터 CI가 이 아래 태그를 바꾼다 — 사람은 손대지 않는다
images:
  - name: ghcr.io/YOUR_ID/devmart-catalog-api
    newTag: YOUR_SHA
  - name: ghcr.io/YOUR_ID/devmart-order-api
    newTag: YOUR_SHA
  - name: ghcr.io/YOUR_ID/devmart-order-worker
    newTag: YOUR_SHA
```

### `images:` — 태그를 한 곳에서

3주차에는 이미지 태그가 Deployment 파일 세 곳에 흩어져 있었습니다. kustomize의 **images 변환기**는 `name`이 같은 이미지를 찾아 **태그만 바꿔 끼웁니다.** 파일 원본은 그대로 두고, 바꿀 곳은 이 목록 하나가 됩니다. CI 봇도 이 목록만 고치면 됩니다.

지금 클러스터에 떠 있는 태그로 채웁니다.

```bash
cd ~/devmart-deploy/devmart
ID=$(gh api user -q .login | tr 'A-Z' 'a-z')                     # 이미지 주소는 소문자
TAG=$(kubectl get deploy catalog-api -n devmart -o jsonpath='{.spec.template.spec.containers[0].image}' | cut -d: -f2)
echo "$ID $TAG"
sed -i "s/YOUR_ID/$ID/g; s/YOUR_SHA/$TAG/g" *.yaml    # macOS: sed -i '' …
grep -A1 "name: ghcr" kustomization.yaml
```

> **🟢 확인: 확인**
>
> ```text
> niceguy61 sha-7c1e9a2
>     - name: ghcr.io/niceguy61/devmart-catalog-api
>       newTag: sha-7c1e9a2
>     - name: ghcr.io/niceguy61/devmart-order-api
>       newTag: sha-7c1e9a2
>     - name: ghcr.io/niceguy61/devmart-order-worker
>       newTag: sha-7c1e9a2
> ```
> 값은 사람마다 다릅니다. `YOUR_`가 하나도 남지 않아야 합니다: `grep -rn YOUR_ .` → 아무것도 안 나옴.

> [!TIP]
> **Deployment 파일 안의 YOUR_ID도**
>
> 3주차 5일차에 Deployment 파일의 `YOUR_ID:YOUR_SHA`를 이미 바꿨다면 그대로 둡니다. 아직 남아 있다면 `grep -rn YOUR_ .`이 알려 줍니다 — 같은 `sed`가 함께 바꿉니다. 어느 쪽이든 최종 태그는 `images:`가 정합니다.

## 실습 3 · 렌더링해 보고, 지금 클러스터와 비교

Argo CD가 할 일을 손으로 먼저 해 봅니다.

```bash
cd ~/devmart-deploy
kubectl kustomize devmart | grep -E '^kind:' | sort | uniq -c
kubectl diff -k devmart; echo "diff 종료 코드: $?"
```

> **🟢 확인: 확인**
>
> ```text
>       5 kind: ConfigMap
>       6 kind: Deployment
>       3 kind: HTTPRoute
>       1 kind: Namespace
>       1 kind: PersistentVolumeClaim
>       1 kind: PrometheusRule
>       5 kind: Service
> diff 종료 코드: 0
> ```
> `kubectl diff`가 아무것도 출력하지 않고 0으로 끝나면 **배포 저장소 = 지금 클러스터**입니다. 무엇인가 나온다면(종료 코드 1) 지난 실습에서 손으로 바꾼 것이 남아 있다는 뜻입니다 — 지우지 말고 기억해 두세요. 5교시에 Argo CD가 같은 것을 보여 줍니다.

> [!WARNING]
> **Secret은 여기에 없다**
>
> `devmart-db`(3주차 5일차)와 `grafana-admin`(어제)은 **파일로 두지 않았습니다.** 배포 저장소는 공개 저장소이고, Git 이력은 지워지지 않습니다. 비밀 값을 Git으로 다루는 방법(Sealed Secrets · External Secrets · SOPS)은 7교시 끝에서 소개만 합니다. 오늘은 "Secret은 클러스터에 이미 있고, Argo CD는 손대지 않는다"로 갑니다.

## 실습 4 · 첫 커밋

```bash
cd ~/devmart-deploy
cat > README.md <<'MD'
# devmart-deploy

DevMart의 원하는 상태. Argo CD가 `devmart/`을 클러스터에 맞춘다.

- 이미지 태그(`devmart/kustomization.yaml`의 `images:`)는 CI 봇이 바꾼다.
- 그 밖의 변경은 PR로.
- Secret은 이 저장소에 두지 않는다.
MD
git add .
git commit -m "DevMart 매니페스트 첫 커밋 (3주차 5일차 + 라우트 · 대시보드 · 규칙)"
git push -u origin main
gh repo view --web
```

> **🟢 확인: 확인**
>
> GitHub 화면에 `README.md`와 `devmart/` 폴더가 보입니다. 이제 **DevMart의 원하는 상태는 이 저장소의 `main`**입니다.

> [!TIP]
> **배포 저장소에도 규칙을**
>
> 오늘은 실습 속도를 위해 `main`에 직접 push합니다. 실무에서는 배포 저장소에도 "PR 필수"를 걸고, CI 봇만 우회 목록에 넣습니다(봇은 GitHub App으로 만든다). 운영 설정 변경도 리뷰를 받게 하기 위해서입니다.

> **🎓 학술 노트 — 배포 파이프라인과 단일 출처**
>
> Humble과 Farley의 *Continuous Delivery*(2010)는 배포 파이프라인의 핵심 규칙으로 "**한 번 빌드한 산출물을 모든 환경에 그대로**"와 "**환경 설정을 버전 관리에**"를 꼽았습니다. 오늘의 구조에서 산출물은 `sha-` 태그가 붙은 이미지이고, 환경 설정은 배포 저장소입니다. 같은 이미지가 kind에서도, 5주차의 EKS에서도 태그만으로 지목됩니다. Forsgren 외의 *Accelerate*(2018)는 "운영 설정까지 버전 관리하는 팀"이 배포 빈도 · 복구 시간에서 뚜렷이 앞선다는 것을 설문으로 보였습니다.

> **📈 트렌드 2026 — 렌더링된 매니페스트를 커밋하기**
>
> Argo CD 3.x에는 **Source Hydrator**가 들어왔습니다. kustomize · Helm의 '원본'을 두는 브랜치와, 그것을 **다 펼친 결과 YAML**을 두는 브랜치를 나누고, Argo CD가 펼친 결과를 커밋합니다. 리뷰어가 "이 PR이 실제로 클러스터의 무엇을 바꾸나"를 YAML 그대로 볼 수 있게 하자는 흐름입니다 — 실습 3에서 `kubectl kustomize`로 펼쳐 본 것과 같은 동기입니다.

> **✅ 확인 문제**
>
> 1. 오늘 CI의 마지막 행동은 무엇이고, 왜 `kubectl apply`가 아닌가요?
> 2. 배포 저장소를 나누는 이유 세 가지는?
> 3. kustomize `images:`의 `name`은 무엇과 맞춰지나요?
> 4. `kubectl diff -k`의 종료 코드 0과 1의 뜻은?
>
> <details><summary>정답</summary>
>
> 1. 배포 저장소에 `git push`. CI가 클러스터 열쇠를 갖지 않게 하려고
> 2. 이력이 섞인다, CI가 자기 자신을 다시 깨운다, 코드 저장소의 PR 필수 규칙과 부딪친다, 권한이 섞인다, 설정만 바꿀 때도 CI가 돈다 중 셋
> 3. Deployment 안 `image:`의 태그 앞부분(저장소 주소). 같으면 태그를 바꿔 끼운다
> 4. 0 — 차이 없음, 1 — 차이 있음 (2 이상은 오류)
>
> </details>

## 참고 문헌

- Argo CD Docs. *Best Practices — Separating Config Vs. Source Code Repositories*. argo-cd.readthedocs.io
- Kubernetes Docs. *Kustomize — images*. kubernetes.io/docs/tasks/manage-kubernetes-objects/kustomization
- GitHub Docs. *About rulesets — Bypass list*. docs.github.com
- Humble, J. & Farley, D. (2010). *Continuous Delivery*. Addison-Wesley.
- Forsgren, N., Humble, J. & Kim, G. (2018). *Accelerate*. IT Revolution.
- Argo CD Docs. *Source Hydrator*. argo-cd.readthedocs.io/en/stable/user-guide/source-hydrator

---

| 이전 | 목차 | 다음 |
|:--|:--:|--:|
| ⬅️ [1교시 · 2일차 요약 + GitOps](lesson-01.md) | [⬆️ 3일차 목차](README.md) | [3교시 · Argo CD 설치](lesson-03.md) ➡️ |
