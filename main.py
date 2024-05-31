from fastapi import FastAPI as FastAPIOffline
import uvicorn
from src.auth.routers import router as router_auth
from src.video.routers import router as router_video
from fastapi.testclient import TestClient
# from src.kafka.routers import router as router_kafka
# from fastapi.middleware.cors import CORSMiddleware
from starlette.middleware.cors import CORSMiddleware

from fastapi import WebSocket

app = FastAPIOffline()
#app.include_router(router_auth)
app.include_router(router_video)
# app.include_router(router_kafka)

@app.middleware("http")
async def add_cors_headers(request, call_next):
    response = await call_next(request)
    response.headers["Access-Control-Allow-Origin"] = "https://www.teste.com.br, http://localhost:3000"
    response.headers["Access-Control-Allow-Credentials"] = "true"
    response.headers["Access-Control-Allow-Methods"] = "GET, POST, PUT, DELETE, OPTIONS"
    response.headers["Access-Control-Allow-Headers"] = "Content-Type, Authorization"
    return response

origins = [
    "https://teste.com.br",
    "http://localhost:3000",
]

app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
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