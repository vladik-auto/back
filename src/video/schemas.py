from datetime import datetime

from pydantic import BaseModel


class UploadVideo(BaseModel):
    title: str
    description: str


class GetVideo(BaseModel):
    id: int
    title: str
    description: str
    url: str


class Employee(BaseModel):
    id : int = None
    first_name: str
    middle_name: str
    last_name: str


class CreatedResponse(BaseModel):
    status: int = 201
    message: str = "Created"



class DeletedResponse(BaseModel):
    status: int = 200
    message: str = "Deleted"


class Violation(BaseModel):
    id : int = None
    name: str
    description: str

class Video(BaseModel):
    id : int = None
    title: str
    description: str

