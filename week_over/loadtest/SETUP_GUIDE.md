# 전체 셋업 가이드 (팀 공통)

## 1. Infra 띄우기 (조교/강사가 1번만)
docker-compose up -d prometheus grafana loki tempo
- Prometheus: http://localhost:9090 (Targets에서 app UP 확인)
- Grafana: http://localhost:3000 (admin/admin)
- Loki: http://localhost:3100/ready
- Tempo: http://localhost:3200/status

## 2. 내 앱에 Observability 끼우기 (팀별)
각 언어별 SETUP.md 참고
- Python: app/python/SETUP.md
- Java: app/java/SETUP.md
- TypeScript: app/typescript/SETUP.md

핵심 3단계:
1) 라이브러리 설치 (requirements / build.gradle / package.json)
2) /metrics 엔드포인트 열기 (Prometheus가 긁어가도록)
3) 미들웨어 1줄 + errorCode 1줄

## 3. Prometheus 설정 확인
prometheus/prometheus.yml:
  - job_name: 'your-team'
    metrics_path: '/metrics' (Python/TS) 또는 '/actuator/prometheus' (Java)
    static_configs: targets: ['host.docker.internal:8080'] # 로컬 앱이면

docker-compose로 앱을 띄우면 'app:8080' 으로, 로컬에서 직접 띄우면 host.docker.internal:8080

## 4. Grafana 연결
grafana/datasource.yml 이미 Exemplars 설정 완료:
- Prometheus -> Tempo 연동 (traceId로 점프)
- Loki -> Tempo 연동 (로그에서 traceId 클릭하면 trace로)

Grafana > Dashboards > Import > grafana/dashboard.json 업로드 -> 12개 패널 즉시 사용

## 5. k6 실행
TARGET_URL=http://localhost:8080/api/order k6 run k6/smoke.TEMPLATE.js
-> Prometheus에서 http_req_duration p95, Grafana에서 Latency Histogram 확인
-> 느린 요청 traceId 클릭 -> Tempo -> Loki 로그까지 점프

## 6. CI 게이트
.github/workflows/k6-ci.yml 에서 TARGET_URL만 팀 API로 변경 후 push
p95>500ms면 CI 실패 -> 배포 차단
