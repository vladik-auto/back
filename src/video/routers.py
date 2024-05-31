from asyncio import sleep

from fastapi import APIRouter
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


