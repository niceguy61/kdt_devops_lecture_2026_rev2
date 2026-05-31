# Mini Deploy Lab

3일차 배포와 실행 환경 표준화 실습용 미니 앱이다. 목적은 복잡한 개발이 아니라, 다른 사람이 같은 앱을 같은 방식으로 실행할 수 있도록 실행 조건을 문서화하고 검증하는 것이다.

## 실행

```bash
cp .env.example .env
python3 app.py
```

다른 터미널에서 확인한다.

```bash
curl http://localhost:8020/
curl http://localhost:8020/health
curl http://localhost:8020/config
tail -n 20 logs/app.log
```

## 포트 변경

`.env`에서 `PORT=8020`을 다른 값으로 바꾼 뒤 서버를 재기동한다.

```bash
sed -i 's/PORT=8020/PORT=8021/' .env
python3 app.py
curl http://localhost:8021/health
```

## 장애 관찰

```bash
curl -i http://localhost:8020/not-found
tail -n 20 logs/app.log
```

확인할 것:
- 404 status code
- `WARN` 로그
- 요청 path
