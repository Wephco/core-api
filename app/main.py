from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
import uvicorn

# from .db import database_models, database
from .routers import users, auth, property_requests, hotel_requests, agents, property_listings

# database_models.Base.metadata.create_all(bind=database.engine)

app = FastAPI()

# CORS Middleware Config
app.add_middleware(CORSMiddleware, allow_origins=[
                   "*"], allow_credentials=True, allow_methods=["*"], allow_headers=["*"])

# root route


@app.get("/")
async def root():
    return {"message": "Deployed from CI/CD Pipeline"}

# add app routes
app.include_router(users.router)
app.include_router(auth.router)
app.include_router(property_requests.router)
app.include_router(hotel_requests.router)
app.include_router(agents.router)
app.include_router(property_listings.router)


# if __name__ == "__main__":
#     uvicorn.run(app, host="0.0.0.0", port=8000)
