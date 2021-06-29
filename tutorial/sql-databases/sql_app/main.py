from typing import (
    List,
    Any
)

from fastapi import (
    Depends, 
    FastAPI, 
    HTTPException,
)
from fastapi import status
from fastapi import responses
from fastapi.responses import RedirectResponse
from sqlalchemy.orm import Session
from sqlalchemy.sql.functions import user

from . import crud, models, schemas
from .database import SessionLocal, engine


models.Base.metadata.create_all(bind=engine)


app = FastAPI()


# Dependency
def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()



@app.get("/")
def root():
    response = RedirectResponse("/docs")
    return response


@app.post("/users/", response_model=schemas.User)
def create_user(
    user: schemas.UserCreate, 
    db: Session = Depends(get_db)
):
    """
    Create a user.
    """
    db_user = crud.get_user_by_email(db, email=user.email)
    if db_user:
        raise HTTPException(status_code=400, detail="Email already registered")
    return crud.create_user(db=db, user=user)


@app.get("/users/", response_model=List[schemas.User])
def read_users(
    skip: int = 0, 
    limit: int = 100, 
    db: Session = Depends(get_db)
):
    """
    Read users.
    """
    users = crud.get_users(db, skip=skip, limit=limit)
    return users


@app.get("/users/{user_id}", response_model=schemas.User)
def read_user(
    user_id: int, 
    db: Session = Depends(get_db)
):
    """
    Read a user.
    """
    db_user = crud.get_user(db, user_id=user_id)
    if db_user is None:
        raise HTTPException(status_code=404, detail="User not found")
    return db_user


@app.put("/users/{user_id}", response_model=schemas.User)
def update_user(
    user_id: int, 
    user_in: schemas.UserUpdate,
    db: Session = Depends(get_db)
) -> Any:
    """
    Update a user.
    """
    db_user = crud.get_user(db=db, user_id=user_id)
    if db_user is None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="User not found")
    return crud.update_user(db=db, db_user=db_user, user_in=user_in)


@app.delete("/users/{user_id}", response_model=schemas.User)
def remove_user(
    user_id: int, 
    db: Session = Depends(get_db)
) -> Any:
    """
    Remove a user.
    """
    db_user = crud.get_user(db=db, user_id=user_id)
    if db_user is None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="User not found")
    return crud.remove_user(db=db, user_id=user_id)


@app.post("/users/{user_id}/items/", response_model=schemas.Item)
def create_item_for_user(
    user_id: int, item: schemas.ItemCreate, db: Session = Depends(get_db)
):
    """
    Create an item for a user.
    """
    db_user = crud.get_user(db=db, user_id=user_id)
    if db_user is None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="User not found")
    return crud.create_user_item(db=db, item=item, user_id=user_id)


@app.get("/items/", response_model=List[schemas.Item])
def read_items(
    skip: int = 0, 
    limit: int = 100, 
    db: Session = Depends(get_db)
):
    """
    Read items.
    """
    items = crud.get_items(db=db, skip=skip, limit=limit)
    return items


@app.get("/items/{item_id}", response_model=schemas.Item)
def read_item(
    item_id: int, 
    db: Session = Depends(get_db)
) -> Any:
    """
    Read an item.
    """
    db_item = crud.get_item(db=db, item_id=item_id)
    if db_item is None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Item not found")
    return db_item


@app.delete("/items/{item_id}", response_model=schemas.Item)
def remove_item(
    item_id: int, 
    db: Session = Depends(get_db)
) -> Any:
    """
    Remove an item.
    """
    db_item = crud.get_item(db=db, item_id=item_id)
    if db_item is None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Item not found")
    db_item = crud.remove_item(db=db, item_id=item_id)
    return db_item


@app.put("/items/{item_id}", response_model=schemas.Item)
def update_item(
    item_id: int, 
    item_in: schemas.ItemUpdate,
    db: Session = Depends(get_db)
) -> Any:
    """
    Update an item.
    """
    db_item = crud.get_item(db=db, item_id=item_id)
    if db_item is None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Item not found")
    return crud.update_item(db=db, db_item=db_item, item_in=item_in)