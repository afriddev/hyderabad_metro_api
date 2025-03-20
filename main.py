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




app = FastAPI()
# Store the database instance in app.state
app.state.database = database

@app.on_event("startup")
async def startup() -> None:
    database_ = app.state.database
    if not database_.is_connected:
        await database_.connect()
        print("✅ Database Connected!")

@app.on_event("shutdown")
async def shutdown() -> None:
    database_ = app.state.database
    if database_.is_connected:
        await database_.disconnect()
        print("✅ Database Disconnected!")


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
