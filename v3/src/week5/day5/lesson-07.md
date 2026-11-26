# 7교시 · 포트폴리오 발표 — 5분 데모와 질의응답

!!! goal "이번 시간에 할 일"
    - 6교시에 쓴 포트폴리오 README를 **5분 발표**로 바꿉니다.
    - 5주 동안 남긴 **증거**(커밋 · PR · 장애 보고서 · 비용 보고 · 대시보드)를 발표 흐름에 꽂습니다.
    - 짝과 **리허설**하고, 정해진 기준으로 서로 피드백합니다.
    - 면접에서 나올 질문 열 개에 **"어디서 해 봤는지"**를 근거로 답하는 연습을 합니다.

!!! key "'할 줄 안다'가 아니라 '해 봤고, 이것이 증거다'"
    채용하는 쪽이 가장 궁금한 것은 도구 이름 목록이 아니라 **"이 사람이 문제를 만났을 때 어떻게 하나"**입니다. 이 과정은 그 증거를 매일 남기게 짜여 있었습니다 — 장애 보고서, PR 리뷰, 롤백 기록, 비용 보고. 오늘은 그것을 **5분 안에 보여 주는** 연습입니다.

## 5분의 순서

| 순서 | 시간 | 내용 | 꽂을 증거 |
|---|---|---|---|
| 1 문제 | 30초 | "작은 쇼핑몰을 노트북에서 클라우드까지 **반복해서 세웠다 지울 수 있게** 만들었다" | README 첫 줄 |
| 2 구조 | 1분 | 그림 한 장 — 손님 → 입구 → 서비스 → DB, Git → CI → Argo CD | 4주차 5일차의 "한 장" |
| 3 데모 | 1분 30초 | **변경 하나가 손님에게 닿는 길**을 실제로 | 커밋 → CI(검문 · 서명) → 배포 저장소 → Argo CD |
| 4 장애 하나 | 1분 | 내가 겪은 장애 하나 — 증상 · 원인 · 조치 · 다음에는 | 3주차 · 4주차 장애 보고서 |
| 5 숫자와 배운 것 | 1분 | 비용 · 시간 · 바뀐 생각 | 5교시 비용 보고, `up.sh` 걸린 시간 |

!!! tip "도구 이름은 이야기 속에서만"
    "Kubernetes, Istio, Argo CD, Terraform을 썼습니다"로 시작하지 않습니다. "배포할 때마다 손으로 하던 일을 **Git 커밋 하나**로 줄였습니다 — Argo CD가 그 일을 합니다"처럼 **문제 → 도구** 순서로 말합니다. 듣는 사람이 그 도구를 몰라도 따라올 수 있습니다.

## 실습 10 · 증거 모으기

!!! lab "실습 목표"
    발표에 쓸 링크 다섯 개와 숫자 세 개를 `presentation.md` 한 파일에 모읍니다.

```bash
cd ~/devops-lab
ME=$(gh api user --jq .login)
{
  echo "# 발표 증거 — $ME"
  echo
  echo "## 링크"
  echo "- 저장소: https://github.com/$ME/devops-lab · devmart-deploy · devmart-infra"
  echo "- 가장 좋았던 PR: $(gh pr list --state merged --limit 20 --json number,title,url -q '.[] | "\(.title) \(.url)"' | head -1)"
  echo "- 장애 보고서: $(git ls-files | grep -iE 'incident|장애' | head -2 | tr '\n' ' ')"
  echo "- 배포 저장소 커밋 수(CI 봇 포함): $(gh api repos/$ME/devmart-deploy/commits --paginate -q '.[].sha' 2>/dev/null | wc -l)"
  echo
  echo "## 숫자"
  echo "- up.sh 걸린 시간: (오늘 2교시에 잰 값)"
  echo "- 5주 AWS 비용: (5교시 비용 보고)"
  echo "- 롤백에 걸린 시간: (4주차 3일차 revert → Argo CD 반영)"
} > presentation.md
cat presentation.md
```

!!! check "이렇게 나오면 성공"
    링크 · 숫자가 채워진 파일이 보입니다. 빈 괄호는 손으로 채웁니다. **숫자가 없는 칸이 가장 약한 칸**입니다 — 기억이 안 나면 해당 날의 노트 · 커밋 시간으로 계산합니다.

## 실습 11 · 데모 리허설

EKS는 5교시에 지웠으므로 데모는 **노트북의 kind**(4주차의 `devmart` 클러스터)로 합니다. 구조는 같고, 오늘 오전에 EKS에서 같은 커밋이 돌았다는 것(3교시)은 **스크린샷**으로 보여 줍니다.

```bash
docker start devmart-control-plane devmart-worker devmart-worker2 2>/dev/null
sleep 40 && kubectl get pods -n devmart --no-headers | awk '{print $3}' | sort | uniq -c
```

데모 각본 — 짝이 시간을 잽니다(1분 30초).

```bash
# ① 바꾸기 — 화면에 보이는 한 줄
cd ~/devops-lab && git switch -c demo/version
sed -i 's/APP_VERSION = .*/APP_VERSION = "2.3.0"/' devmart-msa/catalog-api/app.py      # Mac: sed -i ''
git commit -am "catalog-api 2.3.0 (발표 데모)" && git push -u origin demo/version
gh pr create --fill && gh pr merge --squash --delete-branch --auto
# ② 기다리는 동안 말한다: "지금 CI가 테스트 · 계약 테스트 · 취약점 검문 · 서명을 하고 있습니다"
gh run watch $(gh run list --branch main --limit 1 --json databaseId -q '.[0].databaseId') --exit-status
# ③ 배포 저장소에 봇의 커밋 → Argo CD
git -C ~/devmart-deploy pull -q && git -C ~/devmart-deploy log --oneline -1
kubectl get pods -n devmart -l app=catalog-api -w
```

!!! check "보여 줄 장면"
    - Actions 화면의 초록 체크들(검문 · 서명 포함)
    - `deploy: devmart 이미지 → sha-…` 커밋(사람이 아니라 **봇**이 쓴 것)
    - Pod가 새것으로 바뀌는 `-w` 화면, 그리고 `curl localhost:30080/api/info`의 `"version":"2.3.0"`

    CI가 몇 분 걸리므로, **리허설에서는 끝까지 기다려 실제 시간을 재고**, 발표 때는 미리 해 둔 실행의 화면으로 넘어가도 됩니다. 실제 발표에서 라이브가 실패하면 그것도 이야기거리입니다 — "이 실패는 이렇게 읽습니다"(3주차 2일차 7교시).

!!! warn "데모용 변경도 PR로"
    발표 데모라고 main에 바로 push하지 않습니다(그럴 수도 없습니다 — 3주차의 main 보호). 보는 사람에게 **"이 사람은 급할 때도 절차를 지킨다"**가 전해집니다.

### 짝 피드백 기준

리허설이 끝나면 짝이 아래 표에 1~3점과 한 줄을 적어 줍니다.

| 기준 | 3점이면 |
|---|---|
| 문제가 먼저 나왔나 | 첫 30초에 "무엇을 해결했나"가 들렸다 |
| 증거가 있었나 | 말한 것마다 화면 · 링크 · 숫자가 따라왔다 |
| 장애 이야기 | 증상 → 원인 → 조치 → **다음에는**이 다 있었다 |
| 시간 | 4분 30초 ~ 5분 30초 |
| 모르는 사람도 따라왔나 | 도구 이름이 나올 때 그 일이 무엇인지 함께 말했다 |

## 실습 12 · 질문 열 개 — "어디서 해 봤나"로 답하기

면접에서 자주 나오는 질문입니다. 각 질문에 **이 과정의 어느 날**을 근거로 한두 문장씩 적습니다. 오른쪽 칸은 출발점일 뿐, 자기 경험으로 바꿔 씁니다.

| 질문 | 근거로 꺼낼 날 |
|---|---|
| 1. 컨테이너와 VM의 차이는? | 1주차 2일차 · 2주차 2일차 8교시(cgroups로 직접 제한) |
| 2. MSA를 왜 썼고, 단점은? | 3주차 1일차 — 장애 전파 · 계약이 깨진 날 |
| 3. Pod가 안 뜨면 어떻게 보나? | 3주차 4일차 3 · 8교시의 진단 순서 |
| 4. 비밀값은 어떻게 다뤘나? | 2주차 4일차 · 3주차 5일차 · 3주차 3일차 8교시(etcd 속 원문) |
| 5. 배포 중 장애가 나면? | 3주차 4일차 롤백 · 4주차 3일차 `git revert` |
| 6. 모니터링은 무엇을 보나? | 4주차 2일차 RED · 알림 · Loki · 5주차 2일차 CloudWatch |
| 7. 이미지는 어떻게 믿나? | 2주차 3일차 8교시 · 3주차 2일차 8교시 · 4주차 5일차 7교시 |
| 8. IaC를 왜 쓰나? 실수는 어떻게 막나? | 5주차 2일차의 클릭 수 · 3일차 8교시 lint · plan 리뷰 |
| 9. 클라우드 비용을 어떻게 관리했나? | 5주차 1일차 예산 · 태그, 5일차 비용 보고 |
| 10. 가장 어려웠던 문제와 해결은? | 나의 장애 보고서 중 하나 |

!!! tip "답의 모양 — 상황 · 행동 · 결과 · 배움"
    경험 질문에는 **상황**(무엇이 일어났나) → **행동**(내가 무엇을 했나 — '우리'가 아니라 '나') → **결과**(숫자로) → **배움**(다음에는)으로 답합니다. 예: "4주차에 mTLS STRICT를 켜자 사이트가 503이 됐습니다(상황). ztunnel 로그로 입구가 메시 밖이라는 것을 찾고, 입구 네임스페이스를 메시에 넣었습니다(행동). 3분 안에 복구했고(결과), 이후 STRICT 전에 '밖에서 들어오는 것'부터 세는 점검을 런북에 넣었습니다(배움)."

```bash
code presentation.md          # 질문 열 개의 답을 '## 질문' 아래에 적는다
git add presentation.md && git commit -m "포트폴리오 발표 준비" && git push
```

!!! cleanup "정리"
    ```bash
    kubectl get pods -n devmart | head -3        # 데모 후에도 정상인지
    ```
    kind 클러스터는 8교시 뒤에 꺼도 됩니다(`docker stop devmart-control-plane devmart-worker devmart-worker2`).

!!! academic "학술 노트 — 설명하면 이해가 깊어진다 (Chi 외, 1994)"
    인지과학자 **미셸린 치(Michelene Chi)** 연구진은 학생들에게 교재를 읽으며 **스스로에게 설명하게** 했더니, 그냥 두 번 읽은 학생들보다 이해가 크게 깊어졌다고 보고했습니다(Cognitive Science, 1994). 설명하려면 **빈틈을 메워야** 하고, 그 과정에서 자기가 무엇을 모르는지 드러나기 때문입니다. 오늘 질문 열 개에 "어디서 해 봤나"를 적다가 막힌 칸이 바로 그 빈틈입니다 — 8교시의 30일 계획에 옮깁니다. 남에게 설명하려고 준비할 때 더 잘 배우는 현상은 **가르치며 배우기**(learning by teaching)로도 알려져 있습니다.

    - Chi, M. T. H., De Leeuw, N., Chiu, M.-H., & LaVancher, C. (1994). Eliciting self-explanations improves understanding. *Cognitive Science*, 18(3), 439–477.

!!! trend "트렌드 — 면접이 '해 보기'로"
    DevOps · SRE 채용은 지식 문답보다 **실제로 해 보게 하는** 쪽으로 옮겨 가고 있습니다. 망가진 환경을 주고 고치게 하는 **라이브 트러블슈팅**, 화이트보드에 그리는 **시스템 설계**, 그리고 지원자의 **공개 저장소와 장애 보고서**를 함께 읽는 면접이 늘었습니다. AI 도구를 쓰도록 허용하고 **"AI의 답을 어떻게 검증했나"**를 보는 회사도 생겼습니다(1주차 1일차 3교시, 2주차 1일차 8교시). 오늘 준비한 증거와 진단 순서가 그대로 쓰입니다.

## 정리

- 5분은 **문제 → 구조 → 데모 → 장애 하나 → 숫자와 배움**. 도구 이름은 이야기 속에서만.
- 말한 것마다 **증거**(링크 · 화면 · 숫자)를 붙입니다. 숫자가 없는 칸이 가장 약한 칸입니다.
- 데모 변경도 **PR로** — 절차를 지키는 모습이 전해집니다.
- 질문에는 "어디서 해 봤나"로, 경험 질문에는 **상황 · 행동 · 결과 · 배움**으로 답합니다.

!!! quiz "확인 문제"
    1. 발표를 "제가 쓴 기술은 Kubernetes, Istio…"로 시작하면 무엇이 아쉬운가요?
    2. 라이브 데모가 실패했을 때 할 수 있는 가장 좋은 말은?
    3. 경험 질문에 답하는 네 단계는?
    4. 질문 열 개 중 답을 못 쓴 칸은 어떻게 하나요?
    5. 데모용 한 줄 변경을 main에 바로 push하지 않는 이유 두 가지는?

    ??? answer "정답"
        1. 듣는 사람은 무엇을 해결했는지 모른 채 이름만 듣는다 — 문제를 먼저 말해야 도구가 왜 필요했는지 들린다
        2. "이 실패는 이렇게 읽습니다" — 로그 · 상태를 함께 읽으며 진단 순서를 보여 준다
        3. 상황 · 행동 · 결과 · 배움
        4. 그것이 지금의 빈틈이다 — 8교시의 30일 계획에 넣는다
        5. main 보호 규칙 때문에 할 수 없고, 급할 때도 절차를 지키는 모습을 보여 주기 위해

## 참고 문헌

- Chi, M. T. H., De Leeuw, N., Chiu, M.-H., & LaVancher, C. (1994). Eliciting self-explanations improves understanding. *Cognitive Science*, 18(3).
- Fiorella, L., & Mayer, R. E. (2013). The relative benefits of learning by teaching and teaching expectancy. *Contemporary Educational Psychology*, 38(4), 281–288.
- Google. *Site Reliability Engineering — Postmortem Culture* (장애 이야기의 구조). sre.google/sre-book
- GitHub Docs. *gh pr merge --auto*; *gh run watch*.
