# 1교시: Compose 기본과 검증 루프

![Day 5 Compose Architecture Lab overview](https://raw.githubusercontent.com/niceguy61/kdt_devops_lecture_2026_rev2/main/week2/day5/assets/day5-compose-architecture-lab-overview.png)

## 수업 목표
- Compose architecture를 실제 명령으로 실행한다.
- config/up/ps/logs/curl/exec/down 검증 루프를 적용한다.
- Week 3 MSA service boundary로 연결한다.

## 강의 전개
config/up/ps/logs/down 루프를 아키텍처 공통 기준으로 익힌다. 강사는 starter code와 compose.yaml을 제공하고, 학생은 YAML을 읽은 뒤 실제로 실행해 서비스 관계를 확인한다. 유명 아키텍처를 말로만 설명하지 않고 container, network, volume, port, log 확인 지점으로 확인한다.

이 교시는 설명만 듣고 지나가지 않는다. 명령은 반드시 code block으로 실행하고, 바로 이어서 검증 명령을 실행한다. 정상 출력이 다를 수 있는 부분은 전체 문자열을 외우지 않고 성공 패턴을 확인한다. 실패는 실수를 줄이는 좋은 확인 지점이다. 실패한 명령, 에러 요약, 가설, 다시 확인한 명령을 함께 확인한다.

## 실습 명령
```bash
cd week2/day5/labs/compose-architectures/01-web-postgres
docker compose config
docker compose up -d
```

## 검증 명령
```bash
cd week2/day5/labs/compose-architectures/01-web-postgres
docker compose ps
docker compose logs --tail 80
```

```bash
cd week2/day5/labs/compose-architectures/01-web-postgres
# web가 있는 architecture는 curl로 확인
curl -I http://localhost:18085 || true
# DB가 있는 architecture는 exec 또는 run client로 확인
docker compose exec db psql -U postgres -d app -c 'SELECT 1;' || true
```

## 실패 드릴과 오해 교정
| 상황 | 해석 |
|---|---|
| config 실패 | indentation, env 누락, compose file path를 확인한다. |
| service unhealthy | logs와 dependency readiness를 확인한다. |
| down -v 남용 | database volume 삭제 위험을 설명한다. |

## Cleanup
```bash
cd week2/day5/labs/compose-architectures/01-web-postgres
docker compose down
# 데이터를 초기화해도 되는 실습일 때만 실행
# docker compose down -v
```

Cleanup은 비용과 데이터 안전을 동시에 다룬다. container를 지우는 명령과 volume/network/image를 지우는 명령은 의미가 다르다. 특히 volume 삭제는 database data 삭제일 수 있으므로 실습 volume인지 확인한 뒤 실행한다.

## 주의할 점
- `docker compose config`가 성공해도 서비스가 정상 동작한다는 뜻은 아니다. YAML 문법 확인과 실제 실행 확인을 분리해서 봐야 한다.
- Compose 내부 통신은 service name을 DNS 이름처럼 쓴다. host에서 접속할 때는 published port가 필요하지만, service끼리는 보통 container port로 통신한다.
- `down`과 `down -v`는 다르다. `down -v`는 named volume까지 삭제하므로 DB 데이터나 cache 상태를 초기화해도 되는 실습인지 먼저 확인한다.
- `.env` 값이 없거나 service name을 잘못 쓰면 앱 코드는 정상이어도 연결이 실패한다. 코드부터 고치기 전에 env, network, service name을 먼저 본다.
- 여러 architecture를 실행한 뒤에는 project name, network, volume이 겹치지 않는지 확인한다. 이전 실습의 stale volume이나 port가 다음 실습 실패 원인이 될 수 있다.

## 핵심 포인트
Day 5는 Compose 문법 암기 시간이 아니라 architecture를 실행 가능한 파일로 제공하는 연습이다. Day 2의 volume/network, Day 3의 image, Day 4의 env/logs/cleanup이 Compose 한 파일 안에서 다시 만난다. 학생은 `services`, `ports`, `environment`, `volumes`, `networks`를 YAML 속성으로만 보지 말고 지난 실습의 `docker run` 옵션이 옮겨진 결과로 읽어야 한다.

유명한 아키텍처 패턴을 다룰 때도 그림만 보여주지 않는다. Web+DB, DB UI, cache, reverse proxy, queue+worker는 모두 실제 container로 띄워야 한다. `docker compose config`는 문법 검증이고, `up`은 시작이며, `ps/logs/curl/exec`가 정상 검증이다. `down`과 `down -v`는 cleanup과 data reset의 경계다.

## 운영 해석
Compose는 Kubernetes가 아니다. 하지만 Compose는 multi-service 사고를 배우기에 좋다. service name이 곧 내부 DNS가 되고, volume이 data lifecycle을 담당하며, ports가 host 공개 경계를 만든다. Week 3 MSA로 넘어갈 때 service boundary, dependency, failure propagation을 설명하는 첫 번째 실습 근거가 된다.

각 architecture는 반드시 실행 상태를 확인한다. 학생이 두 개 이상의 architecture를 직접 실행하면 공통 패턴이 보이기 시작한다. 모든 architecture는 config, start, check, logs, cleanup이라는 같은 운영 루프를 가진다.

## 다음 연결
다음 architecture 또는 Week 3 MSA에서 같은 service/network/dependency 관점을 재사용한다.
