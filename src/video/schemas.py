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
