# 8교시 · CI 검문소 늘리기 — 이미지 스캔 · 계약 테스트 · 액션 고정

!!! goal "이번 시간에 할 일"
    - 2주차 3일차 8교시의 **Trivy 검문소**를 `build` 잡에 넣어, 심각한 취약점이 있는 이미지는 **GHCR에 올라가지 못하게** 합니다.
    - 어제 8교시의 **계약 테스트**를 CI에서 DevMart 전체를 띄워 돌립니다.
    - 남이 만든 액션을 **커밋 SHA로 고정**하는 이유를 실제 사고로 이해하고, 하나를 고정해 봅니다.
    - 같은 PR에 커밋을 연달아 올릴 때 낡은 실행을 취소하고(`concurrency`), 멈춘 잡에 시간 제한(`timeout-minutes`)을 겁니다.

!!! key "검문소는 싸고 빨라야 한다"
    6~7교시의 CI는 "테스트가 통과하나, 이미지가 만들어지나"를 봤습니다. 오늘은 **"만들어진 이미지가 안전한가, 다른 서비스와의 약속을 지키나"**를 더합니다. 검문소가 많아질수록 CI가 느려지므로, 각 검사는 **몇 분 안에 끝나고 실패 이유가 한 줄로 보이게** 만듭니다.

## 실습 18 · build 잡에 Trivy 넣기

!!! lab "실습 목표"
    이미지를 **올리기 전에** 러너 안에서 검사하고, CRITICAL 취약점이 있으면 잡을 실패시킵니다.

### 단계 1 — 브랜치

```bash
cd ~/devops-lab
git switch main && git pull
git switch -c ci/gates
code .github/workflows/devmart-ci.yml
```

### 단계 2 — build 잡의 스텝 바꾸기

`build` 잡의 마지막 스텝 **"빌드 (main이면 push까지)"**를 아래 세 스텝으로 바꿉니다.

```yaml
      - name: 빌드 (러너에 싣기만)
        uses: docker/build-push-action@v7
        with:
          context: devmart-msa/${{ matrix.service }}
          load: true                          # 러너의 Docker에 이미지를 싣는다
          push: false
          tags: ${{ steps.meta.outputs.tags }}
          labels: ${{ steps.meta.outputs.labels }}
          cache-from: type=gha,scope=${{ matrix.service }}
          cache-to: type=gha,mode=max,scope=${{ matrix.service }}

      - name: 취약점 검문 (CRITICAL이면 실패)
        env:
          IMAGE: ${{ fromJSON(steps.meta.outputs.json).tags[0] }}
        run: |
          docker run --rm -v /var/run/docker.sock:/var/run/docker.sock \
            aquasec/trivy:0.76.2 image --exit-code 1 --severity CRITICAL \
            --ignore-unfixed --no-progress "$IMAGE"

      - name: GHCR에 올리기 (main에 push될 때만)
        if: github.event_name == 'push'
        env:
          IMAGE: ${{ fromJSON(steps.meta.outputs.json).tags[0] }}
        run: docker push --all-tags "${IMAGE%:*}"     # 태그를 뗀 저장소 이름
```

| 바뀐 곳 | 이유 |
|---|---|
| `load: true`, `push: false` | 먼저 **러너 안에만** 만들어 둔다 — 검사 전에는 아무 데도 내보내지 않는다 |
| `tags[0]` | `metadata-action`이 만든 태그 목록 중 첫 번째(`sha-…`)로 검사 |
| `--ignore-unfixed` | **고친 버전이 아직 없는** 취약점은 지금 우리가 할 수 있는 게 없으므로 검문에서 뺀다(기록은 2주차 3일차의 `.trivyignore` 방식으로) |
| `docker push --all-tags` | 검사를 통과한 뒤에야 그 저장소의 태그를 모두 올린다. `if`로 main에 합쳐질 때만. 로그인 스텝도 같은 조건이라 그대로 둔다 |

!!! tip "`${IMAGE%:*}`"
    셸의 **변수 잘라 내기**입니다. `IMAGE`가 `ghcr.io/me/devmart-catalog-api:sha-1a2b3c4`이면 `%:*`는 **마지막 `:`부터 끝까지를 지운** `ghcr.io/me/devmart-catalog-api`가 됩니다. `metadata-action`이 만든 이름을 그대로 쓰므로, GitHub 아이디에 대문자가 있어도 소문자로 바뀐 이름이 쓰입니다(레지스트리 이름은 소문자만 허용).

## 실습 19 · 계약 테스트 잡 — DevMart 전체를 CI에서

어제 만든 `devmart-msa/contract/catalog-for-order.sh`는 **띄워진 DevMart**가 있어야 돕니다. 러너에도 Docker와 Compose가 있으므로, CI 안에서 통째로 띄웁니다.

`jobs:` 아래, `compose-check` 다음에 새 잡을 추가합니다.

```yaml
  contract:
    runs-on: ubuntu-latest
    timeout-minutes: 10
    defaults:
      run:
        working-directory: devmart-msa
    env:
      DB_PASSWORD: ci-dummy-not-secret      # CI 안에서만 쓰는 가짜 값
    steps:
      - uses: actions/checkout@v6
      - name: DevMart 띄우기
        run: docker compose up -d --build --wait
      - name: 계약 테스트 (order-api → catalog-api)
        run: ./contract/catalog-for-order.sh
      - name: 실패하면 로그 남기기
        if: failure()
        run: docker compose logs --tail 50
      - name: 정리
        if: always()
        run: docker compose down -v
```

| 부분 | 뜻 |
|---|---|
| `--wait` | 모든 서비스가 **running / healthy**가 될 때까지 기다린 뒤 다음 스텝으로 |
| `if: failure()` | 앞 스텝이 실패했을 때만 — 원인을 찾을 **로그를 실행 기록에 남긴다** |
| `if: always()` | 성공하든 실패하든 정리 |
| `timeout-minutes: 10` | 무언가 멈춰도 10분 뒤 끊는다(기본은 6시간 — 무료 사용량을 다 먹는다) |

그리고 `build` 잡이 계약 테스트까지 기다리게 합니다.

```yaml
    needs: [test, compose-check, contract]
```

!!! check "실행 권한 확인"
    스크립트를 커밋할 때 실행 권한(`chmod +x`)이 함께 저장되었는지 확인합니다.
    ```bash
    git ls-files -s devmart-msa/contract/catalog-for-order.sh
    ```
    맨 앞이 `100755`면 됩니다. `100644`면 CI에서 `Permission denied`가 납니다 → `git update-index --chmod=+x devmart-msa/contract/catalog-for-order.sh`

## 실습 20 · 낡은 실행 취소 · 액션 고정

### 단계 1 — `concurrency`

워크플로 맨 위, `permissions:` 아래에 추가합니다.

```yaml
concurrency:
  group: ci-${{ github.ref }}
  cancel-in-progress: true
```

같은 브랜치(PR)에 커밋을 빠르게 세 번 올리면, 앞의 두 실행은 **어차피 쓸모없으므로** 취소하고 마지막 것만 돕니다. 러너 시간과 기다림이 줄어듭니다.

### 단계 2 — 액션을 커밋 SHA로 고정

`uses: actions/checkout@v6`의 `v6`은 **움직일 수 있는 태그**입니다. 액션 저장소의 주인이(또는 그 계정을 훔친 사람이) 태그를 다른 커밋으로 옮기면, 우리 CI는 **다음 실행부터 다른 코드를** 돌립니다. 그래서 중요한 액션은 **바뀌지 않는 커밋 SHA**로 고정합니다.

```bash
git ls-remote --tags https://github.com/actions/checkout | grep -E 'refs/tags/v6\.[0-9]+\.[0-9]+$' | sort -t/ -k3 -V | tail -1
```

!!! check "보이는 것 (예)"
    ```text
    d23441a48e516b6c34aea4fa41551a30e30af803	refs/tags/v6.1.0
    ```
    앞의 40자리가 그 버전의 커밋 SHA입니다.

`checkout` 줄들을 이렇게 바꿉니다(SHA는 직접 조회한 값으로).

```yaml
      - uses: actions/checkout@d23441a48e516b6c34aea4fa41551a30e30af803   # v6.1.0
```

- 뒤의 주석 `# v6.1.0`은 사람이 읽기 위한 것입니다
- 고정하면 **보안 패치도 자동으로 안 들어옵니다.** 그래서 다음 단계의 Dependabot이 짝으로 필요합니다

### 단계 3 — Dependabot이 고정을 최신으로 유지

```bash
code .github/dependabot.yml
```

```yaml
version: 2
updates:
  - package-ecosystem: github-actions
    directory: /
    schedule:
      interval: weekly
```

일주일에 한 번, 고정한 액션에 새 버전이 나오면 Dependabot이 **SHA를 바꾸는 PR**을 열어 줍니다. 사람이 변경 내용을 보고 CI가 초록이면 병합합니다. **고정(안전) + 자동 갱신 PR(최신)**의 조합입니다.

### 단계 4 — 올리고 확인

```bash
git add .github/
git commit -m "CI: Trivy 검문, 계약 테스트 잡, concurrency, checkout SHA 고정, Dependabot"
git push -u origin ci/gates
gh pr create --fill
gh pr checks --watch
```

!!! check "이렇게 나오면 성공"
    ```text
    ✓  test (catalog-api)
    ✓  test (order-api)
    ✓  compose-check
    ✓  contract
    ✓  build (catalog-api)
    ✓  build (order-api)
    ✓  build (order-worker)
    ```
    PR 화면의 `build` 로그를 열어 **"취약점 검문"** 스텝에 `Total: 0 (CRITICAL: 0)`이 보이는지 확인합니다.

### 단계 5 — 필수 검사에 추가하고 병합

**Settings → Rules → Rulesets → main 보호 → Require status checks to pass**에 `contract`를 추가합니다. 그다음 PR을 병합합니다.

!!! example "검문이 실패하면"
    | 실패한 스텝 | 뜻 | 할 일 |
    |---|---|---|
    | 취약점 검문 | 고칠 수 있는 CRITICAL이 있다 | `Fixed Version`을 보고 베이스 이미지를 올리거나 다시 빌드(2주차 3일차 8교시) |
    | 계약 테스트 | 소비자와의 약속을 깼다 | 어제처럼 **늘리기 → 옮기기 → 줄이기**로 다시 |
    | `contract` 잡의 `--wait` 시간 초과 | 서비스가 healthy가 안 됨 | `if: failure()`로 남은 로그에서 원인 |

!!! cleanup "정리"
    ```bash
    git switch main && git pull
    git branch -d ci/gates
    ```

!!! academic "학술 노트 — CI 워크플로의 보안 (Koishybayev 외, 2022)"
    노스캐롤라이나 주립대 연구진은 2022년 USENIX Security에서 공개 GitHub 저장소의 워크플로 수십만 개를 분석한 결과를 발표했습니다. 상당수가 **필요보다 넓은 토큰 권한**을 주고, 남의 액션을 **움직이는 태그로** 가져오며, PR 제목처럼 **외부인이 넣을 수 있는 글자를 그대로 명령에 끼워** 실행하고 있었습니다. CI는 저장소 쓰기 권한과 비밀값을 가진 **가장 강한 자동화**인데, 보안 점검은 가장 덜 받고 있다는 결론이었습니다.

    이 경고는 2025년 3월 현실이 됐습니다. 널리 쓰이던 액션 `tj-actions/changed-files`의 **태그들이 악성 커밋으로 옮겨져**, 그 액션을 태그로 쓰던 수많은 저장소의 CI가 실행 로그에 **비밀값을 찍어 내는** 코드를 돌렸습니다(CVE-2025-30066). **SHA로 고정한 저장소는 영향을 받지 않았습니다.** 6교시에 `permissions:`를 최소로 둔 것, 오늘 SHA로 고정한 것이 이 사고를 막는 두 줄입니다.

    - Koishybayev, I. et al. (2022). Characterizing the security of GitHub CI workflows. *31st USENIX Security Symposium*.
    - CISA (2025.3). *Supply Chain Compromise of Third-Party tj-actions/changed-files (CVE-2025-30066)*.

!!! trend "트렌드 — '고정'을 조직의 규칙으로"
    SHA 고정이 개인의 습관에서 **조직의 규칙**으로 바뀌고 있습니다. GitHub는 조직 · 저장소 설정에서 허용할 액션을 정하고 **SHA로 고정된 액션만 쓰도록 강제**할 수 있게 했습니다. OpenSSF의 **Scorecard**는 오픈소스 저장소가 액션을 고정했는지, 토큰 권한을 줄였는지를 자동으로 점수 매겨, 의존성을 고를 때 참고 지표로 쓰입니다. 4주차 5일차에는 이미지에도 같은 생각(태그가 아니라 다이제스트 · 서명으로 확인)을 적용합니다.

## 정리

- 이미지는 **러너 안에서 만들고(`load: true`) → 검사하고 → 통과하면 올립니다.** 검문은 `--exit-code 1 --severity CRITICAL --ignore-unfixed`.
- 계약 테스트는 CI에서 `docker compose up --wait`로 DevMart를 통째로 띄워 돌립니다. 실패하면 로그를, 끝나면 정리를(`if: failure()`, `if: always()`).
- `concurrency`로 낡은 실행을 취소하고, `timeout-minutes`로 멈춘 잡을 끊습니다.
- 남의 액션은 **커밋 SHA로 고정**하고, **Dependabot**으로 최신을 유지합니다.

!!! quiz "확인 문제"
    1. 이미지 검사를 `docker push` **뒤에** 하면 무엇이 문제인가요?
    2. `--ignore-unfixed`를 쓰는 이유는?
    3. `contract` 잡에서 `if: always()`인 정리 스텝이 없으면 어떻게 되나요? (힌트: 러너는 매번 새것)
    4. `uses: 액션@v6` 대신 `@<SHA>`를 쓰면 막을 수 있는 사고는?
    5. SHA로 고정했을 때 생기는 단점과 그 보완책은?

    ??? answer "정답"
        1. 검사에 걸려도 이미 레지스트리에 올라가 누군가 받아 쓸 수 있습니다. 검사 → 통과 → 올리기 순서여야 합니다.
        2. 고친 버전이 없는 취약점은 지금 할 수 있는 조치가 없어, 검문을 막기만 하고 판단에 도움이 되지 않기 때문입니다(따로 기록·판단).
        3. GitHub 호스팅 러너는 잡이 끝나면 버려지므로 큰 문제는 없지만, 자체 러너라면 컨테이너와 볼륨이 쌓입니다. 습관으로 둡니다.
        4. 액션의 태그가 악성 커밋으로 옮겨지는 공급망 공격(예: tj-actions, 2025)
        5. 보안 패치도 자동으로 들어오지 않습니다 → Dependabot이 갱신 PR을 열게 합니다.

!!! diary "오늘의 배움일기 — 수업 뒤 각자"
    - catalog-api를 얼렸을 때 주문 목록까지 느려진 이유를 '콜센터' 말고 **내 비유**로
    - 재시도가 도움이 된 경우와 해가 된 경우를 숫자(초)와 함께
    - `/health`와 `/ready`를 섞어 쓰면 생기는 사고를 한 문장으로
    - 유령 주문과 유실 주문 — 어느 쪽이 더 무섭다고 느꼈는지, 왜
    - 내 GHCR 이미지 주소 하나와 그 SHA 태그
    - 오늘 본 CI 실패 네 가지 중 실무에서 가장 자주 만날 것 같은 것
    - 내일(Kubernetes) 전에 궁금한 것: 처리기가 죽으면 **누가** 다시 띄워 줄까? 컴퓨터가 여러 대라면?

## 참고 문헌

- Koishybayev, I., Nahapetyan, A., Zachariah, R., Muralee, S., Reaves, B., Kapravelos, A., & Machiry, A. (2022). Characterizing the security of GitHub CI workflows. *USENIX Security '22*.
- CISA (2025). *Supply Chain Compromise of Third-Party tj-actions/changed-files (CVE-2025-30066) and reviewdog/action-setup (CVE-2025-30154)*.
- GitHub Docs. *Security hardening for GitHub Actions — Using third-party actions (pin to a full-length commit SHA)*; *Control the concurrency of workflows and jobs*; *Configuring Dependabot version updates*.
- Docker Docs. *docker/build-push-action — load, push*; *docker compose up --wait*.
- Aqua Security. *Trivy — CI integrations, --exit-code, --ignore-unfixed*.
- OpenSSF. *Scorecard — Pinned-Dependencies, Token-Permissions checks*. scorecard.dev
