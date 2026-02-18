from fastapi import FastAPI, Depends, HTTPException, status
from sqlalchemy.orm import Session
from .db import get_db
from . import crud, schemas

app = FastAPI(title="Users CRUD")


@app.post("/users", response_model=schemas.UserOut, status_code=status.HTTP_201_CREATED)
def create_user(payload: schemas.UserCreate, db: Session = Depends(get_db)):
    existing = crud.get_user_by_email(db, str(payload.email))
    if existing:
        raise HTTPException(status_code=400, detail="Email already exists")
    return crud.create_user(db, payload)


@app.get("/users", response_model=list[schemas.UserOut])
def list_users(skip: int = 0, limit: int = 50, db: Session = Depends(get_db)):
    return crud.list_users(db, skip=skip, limit=limit)


@app.get("/users/{user_id}", response_model=schemas.UserOut)
def get_user(user_id: int, db: Session = Depends(get_db)):
    user = crud.get_user(db, user_id)
    if not user:
        raise HTTPException(status_code=404, detail="User not found")
    return user


@app.patch("/users/{user_id}", response_model=schemas.UserOut)
def update_user(
    user_id: int, payload: schemas.UserUpdate, db: Session = Depends(get_db)
):
    user = crud.get_user(db, user_id)
    if not user:
        raise HTTPException(status_code=404, detail="User not found")
    # if changing email, ensure uniqueness
    if payload.email is not None:
        existing = crud.get_user_by_email(db, str(payload.email))
        if existing and existing.id != user_id:
            raise HTTPException(status_code=400, detail="Email already exists")
    return crud.update_user(db, user, payload)


@app.delete("/users/{user_id}", status_code=status.HTTP_204_NO_CONTENT)
def delete_user(user_id: int, db: Session = Depends(get_db)):
    user = crud.get_user(db, user_id)
    if not user:
        raise HTTPException(status_code=404, detail="User not found")
    crud.delete_user(db, user)
    return None
