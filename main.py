from fastapi import FastAPI
from contextlib import asynccontextmanager
from app.connectDB import database
from app.routes.configure import router as config
from app.routes.getDetails import router as getDetails
from app.middleWare import Custom404Middleware
from app.enums.responseEnums import responseENUMS
from app.routes.getRoute import router as getTrainRoute
from fastapi.middleware.cors import CORSMiddleware
import uvicorn



@asynccontextmanager
async def lifespan(app: FastAPI):
    print("🔄 Connecting to Database...")
    await database.connect()
    print("✅ Database Connected!")
    yield  # Requests will be processed here
    print("🔄 Disconnecting from Database...")
    await database.disconnect()
    print("✅ Database Disconnected!")
app = FastAPI(lifespan=lifespan)


# CORS Middleware
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Custom Middleware
app.add_middleware(Custom404Middleware)

# Routers
app.include_router(config, prefix="/api/config")
app.include_router(getDetails, prefix="/api")
app.include_router(getTrainRoute, prefix="/api/route")

@app.get("/")
def handleHomeRoute():
    return {"message": "Server Running...", "version": "1.0.1"}

@app.get("/health")
def healthCheckUp():
    return {"message": "Good"}

if __name__ == "__main__":
    uvicorn.run("main:app", host="0.0.0.0", port=8000, reload=True)
