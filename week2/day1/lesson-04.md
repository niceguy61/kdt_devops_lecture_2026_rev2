[🏠 과정 목차](../../README.md) › [2주차](../README.md) › [1일차](README.md)

# 4교시 · GitHub 계정과 인증

> [!NOTE]
> **이번 시간에 할 일**
>
> - GitHub 계정을 만들고 2단계 인증을 켭니다.
> - Git이 왜 비밀번호로 로그인하지 않는지 이해합니다.
> - GitHub CLI(`gh`)로 브라우저 로그인을 하고, Git이 그 인증을 쓰게 합니다.
> - 토큰이 어디에 저장되는지, 왜 조심해야 하는지 압니다.

## 비밀번호 대신 토큰

GitHub은 2021년 8월부터 Git 명령(`git push` 등)에서 **계정 비밀번호를 받지 않습니다.** 대신 **토큰** 또는 **SSH 키**를 씁니다.

| 방식 | 비유 | 특징 |
|---|---|---|
| 계정 비밀번호 | 집 열쇠 원본 | 유출되면 모든 것이 열린다 → Git에서는 사용 불가 |
| **토큰** (Personal Access Token) | **용도·기간이 정해진 출입증** | 범위(어떤 저장소, 어떤 권한)와 만료일을 정할 수 있고, 언제든 폐기 가능 |
| SSH 키 | 집에만 맞는 전용 열쇠 쌍 | 한 번 설정하면 편하지만 처음 설정이 조금 어렵다 |

> [!IMPORTANT]
> **토큰은 비밀번호와 똑같이 다룬다**
>
> 토큰은 "로그인된 상태" 그 자체입니다. 토큰을 가진 사람은 여러분인 척 저장소를 지우거나 코드를 바꿀 수 있습니다. 그래서 **채팅, 스크린샷, 코드, 커밋, AI 대화창에 절대 붙여 넣지 않습니다.** 실수로 노출했다면 GitHub **Settings → Developer settings** 또는 `gh auth logout`으로 즉시 폐기합니다.

오늘은 토큰을 손으로 만들어 복사하는 대신, **GitHub CLI(`gh`)**가 브라우저 로그인으로 토큰을 받아 안전하게 저장하고 Git에 연결해 주는 방법을 씁니다. 초보자가 토큰을 복사·붙여넣기하다 노출하는 사고를 줄이는 가장 쉬운 길입니다.

## 실습 6 · GitHub 계정 만들기

> **🧪 실습: 실습 목표**
>
> GitHub 계정을 만들고 2단계 인증(2FA)을 켭니다. **이미 계정이 있다면 단계 2만 확인합니다.**

### 단계 1 — 가입

[github.com](https://github.com) → **Sign up**. 사용자 이름(username)은 **취업 포트폴리오 주소**가 됩니다(`github.com/아이디`). 장난스러운 이름보다 본인을 나타내는 이름을 추천합니다.

### 단계 2 — 2단계 인증 켜기

**프로필 사진 → Settings → Password and authentication → Two-factor authentication → Enable**.

- 휴대폰 인증 앱(Google Authenticator, Microsoft Authenticator 등)으로 QR 코드를 찍습니다.
- 화면에 나오는 **복구 코드(recovery codes)**를 반드시 내려받아 안전한 곳에 보관합니다. 휴대폰을 잃어버렸을 때 유일한 복구 수단입니다.

GitHub은 코드를 올리는 사용자에게 2단계 인증을 요구합니다. 처음부터 켜 두면 나중에 갑자기 막히는 일이 없습니다.

## 실습 7 · GitHub CLI로 로그인

> **🧪 실습: 실습 목표**
>
> `gh`를 설치하고 브라우저로 로그인해, `git push`가 별도 비밀번호 없이 동작하도록 준비합니다.

### 단계 1 — 설치

**Windows — WSL Ubuntu 터미널 (bash) · Linux**

```bash
sudo apt install -y gh
gh --version
```

**Mac — 터미널 (Homebrew)**

```bash
brew install gh
gh --version
```

> **🟢 확인: 이렇게 나오면 성공**
>
> ```text
> gh version 2.45.0 (…)
> ```
> 숫자는 달라도 됩니다. Ubuntu 저장소의 gh는 조금 오래됐지만 수업에는 충분합니다. 최신판은 GitHub 공식 apt 저장소로 깝니다(부록 A).

> [!TIP]
> **다른 설치 방법 — winget · 직접 다운로드**
>
> | 방법 | 어디서 | 명령 · 주소 |
> |---|---|---|
> | winget | Windows PowerShell | `winget install -e --id GitHub.cli` |
> | 직접 다운로드 | 브라우저 | [cli.github.com](https://cli.github.com) · [릴리스](https://github.com/cli/cli/releases) |
>
> winget은 **Windows 쪽**에 설치하므로 PowerShell에서만 보입니다. 수업 명령은 WSL Ubuntu(bash)에서 치므로, Windows 사용자도 위의 **WSL 방법**으로 설치합니다. 전체 목록은 **부록 A · 도구 설치 가이드**.

### 단계 2 — 로그인 시작

```bash
gh auth login
```

화살표 키로 고르고 Enter를 누릅니다. 질문과 고를 답은 이렇습니다.

| 질문 | 고를 답 |
|---|---|
| Where do you use GitHub? | **GitHub.com** |
| What is your preferred protocol for Git operations? | **HTTPS** |
| Authenticate Git with your GitHub credentials? | **Yes** |
| How would you like to authenticate GitHub CLI? | **Login with a web browser** |

### 단계 3 — 브라우저에서 코드 입력

```text
! First copy your one-time code: ABCD-1234
Press Enter to open https://github.com/login/device in your browser...
```

1. 화면의 **8자리 코드**를 기억합니다(이 코드는 몇 분 뒤 만료되는 일회용이라 보여도 괜찮습니다).
2. Enter를 누릅니다. 브라우저가 자동으로 안 열리면(WSL에서 흔함) Windows 브라우저에서 **`https://github.com/login/device`**를 직접 엽니다.
3. 코드를 입력하고 **Authorize**를 누릅니다.

### 단계 4 — 로그인 확인

```bash
gh auth status
```

> **🟢 확인: 이렇게 나오면 성공**
>
> ```text
> github.com
>   ✓ Logged in to github.com account 내아이디 (…)
>   - Active account: true
>   - Git operations protocol: https
>   - Token: gho_************************************
>   - Token scopes: 'gist', 'read:org', 'repo', 'workflow'
> ```
> 토큰이 `*`로 가려져 표시되는 것을 보세요. 도구도 토큰을 화면에 함부로 보여 주지 않습니다.

### 단계 5 — Git이 이 인증을 쓰는지 확인

```bash
git config --global --list | grep credential
```

> **🟢 확인: 이렇게 나오면 성공**
>
> ```text
> credential.https://github.com.helper=
> credential.https://github.com.helper=!/usr/bin/gh auth git-credential
> ```
> `git push`가 GitHub에 로그인해야 할 때 **`gh`에게 토큰을 물어보도록** 연결되었다는 뜻입니다. 단계 2에서 "Authenticate Git… Yes"를 고른 결과입니다. 줄이 안 보이면 `gh auth setup-git`을 실행합니다.

> [!WARNING]
> **토큰은 어디에 저장되나요?**
>
> `gh`는 운영체제의 **안전한 비밀번호 저장소**(Mac 키체인 등)를 쓰려고 합니다. 그런데 WSL처럼 그런 저장소가 없는 환경에서는 `~/.config/gh/hosts.yml` **파일에 평문으로** 저장합니다. 그래서 이 파일은 다른 사람에게 보내거나, 저장소에 넣거나, 화면 공유로 열면 안 됩니다. 1주차 2일차의 **파일 권한**이 여기서 지켜 주는데, `ls -l ~/.config/gh/`로 보면 나만 읽을 수 있게(`-rw-------`) 되어 있습니다.

> **🛠️ 막혔다면: 막혔다면**
>
> | 증상 | 원인 | 해결 |
> |---|---|---|
> | 브라우저가 열리지 않음 | WSL에서 Windows 브라우저를 못 찾음 | 직접 `https://github.com/login/device` 열고 코드 입력 |
> | `code expired` | 일회용 코드 시간 초과 | `gh auth login`을 처음부터 다시 |
> | `E: Unable to locate package gh` | 패키지 목록이 오래됨 | `sudo apt update` 후 다시 |
> | 회사 네트워크에서 로그인 실패 | 방화벽·프록시 | 강사에게 알리고 휴대폰 핫스팟으로 시도 |
> | 이미 다른 계정으로 로그인됨 | — | `gh auth logout` 후 다시 `gh auth login` |

> **🎓 학술 노트 — 비밀번호의 오래된 문제 (Morris & Thompson, 1979)**
>
> Unix를 만든 켄 톰프슨(Ken Thompson)과 로버트 모리스(Robert Morris)는 1979년 논문 「비밀번호 보안: 사례 연구(Password Security: A Case History)」에서 실제 시스템의 비밀번호를 분석했습니다. 놀랍게도 상당수가 짧은 단어나 이름처럼 **쉽게 추측할 수 있는 것**이었습니다. 이 연구는 비밀번호를 원문이 아니라 **해시로 저장**하고, 같은 비밀번호도 다른 값이 되도록 **솔트(salt)**를 섞는 방식을 널리 퍼뜨렸습니다.
>
> 40년이 지난 지금도 문제의 본질은 같습니다. 사람은 기억하기 쉬운 비밀번호를 여러 곳에 재사용하고, 한 곳이 털리면 다른 곳도 털립니다. 그래서 보안은 인증 수단을 여러 종류로 겹칩니다. **아는 것**(비밀번호), **가진 것**(휴대폰, 보안 키), **나 자신**(지문, 얼굴). 오늘 켠 2단계 인증이 바로 "아는 것 + 가진 것"의 조합입니다.
>
> - Morris, R., & Thompson, K. (1979). Password security: A case history. *Communications of the ACM*, 22(11).
> - NIST (2024). *SP 800-63B-4: Digital Identity Guidelines — Authentication and Authenticator Management*.

> **📈 트렌드 — 패스키와 '짧게 사는 토큰'**
>
> 비밀번호를 아예 없애려는 흐름이 빨라지고 있습니다. **패스키(passkey)**는 휴대폰이나 노트북에 저장된 암호 키로 로그인하며, 피싱 사이트에 속아 입력할 비밀번호 자체가 없습니다. GitHub, Google, Apple, Microsoft 모두 패스키 로그인을 지원합니다. 서버와 서버 사이에서도 같은 변화가 있습니다. 오래 유지되는 토큰 대신 **몇 분~몇 시간만 유효한 토큰**을 그때그때 발급하는 방식이 표준이 되어 가고 있습니다. 3주차의 GitHub Actions와 5주차 AWS에서 "키를 저장하지 않고 임시 자격 증명을 받는" OIDC 방식으로 다시 만납니다.

## 정리

- GitHub은 Git 명령에서 **비밀번호를 받지 않습니다.** 토큰 또는 SSH 키를 씁니다.
- 계정에는 **2단계 인증**을 켜고, **복구 코드**를 보관합니다.
- `gh auth login` → 브라우저 로그인 → `gh auth status`로 확인 → Git이 `gh`의 토큰을 씁니다.
- 토큰은 비밀번호와 같습니다. **어디에도 붙여 넣지 않고**, 노출되면 즉시 폐기합니다.

> **✅ 확인 문제**
>
> 1. `git push`할 때 GitHub 계정 비밀번호를 쓸 수 없는 이유는?
> 2. 토큰이 계정 비밀번호보다 안전한 이유 두 가지는?
> 3. 로그인 상태를 확인하는 명령은?
> 4. WSL에서 `gh`의 토큰이 저장되는 파일은?
> 5. 2단계 인증은 인증 요소 중 어떤 두 가지를 겹친 것인가요?
>
> <details><summary>정답</summary>
>
> 1. GitHub이 2021년 8월부터 Git 작업에서 비밀번호 인증을 없앴기 때문
> 2. 범위(권한·저장소)와 만료일을 정할 수 있고, 언제든 그 토큰만 폐기할 수 있다
> 3. `gh auth status`
> 4. `~/.config/gh/hosts.yml`
> 5. 아는 것(비밀번호)과 가진 것(휴대폰 인증 앱)
>
> </details>

## 참고 문헌

- GitHub Blog (2020). *Token authentication requirements for Git operations*.
- GitHub Docs. *About two-factor authentication*, *Managing your personal access tokens*. docs.github.com
- GitHub CLI Manual. *gh auth login*. cli.github.com/manual
- Morris, R., & Thompson, K. (1979). Password security: A case history. *CACM*, 22(11).
- FIDO Alliance. *Passkeys*. fidoalliance.org/passkeys

---

⬅️ 이전: [3교시 · Git 설치와 설정](lesson-03.md) &nbsp;|&nbsp; [⬆️ 1일차 목차](README.md) &nbsp;|&nbsp; 다음: [5교시 · 첫 저장소 — commit과 push](lesson-05.md) ➡️
