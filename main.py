import aiohttp
from fastapi import FastAPI as FastAPIOffline
import uvicorn
from src.auth.routers import router as router_auth
from src.video.routers import router as router_video
from fastapi.testclient import TestClient
# from src.kafka.routers import router as router_kafka
# from fastapi.middleware.cors import CORSMiddleware
from starlette.middleware.cors import CORSMiddleware
from

from fastapi import WebSocket

app = FastAPIOffline()
#app.include_router(router_auth)
app.include_router(router_video)
# app.include_router(router_kafka)

@app.middleware("http")
async def add_cors_headers(request, call_next):
    response = await call_next(request)
    response.headers["Access-Control-Allow-Origin"] = "http://localhost:5173"
    response.headers["Access-Control-Allow-Credentials"] = "true"
    response.headers["Access-Control-Allow-Methods"] = "GET, POST, PUT, DELETE, OPTIONS"
    response.headers["Access-Control-Allow-Headers"] = "Content-Type, Authorization"
    return response

origins = [

    "http://localhost:5173",
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

@app.websocket("/ws")
async def websocket_endpoint(websocket: WebSocket):
    await websocket.accept()
    try:
        async with aiohttp.ClientSession() as session:
            while True:
                img_file = await websocket.receive_bytes()

                # async with session.post('http://<YOLO_server_address>', data=img_file) as resp:
                #     response = await resp.read()
                await websocket.send_text("Hello, World!")



    except Exception:
        print("websocket disconnected")
        await websocket.close()
    finally:
        await websocket.close()



# uvicorn.run(app, host="0.0.0.0", port=8000)