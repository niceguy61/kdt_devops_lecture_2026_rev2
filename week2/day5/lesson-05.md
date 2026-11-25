# 5교시 · Pull Request와 코드 리뷰

> [!NOTE]
> **이번 시간에 할 일**
>
> - **Pull Request(PR)**가 무엇이고 왜 쓰는지 이해합니다.
> - 짝을 내 저장소의 **협업자(collaborator)**로 초대합니다.
> - 브랜치에서 작업한 뒤 PR을 열고, 짝에게 **리뷰**를 받아 병합합니다.
> - 좋은 PR 설명과 좋은 리뷰 코멘트를 쓰는 법을 연습합니다.

## Pull Request = "합쳐 주세요"라는 요청서

4교시에는 내가 브랜치를 만들고 내가 `git merge`로 합쳤습니다. **Pull Request**는 그 사이에 **"이 브랜치를 `main`에 합쳐도 될까요?"라고 묻는 단계**를 넣습니다. PR 페이지에서 동료는 바뀐 줄을 보고, 질문하고, 고칠 점을 말하고, 승인합니다. 3주차에는 여기에 **자동 테스트(CI)**가 붙어 사람과 기계가 함께 검토합니다.

![GitHub Flow — 브랜치 → 커밋 → PR → 리뷰 → 수정 → 승인 → 병합 → 브랜치 삭제](../../assets/week2/day5/w2d5-pr-flow.png)

> **🧩 비유 — 결재 서류**
>
> 브랜치의 커밋들은 **기안서**, PR은 **결재 요청**, 리뷰어는 **결재권자**입니다. 결재권자는 "이 부분 근거가 뭔가요?"(코멘트), "여기 고쳐 오세요"(변경 요청), "승인"을 할 수 있습니다. 결재가 끝난 서류만 **정식 문서(`main`)**가 됩니다. 그리고 모든 결재 기록이 남아, 나중에 "이 줄은 왜 이렇게 바뀌었지?"를 언제든 찾아볼 수 있습니다.

> **📖 용어 — PR과 MR**
>
> GitHub와 Bitbucket은 **Pull Request**, GitLab은 **Merge Request(MR)**라고 부릅니다. 같은 것입니다.

## 실습 8 · 짝 실습 준비

> **🧪 실습: 실습 목표**
>
> 두 사람이 서로를 자기 `devops-lab` 저장소의 협업자로 초대합니다. 아래에서 **A = 나, B = 짝**입니다. 두 사람 모두 자기 저장소에서 똑같이 합니다.

### 단계 1 — 협업자 초대 (A가 B를)

1. 브라우저에서 `https://github.com/내아이디/devops-lab` 을 엽니다.
2. 위쪽 탭의 **Settings** → 왼쪽 메뉴 **Collaborators** 를 누릅니다. (2단계 인증 확인을 요청하면 2주차 1일차에 등록한 방법으로 인증합니다.)
3. **Add people** → 짝의 GitHub 아이디 입력 → **Add 짝아이디 to this repository**.

### 단계 2 — 초대 수락 (B가)

짝의 이메일이나 GitHub 알림(오른쪽 위 종 모양)에 초대가 옵니다. **Accept invitation**을 누릅니다. 또는 `https://github.com/A아이디/devops-lab/invitations` 을 직접 열어도 됩니다.

> **🟢 확인: 이렇게 되면 성공**
>
> A의 **Settings → Collaborators** 목록에 B가 보입니다. 이제 B는 A의 저장소에 리뷰와 병합을 할 수 있습니다.

> [!WARNING]
> **협업자는 '쓰기 권한'**
>
> 협업자는 리뷰뿐 아니라 **코드를 직접 push**할 수도 있습니다. 실습이 끝나면(7교시) 짝을 협업자에서 빼도 됩니다. 회사에서는 개인 저장소 대신 **조직(Organization)과 팀** 단위로 권한을 세밀하게 나눕니다.

### 단계 3 — PR 설명 틀(템플릿) 넣기

PR을 열 때마다 같은 질문에 답하게 하는 **템플릿**을 저장소에 넣어 둡니다. 이 파일 하나만은 `main`에 바로 올립니다.

```bash
cd ~/devops-lab
mkdir -p .github
code .github/pull_request_template.md
```

```markdown
## 무엇을 바꿨나요?
-

## 왜 바꿨나요?
-

## 어떻게 확인했나요?
- [ ] `docker compose up -d --build` 후 http://localhost:8080 확인
- [ ]

## 리뷰어가 특히 봐 줬으면 하는 곳
-
```

```bash
git add .github/pull_request_template.md
git commit -m "PR 템플릿 추가"
git push
```

## 실습 9 · PR 열기 (A)

> **🧪 실습: 실습 목표**
>
> DevMart 상품에 '양말 세트'를 추가하는 작업을 브랜치에서 하고 PR을 엽니다.

### 단계 1 — 브랜치에서 작업

```bash
git switch -c feature/add-socks
code devmart/db/init/01-schema.sql
```

`INSERT` 목록 맨 끝에 한 줄을 추가합니다. 바로 앞 줄 끝의 `;`를 `,`로 바꾸는 것을 잊지 마세요.

```sql
    ('무선 이어폰', 89000),
    ('양말 세트', 9000);
```

초기화 SQL은 **빈 볼륨일 때만** 실행되므로(어제 2교시), 확인하려면 데이터를 지우고 다시 띄웁니다.

```bash
cd devmart
docker compose down -v
docker compose up -d
curl -s http://localhost:8080/api/products | grep -o '양말 세트'
cd ..
```

> **🟢 확인: 이렇게 나오면 성공**
>
> ```text
> 양말 세트
> ```
> 브라우저에도 카드가 6개입니다.

```bash
git add devmart/db/init/01-schema.sql
git commit -m "상품: 양말 세트 추가"
git push -u origin feature/add-socks
```

- `-u origin feature/add-socks` : 이 브랜치를 GitHub에 처음 올리면서, 앞으로 `git push`만 쳐도 이 브랜치로 가도록 연결(**u**pstream)한다

> **🟢 확인: 보이는 것**
>
> ```text
> remote: Create a pull request for 'feature/add-socks' on GitHub by visiting:
> remote:      https://github.com/내아이디/devops-lab/pull/new/feature/add-socks
> ```
> GitHub가 "PR 만들래요?" 주소를 알려 줍니다.

### 단계 2 — PR 만들기

```bash
gh pr create --web
```

브라우저에 PR 작성 화면이 열리고, 본문에 **템플릿이 채워져** 있습니다.

- **base: `main` ← compare: `feature/add-socks`** 인지 확인합니다 (`main`으로 합쳐 달라는 뜻)
- 제목: `상품: 양말 세트 추가`
- 본문: 템플릿의 질문에 답합니다. 예:

```markdown
## 무엇을 바꿨나요?
- 초기화 SQL에 '양말 세트'(9,000원) 상품을 추가했습니다.

## 왜 바꿨나요?
- 겨울 시즌 상품 요청 (실습)

## 어떻게 확인했나요?
- [x] `docker compose down -v` → `up -d` 후 http://localhost:8080 에서 카드 6개 확인

## 리뷰어가 특히 봐 줬으면 하는 곳
- 초기화 SQL이라 **기존 볼륨에는 반영되지 않습니다.** 확인하려면 `down -v`가 필요합니다.
```

- 오른쪽 **Reviewers**의 톱니바퀴 → 짝 선택
- **Create pull request**

> [!TIP]
> **명령줄로만 만들기**
>
> `gh pr create --title "상품: 양말 세트 추가" --body "…" --reviewer 짝아이디` 처럼 브라우저 없이도 만들 수 있습니다. 처음에는 화면을 보며 만드는 것이 이해하기 좋습니다.

## 실습 10 · 리뷰하기 (B)

> **🧪 실습: 실습 목표**
>
> 짝의 PR을 읽고 코멘트를 하나 이상 남긴 뒤 승인합니다.

```bash
gh pr list -R 짝아이디/devops-lab
gh pr view 1 -R 짝아이디/devops-lab --web
```

- `-R 주인/저장소` : 내 저장소가 아니라 **짝의 저장소**를 대상으로
- `1` : PR 번호 (목록에서 확인)

브라우저에서 PR이 열리면:

1. **Conversation** 탭 — 설명을 읽습니다. 무엇을, 왜, 어떻게 확인했는지 적혀 있나요?
2. **Files changed** 탭 — 바뀐 줄이 초록(추가)·빨강(삭제)으로 보입니다.
3. 바뀐 줄 번호 옆의 **`+`** 버튼 → 그 줄에 코멘트를 남깁니다. 예: "가격 9,000원이면 에코백(12,000원)보다 싸네요. 의도한 가격 맞나요?"
4. 오른쪽 위 **Review changes** → 셋 중 하나를 고르고 **Submit review**

| 선택 | 뜻 |
|---|---|
| **Comment** | 의견만 남긴다 (승인도 거절도 아님) |
| **Approve** | 합쳐도 좋다 |
| **Request changes** | 고친 뒤 다시 봐 달라 |

명령줄로도 할 수 있습니다.

```bash
gh pr review 1 -R 짝아이디/devops-lab --approve -b "SQL 문법 확인했고 down -v 안내도 좋습니다. 승인합니다!"
```

> [!WARNING]
> **내 PR은 내가 승인할 수 없다**
>
> GitHub는 PR을 연 사람이 **자기 PR을 승인(Approve)하는 것을 막습니다.** 리뷰의 의미가 "다른 눈으로 보기"이기 때문입니다. 짝이 없으면 강사에게 요청합니다.

## 좋은 리뷰 코멘트

| 덜 좋은 코멘트 | 더 좋은 코멘트 |
|---|---|
| "이상해요" | "9,000원이 에코백보다 싼데 의도한 가격인지 궁금합니다" |
| "이렇게 하면 안 됩니다" | "`;`가 두 번 들어가면 SQL 오류가 날 것 같아요. 이 줄 확인 부탁드려요" |
| (아무 말 없이 Approve) | "로컬에서 `down -v` → `up`으로 카드 6개 확인했습니다. 승인!" |
| "제 스타일은 이게 아니에요" | "(사소) 이름을 '양말 3종 세트'로 하면 더 구체적일 것 같아요. 그대로 가도 괜찮습니다" |

- **코드를 말하지, 사람을 말하지 않는다.** "당신은 틀렸다"가 아니라 "이 줄은 이런 문제가 있을 것 같다".
- **질문으로 쓴다.** 내가 모르는 이유가 있을 수 있습니다.
- **중요도를 밝힌다.** 꼭 고쳐야 하는 것과 "사소(nit)"를 구분합니다.
- 1주차 5일차의 **비난 없는 문화**가 리뷰에서 가장 자주 시험받습니다.

## 실습 11 · 반영하고 병합하기 (A)

리뷰에서 고칠 점이 나왔다면 **같은 브랜치에** 커밋을 더 올립니다. PR은 자동으로 갱신됩니다.

```bash
git switch feature/add-socks         # 이미 이 브랜치라면 생략
# 코멘트에 따라 고치고
git commit -am "리뷰 반영: 상품 이름 수정"
git push
```

승인이 오면 병합합니다.

```bash
gh pr merge 1 --squash --delete-branch
git log --oneline -3
```

- `--squash` : PR의 커밋 여러 개를 **하나로 묶어** `main`에 올린다 (`main`의 기록이 깔끔해진다)
- `--delete-branch` : GitHub와 내 노트북의 `feature/add-socks`를 지우고 `main`으로 옮겨 최신 상태로 맞춘다

> **🟢 확인: 이렇게 나오면 성공**
>
> ```text
> ✓ Squashed and merged pull request 내아이디/devops-lab#1 (상품: 양말 세트 추가)
> ✓ Deleted local branch feature/add-socks and switched to branch main
> ✓ Deleted remote branch feature/add-socks
> a1b2c3d (HEAD -> main, origin/main) 상품: 양말 세트 추가 (#1)
> ```
> 커밋 메시지 끝의 **`(#1)`**이 PR 번호입니다. 나중에 이 커밋을 보면 PR 페이지로 가서 **누가 리뷰했고 어떤 대화가 있었는지** 찾을 수 있습니다.

역할을 바꿔서, **B의 저장소에서 B가 PR을 열고 A가 리뷰**합니다. B는 '목도리'(15,000원) 같은 다른 상품을 추가해 봅니다.

> [!TIP]
> **도전 — `main`을 규칙으로 보호하기**
>
> 저장소 **Settings → Rules → Rulesets → New branch ruleset**에서 대상을 기본 브랜치(`main`)로 정하고 **Require a pull request before merging**(승인 1개)을 켜면, 누구도 `main`에 직접 push할 수 없고 PR과 승인을 거쳐야 합니다. 3주차에는 여기에 "CI 테스트 통과"를 조건으로 더합니다. (저장소 주인은 규칙을 우회할 수 있게 설정되어 있을 수 있으니, 규칙의 Bypass 목록도 확인해 봅니다.)

> **🎓 학술 노트 — 구글의 코드 리뷰 (Sadowski et al., 2018)**
>
> 구글의 연구진은 ICSE 2018(소프트웨어 공학 분야 최고 학회)에서 「현대적 코드 리뷰: 구글 사례 연구」를 발표했습니다. 구글은 거의 **모든 코드 변경이 리뷰를 거치는** 회사입니다. 수백만 건의 리뷰 기록과 개발자 인터뷰를 분석한 결과, 구글의 변경은 대부분 **작았고**(몇 개 파일, 수십 줄), 보통 **리뷰어 한 명**이 보며, 첫 응답까지 **몇 시간 안**에 끝나는 경우가 많았습니다. 개발자들이 꼽은 리뷰의 가치는 버그 찾기뿐 아니라 **지식 공유, 읽기 쉬운 코드, 일관성 유지**였습니다.
>
> 구글이 공개한 리뷰 지침(Google Engineering Practices)의 핵심 문장은 이렇습니다. **"완벽하지 않더라도 코드베이스 전체의 건강을 확실히 나아지게 한다면 승인하라."** 리뷰는 완벽을 요구하는 관문이 아니라 **함께 조금씩 낫게 만드는** 과정이라는 뜻입니다. 작은 PR이 빠른 리뷰를 부르고, 빠른 리뷰가 짧은 브랜치를 가능하게 합니다(4교시).
>
> - Sadowski, C., Söderberg, E., Church, L., Sipko, M., & Bacchelli, A. (2018). Modern code review: A case study at Google. *ICSE-SEIP '18*.

> **📈 트렌드 — 사람 리뷰어 옆의 기계 리뷰어**
>
> 요즘 PR에는 사람 말고도 여러 "리뷰어"가 붙습니다. 3주차에 만들 **CI**가 테스트와 이미지 빌드 결과를 PR에 표시하고, 보안 도구가 취약한 라이브러리나 비밀값을 찾아 코멘트를 남기며, **AI 코드 리뷰 도구**가 변경 요약과 개선 제안을 자동으로 달아 줍니다. 그래도 "**이 변경이 우리 서비스에 맞는가, 왜 이렇게 했는가**"를 판단하고 승인 버튼을 누르는 것은 사람입니다. 또 `CODEOWNERS` 파일로 "`devmart/db/` 아래가 바뀌면 DB 담당자가 반드시 리뷰"처럼 리뷰어를 자동으로 지정하는 것도 흔한 방식입니다.

## 정리

- **PR** = "이 브랜치를 `main`에 합쳐도 될까요?" 요청서. 리뷰와 기록이 남는다.
- 흐름: `switch -c` → 커밋 → `push -u` → `gh pr create` → 리뷰(Comment/Approve/Request changes) → 같은 브랜치에 수정 push → `gh pr merge --squash --delete-branch`.
- 내 PR은 내가 승인할 수 없다.
- 좋은 리뷰: 코드를 말하고, 질문으로, 중요도를 밝혀서.
- 작은 PR → 빠른 리뷰 → 짧은 브랜치.

> **✅ 확인 문제**
>
> 1. PR을 쓰면 `git merge`로 바로 합칠 때보다 무엇이 좋아지나요? 두 가지.
> 2. `git push -u origin feature/add-socks`에서 `-u`는?
> 3. 리뷰에서 고칠 점이 나오면 새 PR을 만들어야 하나요?
> 4. `--squash` 병합을 하면 `main`의 기록은 어떻게 되나요?
> 5. "이상해요"라는 코멘트를 더 좋은 코멘트로 바꿔 보세요.
>
> <details><summary>정답</summary>
>
> 1. 다른 사람이 검토해 실수를 줄이고, 지식이 공유되며, 왜 바뀌었는지 기록이 남는다 (중 두 가지)
> 2. 이 브랜치를 원격 브랜치와 연결해 다음부터 `git push`만으로 올라가게 한다
> 3. 아니다. 같은 브랜치에 커밋을 더 push하면 PR이 자동으로 갱신된다
> 4. PR의 여러 커밋이 하나로 묶여 main에 한 커밋(끝에 PR 번호)으로 남는다
> 5. 예: "가격이 에코백보다 낮은데 의도한 값인지 궁금합니다" — 구체적으로, 질문으로
>
> </details>

## 참고 문헌

- GitHub Docs. *About pull requests*, *Reviewing proposed changes in a pull request*. docs.github.com/pull-requests
- GitHub CLI Manual. *gh pr create / review / merge*. cli.github.com/manual
- GitHub Docs. *About rulesets*, *About code owners*. docs.github.com/repositories
- Google. *Engineering Practices — The Standard of Code Review*. google.github.io/eng-practices
- Sadowski, C. et al. (2018). Modern code review: A case study at Google. *ICSE-SEIP '18*.
