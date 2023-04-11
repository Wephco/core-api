from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

from .db import database_models
from .db import database
from .routers import users, auth, property_requests

database_models.Base.metadata.create_all(bind=database.engine)

app = FastAPI()

# CORS Middleware Config
app.add_middleware(CORSMiddleware, allow_origins=["*"], allow_credentials=True, allow_methods=["*"], allow_headers=["*"])

# add app routes
app.include_router(users.router)
app.include_router(auth.router)
app.include_router(property_requests.router)