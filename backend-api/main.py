from fastapi import FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel
from typing import List, Optional

app = FastAPI()

app.add_middleware(
    CORSMiddleware,
    allow_origins=[
        "http://localhost:5173",  # For local dev
        "https://cbeatrixbacolanta.github.io"  # For the deployed frontend
    ],
    allow_methods=["*"],
    allow_headers=["*"],
)


todos = []
id_counter = 1

class Todo(BaseModel):
    id: int
    title: str
    completed: bool = False

class TodoCreate(BaseModel):
    title: str

class TodoUpdate(BaseModel):
    title: str
    completed: bool

# Routes
@app.get("/todos", response_model=List[Todo])
def get_todos():
    return todos

@app.post("/todos", response_model=Todo)
def create_todo(todo: TodoCreate):
    global id_counter
    new_todo = Todo(id=id_counter, title=todo.title, completed=False)
    todos.append(new_todo)
    id_counter += 1
    return new_todo

@app.put("/todos/{todo_id}", response_model=Todo)
def update_todo(todo_id: int, updated: TodoUpdate):
    for i, t in enumerate(todos):
        if t.id == todo_id:
            todos[i] = Todo(id=todo_id, title=updated.title, completed=updated.completed)
            return todos[i]
    raise HTTPException(status_code=404, detail="Todo not found")

@app.delete("/todos/{todo_id}")
def delete_todo(todo_id: int):
    global todos
    todos = [t for t in todos if t.id != todo_id]
    return {"detail": "Todo deleted"}
