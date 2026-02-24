from fastapi import FastAPI, Depends, HTTPException
from sqlalchemy.orm import Session
from schemas import PersonCreate, PersonResponse, PersonPatch
from database import SessionLocal, engine, Base
from fastapi.responses import JSONResponse
from exceptions import NameAlreadyExistsException

import models
import crud
import schemas
import services

app = FastAPI()

# Create database tables if they do not exist yet
# removed Base.metadata.create_all(bind=engine) now that we are using Alembic for migrations 

def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

@app.get("/health")
def health():
    return {"status": "running"}

from sqlalchemy.exc import IntegrityError

@app.post("/people", response_model=PersonResponse)
def create_person(person: PersonCreate, db: Session = Depends(get_db)):
    return services.create_person_service(db, person)
 
@app.get("/people", response_model=list[schemas.PersonResponse])
def get_people(
    db: Session = Depends(get_db),
    skip: int = 0,
    limit: int = 100,
    min_age: int | None = None,
    name_contains: str | None = None,
):
    return crud.get_people(db, skip=skip, limit=limit, min_age=min_age, name_contains=name_contains)


@app.get("/people/{person_id}", response_model=schemas.PersonResponse)
def get_person(person_id: int, db: Session = Depends(get_db)):
    person = crud.get_person(db, person_id)
    if person is None:
        raise HTTPException(status_code=404, detail="Person not found")
    return person


@app.put("/people/{person_id}", response_model=schemas.PersonResponse)
def update_person(person_id: int, updated: schemas.PersonUpdate, db: Session = Depends(get_db)):
    person = crud.update_person(db, person_id, updated)
    if person is None:
        raise HTTPException(status_code=404, detail="Person not found")
    return person


@app.delete("/people/{person_id}")
def delete_person(person_id: int, db: Session = Depends(get_db)):
    ok = crud.delete_person(db, person_id)
    if not ok:
        raise HTTPException(status_code=404, detail="Person not found")
    return {"message": "Person deleted"}

@app.patch("/people/{person_id}", response_model=schemas.PersonResponse)
def patch_person(person_id: int, patch: schemas.PersonPatch, db: Session = Depends(get_db)):
    person = crud.patch_person(db, person_id, patch)
    if person is None:
        raise HTTPException(status_code=404, detail="Person not found")
    return person

@app.exception_handler(NameAlreadyExistsException)
def name_exists_handler(request, exc):
    return JSONResponse(
        status_code=400,
        content={"detail": "A person with this name already exists."}
    )