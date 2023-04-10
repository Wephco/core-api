from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

from db import database_models
from db.database import engine
from .routers import users, auth

database_models.Base.metadata.create_all(bind=engine)

app = FastAPI()

# CORS Middleware Config
app.add_middleware(CORSMiddleware, allow_origins=["*"], allow_credentials=True, allow_methods=["*"], allow_headers=["*"])

# add app routes
app.include_router(users.router)
app.include_router(auth.router)