# 3교시: 당근형 백엔드 서비스 경계 template

![Backend boundary architecture](https://raw.githubusercontent.com/niceguy61/kdt_devops_lecture_2026_rev2/main/week2/day5/assets/day5-arch-02-backend-boundary.png)

## 수업 목표
- gateway 뒤에 identity API와 payment API를 분리한다.
- 공통 서비스가 많아질 때 service boundary와 장애 영향 범위를 설명한다.
- Adminer가 `db` service name으로 PostgreSQL에 접속하는 흐름을 확인한다.

## 언제 쓰는가
W1D4의 당근형 백엔드 경계 사례를 Compose로 줄인다. 사용자/신뢰 정보는 identity API, 결제 흐름은 payment API로 나뉘고, gateway가 외부 진입점을 맡는다. DB 관리 UI는 확인 도구로 붙이되 공개 범위를 항상 의식한다.

## Template
```bash
cd week2/day5/labs/compose-architectures/02-web-postgres-admin
docker compose config
docker compose up -d
docker compose ps
```

구성:

| Service | 역할 | 공개 범위 |
|---|---|---|
| `gateway` | static page, API route | host `18086` |
| `identity-api` | user/trust API | Compose network 내부 |
| `payment-api` | payment mock API | Compose network 내부 |
| `db` | PostgreSQL 16 | Compose network 내부 |
| `adminer` | DB 관리 UI | host `18087` |
| `db-checker` | DB 연결 확인 app | logs로 결과 확인 |

## Check
```bash
curl -I http://localhost:18086
curl -I http://localhost:18087
curl -s http://localhost:18086/identity/users
curl -s http://localhost:18086/payment/payments
docker compose logs db-checker --tail 30
```

Adminer login:

| 항목 | 값 |
|---|---|
| System | PostgreSQL |
| Server | `db` |
| Username | `postgres` |
| Password | `postgres` |
| Database | `app` |

## 실무 해석
gateway는 `/identity/`를 `identity-api:3000`으로, `/payment/`를 `payment-api:3000`으로 보낸다. Adminer에서 server를 `localhost`로 넣으면 실패한다. Adminer container 입장에서 `localhost`는 자기 자신이고, DB service는 Compose DNS 이름 `db`다.

## Cleanup
```bash
docker compose down
# DB를 초기화할 때만
# docker compose down -v
```
