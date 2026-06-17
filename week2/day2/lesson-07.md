# 7교시: port publish와 network 차이

## 수업 목표
- host 접근과 container 간 접근을 분리한다.
- wrong host/port failure를 재현한다.
- PORTS 출력과 network DNS를 함께 해석한다.

## 강의 전개
port publish는 host 사용자가 container service에 들어오는 문이다. Docker network는 container끼리 통신하는 길이다. 둘을 섞으면 DB 접속 문자열을 계속 틀리게 된다. 이 교시는 같은 PostgreSQL을 host에서는 localhost:15432로, container 내부에서는 paperclip-net-pg:5432로 접근하는 차이를 비교한다.

이 교시는 설명만 듣고 지나가지 않는다. 명령은 반드시 code block으로 실행하고, 바로 이어서 검증 명령을 실행한다. 정상 출력이 다를 수 있는 부분은 전체 문자열을 외우지 않고 성공 패턴을 확인한다. 실패는 원인을 좁히는 단서다. 실패한 명령, 에러 요약, 가설, 다시 실행할 명령을 순서대로 다룬다.

## Imagegen 인포그래픽: port publish와 container network
![Docker host port publish versus container network access](./assets/lesson-07-port-publish-vs-network.png)

이 이미지는 host 접근과 container 접근을 위아래로 분리한다. host에서는 `localhost:15432`와 published port를 사용하고, 같은 Docker network 안에서는 service name과 container port를 사용한다.

## 시각 자료 1: host port와 container port
```mermaid
flowchart LR
  Host[host terminal] -->|localhost:15432| Published[port publish -p 15432:5432]
  Published --> DB[paperclip-net-pg:5432]
  Client[client container] -->|paperclip-net-pg:5432| DB
  Client -.-> WrongPath[wrong: localhost:15432]
  WrongPath -.-> Self[client 자신]
```

이 그림은 host에서 들어가는 경로와 container끼리 통신하는 경로를 분리한다. `15432`는 host 쪽 입구이고, `5432`는 PostgreSQL container 내부 service port다.

## 시각 자료 2: 접속 문자열 선택
```mermaid
flowchart TD
  Start
  Start --> Host[host terminal]
  Start --> SameNet[같은 Docker network의 container]
  Host --> HostDSN["-h localhost -p 15432"]
  SameNet --> NetDSN["-h paperclip-net-pg -p 5432"]
  HostDSN --> OK1[host 접근]
  NetDSN --> OK2[container 간 접근]
  SameNet --> Bad["localhost 또는 15432 사용"]
  Bad --> Fail[혼동으로 실패]
```

접속 문자열은 DB 종류보다 "명령을 실행하는 위치"가 먼저 결정한다. 위치를 먼저 말하고 host와 port를 고르면 실수가 줄어든다.

## 실습 명령
```bash
docker run -d --name paperclip-net-pg --network paperclip-day2-net -e POSTGRES_PASSWORD=postgres -p 15432:5432 -v paperclip-pg16-data:/var/lib/postgresql/data postgres:16
```

## 검증 명령
```bash
docker ps --filter name=paperclip-net-pg
PGPASSWORD=postgres psql -h localhost -p 15432 -U postgres -d paperclip -c "SELECT 1;" || true
docker run --rm --network paperclip-day2-net -e PGPASSWORD=postgres postgres:16 psql -h paperclip-net-pg -U postgres -d paperclip -c "SELECT 1;"
```

## 실습 확장 흐름
| 단계 | 할 일 | 기대되는 관찰 |
|---|---|---|
| 준비 | DB container를 custom network와 published port로 실행한다. | `docker ps` PORTS에 `15432->5432`가 보인다. |
| host 접근 | host `psql` 또는 대체 client로 `localhost:15432`에 접근한다. | host 경로가 성공한다. |
| 내부 접근 | client container에서 `paperclip-net-pg:5432`로 접근한다. | 같은 network 경로가 성공한다. |
| 실패 재현 | client container에서 `localhost`를 사용한다. | client 자신을 가리켜 실패한다. |
| 복구 | 접속 위치에 맞춰 host/port를 바꾼다. | 두 경로의 목적을 분리해 설명할 수 있다. |
| 확인 | PORTS 출력과 DNS 접속을 함께 본다. | publish와 service discovery를 구분한다. |

## 실패 드릴과 오해 교정
| 상황 | 해석 |
|---|---|
| host psql 없음 | docker run --rm postgres client 방식으로 대체한다. |
| container에서 localhost 사용 | client container 자신을 가리키므로 실패한다. |
| 15432와 5432 혼동 | host port는 외부용, container port는 내부 service port다. |

## Cleanup
```bash
docker stop paperclip-net-pg || true
docker rm paperclip-net-pg || true
```

Cleanup은 비용과 데이터 안전을 동시에 다룬다. container를 지우는 명령과 volume/network/image를 지우는 명령은 의미가 다르다. 특히 volume 삭제는 database data 삭제일 수 있으므로 실습 volume인지 확인한 뒤 실행한다.

## 주의할 점
- Container를 삭제해도 named volume의 데이터는 남을 수 있다. 데이터를 초기화하려는 것이 아니라면 `docker volume rm`이나 `down -v`를 실행하지 않는다.
- Host port publish(`-p`)와 container 간 통신은 다른 문제다. 브라우저나 host `psql`로 접근할 때만 host port가 필요하고, 같은 Docker network 안에서는 container name과 container port를 사용한다.
- Volume target path는 image가 실제로 데이터를 쓰는 경로와 맞아야 한다. PostgreSQL은 `/var/lib/postgresql/data`와 `PGDATA` 설정을 확인하지 않으면 데이터가 남지 않거나 엉뚱한 위치에 쌓인다.
- bind mount는 host 경로를 그대로 노출한다. 개인 경로, 권한 문제, 실수로 수정한 host 파일이 container 동작에 영향을 줄 수 있다.
- Cleanup 전에는 지금 지우는 대상이 container인지, volume인지, network인지 먼저 구분한다.

## 핵심 포인트
이 실습의 핵심은 명령어 자체가 아니라 경계다. container는 실행 단위이고, volume은 data lifecycle이며, network는 통신 경계다. 학생이 `docker run` 한 줄을 볼 때 `-v`, `--network`, `-p`를 옵션 목록으로 외우면 뒤에서 Compose와 Kubernetes로 넘어갈 때 같은 혼란이 반복된다. 그래서 각 옵션을 "무엇을 container 밖으로 분리하는가"라는 질문으로 읽게 한다.

강의 중에는 성공 출력보다 실패 출력의 의미를 더 오래 다룬다. port가 열리지 않은 것은 web server 문제가 아닐 수 있고, DB 접속 실패는 password 문제가 아니라 network boundary 문제일 수 있다. host terminal, container 내부, 같은 Docker network의 client container는 모두 서로 다른 관찰 위치다. 학생이 어디에서 명령을 실행하는지 말로 먼저 설명한 뒤 CLI를 실행하게 한다.

## 운영 해석
실무에서 database container를 다룰 때 가장 위험한 실수는 cleanup을 단순 파일 정돈처럼 보는 것이다. container 삭제는 process와 container writable layer를 없애는 것이고, volume 삭제는 data를 삭제하는 것이다. network 삭제는 통신 경로를 없애는 것이다. 이 세 가지를 구분하지 않으면 실습은 성공해도 운영 사고를 배운 셈이 된다.

운영에서는 "실행됐다"보다 어떤 data가 남고 무엇이 삭제되는지가 더 중요하다. Day 2의 storage/network 판단은 Day 5 Compose에서 `volumes`와 `networks`를 읽는 기준이 된다. Compose의 YAML 항목은 갑자기 생긴 문법이 아니라 Day 2에서 손으로 실행한 storage/network 결정을 파일로 옮긴 것이다.

## 혼자 다시 따라오기
최소 성공 경로는 `docker ps`의 PORTS 확인, host 접근 한 번, 같은 network client 접근 한 번이다. host에 `psql`이 없다면 `docker run --rm postgres:16 psql ...` 방식으로 대체한다. 실패하면 접속 위치, host 값, port 값을 한 줄씩 분리해 본다.

## 다음 연결
다음 교시는 storage와 network를 합쳐 Day 2의 실행 경계를 마무리한다.
