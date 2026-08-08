
"""
기존 프로젝트에 1줄로 끼우기
from middleware import ObservabilityMiddleware
app.add_middleware(ObservabilityMiddleware)
"""
import time, uuid, structlog
from starlette.middleware.base import BaseHTTPMiddleware
from opentelemetry import trace
logger = structlog.get_logger()
class ObservabilityMiddleware(BaseHTTPMiddleware):
    async def dispatch(self, request, call_next):
        trace_id = request.headers.get("X-Trace-Id", f"trc_{uuid.uuid4().hex[:8]}")
        start = time.time()
        response = await call_next(request)
        latency = int((time.time()-start)*1000)
        log_data = {
            "service": "your-service-name",
            "traceId": trace_id,
            "method": request.method,
            "path": request.url.path,
            "status": response.status_code,
            "latency": latency,
            "errorCode": getattr(request.state, "errorCode", None),
            "ip": request.client.host,
        }
        if response.status_code >= 500:
            logger.error(**log_data, message="server error")
        else:
            logger.info(**log_data, message="ok")
        response.headers["X-Trace-Id"] = trace_id
        return response
