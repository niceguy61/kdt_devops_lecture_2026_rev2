# 4교시: 환경변수와 설정 파일 지옥

## 수업 목표
- 코드와 설정을 분리하는 이유를 이해한다.
- 환경변수, `.env`, config file이 꼬일 때 생기는 문제를 설명한다.
- AI 기능에서 secret, endpoint, model 설정이 왜 더 민감해지는지 이해한다.

## 시각 자료
![환경변수와 설정 파일 지옥](https://raw.githubusercontent.com/niceguy61/kdt_devops_lecture_2026_rev2/main/week1/day5/assets/lesson-04-env-config-drift.png)

## 도입 시나리오
강사가 다음 장면을 말한다.

```text
내 컴퓨터에서는 로그인 기능이 된다.
친구 컴퓨터에서는 DB 연결이 안 된다.
배포 환경에서는 AI API 호출이 실패한다.

코드는 같은데 왜 결과가 다를까?
```

핵심은 "코드는 같아도 설정이 다르면 다른 프로그램처럼 동작한다"는 점이다.

## 핵심 개념
설정은 코드 밖에서 실행 동작을 바꾸는 값이다.

| 설정 | 예시 |
|---|---|
| DB 접속 정보 | `DB_HOST`, `DB_PORT`, `DB_NAME` |
| 외부 API | `API_URL`, `OPENAI_API_KEY` |
| 실행 모드 | `NODE_ENV`, `APP_ENV` |
| 보안 값 | secret key, token |
| 기능 플래그 | `ENABLE_AI_SEARCH=true` |
| 파일 경로 | upload directory, log directory |

설정을 코드에 직접 박아 넣으면 빠르게 만들 수는 있지만 환경을 바꿀 때 위험해진다.

## 강의 진행 흐름
### 1. 설정이 필요한 이유
같은 코드라도 환경마다 값이 달라진다.

```text
개발 환경: localhost DB 사용
테스트 환경: 테스트 DB 사용
운영 환경: 실제 DB 사용
```

이때 코드가 매번 바뀌면 안 된다. 그래서 설정을 밖으로 빼야 한다.

### 2. 설정이 꼬이는 대표 상황
학생들에게 실제로 자주 생기는 상황을 보여준다.

```text
.env 파일이 없다.
.env.example은 있는데 실제 값이 다르다.
README의 port와 .env의 port가 다르다.
변수 이름이 DB_HOST인지 DATABASE_HOST인지 헷갈린다.
secret을 GitHub에 올릴 뻔했다.
이전 프로젝트의 환경변수가 남아 있다.
터미널을 다시 열지 않아 변경값이 반영되지 않았다.
```

여기서 "환경변수는 보이지 않는 설정"이라 디버깅이 어렵다는 점을 강조한다.

### 3. 설정 drift
drift는 시간이 지나며 문서, 코드, 실제 환경이 서로 달라지는 현상이다.

| 위치 | 값 |
|---|---|
| README | `DB_PORT=3306` |
| `.env.example` | `DB_PORT=3307` |
| 내 컴퓨터 실제 환경변수 | `DB_PORT=3310` |
| backend 코드 기본값 | `DB_PORT=3306` |

이 상태에서는 "왜 내 컴퓨터만 안 되지?"가 반복된다.

### 4. AI 엔지니어링과 연결한다
AI 앱에서는 설정이 더 많고 비싸다.

- 어떤 모델을 쓸 것인가?
- temperature, max token, timeout은 얼마인가?
- embedding model은 무엇인가?
- vector index 이름은 무엇인가?
- API key는 어디서 주입되는가?
- 무료 한도나 비용 제한은 어떻게 걸 것인가?

특히 API key를 코드나 화면에 노출하면 안 된다. 학생들에게 "작동하는 것"과 "안전하게 작동하는 것"은 다르다고 말한다.

## 학생 활동
다음 `.env` 예시를 보고 위험 요소를 찾게 한다.

```text
DB_HOST=localhost
DB_PORT=3306
DB_NAME=app
API_URL=http://localhost:8080
AI_MODEL=gpt-example
OPENAI_API_KEY=sk-실제키를여기에쓰면안됨
ENABLE_AI_SEARCH=true
```

질문:

```text
1. README에 적어도 되는 값은 무엇인가?
2. GitHub에 올리면 안 되는 값은 무엇인가?
3. 친구 컴퓨터에서 바뀔 가능성이 큰 값은 무엇인가?
4. `.env.example`에는 어떤 형태로 적어야 하는가?
```

## Docker 연결
Docker에서는 실행할 때 환경변수를 주입할 수 있다. 나중에는 Compose 파일로 여러 프로그램의 설정을 한곳에서 관리한다.

오늘 기억할 문장:

```text
Docker는 설정을 없애는 도구가 아니라, 설정을 실행 단위와 함께 명시적으로 다루게 만드는 도구다.
```

## 마무리 체크
학생이 말할 수 있어야 하는 문장:

```text
코드가 같아도 환경변수와 설정 파일이 다르면 앱의 동작은 달라질 수 있다.
```
