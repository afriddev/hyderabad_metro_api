from fastapi import FastAPI, Request
from fastapi.responses import JSONResponse
from fastapi.exceptions import RequestValidationError
from contextlib import asynccontextmanager
from app.connectDB import database
from app.routes.configure import router as config
from app.routes.getDetails import router as getDetails
from app.middleWare import Custom404Middleware
from app.enums.responseEnums import responseENUMS
from app.routes.getRoute import router as getTrainRoute
from fastapi.middleware.cors import CORSMiddleware






app = FastAPI()

@app.on_event("startup")
async def startup() -> None:
    database_ = app.state.database
    if not database_.is_connected:
        await database_.connect()


@app.on_event("shutdown")
async def shutdown() -> None:
    database_ = app.state.database
    if database_.is_connected:
        await database_.disconnect()

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

@app.exception_handler(RequestValidationError)
async def validation_exception_handler(request: Request, exc: RequestValidationError):
    return JSONResponse(
        status_code=401,
        content={
            "message": responseENUMS.INVALID_PAYLOAD.value,
        },
    )


app.add_middleware(Custom404Middleware)

app.include_router(config, prefix="/api/config")
app.include_router(getDetails, prefix="/api")
app.include_router(getTrainRoute, prefix="/api/route")


@app.get("/")
def handleHomeRoute():
    return JSONResponse(
        status_code=200, content={"message": "Server Running...", "version": "1.0.1"}
    )


