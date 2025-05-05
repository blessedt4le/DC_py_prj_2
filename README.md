1) Каталог книг (REST API на FastAPI)

Проект представляет собой RESTful сервис для управления каталогом книг с аутентификацией пользователей.

2) Требования
- Python 3.8+
- Установленные зависимости из `requirements.txt`

3) Установка
1. Клонируйте репозиторий:
   ```bash
   git clone https://github.com/blessedt4le/DC_py_prj_2
   cd Book_catalog
   
2. Установите зависимости:
pip install -r requirements.txt

4) Запуск
1. Инициализируйте базу данных:
uvicorn app.main:app --reload

Сервер запустится на http://localhost:8000
Документация к API:
Swagger UI: http://localhost:8000/docs
ReDoc: http://localhost:8000/redoc

5) Запуск тестов
pytest app/tests/test_api.py -v

6) Пример использования
Регистрация пользователя:
curl -X POST "http://localhost:8000/auth/register" -H "Content-Type: application/json" -d '{"email": "user@example.com", "password": "secret"}'

Авторизация пользователя (получение токена)
curl -X POST "http://localhost:8000/auth/token" -H "Content-Type: application/x-www-form-urlencoded" -d "username=user@example.com&password=secret"

Создание автора:
curl -X POST "http://localhost:8000/authors/" -H "Content-Type: application/json" -H "Authorization: Bearer eyJhbGciOiJIUzI1NiIs..." -d '{"name": "Джордж Оруэлл"}'

Создание жанра:
curl -X POST "http://localhost:8000/genres/" -H "Content-Type: application/json" -H "Authorization: Bearer eyJhbGciOiJIUzI1NiIs..." -d '{"name": "Антиутопия"}'

Добавление книги:
curl -X POST "http://localhost:8000/books/" -H "Content-Type: application/json" -H "Authorization: Bearer eyJhbGciOiJIUzI1NiIs..." -d '{"title": "1984", "author_id": 1, "genre_id": 1, "rating": 4.8}'

Получение списка книг:
curl "http://localhost:8000/books/" "Authorization: Bearer eyJhbGciOiJIUzI1NiIs..."

Получение списка пользователей:
curl "http://localhost:8000/auth/users" -H "Authorization: Bearer eyJhbGciOiJIUzI1NiIs..."
