# 4교시: bind mount로 runtime file 제공

## 수업 목표
- bind mount가 host path를 container path에 연결하는 방식임을 설명한다.
- `:ro` read-only mount의 의미를 확인한다.
- nginx container가 host disk의 HTML을 제공하는 과정을 검증한다.

## 50분 흐름
| 시간 | 활동 | 비중 | 산출 |
|---|---|---:|---|
| 0-8분 | Day 2 image COPY와 bind mount 비교 | 설명 15% | 비교표 |
| 8-18분 | mount source/destination 설명 | 설명 20% | mount note |
| 18-32분 | nginx bind mount 실행 | 실행 30% | HTTP evidence |
| 32-42분 | inspect로 mount mode 확인 | 실행 20% | `RW:false` |
| 42-50분 | host path 위험 정리 | 설명 15% | risk note |

### Visual 1: Bind mount runtime file flow
![Bind mount runtime file flow](https://raw.githubusercontent.com/niceguy61/kdt_devops_lecture_2026_rev2/main/week2/day3/assets/lesson-04-bind-mount-runtime-files.png)

Day 3의 bind mount 실습은 host disk의 HTML directory를 nginx container의 `/usr/share/nginx/html`에 연결한다. 이미지는 port 접근 흐름을 함께 보여준다.

## 핵심 설명
Day 2의 `COPY`는 build 시점에 파일을 image 안에 넣는다. Day 3의 bind mount는 run 시점에 host path를 container path에 연결한다. 그래서 host file을 바꾸면 container가 읽는 파일도 달라질 수 있다.

bind mount는 개발 중 빠른 확인에 좋지만, 운영 handoff에서는 host path 의존성을 정확히 남겨야 한다. 다른 사람의 컴퓨터에 같은 path가 없으면 같은 명령이 실패하거나 빈 directory가 mount될 수 있다.

`:ro`는 read-only mount다. container가 host file을 읽을 수는 있지만 쓸 수는 없다. 웹 정적 파일 제공처럼 container가 파일을 수정할 필요가 없는 경우 read-only가 더 안전하다.

## 실행 명령
```bash
docker run -d \
  --name paperclip-day3-web \
  -p 18083:80 \
  -v "$PWD/week2/day3/labs/runtime-site/html:/usr/share/nginx/html:ro" \
  nginx:1.27-alpine

curl -s http://localhost:18083 | grep runtime-site-v1
docker inspect paperclip-day3-web --format '{{json .Mounts}}'
```

## Linux 사전 테스트 결과
HTTP body:

```text
runtime-site-v1
```

mount inspect:

```text
"Type":"bind"
"Source":"/mnt/d/paperclip/week2/day3/labs/runtime-site/html"
"Destination":"/usr/share/nginx/html"
"Mode":"ro"
"RW":false
```

## COPY와 bind mount 비교
| 구분 | `COPY` | bind mount |
|---|---|---|
| 시점 | build time | run time |
| 위치 | image layer 안 | host filesystem |
| 수정 반영 | rebuild 필요 | host file 변경 시 반영 가능 |
| 재현성 | image만 있으면 쉬움 | host path 필요 |
| 운영 위험 | image에 secret 포함 위험 | host path/권한 의존 |

## 핵심 유의사항
bind mount source path는 host 기준이다. container 내부 path가 아니다. `-v "$PWD/...:/usr/share/nginx/html:ro"`에서 왼쪽은 host path, 오른쪽은 container path다.

path가 틀리면 nginx가 기본 page를 보여주거나, 빈 directory가 mount될 수 있다. HTTP 200만 보고 정상이라고 판단하지 말고 body text까지 확인해야 한다.

Windows 사용자는 Docker Desktop file sharing, WSL path, 권한 설정 때문에 bind mount가 다르게 보일 수 있다. macOS 중심 실습에서는 repository path를 기준으로 진행하고, Windows는 WSL2 안의 Linux path에서 실행하는 것을 권장한다.

## 자주 놓치는 지점
| 놓치는 지점 | 증상 | 확인 |
|---|---|---|
| source/destination 순서 혼동 | 파일이 안 보임 | `docker inspect .Mounts` |
| `:ro` 의미 누락 | container가 쓸 수 있다고 생각 | `RW:false` |
| host file 저장 누락 | 변경 반영 안 됨 | host file 내용 확인 |
| browser cache | 예전 내용 보임 | `curl -s` 사용 |
| path 공백/상대 경로 | mount 실패 | 절대 경로 또는 `$PWD` |

## mount evidence 읽기
`docker inspect`의 `.Mounts`에서 최소 네 가지를 본다.

```text
Type
Source
Destination
RW
```

`Type`이 `bind`이면 host path 직접 연결이다. `RW:false`이면 read-only다. `Destination`은 container 내부에서 process가 읽는 path다.

## 운영 관점
bind mount는 source code를 실시간으로 반영해야 하는 개발 환경에서 유용하다. 하지만 배포 artifact로는 image build가 더 재현 가능하다. "개발 편의"와 "배포 재현성"을 같은 것으로 보지 않는다.

## 확장 실습: host 파일 변경 확인
`index.html`의 `runtime-site-v1`을 `runtime-site-v2`로 바꾸는 상황을 가정한다. bind mount에서는 image rebuild 없이 container가 host file을 다시 읽을 수 있다.

확인 흐름:

```bash
curl -s http://localhost:18083 | grep runtime-site-v1
# host 파일 수정 후
curl -s http://localhost:18083 | grep runtime-site-v2
```

주의:
- 실제 수업 자료를 영구 수정하지 않으려면 변경 전후를 기록하고 원복한다.
- browser cache가 의심되면 `curl -s`로 확인한다.
- bind mount는 host 파일 변경이 즉시 보일 수 있지만, image artifact 자체가 바뀐 것은 아니다.

## 배포 관점 질문
| 질문 | 판단 |
|---|---|
| 이 파일이 image에 포함되어야 하는가 | 배포 재현성을 원하면 `COPY` |
| 개발 중 빠른 반영이 필요한가 | bind mount |
| container가 host 파일을 써야 하는가 | 필요 없으면 `:ro` |
| host path가 모든 팀원에게 같은가 | 다르면 README에 기준 경로 명시 |
| 운영 환경에서 host path를 믿을 수 있는가 | 아니라면 image/volume 구조 검토 |

## 보안 유의사항
bind mount는 host filesystem 일부를 container에 노출한다. source path를 넓게 잡으면 필요 없는 파일까지 container가 읽을 수 있다.

좋은 mount:

```text
week2/day3/labs/runtime-site/html:/usr/share/nginx/html:ro
```

위험한 mount:

```text
$HOME:/usr/share/nginx/html
```

두 번째 예시는 home directory 전체를 container에 노출할 수 있으므로 실습 기준으로도 부적절하다.

## 기록 템플릿
```markdown
## Lesson 4 Bind Mount Evidence
- container:
- host source:
- container destination:
- mode:
- RW:
- HTTP body:
- COPY와 다른 점:
- path 오류 시 확인할 명령:
```

## 마무리 점검
```text
bind mount의 왼쪽 path는 ____ 기준이다.
오른쪽 path는 ____ 내부 기준이다.
:ro는 container가 host file을 ____ 수 없게 한다.
```

## cleanup
```bash
docker rm -f paperclip-day3-web
```

## 평가 기준
| 기준 | 2점 evidence |
|---|---|
| mount | source/destination을 구분했다 |
| mode | read-only mount를 확인했다 |
| HTTP | mounted file이 제공됨을 확인했다 |
| 비교 | `COPY`와 bind mount를 구분했다 |

### 공식 근거 링크
- Docker bind mounts: https://docs.docker.com/engine/storage/bind-mounts/
- Docker storage: https://docs.docker.com/engine/storage/
