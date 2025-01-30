from fastapi import FastAPI
from src.Books.routes import book_router
from contextlib import asynccontextmanager
from src.db.main import dataBaseinit

@asynccontextmanager
async def life_span(app:FastAPI):
    print("Server is Starting...")
    await dataBaseinit()
    yield
    print("Server has stopped working...")

version='v1'

app=FastAPI(
    title="My Book Store",
    description="A REST Api for Book Review",
    version=version,
    lifespan=life_span
)

app.include_router(book_router, prefix=f"/api/{version}/books", tags=['Books'])