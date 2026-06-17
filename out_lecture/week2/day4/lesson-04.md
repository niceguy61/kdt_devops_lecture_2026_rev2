# 4교시: inspect/exec 기반 내부 확인

## 수업 목표
- runtime config와 관찰 명령을 구분한다.
- 정상/장애 확인 지점을 선별한다.
- cleanup과 secret 비노출을 적용한다.

## 강의 전개
inspect로 metadata를 보고 exec로 내부를 확인한다.

이 교시는 설명만 듣고 지나가지 않는다. 명령은 반드시 code block으로 실행하고, 바로 이어서 검증 명령을 실행한다. 정상 출력이 다를 수 있는 부분은 전체 문자열을 외우지 않고 성공 패턴을 확인한다. 실패는 실수를 줄이는 좋은 확인 지점이다. 실패한 명령, 에러 요약, 가설, 다시 확인한 명령을 함께 확인한다.

## 실습 명령
```bash
docker inspect paperclip-day4-nginx --format "{{json .NetworkSettings.Ports}}"
docker exec paperclip-day4-nginx ls -l /usr/share/nginx/html
```

## 검증 명령
```bash
docker exec paperclip-day4-nginx sh -c "ps aux | head"
```

## 실패 드릴과 오해 교정
| 상황 | 해석 |
|---|---|
| secret 노출 | README/screenshot/history에 값이 남지 않도록 masking한다. |
| logs만 붙임 | inspect/exec/stats와 함께 원인을 좁힌다. |
| cleanup 과잉 | volume/image/network 삭제 범위를 구분한다. |

## Cleanup
```bash
docker stop paperclip-day4-nginx paperclip-day4-bad || true
docker rm paperclip-day4-nginx paperclip-day4-bad || true
# 생성한 env 파일에는 실제 비밀번호를 남기지 않는다.
```

Cleanup은 비용과 데이터 안전을 동시에 다룬다. container를 지우는 명령과 volume/network/image를 지우는 명령은 의미가 다르다. 특히 volume 삭제는 database data 삭제일 수 있으므로 실습 volume인지 확인한 뒤 실행한다.

## 주의할 점
- Container가 `Up` 상태여도 애플리케이션이 정상이라는 뜻은 아니다. `logs`, HTTP 응답, DB 연결처럼 서비스 관점의 확인을 함께 봐야 한다.
- 환경변수는 runtime 설정이지 image에 굳힐 값이 아니다. password, token, API key는 README, screenshot, terminal history에 남기지 않는다.
- `docker inspect` 출력은 길다. 전체를 복사하기보다 env, mount, network, restart policy처럼 문제와 관련된 영역을 좁혀서 본다.
- `docker exec`는 container 내부 관찰 도구다. host에서 되는 명령이 container 안에서도 된다고 가정하지 않는다.
- 장애 드릴 후에는 실패 container, stale volume, 잘못 만든 network, 오래된 image tag가 다음 실습을 방해할 수 있으므로 cleanup 대상을 구분한다.

## 핵심 포인트
Day 4는 "container가 떠 있다"와 "서비스가 정상이다"를 분리하는 날이다. `docker ps`에서 Up이라고 보여도 application은 설정 누락으로 의미 없는 상태일 수 있다. 반대로 container가 exit된 경우에도 logs를 보면 원인이 명확히 남아 있을 수 있다. 그래서 logs, inspect, exec, stats를 서로 다른 관찰 도구로 가르친다.

환경변수는 편하지만 secret 관리와 연결된다. 수업용 password라도 README나 screenshot에 그대로 남기는 습관은 위험하다. 학생에게 공개해도 되는 것은 env var 이름과 주입 방식이지 실제 credential 값이 아니라는 점을 강조한다. `.env.example`은 형식을 공유하는 파일이고, 실제 `.env`는 로컬 전용이다.

## 운영 해석
장애 분석은 감으로 하는 것이 아니라 관찰 위치를 바꾸며 좁혀가는 일이다. logs는 application이 말한 내용, inspect는 Docker metadata, exec는 container 내부 관찰, stats는 resource 관찰이다. 어떤 문제에는 logs만으로 충분하고, 어떤 문제는 inspect의 network/mount/env를 봐야 한다. 학생이 명령을 많이 아는 것보다 언제 무엇을 볼지 말할 수 있어야 한다.

Cleanup도 Day 4에서 다시 다룬다. 장애 드릴 중에는 실패 container, 잘못 붙은 network, 오래된 volume, 잘못 만든 image tag가 남는다. 남은 자원은 다음 실습의 원인이 되므로, cleanup audit을 주의할 점으로 다룬다.

## 다음 연결
Day 5는 Day 2~4의 옵션을 compose.yaml로 옮겨 유명 아키텍처를 실행한다.
