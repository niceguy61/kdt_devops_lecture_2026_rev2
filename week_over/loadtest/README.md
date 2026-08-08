# 웹 프로젝트 부하 테스트 특강 (2시간) - 강의안

> 제목: 망하기 전에 터뜨려보기 - 웹 프로젝트 부하 테스트 실전
> 시간: 120분 (Part 1: 60분, Part 2: 60분)
> 대상: 백엔드/서버 개발자, SRE, QA

---

## Part 1. 부하 테스트 Fundamental (60분)

### 1. 왜 하느냐? - 부하 테스트의 목적 (10분)

#### 1.1 기능 테스트 vs 부하 테스트
- 기능 테스트: "제대로 동작하는가? (Correctness)"
- 부하 테스트: "감당 가능한가? (Scalability, Reliability)" - 동시성, 시간, 자원 경합
- 예시: 로그인 기능은 1명일 때 OK, 10,000명 동시 로그인 시 DB 커넥션 고갈

#### 1.2 우리가 겪는 3가지 장애 유형
- **Latency 장애**: 응답이 200ms -> 8s로 늘어남. 사용자는 3초면 이탈.
- **Throughput 장애**: RPS가 500에서 더 이상 안 오르고 큐잉됨.
- **Resource Exhaustion**: OOM, FD 고갈, Thread Pool 고갈, CPU Throttling

#### 1.3 비용 관점
- 운영 장애 1시간 비용 = (개발자 야근 + 고객 이탈 + 환불 + 브랜드 실추)
- 부하 테스트 1회 비용 = EC2 몇 대 + 1일 공수. 압도적으로 싸다.
- SLO 기반 사고: "p95 500ms, 가용성 99.9%를 어떻게 증명할 것인가?"

#### 1.4 부하 테스트가 답해야 할 질문 4가지
1. 우리 시스템의 Max RPS는 얼마인가?
2. p95 500ms를 유지할 수 있는 한계는 몇 명인가?
3. 병목은 어디인가? (DB? API? Cache? Network?)
4. Auto Scaling은 제때, 제대로 동작하는가?

### 2. 언제 하느냐? - 라이프사이클 (5분)

#### 2.1 4가지 타이밍
- **개발 전 (Capacity Planning)**: 예상 MAU -> RPS 변환, 서버 사이즈 산정. 예) 10만 MAU = 피크 300 RPS
- **개발 중 (Bottleneck Detection)**: 신규 API 개발 시 단위 부하 테스트로 N+1, 인덱스 누락 찾기
- **배포 전 (Go/No-Go Gate)**: 스테이징에서 운영 예상 트래픽 120%로 검증
- **운영 중 (Soak & Chaos)**: 2시간 이상 장시간 테스트로 메모리 누수 검증

#### 2.2 CI/CD에 녹이는 방법
- PR 단위: Smoke Test (VU 10, 1분) - 기능 깨졌는지 빠른 검증
- 야간: Load Test (VU 200, 30분) - develop 브랜치 대상
- 릴리즈 전: Stress Test (Breaking Point까지) - 수동 트리거

#### 2.3 반드시 해야 하는 이벤트
- 티켓팅, 선착순 쿠폰, 수강신청, 월말 정산, 블랙프라이데이

### 3. 무엇을 테스트 하느냐? - 케이스별 상세 (15분)

#### 3.1 테스트 종류 6가지
1.  **Load Test**: 평소 트래픽. 예) 평시 1000 VU 유지. 시스템이 정상 동작하는지 확인.
2.  **Stress Test**: 한계까지. VU를 100 -> 1000 -> 2000으로 계속 올려 어디서 꺾이는지 확인.
3.  **Spike Test**: 0 -> 5000 VU로 10초 안에 급등. 큐잉, 서킷브레이커, Rate Limit 동작 확인.
4.  **Soak Test (Endurance)**: 100 VU로 2~4시간 유지. 메모리 누수, 커넥션 누수, 로그 파일 증식 확인.
5.  **Scalability Test**: 부하에 따라 HPA, ASG가 scale-out/in 되는지, scale-out 시간은 몇 분인지.
6.  **Breakpoint / Isolation Test**: 전체 시나리오가 아닌 `POST /api/pay` 하나만 집중적으로.

#### 3.2 시나리오 설계 핵심
- **Open Model vs Closed Model**: Open(초당 N명 도착, 실제 유저), Closed(100명이 끝나면 바로 재요청, 부하 발생기).
- **Think Time**: 실제 유저는 API 사이 1~3초 쉼. 없으면 DB에만 극한 부하가 가서 현실과 괴리.
- **Data Feeding**: 유저 1000명이 전부 같은 ID로 로그인하면 캐시 히트율 100%로 왜곡. CSV, Faker로 분산.

#### 3.3 데이터 설계 실패 사례
- 캐시: 동일 상품 ID만 조회 -> Redis 히트 99%, 운영은 60%. 결과 뻥튀기.
- DB: 운영은 1억 건인데 스테이징은 1만 건. 인덱스 없이도 빨라서 병목 못 찾음.

### 4. 구체적 예시 - 어디에 부하를 주나? (10분)

#### 4.1 Hardware / Infra 레벨 부하
- **CPU Bound**: 이미지 리사이징, 암호화, JSON 파싱. CPU 100%에서 Latency 급증.
- **Memory Bound**: 힙 메모리, Off-heap. OOM Killer 동작.
- **Disk I/O Bound**: 로그 과다 기록, 임시 파일 생성. iowait 증가.
- **Network Bound**: 대용량 파일 다운로드, 외부 API 호출 시 대역폭 포화.

#### 4.2 API 레벨 부하
- **REST API**: `GET /products?page=10000` 같은 Deep Pagination 부하.
- **GraphQL**: 클라이언트가 `user { posts { comments { ... } } }` N+1 요청. Depth Limit 필요.
- **gRPC**: HTTP/2 멀티플렉싱, Protobuf 직렬화 비용. 커넥션 1개에 RPS 몰빵.
- **WebSocket**: 10만 연결 유지(Connection) 부하 vs 메시지 전송(Throughput) 부하는 별개.

#### 4.3 Software / App 레벨 부하
- **DB Connection Pool**: HikariCP 10개인데 100개 동시 요청 -> 대기 큐 폭발.
- **Thread Pool**: Tomcat 200 스레드 고갈 시 201번째 요청은 큐에서 대기.
- **GC**: Young GC가 1초에 20번 발생 -> Stop-The-World로 p99 튐.
- **Lock Contention**: synchronized, 분산락(Redisson)으로 인한 병목.
- **Cache Stampede**: 캐시 만료 시 1000개 요청이 동시에 DB로.

### 5. 어떤 툴로 때리나? - 부하 발생기 (10분)

#### 5.1 툴 선정 5대 기준
1. Protocol 지원 (HTTP, gRPC, WS)
2. 스크립트 언어 (개발자가 쓰기 편한가)
3. 분산 부하 지원
4. 리포팅/관측 연동
5. 에코시스템

#### 5.2 대표 툴 비교

| 툴 | 언어 | 장점 | 단점 | 추천 상황 |
| :--- | :--- | :--- | :--- | :--- |
| **k6** | JavaScript | 개발자 친화, Grafana 연동 최고, 클라우드 | JS 외 확장 어려움 | 현업 표준, 대부분 |
| **nGrinder** | Groovy/Jython | GUI로 관리, 한국에서 레퍼런스 많음, 분산 쉬움 | UI 올드, 스크립트 진입장벽 | 대기업, QA팀 주도 |
| **Locust** | Python | 코드 가독성 최고, 시나리오 분기 쉬움 | 고성능에는 리소스 많이 필요 | 복잡한 유저 여정 |
| **JMeter** | Java/GUI | 플러그인 1000개, 프로토콜 최다 | GUI가 무거움, 리소스 많이 먹음 | 레거시, 비개발자 |
| **Gatling** | Scala/Kotlin | 고성능, 리포트 예쁨 | Scala 학습곡선 | Scala 스택, 고성능 필요 |
| **Artillery / Vegeta** | JS / Go | 가볍고 빠름 | 기능 단순 | 간단한 API 스모크 |

#### 5.3 k6 맛보기 스크립트
```javascript
import http from 'k6/http';
import { sleep } from 'k6';
export const options = {
  stages: [
    { duration: '1m', target: 100 }, // 100명까지 증가
    { duration: '3m', target: 100 }, // 100명 유지
    { duration: '1m', target: 0 }, // 0으로 감소
  ],
  thresholds: { 'http_req_duration': ['p(95)<500'] }
};
export default function() {
  http.get('https://api.example.com/products');
  sleep(1);
}
```

### 6. 어떤 툴로 보나? - 측정/관측 스택 (10분)

#### 6.1 관측 3요소
- **Metrics**: 숫자 (CPU 80%, RPS 500) - Prometheus
- **Logs**: 기록 (2026-08-07 ERROR Payment Failed) - Loki, ELK
- **Traces**: 추적 (요청이 A->B->C로 가는데 B에서 800ms) - Jaeger, Tempo, Datadog APM

#### 6.2 스택 비교
- **Prometheus + Grafana**: 무료, 표준. Pull 방식이라 타겟이 죽어도 감지. 직접 구축/운영 필요.
- **Datadog / New Relic**: 유료지만 올인원. APM, Log, Infra 한곳에. 1인당 과금 주의.
- **ELK (Elasticsearch) / Splunk**: 로그 검색/분석 최강. 비용/운영 난이도 높음.
- **Grafana Loki**: 로그도 메트릭처럼. 라벨 기반이라 저렴. Grafana와 찰떡.

#### 6.3 전체 아키텍처
```
[k6, Locust] --(RPS)--> [ALB] --> [App Server (Exporter)] --> [DB, Redis, Kafka]
                                |
                                +-- metrics --> Prometheus --> Grafana
                                +-- logs ----> Loki / ELK --> Grafana / Kibana
                                +-- traces ---> Tempo / Jaeger
```

---

## Part 2. 실전 메트릭과 대시보드 (60분)

### 7. 반드시 봐야 할 핵심 메트릭 12개 (25분)

#### A. 사용자 관점 - Golden Signals
1.  **Latency (p50, p95, p99, p99.9)**: 평균(avg)은 의미 없다. p95가 500ms여도 p99가 5초면 1%는 지옥.
2.  **RPS / TPS (Throughput)**: 초당 처리량. RPS가 더 이상 안 올라가고 Latency만 오르면 포화.
3.  **Error Rate**: `5xx / total`. 4xx는 클라이언트 실수, 5xx는 우리 잘못. 0.1% 넘어가면 알림.
4.  **Concurrent Users (VUs / Active Connections)**: 동접. WAS Thread 수와 직접 연결.

#### B. 시스템 관점 - Resource Saturation
5.  **CPU Usage & Load Average**: `usage > 80%` 지속되면 위험. Load Avg가 코어 수보다 높으면 큐잉.
6.  **Memory Usage & GC**: Heap 사용률, GC Count, GC Pause Time. `java.lang.OutOfMemoryError` 전조.
7.  **Disk I/O & Network I/O**: `iowait`, `iops`, `bytes sent/received`. 로그 폭주로 디스크 풀 현상.
8.  **FD / Socket / Thread Count**: `Too many open files` 에러. 커넥션 누수 탐지 핵심.

#### C. 애플리케이션 내부 - Bottleneck
9.  **DB Connection Pool**: `Active`, `Idle`, `Pending`. Pending이 0보다 크면 대기 발생. 가장 흔한 병목.
10. **Cache Hit/Miss Rate**: Hit 95% -> 80%로 떨어지면 DB로 트래픽 직격. Miss Storm 탐지.
11. **Message Queue Depth / Lag**: Kafka Lag이 계속 증가하면 Consumer가 못 따라감.
12. **Auto Scaling Metrics**: Desired Count vs Actual Count, Scale-Out 소요 시간. 3분 걸리면 그 사이 장애.

### 8. API 전문 메트릭 (10분)

- **API별 Latency Breakdown**: `GET /api/users`는 100ms인데 `GET /api/feed`는 2s. 병목 API 식별.
- **Endpoint별 RPS & Error Heatmap**: 어떤 API가 가장 많이 호출되고, 어디서 에러가 나는지 히트맵.
- **Request / Response Payload Size**: 응답이 2MB면 네트워크가 병목. 압축(gzip) 필요.
- **TTFB vs TTLB**: TTFB가 길면 서버 처리 느림, TTLB가 길면 네트워크/대용량 응답.
- **Upstream / External Latency**: `payment-api` 호출이 3초. 우리 코드는 100ms인데 외부 때문에 p99 터짐. Circuit Breaker 필요 신호.
- **Rate Limit & Throttling Count**: `429 Too Many Requests` 얼마나 발생하는지. 클라이언트 재시도 전략 필요.
- **HTTP Status Code Distribution**: 200, 201, 400, 401, 429, 500, 502, 503 비율 시계열.

### 9. 로그 기반 JSON Filtering & 대시보드화 실전 (25분)

#### 9.1 왜 JSON Logging인가?
- Plain Text: `2026-08-07 User 123 failed to pay` -> 파싱하려면 정규식 지옥.
- JSON: `{"level":"error","userId":123,"action":"pay","durationMs":2300,"errorCode":"PG_TIMEOUT"}` -> 필드 그대로 필터/집계.
- 필수 필드: `timestamp, level, traceId, spanId, method, path, status, durationMs, userId, errorCode, version`

#### 9.2 파이프라인 구조
- **수집**: App -> stdout (json) -> Promtail / Fluent Bit / Vector / Filebeat
- **저장**: Loki (저렴, 라벨 기반) / Elasticsearch (강력한 검색) / S3 + Athena
- **시각화**: Grafana / Kibana / Datadog Log Explorer
- **연결**: Grafana에서 로그 라인 클릭 -> Tempo Trace로 이동 (traceId 기반)

#### 9.3 JSON 필터링으로 만드는 대시보드 12선

> LogQL (Loki) 기준 예시

**1. Latency Histogram by API Path**
```logql
{app="api"} | json | durationMs > 0 | histogram_over_time(durationMs) by (path)
```
-> API별 느린 구간 시각화

**2. Error Top N**
```logql
{app="api"} | json | level="error" | stats by (errorCode) | topk(10)
```
-> 가장 많이 터지는 에러 코드

**3. Slow Query Dashboard**
```logql
{app="db-proxy"} | json | queryType="SELECT" | durationMs > 1000 | line_format "{{.query}} - {{.durationMs}}ms"
```
-> 1초 이상 걸린 쿼리만

**4. User Journey Funnel**
```logql
{app="api"} | json | traceId!="" | group by (traceId) | count by (action)
```
-> traceId로 묶어 로그인->장바구니->결제 이탈률 추적

**5. Abnormal Traffic / IP 탐지**
```logql
{app="api"} | json | stats count() by (clientIp) | count > 1000
```
-> 특정 IP에서 초당 1000회 호출

**6. Business KPI**
```logql
{app="api"} | json | action="payment" | stats count() by (status) | (failed / total) * 100
```
-> 결제 실패율 비즈니스 대시보드

**7. Cache Miss Storm**
```logql
{app="api"} | json | cache="miss" | rate() by (cacheKeyPrefix)
```
-> 특정 시간에 miss가 10배 증가

**8. External API Failure Map**
```logql
{app="api"} | json | upstreamHost!="" | level="error" | stats by (upstreamHost, status)
```
-> 어느 외부 API가 얼마나 실패하는지

**9. GC / OOM 전조 증상**
```logql
{app="api"} | json | message=~"(?i)gc|pause|oom" | count_over_time(5m)
```
-> GC 빈도 급증 알림

**10. Security Audit**
```logql
{app="api"} | json | status=~"401|403" | stats by (clientIp, path) | topk(20)
```
-> 무차별 대입 시도 IP 탐지

**11. Deployment Correlation**
```logql
{app="api"} | json | stats avg(durationMs), errorRate by (version)
```
-> v1.2.3 배포 후 p95가 2배 증가? 롤백 결정

**12. Log Volume & Cost**
```logql
sum by (app, level) (count_over_time({app=~".+"} | json [1m]))
```
-> 앱/레벨별 로그 발생량, 비용 최적화

#### 9.4 쿼리 언어 비교
- **LogQL (Loki)**: `| json | field="value" | rate()` - Prometheus 스타일, 가볍다
- **Datadog**: `@duration:>1000 @http.path:/api/pay` - UI가 강력하고 자동 파싱
- **Lucene (ELK)**: `level:error AND durationMs:>1000` - 검색 기능 최강

#### 9.5 로그-메트릭-트레이스 연결 (가장 중요)
- 로그에 `traceId`를 심으면 Grafana에서 로그 -> Trace -> Metrics로 점프 가능
- Exemplars: Prometheus 메트릭 포인트에 traceId를 붙여서 "이 순간 느려진 요청의 로그 보기"

---

### [마무리] 체크리스트 & Q&A (10분)

**부하 테스트 전 체크리스트 10선**
1. 운영과 동일한 스펙인가? (DB 데이터량 포함)
2. 캐시 웜업 했는가?
3. 외부 API는 Mocking했는가? (진짜 PG사에 부하주면 안됨)
4. 모니터링 대시보드 켜놨는가?
5. 알림 끄거나, 테스트용 채널로 분리했는가?
6. 테스트 데이터는 격리했는가? (운영에 테스트 결제 생성 금지)
7. Auto Scaling Max치는 충분히 높여놨는가?
8. Think Time 넣었는가?
9. 목표치(Threshold) 정의했는가? (p95 < 500ms)
10. 롤백/중단 기준 정했는가? (Error 1% 넘으면 중단)

**자주 하는 실수 Top 5**
- 운영 DB에 그대로 부하
- 로컬에서 1만 VU 쏘기 (본인 PC가 먼저 죽음)
- 평균 Latency만 보고 "빠르다" 착각
- 부하 발생기 모니터링 안함 (발생기가 병목)
- 테스트 후 리소스 정리 안해서 비용 폭탄

# k6 Observability Lab - 2교시 실습용

## 구조
```
k6/ - smoke.js(10줄), load.js, ci-gate.js(p95<500ms)
prometheus/ - prometheus.yml (exemplars 활성화)
grafana/ - dashboard.json (12개 패널), datasource.yml (Exemplars -> Tempo 연동)
app/python|java|typescript - JSON + traceId + errorCode 심기 샘플
docker-compose.yml - 전체 Observability 스택 원클릭 실행
.github/workflows/k6-ci.yml - p95 CI 게이트
```

## 빠른 시작
```bash
git clone https://github.com/niceguy61/kdt_devops_lecture_2026_rev2.git
cd week_over/loadtest
docker-compose up -d
# Smoke Test 10줄
k6 run k6/smoke.js
# Grafana: http://localhost:3000 (admin/admin) 대시보드 import grafana/dashboard.json
```

## 핵심 개념
- 라벨은 적게, JSON 필드는 풍부하게
- errorCode(E001~) + HTTP status(status) 동시 필터 - 커스텀 오류 Top N 핵심
- Metric -> Trace -> Log 점프: Grafana Exemplars 활성화 + traceId 심기
- p95<500ms: 평균이 아닌 95분위수로 CI 게이트

## 체크리스트
동일스펙? 웜업? Mock? ThinkTime? 중단기준?

## 실수 Top5
운영DB직격, 로컬1만VU, 평균만보기, 부하기 미모니터링, 비용폭탄