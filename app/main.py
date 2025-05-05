from fastapi import FastAPI
from app.routers import books, authors, genres, auth
from app.database import Base, engine

Base.metadata.create_all(bind=engine)

app = FastAPI()
app.include_router(books.router)
app.include_router(authors.router)
app.include_router(genres.router)
app.include_router(auth.router)

@app.get("/")
def read_root():
    return {"message": "Welcome to the Book Catalog API"}