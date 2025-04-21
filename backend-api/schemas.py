# app/schemas.py
from pydantic import BaseModel

class TodoBase(BaseModel):
    title: str

class TodoCreate(TodoBase):
    pass

class TodoUpdate(BaseModel):
    title: str
    completed: bool

class TodoRead(TodoBase):
    id: int
    completed: bool

    class Config:
        orm_mode = True
