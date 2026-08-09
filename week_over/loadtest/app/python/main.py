import json
import os
import random
import time
import uuid
from urllib.error import URLError
from urllib.request import Request as UrlRequest, urlopen

import structlog
from fastapi import FastAPI, Request
from fastapi.responses import JSONResponse
from opentelemetry import trace
from opentelemetry.exporter.otlp.proto.grpc.trace_exporter import OTLPSpanExporter
from opentelemetry.instrumentation.fastapi import FastAPIInstrumentor
from opentelemetry.sdk.trace import TracerProvider
from opentelemetry.sdk.trace.export import BatchSpanProcessor
from prometheus_client import Counter, Histogram, make_asgi_app

LOKI_URL = os.getenv("LOKI_URL", "").rstrip("/")

REQUESTS = Counter(
    "http_requests_total",
    "Total HTTP requests",
    ["method", "path", "status"],
)
REQUEST_DURATION = Histogram(
    "http_request_duration_seconds",
    "HTTP request duration in seconds",
    ["method", "path"],
)
APP_LOGS = Counter(
    "app_logs_total",
    "Application log events",
    ["level", "errorCode", "status"],
)


def send_to_loki(logger, method_name, event_dict):
    if LOKI_URL:
        labels = {
            "service": str(event_dict.get("service", "order-api")),
            "level": method_name,
        }
        payload = {
            "streams": [
                {
                    "stream": labels,
                    "values": [[str(time.time_ns()), json.dumps(event_dict, ensure_ascii=False)]],
                }
            ]
        }
        try:
            request = UrlRequest(
                f"{LOKI_URL}/loki/api/v1/push",
                data=json.dumps(payload).encode("utf-8"),
                headers={"Content-Type": "application/json"},
                method="POST",
            )
            with urlopen(request, timeout=0.2):
                pass
        except (OSError, URLError, TimeoutError):
            pass
    return event_dict


structlog.configure(
    processors=[send_to_loki, structlog.processors.JSONRenderer()],
    wrapper_class=structlog.BoundLogger,
)
logger = structlog.get_logger()

app = FastAPI()
app.mount("/metrics", make_asgi_app())

trace.set_tracer_provider(TracerProvider())
tracer = trace.get_tracer(__name__)
span_processor = BatchSpanProcessor(OTLPSpanExporter())
trace.get_tracer_provider().add_span_processor(span_processor)
FastAPIInstrumentor.instrument_app(app)


def get_otel_trace_id(span=None):
    active_span = span or trace.get_current_span()
    span_context = active_span.get_span_context()
    if span_context.is_valid:
        return f"{span_context.trace_id:032x}"
    return f"trc_{uuid.uuid4().hex[:8]}"


@app.middleware("http")
async def add_trace_id(request: Request, call_next):
    request_trace_id = request.headers.get("X-Trace-Id")
    start = time.time()
    with tracer.start_as_current_span("http.request") as request_span:
        trace_id = get_otel_trace_id(request_span)
        response = await call_next(request)
    elapsed = time.time() - start
    status = str(response.status_code)
    REQUESTS.labels(request.method, request.url.path, status).inc()
    REQUEST_DURATION.labels(request.method, request.url.path).observe(elapsed)
    APP_LOGS.labels("info", "", status).inc()
    logger.info(
        service="order-api",
        traceId=trace_id,
        requestTraceId=request_trace_id,
        method=request.method,
        path=request.url.path,
        status=response.status_code,
        latency=int(elapsed * 1000),
        errorCode=None,
        message="request completed",
    )
    response.headers["X-Trace-Id"] = trace_id
    return response


@app.get("/api/health")
def health():
    return {"status": "ok"}


@app.get("/api/order")
def order():
    with tracer.start_as_current_span("db.query") as span:
        trace_id = get_otel_trace_id(span)
        span.set_attribute("db.statement", "SELECT * FROM orders")
        time.sleep(random.uniform(0.05, 0.2))
    if random.random() < 0.02:
        APP_LOGS.labels("error", "E002", "500").inc()
        logger.error(
            service="order-api",
            traceId=trace_id,
            errorCode="E002",
            status=500,
            message="payment timeout",
        )
        return JSONResponse(status_code=500, content={"errorCode": "E002", "status": 500})
    return {"orderId": 123}
