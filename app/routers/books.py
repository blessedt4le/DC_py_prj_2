from typing import List
from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session, joinedload
from app.database import SessionLocal
from app.models import Book, Author, Genre
from app.schemas import BookCreate, BookSchema

router = APIRouter(prefix="/books", tags=["books"])

def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

@router.post("/", response_model=BookSchema, status_code=status.HTTP_201_CREATED)
def create_book(book: BookCreate, db: Session = Depends(get_db)):
    # Проверка существования автора и жанра
    author = db.query(Author).filter(Author.id == book.author_id).first()
    if not author:
        raise HTTPException(status_code=400, detail="Автор не найден")
    
    genre = db.query(Genre).filter(Genre.id == book.genre_id).first()
    if not genre:
        raise HTTPException(status_code=400, detail="Жанр не найден")
    
    # Создание книги через модель SQLAlchemy
    db_book = Book(**book.dict())
    db.add(db_book)
    db.commit()
    db.refresh(db_book)
    return db_book

@router.get("/", response_model=List[BookSchema])
def read_books(skip: int = 0, limit: int = 100, db: Session = Depends(get_db)):
    books = db.query(Book).options(
        joinedload(Book.author),
        joinedload(Book.genre)
    ).offset(skip).limit(limit).all()
    return books

@router.get("/{book_id}", response_model=BookSchema)
def read_book(book_id: int, db: Session = Depends(get_db)):
    book = db.query(Book).filter(Book.id == book_id).first()
    if not book:
        raise HTTPException(status_code=404, detail="Книга не найдена")
    return book

@router.put("/{book_id}", response_model=BookSchema)
def update_book(book_id: int, updated_book: BookCreate, db: Session = Depends(get_db)):
    book = db.query(Book).filter(Book.id == book_id).first()
    if not book:
        raise HTTPException(status_code=404, detail="Книга не найдена")
    
    for key, value in updated_book.dict().items():
        setattr(book, key, value)
    
    db.commit()
    db.refresh(book)
    return book

@router.delete("/{book_id}", status_code=status.HTTP_204_NO_CONTENT)
def delete_book(book_id: int, db: Session = Depends(get_db)):
    book = db.query(Book).filter(Book.id == book_id).first()
    if not book:
        raise HTTPException(status_code=404, detail="Книга не найдена")
    db.delete(book)
    db.commit()
    return