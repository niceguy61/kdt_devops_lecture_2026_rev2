<sub>[🏠 과정 목차](../../README.md) › [2주차](../README.md) › [1일차](README.md) › 2/8교시</sub>

# 2교시 · 터미널과 VS Code

> [!NOTE]
> **이번 시간에 할 일**
>
> - 터미널의 기본 명령으로 폴더를 만들고 이동합니다.
> - Windows 파일과 WSL 파일의 위치 차이를 압니다.
> - VS Code를 설치하고, 터미널에서 `code .`로 폴더를 엽니다.
> - VS Code 안의 터미널을 씁니다.

## 터미널 기본 — 1주차 시연을 이제 직접

1주차 2일차 5교시에 강사가 보여 준 명령을 이제 직접 입력합니다.

| 명령 | 뜻 | 기억하는 법 |
|---|---|---|
| `pwd` | 지금 있는 폴더 | **p**rint **w**orking **d**irectory |
| `ls` / `ls -la` | 폴더 안 목록 / 숨김 파일까지 자세히 | **l**i**s**t |
| `cd 폴더` | 폴더로 이동 | **c**hange **d**irectory |
| `cd ~` / `cd ..` | 홈으로 / 한 칸 위로 | `~`는 홈, `..`는 부모 |
| `mkdir -p 경로` | 폴더 만들기 (중간 폴더까지) | **m**a**k**e **dir**ectory |
| `touch 파일` | 빈 파일 만들기 | 파일을 "건드린다" |
| `cat 파일` | 파일 내용 보기 | con**cat**enate |
| `clear` | 화면 지우기 | `Ctrl` + `L`도 같다 |

> [!TIP]
> **손가락을 아끼는 두 가지 키**
>
> - **Tab** : 파일·폴더 이름을 몇 글자만 치고 Tab을 누르면 나머지를 자동 완성합니다. 오타를 줄이는 가장 좋은 방법입니다.
> - **↑ (위 화살표)** : 방금 입력한 명령을 다시 불러옵니다. 조금 고쳐서 다시 실행할 때 씁니다.

## 실습 3 · 작업 폴더 만들기

> **🧪 실습: 실습 목표**
>
> 이번 주 모든 실습을 담을 `~/devops-lab` 폴더를 만들고, 그 안에서 첫 파일을 만들어 봅니다.

### 단계 1 — 홈에서 시작

```bash
cd ~
pwd
```

> **🟢 확인: 이렇게 나오면 성공**
>
> ```text
> /home/devops
> ```
> Mac은 `/Users/내이름`입니다. 이 위치를 **홈 디렉터리**라고 하고, 줄여서 `~`로 씁니다.

### 단계 2 — 작업 폴더 만들고 들어가기

```bash
mkdir -p ~/devops-lab
cd ~/devops-lab
pwd
```

> **🟢 확인: 이렇게 나오면 성공**
>
> ```text
> /home/devops/devops-lab
> ```

### 단계 3 — 파일 만들고 내용 넣어 보기

```bash
echo "안녕, DevOps" > hello.txt
cat hello.txt
ls -la
```

- `echo "글자"` : 글자를 출력합니다.
- `>` : 출력을 화면 대신 **파일에 씁니다** (기존 내용은 덮어씀). `>>`는 끝에 덧붙입니다.

> **🟢 확인: 이렇게 나오면 성공**
>
> ```text
> 안녕, DevOps
> total 12
> drwxr-xr-x 2 devops devops 4096 Nov 30 10:12 .
> drwxr-x--- 5 devops devops 4096 Nov 30 10:12 ..
> -rw-r--r-- 1 devops devops   17 Nov 30 10:12 hello.txt
> ```
> 1주차 2일차 4교시의 **권한 표기**(`-rw-r--r--`)가 보이나요? 날짜와 크기는 달라도 됩니다.

> [!WARNING]
> **Windows 사용자: 파일은 꼭 Linux 쪽에 두세요**
>
> WSL에서는 Windows의 C 드라이브가 `/mnt/c`로 보입니다. 하지만 실습 파일을 `/mnt/c/Users/...`(Windows 쪽)에 두면, Linux와 Windows 사이를 오가며 파일을 읽느라 **Docker와 Git이 몇 배 느려지고**, 파일 권한과 줄바꿈 문자가 꼬이는 문제가 생깁니다. Docker 공식 문서도 소스 코드를 **Linux 파일 시스템(`~`)**에 두라고 권합니다. 이번 주 모든 실습은 `~/devops-lab` 안에서 합니다.
>
> 반대로 Windows 탐색기에서 Linux 파일을 보고 싶다면, Ubuntu 터미널에서 `explorer.exe .`을 입력하면 됩니다.

## 실습 4 · VS Code 설치와 연결

> **🧪 실습: 실습 목표**
>
> VS Code를 설치하고, 터미널에서 `code .` 한 줄로 작업 폴더를 VS Code에서 엽니다.

### 단계 1 — VS Code 설치

- **Windows**: [code.visualstudio.com](https://code.visualstudio.com)에서 Windows용을 받아 **Windows에** 설치합니다(WSL 안이 아님). 설치 중 **"PATH에 추가"**가 체크되어 있는지 확인합니다.
- **Mac**: 같은 사이트에서 Mac용을 받아 응용 프로그램 폴더로 옮깁니다. 또는 터미널에서 `brew install --cask visual-studio-code`.

설치 파일을 받는 대신 명령 한 줄로 깔 수도 있습니다.

**Windows — PowerShell (winget)**

```powershell
winget install -e --id Microsoft.VisualStudioCode
```

**Mac — 터미널 (Homebrew)**

```bash
brew install --cask visual-studio-code
```

winget은 Windows 10(1809 이상)·11에 기본으로 들어 있는 패키지 관리자입니다. Mac의 Homebrew와 같은 역할입니다.

### 단계 2 — 확장 설치

VS Code 왼쪽의 **확장(Extensions)** 아이콘(네모 네 개)을 누르고 검색해 설치합니다.

| 확장 | 누가 | 하는 일 |
|---|---|---|
| **WSL** (Microsoft) | Windows만 | VS Code가 WSL 안의 파일과 터미널을 직접 다루게 함 |
| **Container Tools** (Microsoft) | 모두 | Dockerfile·compose.yaml 문법 도움, 컨테이너 목록 보기 |
| **Korean Language Pack** | 원하는 사람 | 메뉴를 한국어로 |

### 단계 3 — Mac만: `code` 명령 등록

VS Code에서 `Command` + `Shift` + `P` → **Shell Command: Install 'code' command in PATH** 선택.

### 단계 4 — 터미널에서 VS Code 열기

Ubuntu(또는 Mac) 터미널에서:

```bash
cd ~/devops-lab
code .
```

- `code` : VS Code를 실행합니다.
- `.` : **지금 이 폴더**를 엽니다. (1주차의 `.`은 현재 폴더, `..`은 부모 폴더)

> **🟢 확인: 이렇게 나오면 성공**
>
> - VS Code가 열리고 왼쪽 탐색기에 `hello.txt`가 보입니다.
> - **Windows**: 왼쪽 아래 구석에 초록(또는 파란) 표시로 **`WSL: Ubuntu-24.04`**가 보입니다. 이것이 보여야 VS Code가 Linux 쪽 파일을 직접 다루는 것입니다.

### 단계 5 — VS Code 안의 터미널

VS Code에서 `` Ctrl + ` `` (숫자 1 왼쪽 키)를 누르면 아래쪽에 터미널이 열립니다.

```bash
pwd
```

> **🟢 확인: 이렇게 나오면 성공**
>
> ```text
> /home/devops/devops-lab
> ```
> 이제 **편집은 위에서, 명령은 아래에서** 한 화면으로 할 수 있습니다. 이번 주 내내 이 화면 배치로 일합니다.

> **🛠️ 막혔다면: 막혔다면**
>
> | 증상 | 원인 | 해결 |
> |---|---|---|
> | `code: command not found` (WSL) | VS Code 설치 때 PATH 추가를 안 함 | VS Code 재설치 시 PATH 체크, 또는 Windows 재로그인 후 다시 시도 |
> | `code: command not found` (Mac) | 단계 3을 안 함 | Shell Command 등록 |
> | VS Code는 열리는데 왼쪽 아래에 WSL 표시가 없음 | WSL 확장이 없음 | 단계 2에서 WSL 확장 설치 후 다시 `code .` |
> | 처음 `code .` 실행이 오래 걸림 | WSL 안에 VS Code 서버를 설치하는 중 | 1~2분 기다리면 된다 (처음 한 번만) |

> **🎓 학술 노트 — 셸은 왜 아직도 쓰일까 (Bourne, 1979)**
>
> 그래픽 화면이 있는데 왜 아직도 글자로 명령을 칠까요? 1979년 벨 연구소의 스티븐 본(Stephen Bourne)이 만든 **본 셸(sh)**은 명령을 입력받는 도구이자 **프로그래밍 언어**였습니다. 변수, 조건문, 반복문을 써서 명령들을 묶을 수 있었고, 이것이 지금 우리가 쓰는 **bash**(Bourne Again Shell, 1989)와 **zsh**(Mac 기본)의 조상입니다.
>
> 셸이 50년 가까이 살아남은 이유는 **자동화** 때문입니다. 마우스 클릭은 기록하고 반복하기 어렵지만, 명령은 그대로 파일에 적으면 **스크립트**가 됩니다. 1주차 5일차의 런북에 "복사해 쓰는 명령"이 들어가는 이유, 그리고 2주차의 Dockerfile과 3주차의 CI 파이프라인이 결국 **명령의 목록**인 이유가 여기에 있습니다. 오늘 손에 익히는 명령 하나하나가 나중에 자동화의 재료가 됩니다.
>
> - Bourne, S. R. (1978). The UNIX shell. *The Bell System Technical Journal*, 57(6).

> **📈 트렌드 — 편집기 안으로 들어온 AI**
>
> VS Code는 여러 해 동안 개발자가 가장 많이 쓰는 편집기 자리를 지키고 있고, 최근에는 편집기 안에서 AI가 코드를 제안하고, 터미널 명령을 대신 실행하고, 여러 파일을 한꺼번에 고치는 **코딩 에이전트** 기능이 기본처럼 들어오고 있습니다. Stack Overflow 2026 설문에서도 AI를 쓰는 개발자 중 다수가 코딩 에이전트를 사용한다고 답했습니다. 편리한 만큼 1주차에 배운 원칙이 더 중요해집니다. **AI가 실행하려는 명령을 읽고 이해한 뒤에 허락하기**, 그리고 **비밀값을 AI 대화창에 붙여 넣지 않기**입니다.

## 정리

- `pwd`, `ls`, `cd`, `mkdir -p`, `echo >`, `cat`이 기본 명령이며, **Tab**과 **↑**로 손을 아낍니다.
- 실습 파일은 **`~/devops-lab`**(Linux 쪽)에 둡니다. `/mnt/c`는 느리고 꼬입니다.
- `code .`로 지금 폴더를 VS Code에서 열고, Windows는 왼쪽 아래 **WSL 표시**를 확인합니다.
- 편집은 위에서, 명령은 `` Ctrl + ` `` 터미널에서 합니다.

> **✅ 확인 문제**
>
> 1. 지금 있는 폴더를 알려 주는 명령은?
> 2. `echo "a" > x.txt`와 `echo "a" >> x.txt`의 차이는?
> 3. WSL에서 실습 파일을 `/mnt/c` 아래에 두면 안 되는 이유는?
> 4. `code .`에서 `.`의 의미는?
> 5. Windows의 VS Code가 WSL에 연결되었는지 어디서 확인하나요?
>
> <details><summary>정답</summary>
>
> 1. `pwd`
> 2. `>`는 덮어쓰고, `>>`는 끝에 덧붙인다
> 3. Windows와 Linux 파일 시스템을 오가느라 느리고, 권한·줄바꿈 문제가 생기기 때문
> 4. 현재 폴더
> 5. VS Code 왼쪽 아래 구석의 `WSL: Ubuntu-24.04` 표시
>
> </details>

## 참고 문헌

- Microsoft. *Developing in WSL* (VS Code docs). code.visualstudio.com/docs/remote/wsl
- Docker. *WSL 2 best practices for Docker Desktop on Windows*. docs.docker.com
- Bourne, S. R. (1978). The UNIX shell. *Bell System Technical Journal*, 57(6).
- Stack Overflow (2026). *2026 Developer Survey*. survey.stackoverflow.co

---

| 이전 | 목차 | 다음 |
|:--|:--:|--:|
| ⬅️ [1교시 · 1주차 요약과 작업 환경 준비](lesson-01.md) | [⬆️ 1일차 목차](README.md) | [3교시 · Git 설치와 설정](lesson-03.md) ➡️ |
