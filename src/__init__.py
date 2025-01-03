from fastapi import FastAPI
from src.Books.routes import book_router

version='v1'

app=FastAPI(
    title="My Book Store",
    description="A REST Api for Book Review",
    version=version
)

app.include_router(book_router, prefix=f"/api/{version}/books", tags=['Books'])