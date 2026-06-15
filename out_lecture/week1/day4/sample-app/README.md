# Week 1 Sample Ops App

이 앱은 Day4 공통 샘플앱입니다. 새 앱을 만드는 실습이 아니라 로컬 서버 실행, 성공 확인, 실패 관찰, 오류 확인 기록 작성을 연습하기 위한 자료입니다.

## Start
```bash
python3 -m http.server 8000
```

## Check
브라우저에서 확인합니다.

```text
http://localhost:8000
```

터미널에서 상태 코드를 확인합니다.

```bash
curl -I http://localhost:8000
```

## Expected
- 브라우저에 `정상: data.json을 읽어서 화면에 표시했습니다.`가 보입니다.
- `curl -I` 결과에 `200` 상태 코드가 보입니다.
- 서버 터미널에 `GET /` 또는 `GET /data.json` 로그가 남습니다.

## Stop
서버를 실행 중인 터미널에서 `Ctrl+C`를 누릅니다.

## Troubleshoot
| 증상 | 먼저 확인할 것 |
|---|---|
| `connection refused` | 서버가 켜져 있는지, 포트가 8000인지 확인 |
| `404` | URL 경로와 파일 이름 확인 |
| 데이터가 보이지 않음 | browser console, Network, `data.json` 경로 확인 |
| JSON 오류 | `data.json`의 쉼표, 따옴표, 중괄호 확인 |
