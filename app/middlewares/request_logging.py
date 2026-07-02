import logging
import time
import uuid
from contextvars import ContextVar

from fastapi import Request, Response


logger = logging.getLogger("app.request")
logger.propagate = False
request_id_context: ContextVar[str] = ContextVar("request_id", default="-")
client_ip_context: ContextVar[str] = ContextVar("client_ip", default="-")


def get_client_ip(request: Request) -> str:
    forwarded_for = request.headers.get("x-forwarded-for")
    if forwarded_for:
        return forwarded_for.split(",")[0].strip()

    real_ip = request.headers.get("x-real-ip")
    if real_ip:
        return real_ip.strip()

    if request.client and request.client.host:
        return request.client.host

    return "-"


async def request_logging_middleware(request: Request, call_next) -> Response:
    request_id = request.headers.get("x-request-id", str(uuid.uuid4()))
    client_ip = get_client_ip(request)
    start_time = time.perf_counter()

    request_id_token = request_id_context.set(request_id)
    client_ip_token = client_ip_context.set(client_ip)
    request.state.request_id = request_id
    request.state.client_ip = client_ip

    try:
        response = await call_next(request)
    except Exception:
        duration_ms = (time.perf_counter() - start_time) * 1000
        logger.exception(
            "request_failed method=%s path=%s client_ip=%s request_id=%s duration_ms=%.2f",
            request.method,
            request.url.path,
            client_ip,
            request_id,
            duration_ms,
        )
        raise
    finally:
        request_id_context.reset(request_id_token)
        client_ip_context.reset(client_ip_token)

    duration_ms = (time.perf_counter() - start_time) * 1000
    response.headers["X-Request-ID"] = request_id
    response.headers["X-Process-Time-ms"] = f"{duration_ms:.2f}"

    logger.info(
        "request_completed method=%s path=%s status_code=%s client_ip=%s request_id=%s duration_ms=%.2f user_agent=%s",
        request.method,
        request.url.path,
        response.status_code,
        client_ip,
        request_id,
        duration_ms,
        request.headers.get("user-agent", "-"),
    )

    return response