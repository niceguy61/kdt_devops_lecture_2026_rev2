# 6교시 · 5주 회고 + 포트폴리오

!!! goal "이번 시간에 할 일"
    - 다섯 주를 **내 말로** 한 줄씩 적습니다.
    - KPT로 과정 전체를 회고합니다.
    - 저장소 셋을 묶는 **포트폴리오 README**를 씁니다.

## 실습 7 · 다섯 주를 한 줄씩

```bash
cd ~/devops-lab/aws/w5d5
cp retro-course.md ~/devops-lab/RETRO-COURSE.md
code ~/devops-lab/RETRO-COURSE.md 2>/dev/null || nano ~/devops-lab/RETRO-COURSE.md
```

첫 표를 채웁니다. **도구 이름이 아니라 "할 수 있게 된 일"**로 씁니다.

| 주 | 나쁜 예 | 좋은 예 |
|---|---|---|
| 2주차 | Docker를 배웠다 | 내 앱을 이미지로 만들어 누구 노트북에서나 같게 띄울 수 있다 |
| 4주차 | Argo CD | Git에 커밋하면 클러스터가 따라오게 하고, 손 수정을 찾아 되돌릴 수 있다 |
| 5주차 | Terraform · EKS | VPC부터 EKS까지 코드로 30분에 세우고, 남김없이 지울 수 있다 |

## 실습 8 · KPT

3주차 · 4주차 회고와 같은 방법입니다 — 혼자 10분 → 짝과 5분 → 반 전체에서 Try 하나씩.

!!! tip "과정 회고의 Try"
    주간 회고의 Try는 "다음 주에 할 것"이었습니다. 과정 회고의 Try는 "**과정이 끝난 뒤 30일 안에 할 것**"입니다. 예: "devmart-infra에 RDS 모듈을 더해 db를 옮기고, 오늘 훈련 2를 다시 해 주문이 멈추지 않는 것을 확인한다." — 한 번에 끝낼 수 있는 행동, 확인 방법까지.

## 실습 9 · 포트폴리오 README

5주 동안 저장소가 셋 생겼습니다.

```bash
for r in devops-lab devmart-deploy devmart-infra; do gh repo view $(gh api user -q .login)/$r --json name,url,pushedAt -q '"\(.name)  \(.url)  \(.pushedAt)"'; done
```

이 셋은 각각 **CI · GitOps · IaC**를 보여 줍니다. 처음 보는 사람이 셋의 관계를 알 수 있게, `devops-lab`의 README 맨 위에 틀을 붙입니다.

```bash
cd ~/devops-lab
cat ~/devops-lab/aws/w5d5/portfolio-readme.md > /tmp/portfolio.md
[ -f README.md ] && cat README.md >> /tmp/portfolio.md
mv /tmp/portfolio.md README.md
mkdir -p docs && cp ~/course/assets/week5/day4/w5d4-path.png docs/architecture.png 2>/dev/null || true
cp ~/devops-lab/aws/w5d5/up.sh ~/devops-lab/aws/w5d5/down.sh ~/devops-lab/aws/w5d5/leftovers.sh .
```

편집기로 README를 열어 다듬습니다.

| 칸 | 채울 것 |
|---|---|
| 구조 | `docs/architecture.png`를 넣거나, 직접 그린 그림 — **손님 → NLB → Envoy → 서비스 → db**, **CI → GHCR**, **Git → Argo CD** |
| 재현 | `up.sh` · `down.sh` — 필요한 것(AWS 계정, `aws login`, terraform, kubectl, helm) |
| 운영에서 다룬 것 | 4주차의 관찰 · 메시 · 보안 · 장애 훈련 — **장애 보고서 링크**를 단다 |
| 비용 | 오늘 5교시의 숫자 |
| 배운 점 | 6교시 KPT에서 한두 줄 |

```bash
git add README.md docs up.sh down.sh leftovers.sh
git commit -m "포트폴리오 README — 저장소 셋의 지도"
git push
gh repo view --web
```

!!! check "확인"
    GitHub에서 `devops-lab`을 열면 첫 화면에 **세 저장소의 표 · 구조 · 재현 방법**이 보입니다. `devmart-deploy` · `devmart-infra`의 README에도 "이 저장소는 포트폴리오의 어느 부분인가"를 한 줄 적고 `devops-lab`으로 링크합니다.

!!! warn "공개 저장소를 다시 점검"
    포트폴리오로 공개하기 전에 비밀이 없는지 마지막으로 봅니다.
    ```bash
    for r in ~/devops-lab ~/devmart-deploy ~/devmart-infra; do
      echo "== $r"; git -C $r log -p | grep -nE "AKIA[0-9A-Z]{16}|ghp_[0-9A-Za-z]{30,}|github_pat_|-----BEGIN .*PRIVATE KEY|password *[:=] *['\"][^'\"]{6,}" | head -3
    done
    ```
    아무것도 나오지 않아야 합니다. 무엇이 나오면 **그 키를 먼저 폐기**(AWS · GitHub에서)하고, 그다음 이력 정리를 강사와 함께 합니다 — 이력을 지워도 이미 복제된 곳이 있을 수 있으므로 **폐기가 먼저**입니다.

!!! myth "오해 — 포트폴리오는 화려한 앱이어야 한다"
    DevOps · 클라우드 엔지니어의 포트폴리오에서 보는 것은 앱의 기능이 아니라 ① **재현할 수 있나**(README의 명령으로), ② **운영을 생각했나**(관찰 · 장애 기록 · 비용 · 보안), ③ **판단의 기록**(왜 이 구조인가, 무엇을 포기했나)입니다. 장애 보고서와 "다음에는" 칸이 앱 화면보다 강한 증거가 됩니다.

!!! academic "학술 노트 — 성찰적 실천"
    Schön의 *The Reflective Practitioner*(1983)는 전문가가 일을 하면서(reflection-in-action), 그리고 일이 끝난 뒤(reflection-on-action) **성찰**하며 성장한다고 했습니다. 매일의 배움일기와 주간 · 과정 KPT는 그 '일 뒤의 성찰'을 습관으로 만든 장치였습니다. 애자일의 회고(Derby & Larsen, *Agile Retrospectives*, 2006)도 같은 뿌리에서 나왔습니다.

!!! trend "트렌드 2026 — 증명 가능한 역량"
    채용에서 자격증과 함께 **공개 저장소 · 기술 글 · 재현 가능한 데모**를 보는 흐름이 강해졌고, AI가 코드를 쓰는 시대에는 "**무엇을 왜 그렇게 결정했나**"를 설명하는 능력이 더 중요해졌습니다. 오늘의 README와 장애 보고서가 그 설명입니다.

!!! quiz "확인 문제"
    1. 다섯 주를 '도구'가 아니라 '할 수 있게 된 일'로 적는 이유는?
    2. 저장소 셋이 각각 보여 주는 능력은?
    3. 공개 저장소에서 키를 찾았을 때 가장 먼저 할 일은?

    ??? answer "정답"
        1. 보는 사람(그리고 나)에게 실제로 무엇을 할 수 있는지가 전달되기 때문 — 도구는 바뀌어도 할 수 있는 일은 남는다
        2. devops-lab: CI · 컨테이너화, devmart-deploy: GitOps · 오버레이, devmart-infra: IaC · 원격 state · 키 없는 CI
        3. 그 키를 발급처(AWS · GitHub)에서 폐기한다 — 이력 정리는 그다음

## 참고 문헌

- Schön, D. A. (1983). *The Reflective Practitioner: How Professionals Think in Action*. Basic Books.
- Derby, E. & Larsen, D. (2006). *Agile Retrospectives: Making Good Teams Great*. Pragmatic Bookshelf.
- GitHub Docs. *About READMEs*, *Removing sensitive data from a repository*. docs.github.com
