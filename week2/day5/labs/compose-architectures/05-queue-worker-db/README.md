# Architecture 05: Queue + Worker + Database

```bash
docker compose config
docker compose up -d
docker compose ps
docker compose exec queue redis-cli LPUSH jobs "send-email:42"
docker compose logs worker --tail 40
docker compose exec db psql -U postgres -d jobs -c "SELECT current_database();"
docker compose down
```

이 예제의 worker는 Redis queue에서 job을 꺼내 로그로 보여주는 최소 실습용 worker다. 실제 업무에서는 worker가 job 처리 결과를 DB에 확인한다.
