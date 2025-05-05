from sqlalchemy import Column, Integer, String, Float, ForeignKey
from sqlalchemy.orm import relationship
from app.database import Base

class Author(Base):
    __tablename__ = "authors"
    id = Column(Integer, primary_key=True, index=True)
    name = Column(String, unique=True)
    books = relationship("Book", back_populates="author")

class Genre(Base):
    __tablename__ = "genres"
    id = Column(Integer, primary_key=True, index=True)
    name = Column(String, unique=True)
    books = relationship("Book", back_populates="genre")

class Book(Base):
    __tablename__ = "books"
    id = Column(Integer, primary_key=True, index=True)
    title = Column(String)
    author_id = Column(Integer, ForeignKey("authors.id"))
    genre_id = Column(Integer, ForeignKey("genres.id"))
    rating = Column(Float, default=0.0)
    author = relationship("Author", back_populates="books")
    genre = relationship("Genre", back_populates="books")

class User(Base):
    __tablename__ = "users"
    id = Column(Integer, primary_key=True, index=True)
    email = Column(String, unique=True)
    hashed_password = Column(String)