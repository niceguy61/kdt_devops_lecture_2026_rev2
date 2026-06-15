# 3교시: 포트 번호와 localhost 충돌

## 수업 목표
- `localhost`와 port의 관계를 설명할 수 있다.
- port 충돌이 발생했을 때 단순히 번호만 바꾸면 끝나지 않는 이유를 이해한다.
- Docker의 port binding 개념을 받아들일 준비를 한다.

## 시각 자료
![포트 번호와 localhost 충돌](https://raw.githubusercontent.com/niceguy61/kdt_devops_lecture_2026_rev2/main/week1/day5/assets/lesson-03-port-conflict.png)

## 도입 시나리오
강사가 다음 에피소드를 말한다.

```text
백엔드 서버를 켜려고 했더니 이런 메시지가 나온다.

address already in use
port 8080 is already allocated
```

학생에게 묻는다.

```text
이때 문제는 코드일까, 컴퓨터 환경일까?
```

정답은 둘 중 하나로 단정하지 않는다. 먼저 "이미 같은 입구를 누군가 쓰고 있다"는 현상으로 이해시킨다.

## 핵심 개념
`localhost`는 내 컴퓨터를 가리키는 이름이다. port는 그 컴퓨터 안에서 프로그램을 찾아가는 번호다.

```text
localhost:3000  -> 프론트엔드 개발 서버
localhost:8080  -> 백엔드 API 서버
localhost:3306  -> DB 서버
localhost:6379  -> cache 서버
```

같은 컴퓨터에서 같은 port를 두 프로그램이 동시에 쓸 수 없다. 그래서 충돌이 난다.

## 강의 진행 흐름
### 1. port를 주소가 아니라 "입구 번호"로 설명한다
학생들이 IP, DNS, socket 같은 용어에 익숙하지 않다면 이렇게 말한다.

```text
건물 이름이 localhost라면, port는 방 번호다.
같은 방 번호를 두 사람이 동시에 쓰겠다고 하면 충돌이 난다.
```

단, 비유에 머물지 않고 실제 표현으로 다시 돌아온다.

```text
프로세스는 네트워크 요청을 받기 위해 특정 port를 listen한다.
이미 listen 중인 port는 다른 프로세스가 같은 방식으로 사용할 수 없다.
```

### 2. port 번호만 바꾸면 생기는 연쇄 수정
예를 들어 DB port를 3306에서 3307로 바꾸면 다음도 함께 바뀐다.

| 바뀌는 것 | 예시 |
|---|---|
| backend `.env` | `DB_PORT=3307` |
| DB client 접속 정보 | Host, port |
| README 실행 설명 | 접속 명령 수정 |
| 테스트 설정 | integration test config |
| 스크린샷/문서 | 예전 port 정보 정리 |

즉 port 변경은 한 줄 수정이 아니라 연결된 설정 전체의 수정이다.

### 3. 충돌 원인 찾기
학생에게 원인 후보를 말하게 한다.

```text
1. 이전에 켠 서버가 아직 살아 있다.
2. OS 서비스로 등록된 프로그램이 자동 실행 중이다.
3. 다른 프로젝트가 같은 port를 사용 중이다.
4. IDE나 개발 도구가 내부 서버를 켜 두었다.
5. Docker, VM, WSL 같은 다른 실행 환경이 port를 잡고 있다.
```

오늘은 명령어 암기보다 관점이 중요하다. "누가 이 port를 쓰고 있는가"를 확인해야 한다는 점만 잡는다.

### 4. AI 엔지니어링과 연결한다
AI 앱에서도 port가 늘어난다.

- web UI
- API server
- vector DB
- model serving endpoint
- monitoring dashboard
- prompt playground

실험을 여러 개 동시에 띄우면 port 충돌은 흔하다. 특히 모델 서빙, vector DB, observability 도구를 같이 띄우면 port 설계가 필요해진다.

## 학생 활동
다음 상황을 주고 충돌 지도를 그리게 한다.

```text
프론트엔드: localhost:3000
백엔드 A: localhost:8080
백엔드 B: localhost:8080
DB A: localhost:3306
DB B: localhost:3306
Cache: localhost:6379
AI 실험 서버: localhost:8000
```

질문:

```text
1. 동시에 실행할 수 없는 것은 무엇인가?
2. port를 바꾸면 어느 설정을 같이 바꿔야 하는가?
3. 다른 사람이 이 환경을 재현하려면 어떤 표가 필요할까?
```

## Docker 연결
Docker에서는 container 안쪽 port와 내 컴퓨터에서 접속하는 port를 나누어 생각한다.

```text
host port -> container port
3307      -> 3306
```

오늘은 명령어를 외우지 않는다. 대신 다음 문장을 기억한다.

```text
Docker의 port binding은 내 컴퓨터의 입구 번호와 container 내부의 입구 번호를 연결하는 약속이다.
```

## 마무리 체크
학생이 말할 수 있어야 하는 문장:

```text
port 충돌은 실행 중인 프로그램들이 같은 네트워크 입구를 쓰려고 할 때 생기며, port 변경은 관련 설정 전체에 영향을 준다.
```
