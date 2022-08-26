from fastapi import FastAPI, Response, status, HTTPException, Depends, APIRouter
from .. import models, schemas, utils# .. means upper directory
from ..database import get_db
from sqlalchemy.orm import Session  

router = APIRouter(
    prefix = "/users", # /posts/{id}
    tags= ['Users']
)

#Create User
@router.post("/", status_code=status.HTTP_201_CREATED, response_model=schemas.UserOut)
def create_user(user: schemas.UserCreate, db: Session = Depends(get_db)):
    
    #hash the password - user.password
    hashed_password = utils.hash(user.password)
    user.password = hashed_password #this is gonna update pydentic user model

    new_user = models.Users(**user.dict())
    db.add(new_user)
    db.commit() # #Commit to DB
    db.refresh(new_user) #retrive the data
    return new_user 

#Get User 
@router.get("/{id}", response_model=schemas.UserOut) #response model is hiding the password
def get_user(id: int, db: Session = Depends(get_db)):
    user = db.query(models.Users).filter(models.Users.id == id).first() #works like SQL WHERE. 
                                                            #.first() bring the first found result instead of all()
    if not user:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, 
                            detail=f"User with Id:{id} not found")
        
    return user