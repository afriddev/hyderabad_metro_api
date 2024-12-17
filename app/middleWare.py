from starlette.middleware.base import BaseHTTPMiddleware
from fastapi import Request
from fastapi.responses import JSONResponse


class Custom404Middleware(BaseHTTPMiddleware):
    async def dispatch(self, request: Request, call_next):
        response = await call_next(request)
        if response.status_code == 404:
            return JSONResponse(
                status_code=404,
                content={"message": "Wrong URL, please check the route and try again."},
            )
        return response


#python -B -m uvicorn app.main:app --reload
