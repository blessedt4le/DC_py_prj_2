from typing import List
from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session
from app.database import SessionLocal
from app.models import Author
from app.schemas import AuthorCreate, AuthorSchema

router = APIRouter(prefix="/authors", tags=["authors"])

def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

@router.post("/", response_model=AuthorSchema, status_code=status.HTTP_201_CREATED)
def create_author(author: AuthorCreate, db: Session = Depends(get_db)):
    if db.query(Author).filter(Author.name == author.name).first():
        raise HTTPException(status_code=400, detail="Автор уже существует")
    db_author = Author(name=author.name)
    db.add(db_author)
    db.commit()
    db.refresh(db_author)
    return db_author

@router.get("/", response_model=List[AuthorSchema])
def read_authors(skip: int = 0, limit: int = 100, db: Session = Depends(get_db)):
    return db.query(Author).offset(skip).limit(limit).all()

@router.get("/{author_id}", response_model=AuthorSchema)
def read_author(author_id: int, db: Session = Depends(get_db)):
    author = db.query(Author).filter(Author.id == author_id).first()
    if not author:
        raise HTTPException(status_code=404, detail="Автор не найден")
    return author

@router.delete("/{author_id}", status_code=status.HTTP_204_NO_CONTENT)
def delete_author(author_id: int, db: Session = Depends(get_db)):
    author = db.query(Author).filter(Author.id == author_id).first()
    if not author:
        raise HTTPException(status_code=404, detail="Автор не найден")
    if db.query(Book).filter(Book.author_id == author_id).first():
        raise HTTPException(status_code=400, detail="Невозможно удалить автора с книгами")
    db.delete(author)
    db.commit()
    return