from starlette.middleware.base import BaseHTTPMiddleware
from fastapi import Request
from fastapi.responses import JSONResponse
import logging

logging.basicConfig(level=logging.INFO)

class Custom404Middleware(BaseHTTPMiddleware):
    async def dispatch(self, request: Request, call_next):
        try:
            logging.info(f"Processing request: {request.method} {request.url}")
            response = await call_next(request)
            if response.status_code == 404:
                return JSONResponse(
                    status_code=404,
                    content={"message": "Wrong URL, please check the route and try again."},
                )
            return response
        except Exception as e:
            logging.error(f"Middleware Error: {e}")
            return JSONResponse(
                status_code=500,
                content={"message": "Internal Server Error"},
            )
