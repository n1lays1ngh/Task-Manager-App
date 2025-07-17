from pydantic import BaseModel
import fastapi 
import sqlalchemy


class TaskCreate(BaseModel):
    title: str
    description: str
    completed: bool = False


class Task(TaskCreate):
    id: int


class TaskUpdate(BaseModel):
    title: str
    description: str
    completed: bool

