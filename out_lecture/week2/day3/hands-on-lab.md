# Week 2 Day 3 Hands-on Lab: Image, Dockerfile, Build, Registry

이 lab은 제공된 정적 앱을 Dockerfile로 build하고 image layer/cache/tag/digest를 확인한다.

## Phase A: official image inspect
```bash
docker pull nginx:1.27-alpine
docker images nginx
docker history nginx:1.27-alpine
docker image inspect nginx:1.27-alpine --format "{{.Id}} {{.Architecture}} {{.Size}}"
```

## Phase B: create standard app
```bash
mkdir -p week2/day3/labs/static-site
printf "<h1>day3 static app</h1>" > week2/day3/labs/static-site/index.html
cat > week2/day3/labs/static-site/Dockerfile <<'EOF'
FROM nginx:1.27-alpine
COPY index.html /usr/share/nginx/html/index.html
EXPOSE 80
EOF
printf ".git
*.log
.env
node_modules
" > week2/day3/labs/static-site/.dockerignore
```

## Phase C: build and run
```bash
cd week2/day3/labs/static-site
docker build -t paperclip-static-site:day3 .
docker run -d --name paperclip-day3-static -p 18083:80 paperclip-static-site:day3
curl -I http://localhost:18083
curl -s http://localhost:18083
```

## Phase D: history, inspect, cache
```bash
docker history paperclip-static-site:day3
docker image inspect paperclip-static-site:day3 --format "{{.Id}} {{.Size}} {{.Architecture}}"
printf "<h1>day3 static app v2</h1>" > week2/day3/labs/static-site/index.html
cd week2/day3/labs/static-site
docker build -t paperclip-static-site:day3-v2 .
```

## Phase E: tag and optional push gate
```bash
docker tag paperclip-static-site:day3 paperclip-static-site:day3-reviewed
docker images paperclip-static-site
```

Docker Hub push는 선택이다. push 전에는 repository 공개 범위, secret 포함 여부, tag 이름을 확인한다.

## Phase F: failure drill
```bash
cp -r week2/day3/labs/static-site week2/day3/labs/static-site-broken
rm -f week2/day3/labs/static-site-broken/index.html
cd week2/day3/labs/static-site-broken
docker build -t paperclip-static-site:broken . || true
```

## Cleanup
```bash
docker stop paperclip-day3-static || true
docker rm paperclip-day3-static || true
# 필요 시 image 삭제
# docker image rm paperclip-static-site:day3 paperclip-static-site:day3-v2 paperclip-static-site:day3-reviewed
```

## 주의할 점
- `docker build`의 마지막 `.`은 build context다. 명령을 어느 directory에서 실행하는지 먼저 확인한다.
- `.dockerignore` 없이 `.env`, log, dependency directory가 context에 들어가면 image에 포함될 수 있다.
- `EXPOSE 80`은 host `localhost:18083`을 열어주지 않는다. host 접근에는 `-p 18083:80`이 필요하다.
- tag는 image 이름표다. `docker tag`는 새 build가 아니라 기존 image에 reference를 추가하는 명령이다.
- Docker Hub push는 선택이다. public repository, credential, secret 포함 여부를 확인하지 못하면 push하지 않는다.
