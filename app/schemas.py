from pydantic import BaseModel, EmailStr
from typing import Optional

# Авторы
class AuthorBase(BaseModel):
    name: str

class AuthorCreate(AuthorBase):
    pass

class AuthorSchema(AuthorBase):
    id: int
    class Config:
        from_attributes = True

# Жанры
class GenreBase(BaseModel):
    name: str

class GenreCreate(GenreBase):
    pass

class GenreSchema(GenreBase):
    id: int
    class Config:
        from_attributes = True

# Книги
class BookBase(BaseModel):
    title: str
    author_id: int
    genre_id: int
    rating: float = 0.0

class BookCreate(BookBase):
    pass

class BookSchema(BookBase):
    id: int
    author: Optional[AuthorSchema] = None  # Вложенная схема автора
    genre: Optional[GenreSchema] = None    # Вложенная схема жанра
    class Config:
        from_attributes = True

# Пользователи
class UserBase(BaseModel):
    email: EmailStr

class UserCreate(UserBase):
    password: str

class UserSchema(UserBase):
    id: int
    class Config:
        from_attributes = True

# Аутентификация
class Token(BaseModel):
    access_token: str
    token_type: str

class TokenData(BaseModel):
    email: Optional[str] = None