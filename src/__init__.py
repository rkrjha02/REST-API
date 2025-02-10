from fastapi import FastAPI
from src.Books.routes import book_router
from contextlib import asynccontextmanager
from src.db.main import dataBaseinit
from src.auth.routes import auth_router

#The @asynccontextmanager decorator is used to define an asynchronous context manager. This helps
# manage resources that need setup and cleanup, such as databases or external connections.

@asynccontextmanager
async def life_span(app:FastAPI):
    print("Server is Starting...")
    await dataBaseinit()
    yield
    print("Server has stopped working...")

#Creates a FastAPI instance named app.
# Metadata:
# title: Sets the API title.
# description: Brief API description.
# version: Uses v1 to track API versions.
# lifespan: Uses the life_span function to manage startup and shutdown tasks.

version='v1'

app=FastAPI(
    title="My Book Store",
    description="A REST Api for Book Review",
    version=version,
    lifespan=life_span
)

#book_router: Assumes there is a router (book_router) that contains endpoints related to books.
# prefix=f"/api/{version}/books": All book-related routes will be under /api/v1/books.
# tags=['Books']: Helps organize the API documentation in Swagger UI (/docs).

app.include_router(book_router, prefix=f"/api/{version}/books", tags=['Books'])
app.include_router(auth_router, prefix=f"/api/{version}/auth", tags=['Auth'])