# 8교시 · 셸 다지기 — 파이프 · 리다이렉트 · 변수 · 첫 스크립트

!!! goal "이번 시간에 할 일"
    - 명령의 출력을 **파일로 보내고(`>` `>>` `2>`)**, 다른 명령으로 **잇는(`|`)** 법을 손에 익힙니다.
    - `grep` · `wc` · `sort` · `uniq` · `head` · `tail`로 긴 출력에서 필요한 줄만 골라냅니다.
    - **변수**와 **환경 변수**, `PATH`, 종료 코드 `$?`를 직접 확인합니다.
    - 오늘 설치한 도구를 한 번에 점검하는 **첫 셸 스크립트**를 만들어 커밋합니다.

!!! key "왜 지금 셸인가"
    5주 동안 치는 명령의 대부분은 `docker`, `kubectl`, `aws` 같은 도구 이름 **뒤에 파이프와 변수가 붙은 한 줄**입니다. 예를 들어 4주차에는 이런 줄을 씁니다.

    ```bash
    kubectl get pods -A | grep -v Running | wc -l
    ```

    도구는 매주 바뀌지만 **이음새(파이프 · 리다이렉트 · 변수)**는 끝까지 같습니다. 오늘 한 시간이 5주를 편하게 합니다.

## 실습 13 · 출력의 방향 바꾸기

!!! lab "실습 목표"
    표준 출력과 표준 에러를 구분해서 파일로 보내고, 파이프로 이어 봅니다.

### 단계 1 — 준비

```bash
mkdir -p ~/devops-lab/day1/shell && cd ~/devops-lab/day1/shell
```

### 단계 2 — 출력은 두 갈래다

프로그램의 출력에는 **정상 출력(stdout, 1번)**과 **에러 출력(stderr, 2번)** 두 갈래가 있습니다.

```bash
ls /etc/hostname /없는폴더
```

!!! check "보이는 것"
    ```text
    ls: cannot access '/없는폴더': No such file or directory
    /etc/hostname
    ```
    화면에는 둘이 섞여 보이지만 **다른 통로**로 나왔습니다. 화면에 나온 순서가 바뀌어 보이는 것도 이 때문입니다.

```bash
ls /etc/hostname /없는폴더 > out.txt 2> err.txt
cat out.txt
cat err.txt
```

| 기호 | 뜻 | 기억하는 법 |
|---|---|---|
| `>` | 정상 출력을 파일로 (**덮어쓰기**) | 화살표가 파일을 가리킨다 |
| `>>` | 정상 출력을 파일 끝에 **덧붙이기** | 두 개 = 계속 쌓기 |
| `2>` | 에러 출력을 파일로 | 2번 통로 |
| `2>&1` | 에러도 정상 출력이 가는 곳으로 | "2를 1과 같은 곳으로" |
| `> /dev/null` | 버리기 | Linux의 쓰레기통 |

```bash
ls /etc/hostname /없는폴더 > all.txt 2>&1
cat all.txt
ls /없는폴더 2> /dev/null; echo "에러는 버렸다"
```

!!! warn "`>`는 확인 없이 덮어쓴다"
    `> 중요한파일.txt`를 잘못 치면 내용이 **바로 사라집니다.** 기록을 남길 때는 `>>`를 쓰는 습관을 들입니다.

### 단계 3 — 파이프로 잇기

`|`(파이프)는 앞 명령의 **정상 출력**을 뒤 명령의 **입력**으로 넘깁니다. 1주차 2일차 시연에서 본 그것입니다.

```bash
history | tail -5
ls -l /etc | wc -l
cat /etc/passwd | cut -d: -f7 | sort | uniq -c | sort -rn
```

!!! check "마지막 줄은 이렇게 보입니다"
    ```text
         19 /usr/sbin/nologin
          2 /bin/bash
          1 /bin/sync
          …
    ```
    "이 컴퓨터 사용자들이 어떤 셸을 쓰는지 개수 순으로" — 다섯 개의 작은 명령을 이어 한 질문에 답했습니다. 숫자는 컴퓨터마다 다릅니다.

| 명령 | 하는 일 |
|---|---|
| `cut -d: -f7` | `:`로 나눈 7번째 칸만 |
| `sort` | 줄을 정렬 (`uniq`는 붙어 있는 같은 줄만 합치므로 먼저 정렬) |
| `uniq -c` | 같은 줄을 합치며 개수 표시 |
| `sort -rn` | 숫자(`-n`)로 큰 것부터(`-r`) |

### 단계 4 — `tee`: 화면에도, 파일에도

```bash
docker version 2>&1 | tee docker-version.txt | head -3
```

`tee`는 T자 관처럼 흐름을 둘로 나눕니다. 화면으로 보면서 **증거를 파일로 남길 때** 씁니다. 6교시에 만든 설치 기록을 이렇게 남길 수 있습니다.

## 실습 14 · 긴 출력에서 필요한 줄 찾기

### 단계 1 — `grep`

```bash
grep -n "PRETTY" /etc/os-release
grep -i "ubuntu" /etc/os-release
grep -c "" /etc/passwd
grep -v "nologin" /etc/passwd | head -3
```

| 옵션 | 뜻 |
|---|---|
| `-n` | 줄 번호도 |
| `-i` | 대소문자 무시 |
| `-v` | 이 글자가 **없는** 줄만 (뒤집기) |
| `-c` | 몇 줄인지만 |
| `-r` | 폴더 안을 전부 (`grep -rn "TODO" .`) |
| `-E` | 여러 조건 `grep -E "error|fail"` |

### 단계 2 — 처음과 끝, 그리고 지켜보기

```bash
head -3 /etc/passwd
tail -3 /etc/passwd
```

`tail -f 파일`은 파일 끝을 **계속 지켜봅니다**. 2일차의 `docker logs -f`, 3주차의 `kubectl logs -f`가 같은 생각입니다. 멈출 때는 `Ctrl` + `C`.

!!! tip "손이 빨라지는 키"
    | 키 | 하는 일 |
    |---|---|
    | `Tab` | 파일 · 명령 이름 자동 완성 (두 번 누르면 후보 목록) |
    | `↑` / `↓` | 이전 명령 |
    | `Ctrl` + `R` | 이전 명령 **검색** — 글자를 치면 가장 최근 것이 나온다 |
    | `Ctrl` + `C` | 실행 중인 명령 멈추기 |
    | `Ctrl` + `L` | 화면 지우기 |
    | `Ctrl` + `A` / `E` | 줄 처음 / 끝으로 |

## 실습 15 · 변수 · 환경 변수 · 종료 코드

### 단계 1 — 셸 변수

```bash
NAME=devmart
echo "앱 이름: $NAME"
echo "앱 이름: ${NAME}-api"
```

!!! warn "`=` 양옆에 빈칸을 두지 않는다"
    `NAME = devmart`라고 쓰면 셸은 `NAME`이라는 **명령**을 찾다가 `command not found`를 냅니다. 대부분의 언어와 다른 점이라 처음에 자주 틀립니다.

### 단계 2 — 환경 변수와 `export`

셸 변수는 **그 셸 안에서만** 보입니다. 셸이 실행하는 프로그램에게도 보이게 하려면 `export`합니다. 이것이 **환경 변수**입니다.

```bash
bash -c 'echo "자식이 본 NAME: [$NAME]"'
export NAME
bash -c 'echo "자식이 본 NAME: [$NAME]"'
```

!!! check "이렇게 나오면 성공"
    ```text
    자식이 본 NAME: []
    자식이 본 NAME: [devmart]
    ```
    2주차 4일차에 컨테이너에 `-e DB_HOST=db`로 설정을 넣고, 3주차에 Kubernetes에서 `env:`로 넣는 것이 모두 이 **환경 변수**입니다. 1주차 4일차의 "설정은 코드 밖에"를 실제로 하는 방법입니다.

### 단계 3 — `PATH`: 명령을 어디서 찾나

```bash
echo $PATH | tr ':' '\n'
which git docker code
```

`git`이라고 치면 셸은 `PATH`에 적힌 폴더를 **왼쪽부터 차례로** 뒤져 처음 찾은 것을 실행합니다. 3주차에 `kubectl`을 `/usr/local/bin`에 넣는 이유가 이것입니다. `command not found`가 나오면 "설치가 안 됐거나, `PATH`에 없는 폴더에 있다"입니다.

### 단계 4 — 종료 코드

```bash
ls /etc/hostname; echo "종료 코드: $?"
ls /없는폴더 2>/dev/null; echo "종료 코드: $?"
grep -q "Ubuntu" /etc/os-release && echo "Ubuntu다" || echo "Ubuntu가 아니다"
```

1주차 2일차에 배운 **0은 성공, 0이 아니면 실패**를 `$?`로 직접 봅니다. `&&`는 성공하면 다음, `||`는 실패하면 다음입니다. 3주차 CI는 이 숫자 하나로 통과와 실패를 가릅니다.

## 실습 16 · 첫 셸 스크립트 — 작업대 점검기

!!! lab "실습 목표"
    오늘 설치한 도구가 모두 있는지 한 번에 확인하는 `check-env.sh`를 만들고, 커밋합니다. 앞으로 새 도구를 배울 때마다 이 파일에 한 줄씩 더합니다.

### 단계 1 — 파일 만들기

```bash
cd ~/devops-lab/day1
code check-env.sh
```

아래를 붙여 넣고 저장합니다.

```bash
#!/usr/bin/env bash
# 작업대 점검기 — 필요한 도구가 있는지, 버전은 무엇인지
set -uo pipefail

TOOLS="git gh docker code"
missing=0

for t in $TOOLS; do
  if command -v "$t" > /dev/null; then
    printf '%-8s ✓ %s\n' "$t" "$(command -v "$t")"
  else
    printf '%-8s ✗ 없음\n' "$t"
    missing=$((missing + 1))
  fi
done

if docker info > /dev/null 2>&1; then
  echo "docker   ✓ 엔진 응답"
else
  echo "docker   ✗ 엔진이 꺼져 있음 (Docker Desktop을 켜세요)"
  missing=$((missing + 1))
fi

echo "빠진 것: $missing개"
exit "$missing"
```

| 줄 | 뜻 |
|---|---|
| `#!/usr/bin/env bash` | 이 파일을 **bash로 실행**하라는 표시(셔뱅) |
| `set -uo pipefail` | 없는 변수를 쓰면 에러(`-u`), 파이프 중간 실패도 실패로(`pipefail`) |
| `for t in $TOOLS; do … done` | 목록을 하나씩 돌며 반복 |
| `command -v` | `which`처럼 명령의 위치를 찾음. 없으면 실패(종료 코드 1) |
| `$((…))` | 셸에서 산수 |
| `exit "$missing"` | 빠진 개수를 **종료 코드로** — 0이면 모두 있음 |

### 단계 2 — 실행 권한 주고 실행

```bash
chmod +x check-env.sh
./check-env.sh; echo "종료 코드: $?"
```

!!! check "이렇게 나오면 성공"
    ```text
    git      ✓ /usr/bin/git
    gh       ✓ /usr/bin/gh
    docker   ✓ /usr/bin/docker
    code     ✓ /mnt/c/Users/…/bin/code
    docker   ✓ 엔진 응답
    빠진 것: 0개
    종료 코드: 0
    ```
    Mac은 경로가 `/opt/homebrew/bin/…`이나 `/usr/local/bin/…`입니다.

!!! trouble "막혔다면"
    | 증상 | 원인 | 해결 |
    |---|---|---|
    | `Permission denied` | 실행 권한이 없음 | `chmod +x check-env.sh` (1주차 2일차의 `x` 권한) |
    | `bash: ./check-env.sh: /usr/bin/env: bad interpreter: … ^M` | Windows 줄바꿈(CRLF)으로 저장됨 | VS Code 오른쪽 아래 `CRLF`를 눌러 `LF`로 바꾸고 저장 |
    | `docker ✗ 엔진이 꺼져 있음` | Docker Desktop이 꺼짐 | Docker Desktop 실행 후 다시 |
    | `code ✗ 없음` (Mac) | `code` 명령 미등록 | 4교시 단계 3 |

### 단계 3 — 바깥에서 바꿀 수 있게

검사할 도구 목록을 실행할 때 바꿔 보려고 합니다. 명령 **앞에** `변수=값`을 붙이면 그 명령에게만 환경 변수를 줍니다.

```bash
TOOLS="git kubectl" ./check-env.sh; echo "종료 코드: $?"
```

결과는 그대로 네 도구이고 종료 코드도 0입니다. 스크립트 안의 `TOOLS="git gh docker code"` 줄이 바깥에서 준 값을 **덮어쓰기** 때문입니다. 그 줄을 이렇게 고칩니다.

```bash
TOOLS="${TOOLS:-git gh docker code}"
```

`${변수:-기본값}`은 "바깥에서 정해 줬으면 그것, 아니면 기본값"입니다. 저장하고 다시 실행합니다.

```bash
TOOLS="git kubectl" ./check-env.sh; echo "종료 코드: $?"
./check-env.sh > /dev/null; echo "기본값으로: $?"
```

!!! check "이렇게 나오면 성공"
    ```text
    git      ✓ /usr/bin/git
    kubectl  ✗ 없음
    docker   ✓ 엔진 응답
    빠진 것: 1개
    종료 코드: 1
    기본값으로: 0
    ```
    `kubectl`은 3주차에 설치하므로 지금은 없는 게 정상입니다. **설정은 바깥에서, 기본값은 안에서** — 2주차 4일차의 환경 변수와 같은 설계입니다.

### 단계 4 — 커밋

```bash
cd ~/devops-lab
git add day1/check-env.sh
git commit -m "1일차: 작업대 점검 스크립트"
git push
```

!!! cleanup "정리"
    `~/devops-lab/day1/shell`의 연습 파일(`out.txt` 등)은 커밋하지 않습니다. 지워도 됩니다: `rm -r ~/devops-lab/day1/shell`

!!! academic "학술 노트 — 유닉스 철학 (McIlroy, 1978)"
    파이프를 유닉스에 넣자고 제안한 벨 연구소의 **더글러스 매킬로이(Douglas McIlroy)**는 1978년 『벨 시스템 기술 저널』 유닉스 특집의 머리말에서 유닉스 프로그램을 만드는 원칙을 정리했습니다. **"한 가지 일만 잘하는 프로그램을 만들어라. 다른 프로그램의 입력이 될 것을 예상하고 출력을 만들어라."** 오늘 `cut | sort | uniq -c | sort -rn`으로 질문 하나에 답한 것이 그 결과입니다. 거대한 만능 프로그램 하나 대신 **작은 도구를 이어 붙이는** 방식은 3주차의 마이크로서비스, 4주차의 "한 가지 일을 하는 컨트롤러 여럿" 구조에서 다시 나타납니다.

    - McIlroy, M. D., Pinson, E. N., & Tague, B. A. (1978). UNIX time-sharing system: Foreword. *The Bell System Technical Journal*, 57(6), 1899–1904.

!!! trend "트렌드 — AI 에이전트도 셸로 일한다"
    요즘 AI 코딩 도구는 코드를 제안하는 데서 그치지 않고 **터미널에서 직접 명령을 실행**하며 일합니다. 설치하고, 테스트를 돌리고, `grep`으로 찾고, 실패하면 종료 코드를 보고 다시 시도합니다. 1주차 1일차에 약속한 대로 AI가 하는 일을 **사람이 승인하고 검토**하려면, AI가 치려는 한 줄 — `rm -rf "$DIR"/`의 `$DIR`이 비어 있으면 무슨 일이 생기는지 — 을 읽을 수 있어야 합니다. 셸은 AI 시대에 오히려 **검토자의 기본기**가 되었습니다.

## 정리

- 출력은 **정상(1) · 에러(2)** 두 갈래 — `>` `>>` `2>` `2>&1` `/dev/null`로 방향을 바꿉니다.
- `|`로 작은 명령을 이어 질문에 답합니다: `grep` · `wc` · `sort` · `uniq -c` · `head` · `tail` · `tee`.
- `export`한 변수만 자식 프로그램에 보입니다(환경 변수). `PATH`는 명령을 찾는 폴더 목록입니다.
- 스크립트는 `#!/usr/bin/env bash` + `chmod +x`. 결과를 **종료 코드**로 알리면 다른 프로그램(CI)이 읽을 수 있습니다.

!!! quiz "확인 문제"
    1. `ls 없는파일 > out.txt`를 실행했는데 화면에 에러가 나왔습니다. 왜 파일로 가지 않았나요?
    2. 로그 파일에서 `ERROR`가 있는 줄이 몇 개인지 세는 한 줄 명령은?
    3. `PORT=8080`만 하고 실행한 프로그램이 `PORT`를 못 읽습니다. 무엇이 빠졌나요?
    4. `NAME = devmart`가 `command not found`를 내는 이유는?
    5. 스크립트가 끝에 `exit 2`를 하면, CI는 이것을 성공으로 보나요, 실패로 보나요?

    ??? answer "정답"
        1. `>`는 정상 출력(1번)만 보냅니다. 에러는 2번 통로라 `2>`나 `2>&1`이 필요합니다.
        2. `grep -c "ERROR" 로그파일` (또는 `grep "ERROR" 로그파일 | wc -l`)
        3. `export PORT` — 환경 변수로 내보내지 않아 자식 프로그램에 보이지 않습니다.
        4. `=` 양옆의 빈칸 때문에 셸이 `NAME`을 명령으로 해석합니다.
        5. 실패 — 0이 아닌 종료 코드는 모두 실패입니다.

!!! diary "오늘의 배움일기 — 수업 뒤 각자"
    - 오늘 설치하면서 막혔던 곳 하나와, 어떻게 풀었는지 (또는 아직 못 푼 것)
    - hello-world 출력의 네 단계를 내 말로 한 줄씩 다시 써 보기
    - 내 GitHub 저장소 주소를 적고, 커밋이 몇 개인지 세어 보기
    - 내일 Docker 기본 시간에 꼭 알고 싶은 것 하나

## 참고 문헌

- McIlroy, M. D., Pinson, E. N., & Tague, B. A. (1978). UNIX time-sharing system: Foreword. *The Bell System Technical Journal*, 57(6).
- GNU. *Bash Reference Manual* — Redirections, Pipelines, Shell Parameter Expansion, Exit Status. gnu.org/software/bash/manual
- Shotts, W. (2019). *The Linux Command Line* (2nd ed.). No Starch Press. (무료 온라인판 linuxcommand.org)
- The Open Group. *POSIX.1-2024 Shell Command Language*.
