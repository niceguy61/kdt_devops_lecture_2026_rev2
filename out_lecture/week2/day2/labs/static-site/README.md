# Week 2 Day 2 Static Site Lab

## Build
```bash
docker build -t paperclip-static-site:day2 .
```

## Run
```bash
docker run -d --name paperclip-day2-static -p 18082:80 paperclip-static-site:day2
```

## Check
```bash
curl -I http://localhost:18082
curl -s http://localhost:18082 | grep "Dockerfile로 만든 표준 실습 앱"
docker logs paperclip-day2-static
```

## Cleanup
```bash
docker stop paperclip-day2-static
docker rm paperclip-day2-static
```
