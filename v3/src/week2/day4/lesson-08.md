# 8교시 · 백업과 복구 — pg_dump와 복원 훈련

!!! goal "이번 시간에 할 일"
    - **RPO**(얼마나 잃어도 되나)와 **RTO**(얼마나 빨리 돌아와야 하나)로 백업 계획을 말합니다.
    - 2교시의 파일 복사(`tar`)와 달리 DB가 **일관된 사본**을 만들어 주는 `pg_dump`로 백업합니다.
    - 일부러 데이터를 날리는 **사고**를 내고, 백업으로 되살리며 걸린 시간을 잽니다.
    - 백업한 뒤에 들어온 데이터는 **돌아오지 않는다**는 것을 눈으로 확인합니다.
    - "복원해 보지 않은 백업은 백업이 아니다" — 다른 컨테이너에 복원해 검증합니다.

!!! key "백업의 목적은 복구다"
    백업 파일이 있다는 것과 **되살릴 수 있다**는 것은 다른 이야기입니다. 오늘은 만드는 것보다 **되살리는 연습**에 시간을 씁니다.

## 두 숫자 — RPO와 RTO

| | RPO (Recovery Point Objective) | RTO (Recovery Time Objective) |
|---|---|---|
| 질문 | 사고가 나면 **얼마 전 시점까지** 되돌아가도 되나? | 사고가 나면 **얼마 만에** 다시 열어야 하나? |
| 정하는 것 | 백업을 **얼마나 자주** 하나 | 복구 절차가 **얼마나 빨라야** 하나 |
| 예 | "최대 1시간치 주문은 잃어도 된다" → 1시간마다 백업 | "30분 안에 다시 연다" → 30분 안에 끝나는 복원 절차 |
| 오늘 잴 것 | 백업 후 들어온 상품이 사라지는지 | `time`으로 복원 시간 |

!!! example "백업의 3-2-1 규칙"
    **3**벌을 두고, **2**가지 다른 매체에, **1**벌은 **다른 장소**에. 같은 서버 같은 디스크에 있는 백업은 그 디스크가 고장 나면 함께 사라집니다. 5주차에는 백업을 S3(다른 장소)에 둡니다.

## 실습 12 · 준비 — DevMart 다시 띄우기

```bash
cd ~/devops-lab/devmart
bash ../day4/devmart-up.sh
docker exec db psql -U devmart -d devmart -c "SELECT count(*) FROM products;"
curl -s http://localhost:8080/api/products | head -c 80; echo
```

!!! check "이렇게 나오면 성공"
    ```text
     count
    -------
         6
    ```
    2교시에 넣은 "볼륨 테스트 양말"까지 6개입니다(볼륨을 지우지 않았으므로 남아 있음). 숫자가 다르면 그 숫자를 기억해 둡니다.

## 실습 13 · pg_dump로 백업

```bash
mkdir -p ~/devops-lab/backup
STAMP=$(date +%Y%m%d-%H%M%S)
docker exec db pg_dump -U devmart -d devmart -Fc > ~/devops-lab/backup/devmart-$STAMP.dump
ls -lh ~/devops-lab/backup/*.dump
```

| 부분 | 뜻 |
|---|---|
| `pg_dump` | PostgreSQL이 **한 시점의 일관된 사본**을 만들어 주는 도구. DB가 켜진 채로 안전하다 |
| `-Fc` | PostgreSQL 전용 압축 형식(custom). 나중에 일부만 골라 복원할 수도 있다 |
| `> ~/…/devmart-$STAMP.dump` | 컨테이너 **안에서** 나온 출력을 **내 노트북의 파일**로 받는다 |
| `$(date …)` | 명령의 결과를 그 자리에 넣기 — 파일 이름에 시각을 붙여 덮어쓰지 않게 |

!!! warn "`docker exec`에 `-t`를 붙이지 않는다"
    `docker exec -it db pg_dump …`처럼 `-t`(터미널 흉내)를 붙이면 출력의 줄바꿈 문자가 바뀌어 **이진 파일인 백업이 깨집니다.** 파일로 받을 때는 `-t` 없이 실행합니다. 반대로 파일을 **넣을** 때는 `-i`가 필요합니다(아래 복원).

백업이 읽히는지부터 확인합니다.

```bash
LATEST=$(ls -t ~/devops-lab/backup/*.dump | head -1)
docker exec -i db pg_restore --list < "$LATEST" | grep "TABLE DATA"
```

!!! check "이렇게 나오면 성공"
    ```text
    3365; 0 16389 TABLE DATA public products devmart
    ```
    번호는 달라도 됩니다. `products`의 데이터가 백업 안에 있다는 뜻입니다.

## 실습 14 · 사고 내기

백업 **뒤에** 상품을 하나 더 넣고, 그다음 사고를 냅니다.

```bash
docker exec db psql -U devmart -d devmart -c "INSERT INTO products (name, price) VALUES ('백업 뒤에 들어온 모자', 25000);"
docker exec db psql -U devmart -d devmart -c "DELETE FROM products;"
curl -s http://localhost:8080/api/products; echo
```

!!! check "사고가 났습니다"
    ```text
    DELETE 7
    []
    ```
    `WHERE`를 빠뜨린 `DELETE` — 실제로 가장 흔한 데이터 사고 중 하나입니다. 쇼핑몰의 상품이 **전부** 사라졌습니다.

## 실습 15 · 복원하고 시간 재기

```bash
time docker exec -i db pg_restore -U devmart -d devmart --clean --if-exists < "$LATEST"
docker exec db psql -U devmart -d devmart -c "SELECT id, name FROM products ORDER BY id;"
curl -s http://localhost:8080/api/products | head -c 80; echo
```

- `--clean --if-exists` : 백업에 든 테이블을 **지우고 다시 만든 뒤** 데이터를 채운다(있을 때만 지움)
- `time` : 걸린 시간을 잰다 — 오늘의 **RTO** 측정값

!!! check "이렇게 나오면 성공"
    ```text
    real    0m0.4s
     id |      name
    ----+------------------
      1 | 러닝화
      …
      6 | 볼륨 테스트 양말
    ```
    상품 6개가 돌아왔고, 웹에도 다시 보입니다. 그런데 **"백업 뒤에 들어온 모자"는 없습니다.** 백업 시점 이후의 데이터는 백업에 없기 때문입니다. 이것이 **RPO**입니다. 1시간마다 백업하면 최대 1시간치를 잃습니다.

!!! example "그래서 운영 DB는 이렇게 한다"
    | 방법 | RPO | 쓰는 곳 |
    |---|---|---|
    | 정기 `pg_dump` | 백업 간격 (예: 1시간) | 작은 서비스, 개발 DB |
    | **WAL 보관 + 시점 복구(PITR)** | 몇 초 ~ 몇 분 | 2교시의 `pg_wal` 기록을 계속 모아 두었다가 "사고 1분 전"으로 되감기 |
    | 관리형 DB 자동 백업 | 몇 분 | AWS RDS 등 — 5주차에 "직접 운영하지 않는 DB"로 다시 본다 |

## 실습 16 · 복원 훈련 — 다른 곳에 되살려 검증

운영 DB에 복원해 보는 것은 위험합니다. 그래서 **빈 DB를 하나 더 띄워** 거기에 복원하고, 내용을 확인한 뒤 버립니다. 회사에서는 이것을 정기적으로(예: 매주) 자동으로 합니다.

```bash
docker run -d --name restore-test \
  -e POSTGRES_USER=check -e POSTGRES_DB=check -e POSTGRES_PASSWORD=check-only \
  postgres:18
until docker exec restore-test pg_isready -U check >/dev/null 2>&1; do sleep 1; done
docker exec -i restore-test pg_restore -U check -d check --no-owner < "$LATEST"
docker exec restore-test psql -U check -d check -tAc "SELECT count(*) FROM products;"
docker rm -f restore-test
```

- `--no-owner` : 원래 DB의 주인(`devmart`)이 이 DB에는 없으므로, 주인 정보는 빼고 복원
- `-tAc` : 머리줄 없이 값만 — 스크립트에서 숫자를 비교하기 좋다

!!! check "이렇게 나오면 성공"
    ```text
    6
    ```
    백업 파일 하나로 **완전히 다른 DB**를 되살렸습니다. 이 숫자를 기대값과 비교하는 스크립트를 매주 돌리면, "백업이 깨져 있었다"를 사고 **전에** 알 수 있습니다.

## 실습 17 · 백업 스크립트

7교시의 스크립트 옆에 백업 스크립트를 만듭니다.

```bash
code ~/devops-lab/day4/devmart-backup.sh
```

```bash
#!/usr/bin/env bash
# DevMart DB 백업 — 시각을 붙여 저장하고, 7일 지난 것은 지운다
set -euo pipefail
DIR=~/devops-lab/backup
mkdir -p "$DIR"
FILE="$DIR/devmart-$(date +%Y%m%d-%H%M%S).dump"

docker exec db pg_dump -U devmart -d devmart -Fc > "$FILE"
docker exec -i db pg_restore --list < "$FILE" > /dev/null     # 읽히는지 바로 확인
echo "백업: $FILE ($(du -h "$FILE" | cut -f1))"

find "$DIR" -name 'devmart-*.dump' -mtime +7 -print -delete     # 보관 기간 7일
```

```bash
chmod +x ~/devops-lab/day4/devmart-backup.sh
~/devops-lab/day4/devmart-backup.sh
```

!!! check "이렇게 나오면 성공"
    ```text
    백업: /home/devops/devops-lab/backup/devmart-20261126-171503.dump (4.0K)
    ```

- `set -euo pipefail` : `pg_dump`가 실패하면 **빈 파일을 '백업'이라고 남기지 않고** 멈춘다
- `find … -mtime +7 -delete` : 7일 넘은 백업을 지운다 — 1주차 2일차 8교시의 "디스크 100%"를 막는 보관 정책
- 정기 실행은 Linux의 `cron`이나 4주차의 Kubernetes **CronJob**이 맡습니다

!!! cleanup "정리와 커밋"
    ```bash
    cd ~/devops-lab/devmart
    bash ../day4/devmart-down.sh          # 데이터(볼륨)는 남긴다
    cd ~/devops-lab
    git add day4/devmart-backup.sh
    git status --short                    # backup/*.dump가 없는지 확인 (.gitignore)
    git commit -m "4일차: DB 백업 스크립트와 복원 훈련"
    git push
    ```
    백업 파일에는 **고객 데이터**가 들어 있으므로 Git에 올리지 않습니다. 2교시에 `.gitignore`에 넣은 `backup/`이 막아 줍니다.

!!! academic "학술 노트 — 백업이 다섯 개였는데 (GitLab, 2017)"
    2017년 1월 31일, GitLab.com의 엔지니어가 밤늦게 복제 문제를 고치다가 **운영 DB 서버의 데이터 폴더를 지우는** 명령을 실행했습니다. 회사에는 백업 방법이 **다섯 가지**나 있었지만, 확인해 보니 정기 `pg_dump`는 버전이 맞지 않아 몇 달 동안 **빈 파일**만 만들고 있었고, 실패 알림 메일은 메일 인증(DMARC) 설정 때문에 전달되지 않아 아무도 몰랐으며, 다른 방법들도 꺼져 있거나 쓸 수 없었습니다. 결국 우연히 6시간 전에 떠 둔 사본으로 복구했고, 그 사이의 데이터는 잃었습니다. GitLab은 이 과정을 **실시간 방송과 공개 포스트모템**(1주차 5일차)으로 남겼고, 교훈은 한 줄이었습니다. **"복원해 보지 않은 백업은 백업이 아니다."** 오늘 스크립트의 `set -e`와 `pg_restore --list`, 실습 16의 복원 훈련이 그 교훈을 코드로 옮긴 것입니다.

    - GitLab (2017.2.10). *Postmortem of database outage of January 31*. about.gitlab.com/blog

!!! trend "트렌드 — 지울 수 없는 백업"
    랜섬웨어 공격자는 데이터를 암호화하기 전에 **백업부터 찾아 지웁니다.** 그래서 정해진 기간 동안 **누구도(관리자도) 지우거나 바꿀 수 없는** 불변(immutable) 백업이 표준이 되고 있습니다. AWS S3의 **객체 잠금(Object Lock)**, AWS Backup Vault Lock이 그 예입니다. 3-2-1 규칙에 "**1**벌은 불변, 복원 검증 오류 **0**"을 더한 **3-2-1-1-0** 규칙도 쓰입니다.

## 정리

- 백업 계획은 **RPO**(얼마나 잃어도 되나 → 백업 간격)와 **RTO**(얼마나 빨리 → 복원 절차)로 말합니다.
- `pg_dump -Fc`는 켜진 DB에서도 **일관된 사본**을 만듭니다. 파일로 받을 때 `docker exec`에 `-t`를 붙이지 않습니다.
- 복원은 `pg_restore --clean --if-exists`. 백업 **뒤의** 데이터는 돌아오지 않습니다.
- **복원해 보지 않은 백업은 백업이 아닙니다.** 다른 컨테이너에 정기적으로 되살려 숫자를 비교합니다.
- 백업 파일은 고객 데이터 — Git에 올리지 않고, 보관 기간을 정해 지웁니다.

!!! quiz "확인 문제"
    1. "최대 15분치 데이터만 잃어도 된다"는 RPO와 RTO 중 무엇인가요? 그러려면 무엇을 바꿔야 하나요?
    2. `docker exec -it db pg_dump … > backup.dump`로 만든 백업이 복원되지 않습니다. 원인은?
    3. 오후 2시에 백업하고, 2시 30분에 주문이 들어오고, 3시에 사고가 나서 2시 백업으로 복원했습니다. 2시 30분 주문은?
    4. 백업 스크립트 맨 위의 `set -euo pipefail`은 어떤 사고를 막나요?
    5. GitLab 사고의 교훈을 한 문장으로?

    ??? answer "정답"
        1. RPO — 백업(또는 WAL 보관) 간격을 15분 이하로 줄여야 합니다.
        2. `-t`가 터미널 흉내를 내면서 이진 출력의 줄바꿈 문자를 바꿔 파일이 깨졌습니다. `-t` 없이 다시 백업합니다.
        3. 사라집니다. 백업 시점 이후 데이터라 백업에 없습니다.
        4. `pg_dump`가 실패했는데도 빈 파일을 백업이라고 남기고 다음 단계로 넘어가는 사고
        5. 복원해 보지 않은 백업은 백업이 아니다.

!!! diary "오늘의 배움일기 — 수업 뒤 각자"
    - 볼륨 없이 DB를 지웠을 때와, 볼륨을 붙이고 지웠을 때의 차이를 '호텔 방과 금고'로 설명해 보기
    - 이름 있는 볼륨과 바인드 마운트를 각각 언제 쓰는지 내 말로 한 줄씩
    - 5교시 고장 세 가지 중 가장 헷갈렸던 것과, 로그의 어떤 문장으로 구분했는지
    - 오늘 `history | grep`으로 비밀번호를 찾았을 때 든 생각
    - DevMart 화면을 처음 봤을 때 소감 — 그리고 세 컨테이너를 띄우는 명령을 동료에게 어떻게 전해 줄지
    - 내일(Compose + GitHub 협업) 전에 궁금한 것

## 참고 문헌

- PostgreSQL Global Development Group. *PostgreSQL 18 Documentation* — Chapter 25 Backup and Restore; `pg_dump`; `pg_restore`; Continuous Archiving and Point-in-Time Recovery (PITR).
- GitLab (2017). *Postmortem of database outage of January 31*. about.gitlab.com/blog/2017/02/10/postmortem-of-database-outage-of-january-31
- NIST (2010). *SP 800-34 Rev. 1: Contingency Planning Guide for Federal Information Systems* — RPO, RTO.
- AWS Documentation. *Amazon S3 Object Lock*; *AWS Backup Vault Lock*.
- Docker Docs. *docker container exec — -i, -t*.
