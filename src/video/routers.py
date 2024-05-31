from asyncio import sleep

from fastapi import APIRouter
import aiohttp
from fastapi import BackgroundTasks
from fastapi import Depends
from fastapi import File
from fastapi import Form
from fastapi import HTTPException
from fastapi import UploadFile
from src.auth.schemas import User
from src.dependencies import get_current_user as get_user
from src.video.services import save_video
from src.video.schemas import GetVideo
from fastapi import WebSocket
from starlette.websockets import WebSocketState

router = APIRouter(
    prefix="/video",
    tags=["Video"],
    responses={404: {"description": "Not found"}},
)


@router.post("/", response_model=GetVideo)
async def create_video(
        title: str = Form(...),
        description: str = Form(...),
        file: UploadFile = File(...),
        user: User = Depends(get_user)
):
    """ Add video """
    return await save_video(user, file, title, description)


def mock_video():
    i = 0
    while True:
        yield i
        i += 1


video_gen = mock_video()



@router.websocket("/ws/")
async def websocket_endpoint(websocket: WebSocket):
    await websocket.accept()
    try:
        async with aiohttp.ClientSession() as session:
            while True:
                img_file = await websocket.receive_text()

                # async with session.post('http://<YOLO_server_address>', data=img_file) as resp:
                #     response = await resp.read()
                await websocket.send_text(str(next(video_gen)))

    except Exception:
        print("websocket disconnected")
        await websocket.close()
    finally:
        await websocket.close()