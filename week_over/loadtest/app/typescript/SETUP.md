# TypeScript 팀 셋업

1. 설치
npm install @opentelemetry/api @opentelemetry/sdk-node @opentelemetry/exporter-trace-otlp-grpc @opentelemetry/auto-instrumentations-node prom-client
# 또는 package.observability.json 참고

2. Prometheus 메트릭 엔드포인트 열기 (server.ts에 5줄)
import client from 'prom-client';
const collectDefaultMetrics = client.collectDefaultMetrics;
collectDefaultMetrics();
app.get('/metrics', async (req,res)=>{
  res.set('Content-Type', client.register.contentType);
  res.end(await client.register.metrics());
});

3. Observability 미들웨어 끼우기
import { observability } from './observability';
app.use(observability({serviceName: 'your-team'}));

4. OpenTelemetry SDK 초기화 (server.ts 최상단에)
import { NodeSDK } from '@opentelemetry/sdk-node';
import { getNodeAutoInstrumentations } from '@opentelemetry/auto-instrumentations-node';
const sdk = new NodeSDK({
  instrumentations: [getNodeAutoInstrumentations()]
});
sdk.start();

5. 확인
curl http://localhost:8080/metrics
