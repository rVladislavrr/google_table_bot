import uuid

from starlette.middleware.base import BaseHTTPMiddleware
from starlette.requests import Request


class LoggingMiddleware(BaseHTTPMiddleware):
    async def dispatch(self, request: Request, call_next):

        request_id = str(uuid.uuid4())
        request.state.request_id = request_id

        return await call_next(request)