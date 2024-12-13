from fastapi import FastAPI, Request
from fastapi.responses import JSONResponse
from fastapi.exceptions import RequestValidationError
from contextlib import asynccontextmanager
from app.connectDB import database
from app.routes.configureTrainDetailsRoute import router as train_router
from . import middleWare


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
        status_code=400,
        content={
            "message": "Invalid payload, please check your data.",
        },
    )


app.add_middleware(middleWare.Custom404Middleware)
app.include_router(train_router, prefix="/config/train/route")


@app.get("/")
def handleHomeRoute():
    return JSONResponse(
        status_code=200, content={"message": "Server Running...", "version": "1.0.1"}
    )
