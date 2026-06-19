# 5교시: Nginx reverse proxy + multiple web services template

![Reverse proxy architecture](./assets/day5-arch-04-reverse-proxy.png)

## 수업 목표
- 외부 traffic 진입점과 내부 upstream service를 분리한다.
- `web-a`, `web-b`를 host에 직접 공개하지 않는 이유를 설명한다.
- upstream 장애를 proxy logs로 확인한다.

## 언제 쓰는가
여러 web/API service를 하나의 entrypoint 뒤에 숨기고 path나 host 기준으로 routing할 때 사용한다. Week 3 MSA에서 gateway/API gateway 개념으로 넘어가기 전 가장 이해하기 쉬운 구조다.

## Template
```bash
cd week2/day5/labs/compose-architectures/04-nginx-reverse-proxy
docker compose config
docker compose up -d
docker compose ps
```

구성:

| Service | 역할 | 공개 범위 |
|---|---|---|
| `proxy` | 외부 진입점, `/a/`, `/b/` routing | host `18089` |
| `web-a` | 내부 web app A | Compose network 내부 |
| `web-b` | 내부 web app B | Compose network 내부 |

## Check
```bash
curl -s http://localhost:18089/a/
curl -s http://localhost:18089/b/
docker compose logs proxy --tail 40
```

Expected:

```text
Web A
Web B
```

## Failure drill
```bash
docker compose stop web-b
curl -i http://localhost:18089/b/ || true
docker compose logs proxy --tail 20
docker compose up -d web-b
```

proxy는 살아 있지만 upstream이 죽으면 `/b/`만 실패한다. 이 차이가 gateway 장애인지, backend 장애인지 구분하는 첫 단서다.

## Cleanup
```bash
docker compose down
```
