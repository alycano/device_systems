import time
import uuid
import logging
from fastapi import Request
from starlette.middleware.base import BaseHTTPMiddleware

logging.basicConfig(level=logging.INFO, format="%(asctime)s | %(message)s")
logger = logging.getLogger("device_systems")

class RequestMiddleware(BaseHTTPMiddleware):
    async def dispatch(self, request: Request, call_next):
        start_time = time.time()
        request_id = request.headers.get("X-Request-ID", str(uuid.uuid4().hex[:8]))

        response = await call_next(request)

        process_time = round(time.time() - start_time, 4)
        response.headers["X-Process-Time"] = str(process_time)
        response.headers["X-App-Name"] = "device_systems"
        response.headers["X-Request-ID"] = request_id

        logger.info("%s %s -> %s", request.method, request.url.path, response.status_code)

        return response