# Week 1 Day 2: 작업공간, Git/GitHub, 공식 문서, CLI, 컴퓨팅 구성요소 입문

## 개요
Day 2는 Day 1 OT에서 정한 개인 목표와 막힘 기록을 실제 학습 작업공간으로 옮기는 날이다. 학생은 GitHub repository, VS Code 터미널, CLI 확인 기록, 공식 문서 읽기 기록을 만들고, compute, memory, storage, network를 "서비스를 실행하기 위해 확인해야 하는 상태"로 이해한다.

오늘은 미니앱을 만들지 않는다. 목표는 구현이 아니라 실행 환경을 설명하고, 명령 결과를 근거로 남기고, 모르는 내용을 공식 문서와 실제 출력으로 검증하는 기본 습관을 만드는 것이다.

## 챌린저 빠른 시작
Day 2에서 막히는 대부분의 문제는 "도구가 없는지", "도구는 있는데 터미널에서 못 찾는지", "계정 인증이 막힌 것인지"가 섞여서 생긴다. 먼저 설치 가이드를 보고 한 줄씩 확인한다.

- 설치 가이드: [필수 소프트웨어 설치 가이드](../../docs/software-installation-guide.md)
- 오늘 반드시 확인할 명령: `git --version`, `pwd`, `python3 --version`, `curl --version`
- VS Code 확인: GUI에서 `Terminal > New Terminal`을 열고 `pwd`, `git --version`을 실행한다.
- 실패 기록 형식: "OS / 실행 명령 / 에러 한 줄 / 확인한 공식 문서 URL"

## 학습 목표
- Day 1 OT 산출물을 개인 작업공간과 GitHub repository로 연결한다.
- Git, GitHub, VS Code 터미널의 준비 상태를 공개 가능한 확인 기록으로 기록한다.
- 공식 문서에서 사전 조건, 버전, warning, 명령을 찾는다.
- CLI 명령을 "무엇을 확인하는가"라는 운영 질문과 연결한다.
- compute, memory, storage, network의 차이를 로컬 환경 확인 기록으로 설명한다.

## 교시 목록
- 1교시: Day1 OT 연결 및 학습 작업공간 준비
- 2교시: GitHub 계정, Git 설치, VS Code 확인
- 3교시: Git/GitHub 기본 실습 - repository, clone, commit, push, README 확인 기록
- 4교시: 공식 문서 읽기와 AI 답변 검증
- 5교시: Linux/CLI 기본 - `pwd`, `ls`, `cd`, `cat`, `grep`, `curl`, `ps`, `kill`, `env`
- 6교시: Compute와 process - CPU, process, thread, 명령, exit code
- 7교시: Memory와 storage - RAM, filesystem, 경로, persistence, permission
- 8교시: Network/HTTP 기본 - localhost, IP, DNS, TCP, port, request/response, status code

## 공식 참고 자료
| 주제 | 참고 자료 | 오늘 확인할 키워드 |
|---|---|---|
| GitHub account | https://docs.github.com/en/get-started/start-your-journey/creating-an-account-on-github | account, email, MFA |
| Git install | https://git-scm.com/book/en/v2/Getting-Started-Installing-Git | install, 버전, OS |
| VS Code | https://code.visualstudio.com/docs | 터미널, command line |
| README | https://docs.github.com/en/repositories/managing-your-repositorys-settings-and-features/customizing-your-repository/about-readmes | README, repository root |
| HTTP | https://developer.mozilla.org/en-US/docs/Web/HTTP/Guides/Overview | request, response, 상태 |
| Coreutils | https://www.gnu.org/software/coreutils/manual/ | pwd, ls, cat |
| Linux man-pages | https://www.kernel.org/doc/man-pages/ | ps, kill, env |

## 필수 확인 기록
| 확인 기록 | 제출 기준 |
|---|---|
| GitHub repository URL | 공개해도 되는 repository 주소 |
| Git 버전 | `git --version` 출력 |
| VS Code 터미널 | 터미널에서 `pwd` 실행 결과 또는 막힘 기록 |
| README 확인 표 | repository root의 README에 표 작성 |
| 공식 문서 읽기 기록 | URL, 버전/사전 조건/warning 기록 |
| CLI 명령 확인 표 | 명령, 확인한 상태, 결과 요약 |
| Component concept 기록 | compute/memory/storage/network 구분 |

## 50분 수업 운영 기준
각 교시는 다음 흐름을 기본으로 한다.

| 시간 | 활동 |
|---|---|
| 0-5분 | 이전 교시 확인 기록 점검 |
| 5-15분 | 개념 설명과 현업 문제 연결 |
| 15-35분 | 명령 실습, 관찰, 기록 |
| 35-45분 | 흔한 실패와 오해 정리 |
| 45-50분 | 확인 질문과 다음 주차 매핑 |

## 비용/보안 주의사항
- 오늘은 클라우드 리소스를 만들지 않으므로 비용이 발생하지 않아야 한다.
- GitHub 비밀번호, 토큰, MFA 코드, email 인증 코드는 README, 스크린샷, 화면 공유에 남기지 않는다.
- 비밀값은 "값"이 아니라 "필요 여부와 관리 방식"만 문서화한다.

## 수업 종료 전 체크리스트
- [ ] GitHub repository URL을 기록했다.
- [ ] `git --version` 결과를 기록했다.
- [ ] VS Code 터미널 또는 막힘 기록을 기록했다.
- [ ] README 확인 표를 commit했다.
- [ ] 공식 문서 읽기 기록을 작성했다.
- [ ] CLI 명령 확인 표를 작성했다.
- [ ] compute, memory, storage, network를 한 문장씩 설명했다.

## 다음 주차 매핑
Day 2의 네 가지 구성요소는 이후 모든 주차의 spine이다. Docker는 process와 filesystem을 image/container로 묶고, Kubernetes는 process와 network entry를 Pod/Service로 관리한다. AWS는 compute/storage/network를 계정과 권한이 있는 관리형 리소스로 제공하고, Terraform은 그 리소스의 desired state를 코드로 기록한다.

## 시각 자료
![Week 1 computing component spine](../assets/week1-computing-spine.png)

이 이미지는 Day2의 compute, memory, storage, network 개념이 Week2 Docker, Week4 Kubernetes, Week5 AWS, Week6 Terraform으로 어떻게 확장되는지 보여준다.
