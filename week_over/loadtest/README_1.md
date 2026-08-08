
# k6-observability-lab (팀별 코드에 끼워넣기 버전)

팀별 프로젝트가 달라서 통째 교체 불가능 -> 미들웨어 1줄 + 에러코드 1줄 방식

## Python
from middleware import ObservabilityMiddleware
app.add_middleware(ObservabilityMiddleware)
# 팀 로직: request.state.errorCode = "E002"

## Java
request.setAttribute("errorCode","E002");

## TypeScript
app.use(observability({ serviceName: 'your-team' }));
// (req as any).errorCode = 'E002';

## k6
TARGET_URL=https://your-team-api.com/api/order k6 run k6/smoke.TEMPLATE.js

## Grafana
dashboard.json 12개 패널은 그대로 사용, JSON 로그면 자동 수집
