# 6교시: 빠르게 같은 환경을 만들고 싶다면

## 수업 목표
- "내 컴퓨터에서는 된다"가 충분한 설명이 아님을 이해한다.
- 재현 가능한 실행 환경을 만들기 위해 기록해야 할 항목을 정리한다.
- Dockerfile과 Compose가 등장하기 전, 왜 환경 문서화가 필요한지 이해한다.

## 시각 자료
![빠르게 같은 환경 만들기](https://raw.githubusercontent.com/niceguy61/kdt_devops_lecture_2026_rev2/main/week1/day5/assets/lesson-06-reproducible-environment.png)

## 도입 시나리오
강사가 다음 상황을 제시한다.

```text
새 컴퓨터를 받았다.
어제 만든 앱을 다시 실행해야 한다.

그런데 기억나는 것은 "npm install 했던 것 같은데..." 정도다.
```

학생들에게 묻는다.

```text
어제의 내 컴퓨터 환경을 오늘 새 컴퓨터에 다시 만들려면 무엇이 필요할까?
```

## 핵심 개념
재현 가능성은 같은 입력과 절차로 같은 결과를 다시 만들 수 있는 능력이다. 개발 환경에서는 다음을 뜻한다.

| 항목 | 필요한 기록 |
|---|---|
| OS | Windows, macOS, Linux, WSL 여부 |
| runtime | Node.js/Python/Java 버전 |
| package manager | npm, pnpm, pip, poetry |
| dependency | lock file, requirements |
| external program | DB, cache, queue |
| port | 접속 번호 목록 |
| environment variable | `.env.example` |
| initial data | seed data, migration |
| start command | 실행 순서 |
| check command | 정상 확인 방법 |
| stop command | 종료 방법 |

## 강의 진행 흐름
### 1. 설치 가이드와 실행 가이드는 다르다
설치 가이드는 필요한 것을 컴퓨터에 넣는 절차다. 실행 가이드는 그것을 어떤 순서로 켜고 확인하는 절차다.

```text
설치: Node.js 설치, DB 설치, package 설치
실행: DB 켜기, backend 켜기, frontend 켜기, 브라우저 확인
검증: health check, sample login, log 확인
종료: 서버 중지, DB 중지
```

초보 수업에서는 설치까지만 말하면 부족하다. 실행과 종료까지 있어야 다음 사람이 따라올 수 있다.

### 2. 같은 환경을 만들기 어렵게 하는 것
학생들이 직접 겪는 장애를 나열한다.

```text
설치 링크가 바뀐다.
버전이 자동으로 최신 버전으로 설치된다.
내가 중간에 클릭한 옵션을 기억하지 못한다.
터미널 경로가 다르다.
이미 설치된 프로그램 때문에 결과가 달라진다.
DB 초기 데이터가 다르다.
환경변수 값이 빠진다.
```

여기서 "설명 가능한 절차"와 "자동화 가능한 절차"의 차이를 설명한다. Docker는 나중에 이 절차를 더 많이 자동화하게 해 준다.

### 3. README를 실행 계약으로 본다
README는 소개 문서가 아니라 실행 계약이어야 한다.

```text
1. prerequisites
2. install
3. configure
4. start
5. check
6. stop
7. troubleshoot
```

학생들이 만든 README가 이 순서를 갖추면 Week2 Docker 수업에서 Dockerfile/Compose로 옮기기 쉽다.

### 4. AI 엔지니어링과 연결한다
AI 실험은 재현성이 특히 어렵다.

- 모델 버전이 바뀐다.
- prompt가 바뀐다.
- temperature가 다르면 결과가 달라진다.
- embedding model이 바뀌면 검색 결과가 달라진다.
- 외부 API 응답이 시점에 따라 달라질 수 있다.

그래서 AI 앱에서는 코드뿐 아니라 model, prompt, config, sample input, expected behavior를 함께 기록해야 한다.

## 학생 활동
수업에서 사용한 앱을 기준으로 "새 컴퓨터 실행 체크리스트"를 작성한다.

```text
필요한 프로그램:
필요한 버전:
필요한 port:
필요한 환경변수:
초기 데이터:
실행 순서:
정상 확인 방법:
중지 방법:
자주 나는 오류:
```

공유할 때는 완벽한 답보다 빠진 항목을 찾는 데 집중한다.

## Docker 연결
오늘의 내용을 Docker 용어로 옮기면 다음과 같다.

| 오늘의 문서 항목 | Docker에서 이어질 항목 |
|---|---|
| 필요한 프로그램과 버전 | base image, image tag |
| 설치 명령 | Dockerfile layer |
| 실행 명령 | CMD, ENTRYPOINT |
| 환경변수 | env, `.env` |
| port 목록 | ports |
| DB와 backend 동시 실행 | compose services |
| 초기 데이터 | volume, init script |

오늘 기억할 문장:

```text
Docker를 배우기 전에 먼저 "내 환경을 설명할 수 있어야" Docker가 무엇을 줄여 주는지 보인다.
```

## 마무리 체크
학생이 말할 수 있어야 하는 문장:

```text
재현 가능한 환경은 설치, 설정, 실행, 확인, 종료 절차가 문서로 남아 있어야 한다.
```
