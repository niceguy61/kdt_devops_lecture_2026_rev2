from fastapi import FastAPI, Request
import structlog, uuid, time, random
from opentelemetry import trace
from opentelemetry.instrumentation.fastapi import FastAPIInstrumentor
from opentelemetry.exporter.otlp.proto.grpc.trace_exporter import OTLPSpanExporter
from opentelemetry.sdk.trace import TracerProvider
from opentelemetry.sdk.trace.export import BatchSpanProcessor

# JSON Logger + traceId
structlog.configure(
    processors=[structlog.processors.JSONRenderer()],
    wrapper_class=structlog.BoundLogger,
)
logger = structlog.get_logger()

app = FastAPI()
trace.set_tracer_provider(TracerProvider())
tracer = trace.get_tracer(__name__)
span_processor = BatchSpanProcessor(OTLPSpanExporter())
trace.get_tracer_provider().add_span_processor(span_processor)
FastAPIInstrumentor.instrument_app(app)

@app.middleware("http")
async def add_trace_id(request: Request, call_next):
    trace_id = request.headers.get("X-Trace-Id", f"trc_{uuid.uuid4().hex[:8]}")
    start = time.time()
    response = await call_next(request)
    latency = int((time.time()-start)*1000)
    # 핵심 10필드 + errorCode
    logger.info(
        service="order-api",
        traceId=trace_id,
        method=request.method,
        path=request.url.path,
        status=response.status_code,
        latency=latency,
        errorCode=None, # 정상시 None, 실패시 E001 등
        message="request completed"
    )
    response.headers["X-Trace-Id"] = trace_id
    return response

@app.get("/api/order")
def order():
    with tracer.start_as_current_span("db.query") as span:
        span.set_attribute("db.statement", "SELECT * FROM orders")
        time.sleep(random.uniform(0.05,0.2))
    if random.random() < 0.02:
        logger.error(service="order-api", traceId="trc_xxx", errorCode="E002", status=500, message="payment timeout")
        return {"errorCode":"E002","status":500}
    return {"orderId":123}