# 6교시: CloudWatch Logs 기본

![CloudWatch Logs flow](./assets/lesson-06-cloudwatch-logs.png)

## 수업 목표
- app stdout/stderr가 CloudWatch Logs의 log group/log stream으로 연결되는 흐름을 이해한다.
- ECS/App Runner logs 위치를 찾는다.
- log가 없을 때 logging 설정, service 상태, app 실행 여부를 확인한다.

## 오늘 반드시 가져갈 것
| 필수 개념 | 왜 필수인가 | 놓치면 생기는 문제 | 확인 지점 |
|---|---|---|---|
| Log group | 같은 목적의 log stream 묶음이다 | 로그 위치를 못 찾는다 | CloudWatch Logs |
| Log stream | task/instance/deployment 단위 log 흐름이다 | 어떤 실행 단위의 로그인지 모른다 | stream name/time |
| stdout/stderr | container app log의 기본 출구다 | 파일 로그만 찾다가 놓친다 | app output |
| Retention | log도 저장 비용과 보존 정책이 있다 | 불필요한 로그가 계속 쌓인다 | retention setting |

## CloudWatch Logs 구조
```mermaid
flowchart LR
  App["Container stdout/stderr"] --> Driver["Log config"]
  Driver --> Group["Log Group"]
  Group --> Stream1["Log Stream task A"]
  Group --> Stream2["Log Stream task B"]
  Group --> Search["Filter/Search"]
```

## ECS logs
ECS task definition에는 log configuration이 들어갈 수 있다. `awslogs` driver를 쓰면 CloudWatch Logs로 container output을 보낼 수 있다.

| 확인 | 의미 |
|---|---|
| log group | service/app 단위 log 묶음 |
| log stream prefix | task/container 구분 |
| timestamp | 장애 시점 비교 |
| error message | config/port/crash 원인 |

## App Runner logs
App Runner도 service log를 CloudWatch에서 확인할 수 있다. build/deploy/app log가 나뉘어 보일 수 있으므로 "어느 단계의 로그인가"를 구분한다.

| 로그 | 질문 |
|---|---|
| deployment log | image pull/build/deploy가 성공했는가 |
| application log | app이 시작되고 요청을 처리하는가 |
| service event | service 상태 전환이 있었는가 |

## Log가 없을 때
| 증상 | 첫 확인 |
|---|---|
| log group이 없음 | logging 설정, service 생성 여부 |
| log stream이 없음 | task가 실제 실행됐는가 |
| error가 안 보임 | app이 stdout/stderr로 출력하는가 |
| 시간이 안 맞음 | time range, Region |


## 50분 수업 운영 흐름
| 시간 | 활동 | 확인할 evidence |
|---|---|---|
| 0~10분 | log group/stream 개념 | CW Logs map |
| 10~20분 | ECS/App Runner log 위치 찾기 | log group name |
| 20~30분 | 정상 요청 로그 확인 | timestamp/event |
| 30~40분 | 오류 로그 해석 | error pattern |
| 40~50분 | retention/cost 확인 | retention setting |

## 로그를 읽는 순서
먼저 시간 범위를 장애 시점으로 맞춘다. 그 다음 service/task/deployment에 해당하는 log stream을 고른다. 마지막으로 error, warning, startup message, request log를 본다. 로그를 볼 때 가장 흔한 실수는 time range가 맞지 않아 "로그가 없다"고 판단하는 것이다.

## 로그와 이벤트 구분
CloudWatch Logs는 app이 남긴 출력이고, ECS/App Runner event는 service lifecycle 상태 변화다. task가 왜 stopped 되었는지는 ECS task stopped reason이나 service event가 더 직접적일 수 있다. app stack trace는 log stream에서 본다.

## 보존 정책
학습 계정에서 log group이 무기한 보존되면 비용은 작더라도 관리 부채가 된다. 실습용 log group에는 retention을 짧게 두는 습관을 만든다.

## 장애 예시
| 로그 | 해석 | 다음 확인 |
|---|---|---|
| listen EADDRINUSE | port 충돌 | container port/process |
| missing env | config 누락 | env/secret 설정 |
| connection refused DB | DB endpoint/SG | Day4 연결 |
| permission denied | IAM/role/파일 권한 | task role, policy |

## 강사 보강 노트
이 교시는 `CloudWatch Logs`을 학생이 말로 설명할 수 있게 만드는 데 초점을 둔다. Console 화면을 따라 누르는 시간으로만 흘러가면 학생은 성공 화면은 보지만, 다음 날 같은 resource를 혼자 다시 만들거나 장애를 설명하지 못한다. 각 단계마다 "지금 무엇을 결정했는가", "그 결정은 비용/보안/관찰 중 어디에 영향을 주는가"를 짧게 되묻는다.

## 학생이 자주 흔들리는 지점
| 흔들리는 지점 | 강사 개입 문장 |
|---|---|
| Region을 틀림 | "지금 화면에서 그 판단을 증명하는 값이 어디에 있나요?" |
| stdout/stderr가 어디로 가는지 모름 | "이 값이 바뀌면 접속, 비용, 권한 중 무엇이 먼저 달라질까요?" |
| retention을 무한정 방치함 | "성공 화면 말고 실패했을 때 다시 볼 evidence를 남겼나요?" |

## 실습 중 멈춤 포인트
- 첫 번째 멈춤: 학생이 resource를 생성하기 전에 이름, Region, tag, 예상 비용 발생 지점을 말하게 한다.
- 두 번째 멈춤: 성공 화면이 나온 직후 resource ID와 상태값을 evidence note에 적게 한다.
- 세 번째 멈춤: 실패나 지연이 생기면 새로 클릭하기 전에 이전 단계의 화면과 명령을 다시 보게 한다.
- 네 번째 멈춤: 정리 단계에서 "삭제했다"가 아니라 "검색해도 남아 있지 않다"를 확인하게 한다.

## 확인 질문
1. 오늘 만든 resource가 어느 Region과 어느 계정 경계에 있는가?
2. 이 resource가 비용을 만들기 시작하는 시점은 언제인가?
3. 접속이 실패하면 app, network, permission 중 무엇을 먼저 확인할 것인가?
4. 수업이 끝난 뒤 남겨도 되는 resource와 지워야 하는 resource는 무엇인가?

## 제출 evidence 기준
| evidence | 좋은 예 | 부족한 예 |
|---|---|---|
| 화면 캡처 | log group name | 성공 toast만 보이는 캡처 |
| 설정 기록 | log stream timestamp | "기본값 사용"이라고만 적음 |
| 운영 판단 | retention setting | "잘 됨", "안 됨"으로만 적음 |

## Evidence Note
```markdown
# W5D3S6 CloudWatch Logs
- Service:
- Log group:
- Log stream:
- 확인한 시간대:
- 정상 log:
- error/warning:
- retention:
```

## 혼자 다시 따라오기
- 최소 재현 경로: CloudWatch Logs에서 오늘 service의 log group과 stream을 찾고 요청 시각 전후 로그를 확인한다.
- 공식 문서 키워드: `CloudWatch Logs`, `log group`, `log stream`, `ECS awslogs`.
- 스스로 확인할 화면: CloudWatch Logs groups, stream events, ECS task logs, App Runner logs.
- 흔한 실패 3개: Region이 다름, time range가 맞지 않음, service는 stopped인데 로그를 찾음.
- 다음 준비 상태: app 장애 시 log group과 log stream을 찾아 첫 error를 읽을 수 있어야 한다.

## 한 줄 요약
```text
CloudWatch Logs는 container가 남긴 stdout/stderr를 운영 증거로 모으는 곳이다.
```
