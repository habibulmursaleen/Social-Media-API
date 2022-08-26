from email import utils
from os import access
from fastapi import Response, status, HTTPException, Depends, APIRouter
from fastapi.security.oauth2 import OAuth2PasswordRequestForm
from .. import database, schemas, models, utils, oauth2 
from sqlalchemy.orm import Session  

router = APIRouter(
    tags= ['Authentication'] #documentation grp
)

@router.post('/login', response_model=schemas.Token)
def login(users_credentials: OAuth2PasswordRequestForm= Depends(), db: Session = Depends(database.get_db)):
    #only takes Username as input i.g. email, username, id but stores in Username
    user = db.query(models.Users).filter(models.Users.email == users_credentials.username).first() 
    if not user:
        raise HTTPException(status_code=status.HTTP_403_FORBIDDEN, 
                            detail=f"Invalid Credentials")
        
    if not utils.verify(users_credentials.password, user.password):
        raise HTTPException(status_code=status.HTTP_403_FORBIDDEN, 
                            detail=f"Invalid Credentials")
    
    #create a token from Oauth2
    access_token= oauth2.create_access_token(data = {"user_id": user.id})
    return {"access_token": access_token, "token_type": "bearer"}    
