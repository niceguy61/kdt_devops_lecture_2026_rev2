# 3교시: Inspect와 exec로 내부 확인

![Inspect and exec evidence infographic](./assets/lesson-04-inspect-exec-evidence.png)

## 수업 목표
- `docker inspect`와 `docker exec`의 역할을 구분한다.
- port, image, restart policy 같은 metadata를 선별해서 확인한다.
- container 내부 filesystem/process를 직접 확인한다.

## 개념 설명
`inspect`는 Docker가 알고 있는 metadata를 보는 명령이다. port mapping, network, mount, image, env, restart policy처럼 container 외부 계약을 확인할 때 유용하다. `exec`는 이미 실행 중인 container 안에서 명령을 실행한다. filesystem, process, config file, network tool 존재 여부처럼 내부 상태를 볼 때 쓴다.

두 명령을 섞어 쓰면 안 된다. port mapping이 궁금하면 `inspect`, nginx가 실제로 어떤 파일을 serving하는지 궁금하면 `exec`가 맞다.

단, `inspect`와 `exec env`는 secret을 보여줄 수 있다. `--env-file .env`로 넣은 값도 container metadata나 container 내부 환경에서 확인될 수 있다. 그래서 수업 기록에는 전체 출력 대신 필요한 key와 masking된 값만 남긴다.

## 실습 명령
```bash
docker inspect paperclip-day4-nginx --format 'Ports={{json .NetworkSettings.Ports}}'
docker inspect paperclip-day4-nginx --format 'Image={{.Config.Image}} Restart={{json .HostConfig.RestartPolicy}}'
docker exec paperclip-day4-nginx ls -l /usr/share/nginx/html
docker exec paperclip-day4-nginx sh -c 'ps | head'
```

Expected:

```text
Ports={"80/tcp":[{"HostIp":"0.0.0.0","HostPort":"18084"}]}
Image=nginx:1.27-alpine
index.html
nginx
```

## 선택 기준
| 알고 싶은 것 | 먼저 쓸 명령 |
|---|---|
| host port가 어디에 연결됐는가 | `docker inspect ... NetworkSettings.Ports` |
| 어떤 image로 떴는가 | `docker inspect ... Config.Image` |
| restart policy가 무엇인가 | `docker inspect ... HostConfig.RestartPolicy` |
| container 안에 파일이 있는가 | `docker exec ... ls` |
| process가 무엇인가 | `docker exec ... ps` |
| env key가 적용됐는가 | `docker inspect ... Config.Env` 또는 `docker exec ... env` |

## env 확인 시 masking
env 확인이 필요하면 key 이름과 적용 여부를 본다.

```bash
docker rm -f paperclip-day4-env-inspect || true
docker run -d --name paperclip-day4-env-inspect --env-file week2/day4/labs/env-report/.env alpine:3.20 sleep 300
docker inspect paperclip-day4-env-inspect --format '{{range .Config.Env}}{{println .}}{{end}}' \
  | grep -E 'APP_ENV|FEATURE_FLAG|DB_PASSWORD' \
  | sed -E 's/DB_PASSWORD=.*/DB_PASSWORD=***masked***/'
docker exec paperclip-day4-env-inspect sh -c 'env | grep -E "APP_ENV|FEATURE_FLAG|DB_PASSWORD"' \
  | sed -E 's/DB_PASSWORD=.*/DB_PASSWORD=***masked***/'
```

Expected:

```text
APP_ENV=practice
FEATURE_FLAG=on
DB_PASSWORD=***masked***
```

해석: `inspect`와 `exec env` 모두 값 확인이 가능하다. 그래서 문제 해결에는 유용하지만, 제출물이나 질문 글에는 masking이 필요하다.

## 판단 drill
다음 상황에서 먼저 쓸 명령을 고른다.

| 상황 | 먼저 볼 증거 | 이유 |
|---|---|---|
| host port가 열렸는지 모르겠다 | `docker inspect ... NetworkSettings.Ports` | Docker가 적용한 publish 정보를 본다. |
| nginx가 어떤 파일을 serving하는지 모르겠다 | `docker exec ... ls /usr/share/nginx/html` | container 내부 filesystem을 본다. |
| env가 들어갔는지 확인해야 한다 | `inspect` 또는 `exec env` + masking | 값 확인은 가능하지만 기록은 masking한다. |
| process가 죽었는지 모르겠다 | `docker inspect ... State` 또는 `docker ps -a` | container 상태와 exit code를 본다. |

## 주의
`docker inspect` 전체 JSON을 README에 붙이면 읽기 어렵다. 문제와 관련된 field만 뽑아서 증거로 남긴다.

Kubernetes에서도 같은 기준이 이어진다. Pod의 env, ConfigMap, Secret mount를 확인할 수는 있지만, 민감한 값을 그대로 issue나 README에 붙이면 안 된다.

## 다음 연결
다음 교시는 resource 관찰과 restart policy를 다룬다.
