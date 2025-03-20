from starlette.middleware.base import BaseHTTPMiddleware
from fastapi import Request
from fastapi.responses import JSONResponse
import traceback

class Custom404Middleware(BaseHTTPMiddleware):
    async def dispatch(self, request: Request, call_next):
        try:
            response = await call_next(request)
            if response.status_code == 404:
                return JSONResponse(
                    status_code=404,
                    content={"message": "Wrong URL, please check the route and try again."},
                )
            return response
        except AssertionError as e:
            return JSONResponse(
                status_code=400,
                content={"error": "AssertionError", "message": str(e), "trace": traceback.format_exc()},
            )
        except Exception as e:
            return JSONResponse(
                status_code=500,
                content={"error": "Internal Server Error", "message": str(e), "trace": traceback.format_exc()},
            )
