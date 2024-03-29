from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

from .routers import property_requests, hotel_requests, agents, property_listings, users, auth, consultation, diaspora_property_listings

# database_models.Base.metadata.create_all(bind=database.engine)

app = FastAPI()

origins = ["*"]

# CORS Middleware Config
app.add_middleware(CORSMiddleware, allow_origins=origins,
                   allow_credentials=True, allow_methods=["*"], allow_headers=["*"])


# add app routes
app.include_router(users.router)
app.include_router(auth.router)
app.include_router(property_requests.router)
app.include_router(hotel_requests.router)
app.include_router(agents.router)
app.include_router(property_listings.router)
app.include_router(diaspora_property_listings.router)
app.include_router(consultation.router)


@app.get("/")
async def root():
    return {"Wephco Core API": "Author - Neto"}


# if __name__ == "__main__":
#     uvicorn.run(app, host="0.0.0.0", port=8000)
