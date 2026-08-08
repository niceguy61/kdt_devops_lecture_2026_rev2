# Python 팀 셋업 (5분)

1. 라이브러리 설치
pip install -r requirements-observability.txt
# 또는 pip install structlog opentelemetry-api opentelemetry-sdk opentelemetry-exporter-otlp opentelemetry-instrumentation-fastapi prometheus-client

2. Prometheus 메트릭 엔드포인트 열기 (app/main.py에 3줄)
from prometheus_client import Counter, Histogram, make_asgi_app
metrics_app = make_asgi_app()
app.mount("/metrics", metrics_app)  # -> http://localhost:8080/metrics 에서 스크랩

3. 미들웨어 끼우기 (1줄)
from middleware import ObservabilityMiddleware
app.add_middleware(ObservabilityMiddleware)

4. docker-compose에서 Prometheus가 내 앱을 스크랩하도록 (이미 되어있음)
prometheus.yml:
  scrape_configs:
    - job_name: 'your-team-api'
      targets: ['app:8080']  # 팀 도커 서비스명:포트

5. 환경변수
OTEL_EXPORTER_OTLP_ENDPOINT=http://tempo:4317
LOKI_URL=http://loki:3100

6. 확인
curl http://localhost:8080/metrics  # 메트릭 나와야 함
curl http://localhost:8080/api/order -H "X-Trace-Id: trc_test" # 로그에 traceId 찍히는지
