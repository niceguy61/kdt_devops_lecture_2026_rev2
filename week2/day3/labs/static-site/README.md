# Day 3 Static Site Lab

```bash
docker build -t paperclip-static-site:day3 .
docker run -d --name paperclip-day3-static -p 18083:80 paperclip-static-site:day3
curl -I http://localhost:18083
```

```bash
docker stop paperclip-day3-static || true
docker rm paperclip-day3-static || true
```
