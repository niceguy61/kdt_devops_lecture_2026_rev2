# Week 1 Glossary: 컴퓨팅 펀더멘털과 운영 증거

이 용어집은 단어 암기장이 아니다. 각 용어를 "무엇을 확인해야 하는가", "어떤 evidence를 남겨야 하는가", "나중에 어떤 도구로 이어지는가"로 읽는다.

## Beginner Reading Rule
| 읽는 기준 | 질문 |
|---|---|
| 뜻 | 이 단어가 어떤 대상을 가리키는가 |
| Evidence | 내 컴퓨터에서 무엇으로 확인하는가 |
| 흔한 오해 | 초보자가 무엇과 헷갈리는가 |
| Later mapping | Docker, Kubernetes, AWS, Terraform에서 어떤 이름으로 다시 나오는가 |

## Spine Components
### Compute
- 뜻: CPU가 명령을 실행해 process를 움직이는 영역.
- Week 1 evidence: 실행 명령, process 이름, exit code.
- 확인 명령: `ps`, `python3 -m http.server`, `echo $?`.
- 흔한 오해: compute를 "서버 컴퓨터"로만 생각한다. 로컬에서 실행한 작은 process도 compute evidence다.
- Later mapping: Docker container, Kubernetes Pod, AWS EC2/ECS/Lambda.

### Memory
- 뜻: 실행 중인 process가 사용하는 임시 작업 공간.
- Week 1 evidence: memory 사용 관찰 note.
- 확인 명령: `ps`, Activity Monitor, System Monitor.
- 흔한 오해: memory와 storage를 모두 "저장 공간"으로 부른다. memory는 process가 꺼지면 사라지는 임시 작업 공간이다.
- Later mapping: container memory limit, Kubernetes requests/limits, instance size.

### Storage
- 뜻: 파일과 데이터가 저장되고 다시 읽히는 영역.
- Week 1 evidence: project path, `data/*.json`, README path.
- 확인 명령: `pwd`, `ls`, `cat`, `du`.
- 흔한 오해: 브라우저에 보이면 저장된 것이라고 생각한다. 실제 저장 위치는 file path로 확인해야 한다.
- Later mapping: Docker volume, Kubernetes Volume, AWS S3/EBS/RDS.

### Network
- 뜻: 요청이 주소, 포트, 프로토콜을 통해 이동하는 경로.
- Week 1 evidence: URL, localhost, port, HTTP status.
- 확인 명령: `curl -I http://localhost:8000`, browser, `hostname -I`.
- 흔한 오해: `localhost`를 인터넷 주소로 생각한다. `localhost`는 내 컴퓨터 자신을 가리킨다.
- Later mapping: Docker port binding, Kubernetes Service/Ingress, AWS VPC/ALB/security group.

### Process Lifecycle
- 뜻: 프로그램이 시작, 실행, 실패, 중지, 재시작되는 흐름.
- Week 1 evidence: start/check/stop/recheck command.
- 확인 명령: 시작 명령, `ps`, `Ctrl+C`, 재확인 명령.
- 흔한 오해: 창이 열려 있으면 서비스가 실행 중이라고 본다. 서비스 상태는 process와 HTTP response로 확인한다.
- Later mapping: Docker run/stop, Kubernetes rollout/probe, Terraform apply/destroy.

### Configuration
- 뜻: 같은 코드가 다른 환경에서 다르게 동작하도록 주입되는 값.
- Week 1 evidence: config key, environment variable name, secret non-exposure note.
- 확인 명령: `env | grep KEY`, config file path 확인.
- 흔한 오해: 설정 값을 코드에 바로 넣는다. 나중에 환경이 바뀌면 재사용과 보안이 어려워진다.
- Later mapping: Docker env, Kubernetes ConfigMap/Secret, AWS Parameter Store.

### Identity And Access
- 뜻: 누가 무엇을 할 수 있는지 정하는 계정, 권한, 인증 정보.
- Week 1 evidence: public/private repo decision, token non-exposure.
- 확인 방법: GitHub 로그인 상태, repository 권한, MFA 상태, push 실패 메시지.
- 흔한 오해: 인증 실패를 Git 오류로만 본다. 계정, token, repository 권한, credential cache가 모두 원인일 수 있다.
- Later mapping: Kubernetes ServiceAccount/RBAC, AWS IAM/MFA/role.

### Observability
- 뜻: 시스템 상태를 밖에서 판단하게 해주는 log, status, metric, event, trace.
- Week 1 evidence: log excerpt, HTTP status, RCA table.
- 확인 명령: `curl -I`, browser console, terminal output, log excerpt.
- 흔한 오해: "잘 되는 것 같다"를 evidence로 쓴다. 관찰 가능성은 다른 사람도 다시 확인할 수 있는 출력이어야 한다.
- Later mapping: Docker logs, Kubernetes events/probes, AWS CloudWatch/CloudTrail.

### Cost Or Resource Boundary
- 뜻: 컴퓨터 자원과 비용이 무한하지 않다는 제한.
- Week 1 evidence: paid API excluded note, local resource blocker.
- 확인 방법: 유료 API 사용 여부, cloud resource 생성 여부, 실행 중인 process 수, disk 사용량.
- 흔한 오해: 로컬 실습은 비용과 무관하다고 본다. 로컬에서도 disk, battery, memory, port 같은 자원 제한이 있다.
- Later mapping: Kubernetes capacity, AWS billing/budget, Terraform destroy.

## Tool And Setup Terms
| Term | 뜻 | 초보자 확인 기준 |
|---|---|---|
| Terminal | 명령을 입력하고 출력 evidence를 받는 인터페이스 | `pwd`가 현재 위치를 출력한다 |
| Shell | terminal 안에서 명령을 해석하는 프로그램 | macOS는 보통 zsh, Linux는 bash가 많다 |
| CLI | Command Line Interface. GUI 대신 명령으로 도구를 사용하는 방식 | `git --version`, `curl --version` 같은 명령이 실행된다 |
| PATH | shell이 실행 파일을 찾는 위치 목록 | 설치했는데 command not found면 PATH 문제일 수 있다 |
| Git | 로컬 변경 이력을 저장하는 version control 도구 | `git --version`이 출력된다 |
| GitHub | Git repository를 원격에서 저장하고 협업하는 서비스 | browser에서 로그인하고 repository를 볼 수 있다 |
| Repository | 코드와 문서의 변경 이력을 담는 저장소 | root에 `README.md`가 있다 |
| Commit | 변경 묶음에 메시지를 붙여 기록하는 행위 | `git log --oneline`에 기록이 남는다 |
| Push | 로컬 commit을 원격 repository로 올리는 행위 | GitHub 웹에서 README 변경이 보인다 |
| VS Code | 코드 편집기와 terminal을 함께 제공하는 개발 환경 | VS Code terminal에서 `pwd`가 실행된다 |
| Python 3 | Week 1 로컬 정적 서버 실행에 쓰는 언어/runtime | `python3 --version`이 출력된다 |
| curl | HTTP 요청과 응답 header를 CLI에서 확인하는 도구 | `curl -I https://example.com`이 status line을 출력한다 |
| Homebrew | macOS/Linux에서 CLI 도구를 설치하는 package manager | `brew --version`이 출력된다 |
| Package manager | OS에 소프트웨어를 설치/업데이트하는 도구 | macOS `brew`, Ubuntu `apt`, Fedora `dnf` |
| MFA | 로그인 시 password 외 추가 인증을 요구하는 보안 방식 | 인증 코드는 절대 기록하지 않는다 |
| PAT | Personal Access Token. GitHub API/CLI 인증에 쓰는 제한된 token | 값이 아니라 사용 여부와 권한 범위만 기록한다 |
| Secret | password, token, key처럼 노출되면 안 되는 값 | README, screenshot, terminal history에 남기지 않는다 |

## CLI Command Terms
| Command | 뜻 | evidence로 남길 것 |
|---|---|---|
| `pwd` | 현재 directory 출력 | 작업 path |
| `ls` | 파일 목록 출력 | 필요한 파일 존재 여부 |
| `cd` | directory 이동 | 이동 전후 path |
| `cat` | 파일 내용 출력 | 민감정보 없는 일부 내용 |
| `grep` | 텍스트에서 단서 검색 | 검색된 한 줄 |
| `curl -I` | HTTP header와 status 확인 | status line, 대표 header |
| `ps` | process 목록 확인 | 실행 중인 process 이름 |
| `kill` | process에 종료 signal 전송 | 대상 process를 확인한 뒤 사용 |
| `env` | 환경변수 목록 출력 | secret 값이 아닌 key 이름 |

## Professional Terms
### DevOps
- 뜻: 개발과 운영을 잇는 문화, practice, automation의 조합.
- 공식 참고: https://aws.amazon.com/devops/what-is-devops/
- Week 1 사용 위치: Day 1, Day 5 handoff.

### Handoff
- 뜻: 다른 사람이 산출물을 이어받아 실행, 확인, 문제 대응을 할 수 있게 넘기는 것.
- Week 1 evidence: README, known issue, risk table.

### RCA
- 뜻: 장애나 실패를 증상, 영향, 원인 후보, 수정, 재확인, 예방으로 기록하는 절차.
- 공식 연결: Google SRE postmortem culture.

### README
- 뜻: 저장소의 목적, 실행 방법, 확인 방법, 제한을 설명하는 기본 문서.
- 공식 참고: https://docs.github.com/en/repositories/managing-your-repositorys-settings-and-features/customizing-your-repository/about-readmes

### Future Anchor
- 뜻: Week 1에서 깊게 가르치지 않고, 나중에 배울 기술이 어떤 문제를 해결하는지만 연결하는 용어.
- 예: Docker, Kubernetes, AWS, Terraform, Well-Architected, DORA.

## Evidence Words
| Term | 뜻 | 좋은 예 |
|---|---|---|
| Evidence | 다른 사람이 다시 확인할 수 있는 증거 | command, output, path, URL, status |
| Blocker | 진행을 막는 조건 | OS, 명령, 에러, 시도한 문서 URL 포함 |
| Runbook | 반복 실행/점검/복구 절차 문서 | start/check/stop/troubleshoot |
| Handoff note | 다음 사람이 이어받을 수 있게 남기는 요약 | 실행 조건, known issue, 확인 결과 |
| RCA | 실패를 증상, 영향, 원인 후보, 조치, 재확인으로 정리하는 기록 | "왜 추정했는지"와 "어떻게 재확인했는지" 포함 |
