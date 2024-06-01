from asyncio import sleep
from fastapi.exceptions import HTTPException
from typing import Annotated, List
from random import randint
from fastapi import APIRouter
import aiohttp
from fastapi import BackgroundTasks
from fastapi import Depends
from sqlalchemy.ext.asyncio import AsyncSession
from src.dependencies import get_db
from src.video import services

from src.video import schemas
from fastapi import WebSocket
from starlette.websockets import WebSocketState

router = APIRouter(
    prefix="/video",
    tags=["Video"],
    responses={404: {"description": "Not found"}},
)


@router.get("/", response_model=list[schemas.Employee])
async def get_employees(
        db: AsyncSession = Depends(get_db)
):
    scalar = await services.get_employees(db=db)
    return scalar


@router.post("/add_employee/", response_model=schemas.CreatedResponse)
async def add_employee(employee: schemas.Employee, db: AsyncSession = Depends(get_db)):
    new_employee = await services.create_employee(db=db,
                                   first_name=employee.first_name,
                                   middle_name=employee.middle_name,
                                   last_name=employee.last_name)

    return schemas.CreatedResponse()


@router.post("/add_violations/", response_model=schemas.CreatedResponse)
async def add_violation(violation: schemas.Violation, db: AsyncSession = Depends(get_db)):
    await services.create_violation(db=db,
                                    name=violation.name,
                                    description=violation.description)

    return schemas.CreatedResponse()



@router.get("/get_violations/", response_model=list[schemas.Violation])
async def get_violations(db: AsyncSession = Depends(get_db)):
    scalar = await services.get_violations(db=db)
    return scalar
@router.delete("/del_violations/{violation_id}", response_model=schemas.DeletedResponse)
async def del_violation(violation_id : int, db: AsyncSession = Depends(get_db)):
    await services.delete_violation(db=db, violation_id=violation_id)


def random_video():
    return randint(0, 10)



def mock_video():
    i = 0


    while True:
        random = randint(0, 10)
        mockdata = True if random > 9 else False
        yield {i:mockdata}

        i += 1


video_gen = mock_video()


@router.websocket("/ws/videoinput")
async def websocket_output(websocket: WebSocket):
    await websocket.accept()
    try:
        async with aiohttp.ClientSession() as Session:
            while True:
                img_file = await websocket.receive_bytes()
                # async with Session.post('http://<YOLO_server_address>', data=img_file) as resp:
                #     response = await resp.read()
                # это просто для дебага
                print(img_file)
                await websocket.send_text(str(next(video_gen)))

    except Exception as e:
        print(f"websocket disconnected{e}")
        await websocket.close()
    finally:
        await websocket.close()

@router.websocket("/ws/videooutput")
async def websocket_output(websocket: WebSocket):
    await websocket.accept()
    try:
        async with aiohttp.ClientSession() as Session:
            while True:
                img_file = await websocket.receive_text()
                # async with Session.post('http://<YOLO_server_address>', data=img_file) as resp:
                #     response = await resp.read()
                # это просто для дебага
                await websocket.send_text(str(next(video_gen)))

    except Exception:
        print("websocket disconnected")
        await websocket.close()

# @router.post("/", response_model=GetVideo)
# async def create_video(
#         title: str = Form(...),
#         description: str = Form(...),
#         file: UploadFile = File(...),
#         user: User = Depends(get_user)
# ):
#     """ Add video """
#     return await save_video(user, file, title, description)


@router.get("/videos/", response_model=List[schemas.Video])
def read_videos(skip: int=0, limit: int=100, db: AsyncSession = Depends(get_db)):
    return services.get_videos(db, skip=skip, limit=limit)


@router.get("/videos/{video_id}", response_model=schemas.Video)
def read_video(video_id: int, db: AsyncSession = Depends(get_db)):
    video = services.get_video(db, video_id=video_id)
    if video is None:
        raise HTTPException(status_code=404, detail="Video not found")
    return video


# Routes for Violations
# @router.get("/violations/", response_model=List[schemas.Violation])
# def read_violations(skip: int=0, limit: int=100, db: AsyncSession = Depends(get_db)):
#     return services.get_violations(db, skip=skip, limit=limit)


@router.get("/violations/{violation_id}", response_model=schemas.Violation)
def read_violation(violation_id: int, db: AsyncSession = Depends(get_db)):
    violation = services.get_violation(db, violation_id=violation_id)
    if violation is None:
        raise HTTPException(status_code=404, detail="Violation not found")
    return violation


# Routes for Employee
# @router.get("/employees/", response_model=List[schemas.Employee])
# def read_employees(skip: int=0, limit: int=100, db: AsyncSession = Depends(get_db)):
#     return services.get_employees(db, skip=skip, limit=limit)


@router.get("/employees/{employee_id}", response_model=schemas.Employee)
def read_employee(employee_id: int, db: AsyncSession = Depends(get_db)):
    employee = services.get_employee(db, employee_id=employee_id)
    if employee is None:
        raise HTTPException(status_code=404, detail="Employee not found")
    return employee


# Update and delete routes for Video
@router.put("/videos/{video_id}", response_model=schemas.Video)
def update_video(video_id: int, video: schemas.Video, db: AsyncSession = Depends(get_db)):
    db_video = services.get_video(db, video_id=video_id)
    if db_video is None:
        raise HTTPException(status_code=404, detail="Video not found")
    return services.update_video(db, db_video=db_video, video=video)

@router.delete("/videos/{video_id}", response_model=schemas.Video)
def delete_video(video_id: int, db: AsyncSession = Depends(get_db)):
    db_video = services.get_video(db, video_id=video_id)
    if db_video is None:
        raise HTTPException(status_code=404, detail="Video not found")
    return services.delete_video(db, db_video=db_video)


# Update and delete routes for Violation
@router.put("/violations/{violation_id}", response_model=schemas.Violation)
def update_violation(violation_id: int, violation: schemas.Violation, db: AsyncSession = Depends(get_db)):
    db_violation = services.get_violation(db, violation_id=violation_id)
    if db_violation is None:
        raise HTTPException(status_code=404, detail="Violation not found")
    return services.update_violation(db, db_violation=db_violation, violation=violation)

@router.delete("/violations/{violation_id}", response_model=schemas.Violation)
def delete_violation(violation_id: int, db: AsyncSession = Depends(get_db)):
    db_violation = services.get_violation(db, violation_id=violation_id)
    if db_violation is None:
        raise HTTPException(status_code=404, detail="Violation not found")
    return services.delete_violation(db, db_violation=db_violation)


# Update and delete routes for Employee
@router.put("/employees/{employee_id}", response_model=schemas.Employee)
def update_employee(employee_id: int, employee: schemas.Employee, db: AsyncSession = Depends(get_db)):
    db_employee = services.get_employee(db, employee_id=employee_id)
    if db_employee is None:
        raise HTTPException(status_code=404, detail="Employee not found")
    return services.update_employee(db, db_employee=db_employee, employee=employee)

@router.delete("/employees/{employee_id}", response_model=schemas.Employee)
def delete_employee(employee_id: int, db: AsyncSession = Depends(get_db)):
    db_employee = services.get_employee(db, employee_id=employee_id)
    if db_employee is None:
        raise HTTPException(status_code=404, detail="Employee not found")
    return services.delete_employee(db, db_employee=db_employee)
