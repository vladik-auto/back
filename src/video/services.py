import shutil
from typing import List
from uuid import uuid4

from fastapi import UploadFile, HTTPException
from fastapi.background import BackgroundTasks

from src.auth.schemas import User
from src.video.models import Video
from src.video.schemas import UploadVideo



# async def upload_video(file_name: str, file: UploadFile):
#     async with file.open("wb") as buffer:
#         content = await file.read()
#         await buffer.write(content)


async def upload_video(file_name: str, file: UploadFile):
    with open(file_name, "wb") as buffer:
        content = await file.read()  # Read the file
        buffer.write(content)  #

# async def upload_video(video: UploadFile = File(...)):
#     with open(f"{video.filename}", "wb") as buffer:
#         shutil.copyfileobj(video.file, buffer)
#
#     return JSONResponse(status_code=200, content={"filename": video.filename})


async def save_video(
        user: User,
        file: UploadFile,
        title: str,
        description: str,
):
    file_name = f'media/{user.id}_{uuid4()}.mp4'
    if file.content_type == 'video/mp4':
        # back_tasks.add_task(write_video, file_name, file)
        await upload_video(file_name, file)
    else:
        raise HTTPException(status_code=418, detail="It isn't mp4")
    info = UploadVideo(title=title, description=description)
    return await Video.save(**info)



# def save_video_to_file(file, path: str):
#     with open(path, "wb") as buffer:
#         shutil.copyfileobj(file.file, buffer)
#
# def save_video_to_db(db: Session, path: str, filename: str):
#     new_video = Video(video_path=path, video_name=filename)
#     db.add(new_video)
#     db.commit()