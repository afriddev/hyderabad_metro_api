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

@asynccontextmanager
async def lifespan(app: FastAPI):
    await database.connect()
    print("Database connected!")
    yield
    await database.disconnect()
    print("Database disconnected!")

app = FastAPI(lifespan=lifespan)

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


