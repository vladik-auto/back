import shutil
from sqlalchemy import select, delete
from typing import List
from uuid import uuid4

from fastapi import UploadFile, HTTPException
from fastapi.background import BackgroundTasks

from src.video.schemas import Employee as EmployeeSchema, Employee, Violation, Video
from src.video import models
from sqlalchemy.ext.asyncio import AsyncSession
from src.video.schemas import UploadVideo


# async def upload_video(file_name: str, file: UploadFile):
#     async with file.open("wb") as buffer:
#         content = await file.read()
#         await buffer.write(content)


# async def upload_video(file_name: str, file: UploadFile):
#     with open(file_name, "wb") as buffer:
#         content = await file.read()  # Read the file
#         buffer.write(content)  #

# async def upload_video(video: UploadFile = File(...)):
#     with open(f"{video.filename}", "wb") as buffer:
#         shutil.copyfileobj(video.file, buffer)
#
#     return JSONResponse(status_code=200, content={"filename": video.filename})


# async def save_video(
#         user: User,
#         file: UploadFile,
#         title: str,
#         description: str,
# ):
#     file_name = f'media/{user.id}_{uuid4()}.mp4'
#     if file.content_type == 'video/mp4':
#         # back_tasks.add_task(write_video, file_name, file)
#         await upload_video(file_name, file)
#     else:
#         raise HTTPException(status_code=418, detail="It isn't mp4")
#     info = UploadVideo(title=title, description=description)
#     return await Video.save(**info)


# def save_video_to_file(file, path: str):
#     with open(path, "wb") as buffer:
#         shutil.copyfileobj(file.file, buffer)
#
# def save_video_to_db(db: Session, path: str, filename: str):
#     new_video = Video(video_path=path, video_name=filename)
#     db.add(new_video)
#     db.commit()


async def create_employee(
        first_name: str,
        middle_name: str,
        last_name: str,
        db: AsyncSession
):
    new_employee = models.Employee(first_name=first_name, middle_name=middle_name, last_name=last_name)
    await new_employee.save(db=db)
    return new_employee


async def get_employees(
        db: AsyncSession
):
    result = await db.execute(select(models.Employee))

    employees = result.scalars().all()

    return employees


async def create_violation(

        name: str,
        description: str,
        db: AsyncSession
):
    new_violation = models.Violations(name=name, description=description)
    await new_violation.save(db=db)
    return


async def delete_violation(
        db: AsyncSession,
        violation_id: int
):
    await db.execute(delete(models.Violations).where(models.Violations.id == violation_id))
    await db.commit()


async def get_violations(
        db: AsyncSession
):
    result = await db.execute(select(models.Violations))

    violations = result.scalars().all()

    return violations


async def delete_employee(
        db: AsyncSession,
        employee_id: int
):
    await db.execute(delete(models.Employee).where(models.Employee.id == employee_id))
    await db.commit()

async def delete_video(
        db: AsyncSession,
        video_id: int
):
    await db.execute(delete(models.Video).where(models.Video.id == video_id))
    await db.commit()

async def get_video(
        db: AsyncSession,
        video_id: int
):
    result = await db.execute(select(models.Video).where(models.Video.id == video_id))
    video = result.scalars().first()
    return video

async def update_video(
        db: AsyncSession,
        db_video: models.Video,
        video: UploadVideo
):
    db_video.title = video.title
    db_video.description = video.description
    await db.commit()
    await db.refresh(db_video)
    return db_video

async def get_videos(
        db: AsyncSession
):
    result = await db.execute(select(models.Video))
    videos = result.scalars().all()
    return videos

async def get_vialations(
        db: AsyncSession,

):
    result = await db.execute(select(models.Violations))
    violations = result.scalars().all()
    return violations

async def get_violation(
        db: AsyncSession,
        violation_id: int
):
    result = await db.execute(select(models.Violations).where(models.Violations.id == violation_id))
    violation = result.scalars().first()
    return violation

async def get_employee(
        db: AsyncSession,
        employee_id: int
):
    result = await db.execute(select(models.Employee).where(models.Employee.id == employee_id))
    employee = result.scalars().first()
    return employee

async def update_employee(
        db: AsyncSession,
        db_employee: models.Employee,
        employee: Employee
):

    db_employee.first_name = employee.first_name
    db_employee.middle_name = employee.middle_name
    db_employee.last_name = employee.last_name
    await db.commit()
    await db.refresh(db_employee)
    return db_employee

async def update_violation(
        db: AsyncSession,
        db_violation: models.Violations,
        violation: Violation
):
    db_violation.name = violation.name
    db_violation.description = violation.description
    await db.commit()
    await db.refresh(db_violation)
    return db_violation

