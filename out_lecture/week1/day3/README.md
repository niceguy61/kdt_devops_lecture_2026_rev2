# Week 1 Day 3: 로컬 정적 서버, 로그/설정, 재현성, RCA, AI 검증, spine 매핑

## Overview
Day 3는 Day 2에서 준비한 repository와 CLI evidence를 사용해 로컬 정적 서버를 실행하고 관찰하는 날이다. 학생은 `python3 -m http.server`로 정적 파일을 제공하고, browser와 `curl`로 HTTP status를 확인하며, log, config, secret, 실행 조건, 재현성, RCA, AI 검증 기준을 문서화한다.

중요한 제한: Day 3에서는 미니앱 구현을 시작하지 않는다. HTML 파일은 정적 서버 확인을 위한 최소 파일이며, 기능 개발이나 앱 설계는 Day 4 이후로 넘긴다. 오늘의 목표는 "작게 실행하고, 정확히 관찰하고, 재현 가능하게 기록하는 능력"이다.

## Learning Goals
- 로컬 정적 서버의 source, runtime, command, port, data, dependency를 설명한다.
- log, config, secret을 구분하고 secret value를 노출하지 않는다.
- README에 start/check/stop/expected result/troubleshooting을 작성한다.
- 실패를 reproduce, observe, hypothesize, fix, recheck, prevent 순서로 기록한다.
- AI Coding Tool 답변을 공식 문서, 실행 결과, 보안/비용 기준으로 검증한다.
- process, file, port, HTTP, log evidence를 Docker/Kubernetes/AWS/Terraform spine에 매핑한다.

## Lesson Index
- 1교시: 로컬 정적 서버 실행 - `python3 -m http.server`, browser/curl 확인
- 2교시: Log, config, secret - stdout/stderr, error message, env var, secret non-exposure
- 3교시: 서비스 실행 조건 - source, runtime, command, port, data, dependency
- 4교시: 재현 가능성 - README, path, expected result, clean directory
- 5교시: 실패 분석 라이프사이클 - reproduce, observe, hypothesize, fix, recheck, prevent
- 6교시: 관찰 가능성과 배포 preview - logs/status evidence, build, artifact, release, deploy, rollback
- 7교시: AI Coding Tool 사용 원칙 - 공식 문서 확인, 실행 검증, secret/cost/API 위험
- 8교시: 컴퓨팅 spine 매핑 노트

## Official References
| Topic | Reference | 오늘 확인할 키워드 |
|---|---|---|
| Python http.server | https://docs.python.org/3/library/http.server.html | directory, port, security warning |
| Python command line | https://docs.python.org/3/using/cmdline.html | `-m` module execution |
| MDN HTTP | https://developer.mozilla.org/en-US/docs/Web/HTTP/Guides/Overview | request, response, status |
| Twelve-Factor App config | https://12factor.net/config | config, env vars, credentials |
| GitHub README | https://docs.github.com/en/repositories/managing-your-repositorys-settings-and-features/customizing-your-repository/about-readmes | start/check/troubleshooting |
| Google SRE Book | https://sre.google/sre-book/monitoring-distributed-systems/ | monitoring, symptoms, causes |

## Required Evidence
| Evidence | 제출 기준 |
|---|---|
| Service execution contract | source/runtime/command/port/data/dependency |
| HTTP check | browser 또는 `curl -I` status |
| Log/config/secret note | log example, config key, secret non-exposure |
| Reproducibility checklist | clean directory 기준 실행 절차 |
| RCA record | 404 또는 port conflict 등 하나의 실패 분석 |
| AI verification note | 공식 문서/실행/secret/cost/API 위험 검증 |
| Computing spine mapping | Docker/Kubernetes/AWS/Terraform 연결 표 |

## 비용/보안 주의사항
- 오늘은 로컬 서버만 실행한다. 외부 클라우드 리소스, 유료 API, 배포 서비스 가입을 요구하지 않는다.
- `http.server`는 학습용 로컬 정적 서버다. production web server로 사용하지 않는다.
- secret value는 README와 화면 공유에 기록하지 않는다. config key 이름과 관리 원칙만 기록한다.

## 수업 종료 전 체크리스트
- [ ] `python3 -m http.server 8000`을 실행했다.
- [ ] `curl -I http://localhost:8000` 또는 browser로 status를 확인했다.
- [ ] server terminal log에서 request evidence를 찾았다.
- [ ] 실행 조건 6가지를 표로 작성했다.
- [ ] README 재현성 절차를 작성했다.
- [ ] 하나의 실패를 RCA로 기록했다.
- [ ] AI 답변 검증표를 작성했다.
- [ ] spine mapping 표를 완성했다.

## 다음 주차 매핑
Day 3의 로컬 정적 서버는 이후 Docker image, Kubernetes Deployment/Service, AWS hosting, Terraform-managed infrastructure로 이어지는 가장 작은 실행 단위다. 단, 오늘은 구현을 늘리지 않고 실행 조건과 evidence만 고정한다.

## Visual Support
![Local service evidence flow](https://raw.githubusercontent.com/niceguy61/kdt_devops_lecture_2026_rev2/main/week1/assets/week1-service-evidence-flow.png)

이 이미지는 Day3의 파일 작성, 실행 명령, 프로세스, 포트, HTTP 상태, 로그, README, RCA 흐름을 하나의 evidence chain으로 연결한다.
