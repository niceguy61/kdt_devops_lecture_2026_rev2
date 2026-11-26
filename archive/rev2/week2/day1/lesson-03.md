# 3교시 · Git 설치와 설정

> [!NOTE]
> **이번 시간에 할 일**
>
> - Git을 설치하고 버전을 확인합니다.
> - 커밋에 남을 이름과 이메일을 설정합니다.
> - 기본 브랜치 이름과 편집기를 설정합니다.
> - 설정이 어디에 저장되는지 확인합니다.

## 왜 설정부터 하나요?

1주차 5일차에 "커밋에는 **누가, 언제, 무엇을, 왜**가 남는다"고 배웠습니다. 그 **"누가"**를 Git에게 알려 주는 것이 오늘의 설정입니다. 설정하지 않으면 커밋할 때 Git이 "당신은 누구인가요?"라며 멈춥니다.

## 실습 5 · Git 설치와 설정

> **🧪 실습: 실습 목표**
>
> Git을 설치하고, 이름·이메일·기본 브랜치·편집기를 설정한 뒤 `git config --list`로 확인합니다.

### 단계 1 — 설치

**Windows(WSL Ubuntu) / Linux:**

```bash
sudo apt install -y git
git --version
```

**Mac:**

```bash
brew install git
git --version
```

> **🟢 확인: 이렇게 나오면 성공**
>
> ```text
> git version 2.43.0
> ```
> 숫자는 달라도 됩니다. Ubuntu 24.04에는 Git이 이미 들어 있는 경우가 많아 "이미 최신 버전"이라는 메시지가 나올 수도 있습니다.

### 단계 2 — 이름과 이메일

```bash
git config --global user.name "홍길동"
git config --global user.email "gildong@example.com"
```

- `--global` : 이 컴퓨터의 **내 계정 전체**에 적용합니다(모든 저장소 공통).
- 이름과 이메일은 **커밋 기록에 영구히 남고, 공개 저장소라면 누구나 볼 수 있습니다.**

> [!TIP]
> **이메일을 공개하고 싶지 않다면**
>
> 다음 시간에 GitHub 가입 후 **Settings → Emails**에서 **"Keep my email addresses private"**를 켜면 `숫자+아이디@users.noreply.github.com` 형식의 가림용 주소를 줍니다. 그 주소를 `user.email`로 다시 설정하면 커밋에 진짜 이메일이 남지 않습니다. 취업 포트폴리오로 쓸 저장소라면 고려해 볼 만합니다.

### 단계 3 — 기본 브랜치 이름과 편집기

```bash
git config --global init.defaultBranch main
git config --global core.editor "code --wait"
```

- `init.defaultBranch main` : 새 저장소의 첫 브랜치 이름을 `main`으로 합니다. GitHub의 기본값과 맞추기 위함입니다.
- `core.editor "code --wait"` : 커밋 메시지를 길게 쓸 때 VS Code가 열리게 합니다. `--wait`은 창을 닫을 때까지 Git이 기다리라는 뜻입니다.

### 단계 4 — 줄바꿈 설정 (Windows WSL 사용자만)

```bash
git config --global core.autocrlf input
```

Windows와 Linux는 **줄바꿈 문자**가 다릅니다(Windows는 `CRLF`, Linux·Mac은 `LF`). 이 설정은 저장소에는 항상 `LF`로 저장되게 해서, 컨테이너 안(Linux)에서 셸 스크립트가 `\r: command not found` 같은 에러를 내는 것을 막습니다.

### 단계 5 — 확인

```bash
git config --global --list
```

> **🟢 확인: 이렇게 나오면 성공**
>
> ```text
> user.name=홍길동
> user.email=gildong@example.com
> init.defaultbranch=main
> core.editor=code --wait
> core.autocrlf=input
> ```
> Mac은 마지막 줄이 없어도 됩니다.

### 단계 6 — 설정은 어디에 저장될까?

```bash
cat ~/.gitconfig
```

> **🟢 확인: 이렇게 나오면 성공**
>
> ```text
> [user]
>         name = 홍길동
>         email = gildong@example.com
> [init]
>         defaultBranch = main
> [core]
>         editor = code --wait
>         autocrlf = input
> ```
> `git config` 명령은 결국 **홈 폴더의 텍스트 파일 하나**를 고치는 것입니다. 1주차 2일차의 "설정은 파일이다"가 여기서도 나타납니다. 이름이 점(`.`)으로 시작하는 파일은 숨김 파일이라 `ls`로는 안 보이고 `ls -a`로 보입니다.

| 설정 범위 | 옵션 | 저장 위치 | 적용 대상 |
|---|---|---|---|
| 시스템 | `--system` | `/etc/gitconfig` | 이 컴퓨터의 모든 사용자 |
| 사용자 | `--global` | `~/.gitconfig` | 나의 모든 저장소 |
| 저장소 | (없음) | 저장소 안 `.git/config` | 그 저장소만 |

좁은 범위가 넓은 범위를 이깁니다. 회사 저장소에서만 회사 이메일을 쓰고 싶다면, 그 저장소 안에서 `--global` 없이 설정하면 됩니다.

> **🛠️ 막혔다면: 막혔다면**
>
> | 증상 | 원인 | 해결 |
> |---|---|---|
> | `E: Unable to locate package git` | 패키지 목록이 오래됨 | `sudo apt update` 후 다시 설치 |
> | Mac에서 `xcode-select` 설치 창이 뜸 | 개발자 도구가 없어서 | 창에서 **설치**를 누르고 기다린 뒤 다시 |
> | 이름을 잘못 입력함 | — | 같은 명령을 올바른 값으로 다시 실행하면 덮어쓴다 |
> | 따옴표 안의 한글이 깨져 보임 | 터미널 글꼴 문제 | 표시만의 문제이며 값은 정상. `cat ~/.gitconfig`로 확인 |

> **🎓 학술 노트 — 내용으로 이름 짓기 (Content-Addressable Storage)**
>
> Git은 파일을 "파일 이름"이 아니라 **내용으로 만든 지문(해시)**으로 저장합니다. 파일 내용을 SHA-1(최근에는 SHA-256도 지원) 함수에 넣으면 40자리(또는 64자리) 16진수 값이 나오고, 이 값이 그 내용의 이름이 됩니다. 내용이 한 글자라도 바뀌면 이름도 완전히 바뀝니다.
>
> 이런 저장 방식을 **내용 주소 지정 저장소(content-addressable storage)**라고 합니다. 장점은 세 가지입니다. ① 같은 내용은 한 번만 저장되어 공간을 아낍니다. ② 내용이 몰래 바뀌면 이름이 안 맞아 바로 들통납니다(1주차 5일차의 "위변조 감지"). ③ 이름만 비교하면 두 저장소가 같은지 금방 알 수 있습니다.
>
> 이 아이디어는 Git만의 것이 아닙니다. **내일 배울 Docker 이미지의 레이어**와 **3일차의 이미지 다이제스트(`sha256:...`)**도 똑같은 원리입니다. 오늘 Git에서 본 긴 16진수 문자열을 내일 Docker에서 또 만나게 됩니다.
>
> - Chacon, S., & Straub, B. (2014). *Pro Git*, Ch. 10 Git Internals. Apress.
> - Merkle, R. C. (1987). A digital signature based on a conventional encryption function. *CRYPTO '87*. (머클 트리)

> **📈 트렌드 — 커밋에도 서명한다**
>
> `user.name`과 `user.email`은 누구나 아무 값으로나 설정할 수 있습니다. 즉 남의 이름으로 커밋을 만드는 것도 기술적으로 가능합니다. 그래서 공급망 보안(1주차 5일차)이 중요해지면서, 커밋에 **암호학적 서명**을 붙이는 회사가 늘고 있습니다. Git은 이제 GPG뿐 아니라 **SSH 키로도 커밋에 서명**할 수 있고, GitHub은 서명이 확인된 커밋에 **Verified** 표시를 붙입니다. 저장소 설정에서 "서명된 커밋만 허용"을 켜는 조직도 많아지고 있습니다. 지금은 몰라도 되지만, 첫 직장에서 "커밋 서명 설정하세요"라는 안내를 받으면 오늘의 설정 파일을 떠올리면 됩니다.

## 정리

- Git은 `apt`(Ubuntu) 또는 `brew`(Mac)로 설치합니다.
- `user.name`, `user.email`은 **모든 커밋에 영구히 남습니다.** 가림용 이메일도 쓸 수 있습니다.
- 기본 브랜치는 `main`, 편집기는 `code --wait`, Windows는 `core.autocrlf input`.
- 설정은 `~/.gitconfig` **텍스트 파일**에 저장되고, 저장소 설정이 전역 설정을 이깁니다.

> **✅ 확인 문제**
>
> 1. 커밋에 남을 내 이름을 설정하는 명령은?
> 2. `--global` 설정은 어느 파일에 저장되나요?
> 3. Windows에서 `core.autocrlf input`을 설정하는 이유는?
> 4. 회사 저장소에서만 다른 이메일을 쓰려면?
> 5. Git이 파일을 저장하는 방식의 이름은? (내일 Docker에서도 나온다)
>
> <details><summary>정답</summary>
>
> 1. `git config --global user.name "이름"`
> 2. `~/.gitconfig`
> 3. 줄바꿈 문자를 LF로 통일해, Linux(컨테이너)에서 스크립트 에러가 나지 않게 하려고
> 4. 그 저장소 안에서 `--global` 없이 `git config user.email` 설정
> 5. 내용 주소 지정 저장소(content-addressable storage, 해시)
>
> </details>

## 참고 문헌

- Git. *git-config Documentation*. git-scm.com/docs/git-config
- Chacon, S., & Straub, B. (2014). *Pro Git* (2nd ed.), Ch. 1.6, Ch. 10. git-scm.com/book/ko/v2
- GitHub Docs. *Setting your commit email address*, *About commit signature verification*. docs.github.com
