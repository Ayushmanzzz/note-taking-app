from fastapi import FastAPI
from fastapi import HTTPException
from pydantic import BaseModel
from typing import List

class Note(BaseModel):
    title:str
    content:str
    tags: List[str] = []

app = FastAPI()
notes = {}

@app.get("/")
def home():
    return {"message":"API is working"}


@app.post("/notes/{note_id}")
def create_note(note_id: int, note: Note):
    if note_id in notes:
        raise HTTPException(status_code=400, detail="Note Already Exists")
    notes[note_id] = note.model_dump()
    return{"message": "Note Created",
           "data": notes[note_id]}

@app.get("/notes")
def show_all():
    return notes

@app.get("/notes/{note_id}")
def show(note_id: int):
    if note_id in notes:
        return notes[note_id]
    else:
        raise HTTPException(status_code= 404, detail= "Note doesnt exist")

@app.put("/notes/{note_id}")
def update_note(note_id: int, note:Note):
    if note_id not in notes:
        raise HTTPException(status_code=404, detail="Note not found")
    notes[note_id] = note.model_dump()
    return {
        "message":"Note Updated",
        "note":notes[note_id]
    }

@app.delete("/notes/{note_id}")
def delete_note(note_id: int):
    if note_id not in notes:
        raise HTTPException(status_code=404, detail="Note doesn't exist")
    del notes[note_id]
    return{"message":"Note Deleted"}
