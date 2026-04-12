from fastapi import FastAPI, Depends, HTTPException
from sqlalchemy.orm import Session

from database import engine, sessionLocal
from models import Base, Note
from schemas import NoteCreate, NoteResponse

app = FastAPI()

Base.metadata.create_all(bind=engine)

def get_db():
    db = sessionLocal()
    try:
        yield db
    finally:
        db.close()



@app.get("/")
def home():
    return {"message":"API is working"}

# create note
@app.post("/notes/", response_model=NoteResponse)
def create_note(note: NoteCreate, db: Session = Depends(get_db)):
    tags_str = ",".join(note.tags)
    new_note = Note(title = note.title,
                    content = note.content,
                    tags = tags_str)
    db.add(new_note)
    db.commit()
    db.refresh(new_note)

    return {
        "id": new_note.id,
        "title": new_note.title,
        "content": new_note.content,
        "tags": new_note.tags.split(",") if new_note.tags else []
    }

# read all notes
@app.get("/notes/", response_model=list[NoteResponse])
def get_notes(db: Session = Depends(get_db)):
    notes = db.query(Note).all()
    result = []
    for note in notes:
        result.append({
            "id": note.id,
            "title": note.title,
            "content": note.content,
            "tags": note.tags.split(",") if note.tags else[]
        })
    return result

# get a particular note
@app.get("/notes/{note_id}", response_model=NoteResponse)
def get_note(note_id: int, db: Session = Depends(get_db)):

    note = db.query(Note).filter(Note.id == note_id).first()

    if not note:
        raise HTTPException(status_code= 404, detail= "Note doesnt exist")
    return {
        "id": note.id,
        "title": note.title,
        "content": note.content,
        "tags": note.tags.split(",") if note.tags else []
    }

# update note
@app.put("/notes/{note_id}", response_model=NoteResponse)
def update_note(note_id: int, updated: NoteCreate, db: Session = Depends(get_db)):

    note = db.query(Note).filter(Note.id == note_id).first()

    if not note:
        raise HTTPException(status_code=404, detail="Note not found")
    note.title = updated.title
    note.content = updated.content
    note.tags = ",".join(updated.tags)
    db.commit()
    db.refresh(note)

    return {
        "id": note.id,
        "title": note.title,
        "content": note.content,
        "tags": note.tags.split(",") if note.tags else []
    }

# delete note
@app.delete("/notes/{note_id}")
def delete_note(note_id: int, db: Session = Depends(get_db)):

    note = db.query(Note).filter(Note.id == note_id).first()
    if not note:
        raise HTTPException(status_code=404, detail="Note doesn't exist")
    
    db.delete(note)
    db.commit()

    return{"message":"Note Deleted"}