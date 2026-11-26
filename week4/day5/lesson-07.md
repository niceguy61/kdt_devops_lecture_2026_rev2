<sub>[🏠 과정 목차](../../README.md) › [4주차](../README.md) › [5일차](README.md) › 7/8교시</sub>

# 7교시 · 공급망 보안 — cosign 서명과 Kyverno 검증

> [!NOTE]
> **이번 시간에 할 일**
>
> - "이 이미지는 **우리 CI가** 만든 것이 맞나?"를 기계가 확인할 수 있게 **서명**합니다.
> - 열쇠를 보관하지 않는 **keyless 서명**(GitHub Actions의 OIDC 신원 + Sigstore)을 CI에 넣습니다.
> - 서명을 `cosign verify`로 직접 확인하고, 서명에 **누가 · 어느 워크플로 · 어느 커밋**이 적혔는지 읽습니다.
> - Kyverno **ImageValidatingPolicy**로 서명 없는 DevMart 이미지는 클러스터에 **들어오지 못하게** 합니다.

> [!IMPORTANT]
> **5교시까지 막은 것과 못 막은 것**
>
> 5교시의 정책은 "**어떻게** 실행하나"(limits, root 금지, latest 금지)를 봤습니다. 그런데 누군가 GHCR 토큰을 훔쳐 **같은 이름 · 그럴듯한 태그**로 악성 이미지를 올리면, 그 이미지는 모든 정책을 통과합니다. 1주차 5일차 7교시의 SolarWinds · xz처럼 **"어디서 왔나"**를 확인해야 합니다. 그 증명이 **서명**입니다.

## 서명은 어떻게 동작하나 — keyless

| 전통적 서명 | keyless 서명 (Sigstore) |
|---|---|
| 개인 열쇠 파일을 **오래 보관** — 잃어버리거나 새면 끝 | 열쇠를 **서명할 때만 잠깐** 만들고 버린다 |
| "이 열쇠의 주인"을 믿는다 | "이 **신원**(GitHub의 이 저장소 · 이 워크플로)"을 믿는다 |
| 열쇠를 어떻게 배포 · 교체하나가 숙제 | 신원 증명은 **OIDC 토큰**(5주차 OIDC와 같은 것), 기록은 공개 장부(**Rekor**) |

```text
CI(GitHub Actions) ──OIDC 토큰("나는 YOUR_ID/devops-lab의 devmart-ci.yml, main")──▶ Fulcio(인증 기관)
                  ◀── 10분짜리 인증서 ──
이미지 digest에 서명 → 서명을 GHCR에 함께 저장 → 서명 사실을 Rekor(공개 장부)에 기록
클러스터의 Kyverno ── "이 이미지의 서명에 적힌 신원이 우리 CI가 맞나?" ──▶ 맞으면 통과
```

## 실습 14 · CI에 서명 넣기 (devops-lab PR)

```bash
cd ~/devops-lab
git switch main && git pull
git switch -c ci/sign
code .github/workflows/devmart-ci.yml
```

### 단계 1 — build 잡에 권한 하나

```yaml
    permissions:
      contents: read
      packages: write
      id-token: write                 # GitHub OIDC 토큰을 받을 권한 — 서명용 신원
```

### 단계 2 — 올린 뒤 서명하는 두 스텝

`build` 잡의 **"GHCR에 올리기"** 스텝 바로 아래에 추가합니다.

```yaml
      - uses: sigstore/cosign-installer@881c63bd87e38389154debd8331404ce7ca8a3ab   # v4.1.4
        if: github.event_name == 'push'
      - name: 서명 (keyless — 보관하는 열쇠 없음)
        if: github.event_name == 'push'
        env:
          IMAGE: ${{ fromJSON(steps.meta.outputs.json).tags[0] }}
        run: |
          DIGEST_REF=$(docker inspect --format '{{index .RepoDigests 0}}' "$IMAGE")
          echo "서명 대상: $DIGEST_REF"
          cosign sign --yes "$DIGEST_REF"
```

| 부분 | 뜻 |
|---|---|
| `id-token: write` | 이 잡이 GitHub에게 "나는 누구다"라는 **OIDC 토큰**을 받아도 된다 |
| `RepoDigests` | 방금 올린 이미지의 **digest 주소**(`…@sha256:…`). 태그가 아니라 **내용**에 서명한다(2주차 3일차: 태그는 움직이고 digest는 안 움직인다) |
| `--yes` | Rekor 공개 장부에 기록하는 것에 동의 — 서명 사실이 **누구나 볼 수 있게** 남는다 |

### 단계 3 — PR → 병합 → 새 이미지

```bash
git add .github/workflows/devmart-ci.yml
git commit -m "CI: cosign keyless 서명"
git push -u origin ci/sign
gh pr create --fill && gh pr checks --watch
gh pr merge --squash --delete-branch
gh run watch $(gh run list --branch main --limit 1 --json databaseId -q '.[0].databaseId')
```

> **🟢 확인: 이렇게 나오면 성공**
>
> main의 실행에서 `build (catalog-api)` 로그를 열면 서명 스텝에 다음이 보입니다.
> ```text
> 서명 대상: ghcr.io/you/devmart-catalog-api@sha256:4f1c…
> Generating ephemeral keys...
> Retrieving signed certificate...
> tlog entry created with index: 712345678
> Pushing signature to: ghcr.io/you/devmart-catalog-api
> ```
> 이어서 `update-manifest`가 배포 저장소에 새 태그를 커밋하고, Argo CD가 1~3분 안에 DevMart를 **서명된 새 이미지로** 바꿉니다(3일차).

## 실습 15 · 서명 직접 확인하기

```bash
ID=$(gh api user --jq .login | tr 'A-Z' 'a-z')
NEW=$(kubectl get deploy catalog-api -n devmart -o jsonpath='{.spec.template.spec.containers[0].image}')
echo $NEW
docker run --rm ghcr.io/sigstore/cosign/cosign:v3.1.6 verify "$NEW" \
  --certificate-oidc-issuer https://token.actions.githubusercontent.com \
  --certificate-identity-regexp "^https://github.com/$ID/devops-lab/\.github/workflows/devmart-ci\.yml@refs/heads/main$" \
  2>/dev/null | jq -r '.[0].optional | "\(.Subject)\n저장소 커밋: \(.githubWorkflowSha)\n트리거: \(.githubWorkflowTrigger)"'
```

> **🟢 확인: 이렇게 나오면 성공**
>
> ```text
> https://github.com/you/devops-lab/.github/workflows/devmart-ci.yml@refs/heads/main
> 저장소 커밋: 9c2e7a1…
> 트리거: push
> ```
> 서명 안에 **어느 저장소의 어느 워크플로가, 어느 커밋에서, main으로 push될 때** 만들었는지가 들어 있습니다. 내 노트북에서 손으로 올린 이미지는 이 신원을 가질 수 없습니다.

옛 이미지(서명 넣기 전)는 어떨까요?

```bash
OLD_TAG=$(git -C ~/devmart-deploy log -p --reverse devmart/kustomization.yaml | grep -oE "newTag: sha-[0-9a-f]{7}" | head -1 | cut -d' ' -f2)
OLD="ghcr.io/$ID/devmart-catalog-api:$OLD_TAG"
echo $OLD
docker run --rm ghcr.io/sigstore/cosign/cosign:v3.1.6 verify "$OLD" \
  --certificate-oidc-issuer https://token.actions.githubusercontent.com \
  --certificate-identity-regexp "^https://github.com/$ID/devops-lab/.*" 2>&1 | tail -1
```

> **🟢 확인: 서명이 없다**
>
> ```text
> Error: no signatures found
> ```

## 실습 16 · 서명 없는 이미지는 못 들어오게

### 단계 1 — 정책 (먼저 Audit)

```bash
cd ~/devops-lab/k8s/w4d5
code kyverno/verify-devmart-images.yaml
```

```yaml
apiVersion: policies.kyverno.io/v1
kind: ImageValidatingPolicy
metadata:
  name: verify-devmart-images
spec:
  validationActions: [Audit]          # 먼저 보고만 (5교시와 같은 순서)
  failurePolicy: Ignore               # Kyverno가 아프면 일단 통과 — Deny로 바꿀 때 Fail로
  webhookConfiguration:
    timeoutSeconds: 20                # 서명 확인은 인터넷(Rekor)을 다녀온다
  matchConstraints:
    namespaceSelector:
      matchExpressions:
        - { key: kubernetes.io/metadata.name, operator: In, values: [devmart] }
    resourceRules:
      - apiGroups: [""]
        apiVersions: [v1]
        operations: [CREATE]
        resources: [pods]
  matchImageReferences:
    - glob: "ghcr.io/YOUR_ID/devmart-*"   # 우리 이미지만 — postgres · redis · nginx는 대상 아님
  validationConfigurations:
    mutateDigest: false               # Pod의 이미지 주소를 바꾸지 않는다 (Argo CD와 다툼 방지)
    verifyDigest: false
    required: true
  attestors:
    - name: ourci
      cosign:
        keyless:
          identities:
            - issuer: https://token.actions.githubusercontent.com
              subjectRegExp: "^https://github.com/YOUR_ID/devops-lab/\\.github/workflows/devmart-ci\\.yml@refs/heads/main$"
  validations:
    - expression: images.containers.map(image, verifyImageSignatures(image, [attestors.ourci])).all(e, e > 0)
      message: "DevMart 이미지는 우리 CI(main)가 서명한 것만 실행할 수 있습니다."
```

```bash
sed -i "s/YOUR_ID/$ID/g" kyverno/verify-devmart-images.yaml        # Mac: sed -i ''
kubectl apply -f kyverno/verify-devmart-images.yaml
kubectl rollout restart deployment catalog-api -n devmart
sleep 30
kubectl get policyreports -n devmart -o wide 2>/dev/null | head -5
```

> **🟢 확인: 보이는 것**
>
> `catalog-api` Pod의 보고서에 `verify-devmart-images`가 **PASS**로 나오면 지금 도는 이미지는 서명됐다는 뜻입니다. `FAIL`이 있다면 아직 서명 전 이미지가 도는 것 — Argo CD가 새 태그로 바꿨는지(`argocd app get devmart`) 확인합니다.

### 단계 2 — Deny로

```bash
sed -i 's/validationActions: \[Audit\]/validationActions: [Deny]/; s/failurePolicy: Ignore/failurePolicy: Fail/' kyverno/verify-devmart-images.yaml
kubectl apply -f kyverno/verify-devmart-images.yaml
kubectl run unsigned -n devmart --image="$OLD" --restart=Never
kubectl run signed   -n devmart --image="$NEW" --restart=Never -- sleep 30
```

> **🟢 확인: 이렇게 나오면 성공**
>
> ```text
> Error from server: admission webhook "….kyverno.svc-fail" denied the request:
>   … verify-devmart-images: DevMart 이미지는 우리 CI(main)가 서명한 것만 실행할 수 있습니다.
> pod/signed created
> ```
> - 서명 없는 옛 이미지는 **문 앞에서** 거절됐습니다(5교시의 latest 금지처럼)
> - 같은 이름의 이미지라도 **우리 CI의 신원**이 서명한 것만 들어옵니다. 토큰을 훔쳐 GHCR에 올려도, 그 사람은 `devops-lab`의 main 워크플로가 될 수 없습니다

> [!WARNING]
> **Deny를 켜기 전에 반드시 확인할 것**
>
> - 지금 도는 **모든** DevMart 이미지가 서명됐는가(단계 1의 보고서). 아니면 다음 재시작 때 Pod가 못 뜹니다
> - `failurePolicy: Fail`이면 Kyverno가 멈췄을 때 DevMart Pod도 새로 못 뜹니다. 운영은 Kyverno를 2대 이상으로 둡니다
> - 서명 확인은 **인터넷(Rekor · TUF)**에 다녀옵니다. 인터넷이 막힌 클러스터는 Sigstore를 사내에 따로 둡니다

```bash
kubectl delete pod signed -n devmart --ignore-not-found
cd ~/devops-lab && git add k8s/w4d5/kyverno/verify-devmart-images.yaml
git commit -m "4주차 5일차: 서명 검증 정책 (keyless, Deny)" && git push
```

> **🧹 정리: 정리**
>
> 정책은 **Deny로 남겨 둡니다.** 이제 DevMart에 들어오는 이미지는 "테스트 · 검문 · 서명을 거친 main의 CI 결과물"뿐입니다. 5주차 EKS에도 같은 정책을 가져갑니다.

> **🎓 학술 노트 — 모두를 위한 서명 (Newman 외, CCS 2022)**
>
> 소프트웨어 서명은 오래전부터 있었지만, 오픈소스에서는 거의 쓰이지 않았습니다. 열쇠를 **안전하게 보관하고, 잃어버렸을 때 교체하고, 사용자에게 공개 열쇠를 배포하는** 일이 너무 어려웠기 때문입니다. 「Sigstore: Software Signing for Everybody」(Newman · Meyers · Torres-Arias, ACM CCS 2022)는 이 문제를 **열쇠 대신 신원**으로 풀었습니다. 서명할 때만 쓰는 임시 열쇠에, OIDC로 확인한 신원을 담은 **짧은 인증서**를 붙이고, 모든 서명을 **투명성 로그**(인증서 투명성 CT의 아이디어)에 남겨 나중에라도 감사할 수 있게 한 것입니다. 1주차 5일차 7교시의 Thompson이 "믿지 말고 증명을 남겨라"를 말했다면, Sigstore는 그 증명을 **누구나 공짜로** 남길 수 있게 만든 것입니다.
>
> - Newman, Z., Meyers, J. S., & Torres-Arias, S. (2022). Sigstore: Software signing for everybody. *ACM CCS '22*, 2353–2367.

> **📈 트렌드 — 서명에서 '증명(attestation)'으로**
>
> 서명은 "누가 만들었나"를 말합니다. 그다음 단계는 "**어떻게** 만들었나"입니다. **SLSA** 출처 증명(provenance)은 어느 소스 커밋을, 어느 빌드 시스템이, 어떤 단계로 빌드했는지를 서명된 문서로 이미지에 붙입니다. GitHub Actions는 `actions/attest-build-provenance`로 이것을 한 스텝으로 만들고, Kubernetes 프로젝트 자신도 릴리스를 Sigstore로 서명합니다. 2주차 3일차의 SBOM도 같은 방식으로 **서명된 증명**으로 붙일 수 있습니다. 오늘 Kyverno가 서명을 확인했듯이, 앞으로 정책은 "SLSA 레벨 3 이상으로 빌드된 이미지만" 같은 조건을 확인하게 됩니다.

## 정리

- 정책(5교시)은 "어떻게 실행하나"를, 서명은 **"어디서 왔나"**를 봅니다.
- **keyless 서명**: CI의 OIDC 신원으로 짧은 인증서를 받아 **digest**에 서명하고, 공개 장부(Rekor)에 기록합니다. 보관할 열쇠가 없습니다.
- `cosign verify --certificate-identity-regexp --certificate-oidc-issuer`로 **누가 · 어느 워크플로 · 어느 커밋**인지 확인합니다.
- Kyverno **ImageValidatingPolicy**: 우리 이미지(glob)는 우리 CI의 신원(subjectRegExp)이 서명한 것만. Audit로 확인한 뒤 Deny.

> **✅ 확인 문제**
>
> 1. 5교시의 정책을 모두 통과하는 악성 이미지가 있을 수 있는 이유는?
> 2. keyless 서명에서 "열쇠" 대신 믿는 것은 무엇인가요?
> 3. 태그가 아니라 digest에 서명하는 이유는?
> 4. ImageValidatingPolicy에서 `mutateDigest: false`로 둔 이유는?
> 5. 서명 검증을 Deny로 켜기 전에 확인해야 할 것 두 가지는?
>
> <details><summary>정답</summary>
>
> 1. 정책은 실행 방식(limits · root · latest)만 보고, 이미지가 **누가 만든 것인지**는 보지 않기 때문
> 2. OIDC로 확인된 **신원**(GitHub의 저장소 · 워크플로 · 브랜치)과 공개 장부의 기록
> 3. 태그는 다른 내용으로 옮겨 붙일 수 있지만 digest는 내용 그 자체라서
> 4. Pod의 이미지 주소를 Kyverno가 바꾸면 Git(배포 저장소)과 달라져 Argo CD와 다툴 수 있기 때문
> 5. 지금 도는 모든 대상 이미지가 서명됐는지(Audit 보고서), Kyverno가 멈췄을 때의 영향(failurePolicy · 대수) — 그리고 인터넷 연결
>
> </details>

## 참고 문헌

- Newman, Z., Meyers, J. S., & Torres-Arias, S. (2022). Sigstore: Software signing for everybody. *Proceedings of ACM CCS '22*.
- Sigstore Documentation. *Cosign — Keyless signing, Verifying signatures (--certificate-identity, --certificate-oidc-issuer)*; *Fulcio*; *Rekor*. docs.sigstore.dev
- Kyverno Documentation. *ImageValidatingPolicy — attestors (cosign keyless), matchImageReferences, validationConfigurations, verifyImageSignatures()*. kyverno.io/docs
- GitHub Docs. *Security hardening your deployments — OpenID Connect*; *Using artifact attestations to establish provenance for builds*.
- OpenSSF. *SLSA v1.0 — Provenance*. slsa.dev

---

| 이전 | 목차 | 다음 |
|:--|:--:|--:|
| ⬅️ [6교시 · 4주차 종합 장애 훈련](lesson-06.md) | [⬆️ 5일차 목차](README.md) | [8교시 · 4주차 회고 + 보안 점검표](lesson-08.md) ➡️ |
