# 7교시: 개인 면담 및 환경 점검 - Docker blocker triage

## 수업 목표
- Docker Desktop 실행, CLI 연결, image pull, port binding, log 확인 중 막힌 지점을 evidence로 분류한다.
- 개인 면담 시간에도 실행 80% 원칙을 유지해, 설명보다 재실행과 확인에 시간을 쓴다.
- blocker를 "안 됨"이 아니라 증상, 명령, 출력, 가설, 재확인으로 기록한다.

## 50분 흐름
| 시간 | 활동 | 비중 | 학생 산출 |
|---|---|---:|---|
| 0-5분 | blocker 기록 양식 공유 | 설명 10% | blocker template |
| 5-20분 | 개인별 Docker 상태 점검 | 실행 30% | version/pull status |
| 20-35분 | port/log 문제 재현과 복구 | 실행 30% | RCA mini note |
| 35-45분 | 면담 대상별 보충 조치 | 실행 20% | recheck evidence |
| 45-50분 | 해결/보류/다음 행동 분류 | 설명 10% | action item |

### Visual 1: Docker 트러블슈팅 랩
![Docker 트러블슈팅 랩](https://raw.githubusercontent.com/niceguy61/kdt_devops_lecture_2026_rev2/main/week2/day1/assets/lesson-07-docker-troubleshooting-lab.png)

이 이미지는 증상, 증거, 다음 행동을 나누어 blocker를 처리하는 흐름을 보여준다. 문제를 추측으로 처리하지 않고 `docker version`, `docker ps`, `docker logs`, `curl -I` 같은 출력으로 좁힌다.

## 점검 명령 세트

아래 명령은 순서대로 실행한다. 막히는 지점이 나오면 그 줄의 출력만 기록하지 말고 이전 단계의 정상 여부도 같이 기록한다.

```bash
docker version
docker pull nginx:latest
docker run -d --name paperclip-day1-nginx -p 18080:80 nginx:latest
docker ps --filter name=paperclip-day1-nginx
curl -I http://localhost:18080
docker logs paperclip-day1-nginx
docker stop paperclip-day1-nginx
docker rm paperclip-day1-nginx
```

## Linux 사전 테스트 기준값
| 단계 | 확인된 결과 |
|---|---|
| `docker version` | Client `29.0.2`, Server `29.3.1`, linux/amd64 |
| `docker pull nginx:latest` | `Image is up to date for nginx:latest` |
| `docker run -d ...` | container ID 출력 |
| `docker ps` | `0.0.0.0:18080->80/tcp`, name `paperclip-day1-nginx` |
| `curl -I` | `HTTP/1.1 200 OK` |
| `docker logs` | nginx entrypoint와 worker process start log |
| `docker stop`/`rm` | 각각 `paperclip-day1-nginx` 출력 |
| cleanup recheck | `docker ps --filter name=...` 헤더만 출력 |

## Blocker triage table
| 증상 | 먼저 볼 evidence | 가능한 원인 | 다음 행동 |
|---|---|---|---|
| `docker` command not found | terminal output | Docker CLI 미설치 또는 PATH 문제 | Docker Desktop 설치/terminal 재시작 |
| Server 연결 error | `docker version` Client/Server | Docker Desktop/daemon 미실행 | Desktop 실행 후 재확인 |
| pull 실패 | `docker pull` output | network, registry, image name | network/auth/image name 확인 |
| port 충돌 | `docker run` error, `docker ps` | host port 사용 중 | 기존 container 정리 또는 host port 변경 |
| HTTP 응답 없음 | `docker ps`, `curl -I` | port mapping 오류 또는 container 종료 | `docker logs`, `docker ps -a` 확인 |
| log에 앱 error | `docker logs` | container 내부 process 문제 | error line 기록 후 재현 |

## 개인 면담 기록 양식
```markdown
## Docker Blocker Note
- 문제 상황:
- 실행한 명령:
- 핵심 출력:
- 정상 기준과 다른 점:
- 가설:
- 시도한 조치:
- 재확인 결과:
- 다음 행동:
```

## 운영 관점
개인 면담 시간은 학생마다 다른 환경 차이를 줄이는 시간이다. macOS 기본 경로에서는 Docker Desktop running 상태, chip별 설치 파일, `docker version` Client/Server 연결을 우선 본다. Windows 사용자는 WSL 2, virtualization, 권한 조건을 별도 경로로 확인한다.

## 평가 기준
| 기준 | 2점 evidence |
|---|---|
| blocker 품질 | 증상, 명령, 출력, 가설, 재확인을 기록했다. |
| 실행 중심 | 면담 시간 대부분을 재실행과 확인에 사용했다. |
| 원인 분류 | daemon, image pull, port, log, 권한 중 어디 문제인지 분류했다. |
| 보안 | credential/token/MFA를 기록하지 않았다. |
| 다음 행동 | 해결, 보류, 보충 실습 중 하나로 상태를 분류했다. |

### 공식 근거 링크
- Docker Docs: Troubleshoot Docker Desktop, https://docs.docker.com/desktop/troubleshoot/
- Docker Docs: docker container logs, https://docs.docker.com/reference/cli/docker/container/logs/

### 다음 연결
다음 교시는 보충 실습이다. 해결된 학생은 같은 cycle을 반복해 손에 익히고, 해결되지 않은 학생은 blocker note를 기준으로 다음 행동을 정리한다.
