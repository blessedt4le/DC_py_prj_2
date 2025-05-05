from fastapi.testclient import TestClient
from app.main import app
from app.database import SessionLocal
from app.models import User, Author, Genre, Book

client = TestClient(app)

# Вспомогательные функции
def override_get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

def clear_database():
    db = SessionLocal()
    try:
        db.query(Book).delete()
        db.query(Author).delete()
        db.query(Genre).delete()
        db.query(User).delete()
        db.commit()
    finally:
        db.close()

# Тесты
def test_register_user():
    clear_database()
    # Регистрация пользователя
    response = client.post(
        "/auth/register",
        json={"email": "user@example.com", "password": "secret"}
    )
    assert response.status_code == 201
    assert response.json() == {"email": "user@example.com", "id": 1}

def test_login_user():
    # Авторизация и получение токена
    response = client.post(
        "/auth/token",
        data={"username": "user@example.com", "password": "secret"}
    )
    assert response.status_code == 200
    assert "access_token" in response.json()
    return response.json()["access_token"]

def test_create_author_and_genre():
    token = test_login_user()
    # Создание автора
    response_author = client.post(
        "/authors/",
        json={"name": "Джордж Оруэлл"},
        headers={"Authorization": f"Bearer {token}"}
    )
    assert response_author.status_code == 201
    # Создание жанра
    response_genre = client.post(
        "/genres/",
        json={"name": "Антиутопия"},
        headers={"Authorization": f"Bearer {token}"}
    )
    assert response_genre.status_code == 201

def test_create_book():
    token = test_login_user()
    # Добавление книги
    response = client.post(
        "/books/",
        json={
            "title": "1984",
            "author_id": 1,
            "genre_id": 1,
            "rating": 4.8
        },
        headers={"Authorization": f"Bearer {token}"}
    )
    assert response.status_code == 201
    data = response.json()
    assert data["title"] == "1984"
    assert data["author"]["name"] == "Джордж Оруэлл"
    assert data["genre"]["name"] == "Антиутопия"

def test_get_books():
    # Получение списка книг
    response = client.get("/books/")
    assert response.status_code == 200
    data = response.json()
    assert len(data) == 1
    assert data[0]["title"] == "1984"

def test_get_users():
    token = test_login_user()
    # Получение списка пользователей
    response = client.get(
        "/auth/users",
        headers={"Authorization": f"Bearer {token}"}
    )
    assert response.status_code == 200
    data = response.json()
    assert len(data) == 1
    assert data[0]["email"] == "user@example.com"

def test_protected_endpoints():
    # Попытка создать книгу без токена
    response = client.post(
        "/books/",
        json={"title": "Неавторизованная книга", "author_id": 1, "genre_id": 1}
    )
    assert response.status_code == 401