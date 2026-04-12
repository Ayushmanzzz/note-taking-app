from pydantic import BaseModel
from typing import List

class NoteCreate(BaseModel):
    title: str
    content: str
    tags: List[str] = []

class NoteResponse(BaseModel):
    id: int
    title: str
    content: str
    tags: List[str] = []

    class Config:
        from_attributes = True

