from fastapi import FastAPI as FastAPIOffline
import uvicorn
from src.auth.routers import router as router_auth
from src.video.routers import router as router_video
from fastapi.testclient import TestClient
# from src.kafka.routers import router as router_kafka
# from fastapi.middleware.cors import CORSMiddleware
from fastapi.middleware.cors import CORSMiddleware
from fastapi import WebSocket

app = FastAPIOffline()
#app.include_router(router_auth)
app.include_router(router_video)
# app.include_router(router_kafka)

origins = [
    "http://localhost.tiangolo.com",
    "https://localhost.tiangolo.com",
    "http://localhost",
    "http://localhost:8080",
    "http://localhost:8000",
]


app.add_middleware(
    CORSMiddleware,
    allow_origins=[origins],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)
@app.get("/")
async def root():
    return {"message": "Hello World"}


@app.websocket("/ws/")
async def websocket_endpoint(websocket: WebSocket):
    await websocket.accept()



# uvicorn.run(app, host="0.0.0.0", port=8000)