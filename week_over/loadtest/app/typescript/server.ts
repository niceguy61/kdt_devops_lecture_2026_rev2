import express from 'express';
import { trace } from '@opentelemetry/api';
import { NodeSDK } from '@opentelemetry/sdk-node';
import { OTLPTraceExporter } from '@opentelemetry/exporter-trace-otlp-grpc';

const sdk = new NodeSDK({ traceExporter: new OTLPTraceExporter() });
sdk.start();

const app = express();
const tracer = trace.getTracer('order-api');

app.use((req, res, next) => {
  const traceId = (req.headers['x-trace-id'] as string) || `trc_${Math.random().toString(36).slice(2,10)}`;
  const start = Date.now();
  res.setHeader('X-Trace-Id', traceId);
  res.on('finish', () => {
    const log = {
      timestamp: new Date().toISOString(),
      level: res.statusCode >= 500 ? 'error' : 'info',
      service: 'order-api',
      traceId,
      spanId: trace.getActiveSpan()?.spanContext().spanId,
      method: req.method,
      path: req.path,
      status: res.statusCode,
      latency: Date.now() - start,
      errorCode: null, // 실패시 E001, E002...
      message: 'request completed'
    };
    console.log(JSON.stringify(log)); // stdout -> Promtail -> Loki
  });
  next();
});

app.get('/api/order', (req, res) => {
  const span = tracer.startSpan('db.query');
  span.setAttribute('db.statement', 'SELECT * FROM orders');
  setTimeout(() => {
    span.end();
    res.json({ orderId: 123 });
  }, 120);
});

app.listen(8080);