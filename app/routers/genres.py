from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session
from typing import List
from app.database import SessionLocal
from app.models import Genre, Book
from app.schemas import GenreCreate, GenreSchema

router = APIRouter(prefix="/genres", tags=["genres"])

def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

@router.post("/", response_model=GenreSchema, status_code=status.HTTP_201_CREATED)
def create_genre(genre: GenreCreate, db: Session = Depends(get_db)):
    # Проверка уникальности жанра
    existing_genre = db.query(Genre).filter(Genre.name == genre.name).first()
    if existing_genre:
        raise HTTPException(status_code=400, detail="Жанр уже существует")
    
    db_genre = Genre(name=genre.name)
    db.add(db_genre)
    db.commit()
    db.refresh(db_genre)
    return db_genre

@router.get("/", response_model=List[GenreSchema])
def read_genres(skip: int = 0, limit: int = 100, db: Session = Depends(get_db)):
    return db.query(Genre).offset(skip).limit(limit).all()

@router.get("/{genre_id}", response_model=GenreSchema)
def read_genre(genre_id: int, db: Session = Depends(get_db)):
    genre = db.query(Genre).filter(Genre.id == genre_id).first()
    if not genre:
        raise HTTPException(status_code=404, detail="Жанр не найден")
    return genre

@router.put("/{genre_id}", response_model=GenreSchema)
def update_genre(genre_id: int, updated_genre: GenreCreate, db: Session = Depends(get_db)):
    genre = db.query(Genre).filter(Genre.id == genre_id).first()
    if not genre:
        raise HTTPException(status_code=404, detail="Жанр не найден")
    
    # Проверка уникальности нового имени
    existing_genre = db.query(Genre).filter(Genre.name == updated_genre.name, Genre.id != genre_id).first()
    if existing_genre:
        raise HTTPException(status_code=400, detail="Название жанра уже занято")
    
    genre.name = updated_genre.name
    db.commit()
    db.refresh(genre)
    return genre

@router.delete("/{genre_id}", status_code=status.HTTP_204_NO_CONTENT)
def delete_genre(genre_id: int, db: Session = Depends(get_db)):
    genre = db.query(Genre).filter(Genre.id == genre_id).first()
    if not genre:
        raise HTTPException(status_code=404, detail="Жанр не найден")
    
    # Проверка связанных книг
    if db.query(Book).filter(Book.genre_id == genre_id).first():
        raise HTTPException(status_code=400, detail="Невозможно удалить жанр с книгами")
    
    db.delete(genre)
    db.commit()
    return