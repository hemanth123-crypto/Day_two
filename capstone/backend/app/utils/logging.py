from __future__ import annotations
import logging
import time
from typing import Callable
from fastapi import Request, Response
from starlette.middleware.base import BaseHTTPMiddleware

# Configure root logger with standard formatting
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s [%(levelname)s] %(name)s: %(message)s',
    datefmt='%Y-%m-%d %H:%M:%S',
)

logger = logging.getLogger('course_finder')


class RequestLoggingMiddleware(BaseHTTPMiddleware):
    """
    HTTP Middleware that logs all incoming API requests with execution timing.
    Guarantees secrets, API keys, and sensitive tokens are never logged.
    """
    async def dispatch(self, request: Request, call_next: Callable) -> Response:
        start_time = time.time()
        client_host = request.client.host if request.client else "unknown"
        method = request.method
        path = request.url.path

        # Log request start (without secrets or authorization headers)
        logger.info(f"Incoming {method} {path} from {client_host}")

        try:
            response = await call_next(request)
            process_time_ms = round((time.time() - start_time) * 1000, 2)
            logger.info(f"Completed {method} {path} -> {response.status_code} in {process_time_ms}ms")
            response.headers["X-Process-Time-Ms"] = str(process_time_ms)
            return response
        except Exception as exc:
            process_time_ms = round((time.time() - start_time) * 1000, 2)
            logger.error(f"Error {method} {path} after {process_time_ms}ms: {exc}")
            raise
