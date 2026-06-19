# Architecture 07: Frontend + Gateway + API + DB

![MSA preview architecture](https://raw.githubusercontent.com/niceguy61/kdt_devops_lecture_2026_rev2/main/week2/day5/assets/day5-arch-07-msa-preview.png)

Week 3 MSA로 넘어가기 전 마지막 Compose template이다. browser traffic은 `gateway`로 들어오고, gateway는 static frontend와 API path를 나눈다. API는 service name `db`로 PostgreSQL에 연결한다.

## Run
```bash
docker compose config
docker compose up -d
docker compose ps
```

## Check
```bash
curl -s http://localhost:18091 | grep week2-day5-msa-preview
curl -s http://localhost:18091/api/services
docker compose logs gateway --tail 40
docker compose logs api --tail 40
```

Expected:

```text
week2-day5-msa-preview
"name":"gateway"
"name":"api"
```

## Cleanup
```bash
docker compose down
# data reset이 필요할 때만
# docker compose down -v
```

`down -v`는 PostgreSQL volume을 삭제한다.
