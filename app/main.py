from this import d
from fastapi import FastAPI
from . import models 
from .database import engine 
from .routers import posts, users, auth, vote
from .config import settings
from fastapi.middleware.cors import CORSMiddleware


#This is going to create all the models and tables 
#models.Base.metadata.create_all(bind=engine) 
#we dont need this anymore as we have Alembic 

app = FastAPI() 

#lists of URLs that can talk to my API. for a public API ["*"]
#origins = ["https://www.google.com"]
origins = ["*"]

app.add_middleware(
    CORSMiddleware, #this functions runs before every requests 
    allow_origins=origins, #what domain can talk to our api 
    allow_credentials=True,
    allow_methods=["*"], #allow request post/get/delete
    allow_headers=["*"],
)

app.include_router(auth.router)
app.include_router(users.router)
app.include_router(posts.router)
app.include_router(vote.router)

#path operation/route 
@app.get("/")
async def root():
    return {"message": "Welcome to my FastAPI!!!!!"}

