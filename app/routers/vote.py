from fastapi import FastAPI, Response, status, HTTPException, Depends, APIRouter
from app import oauth2
from .. import models, schemas, oauth2 # .. means upper directory
from ..database import get_db
from sqlalchemy.orm import Session  
from typing import List, Optional

router = APIRouter(
    prefix = "/vote", 
    tags= ['Vote'] 
)

@router.post("/", status_code=status.HTTP_201_CREATED)
def vote(vote: schemas.Vote, db: Session = Depends(get_db), current_user: int= Depends(oauth2.get_current_user)):

    post = db.query(models.Post).filter(models.Post.id == vote.post_id).first()
    if not post: 
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, 
                            detail=f"Post with Id:{id} not found")
    
    vote_query = db.query(models.Votes).filter(
        models.Votes.post_id == vote.post_id, 
        models.Votes.user_id == current_user.id)
    found_vote = vote_query.first()

    #to like/vote
    if (vote.dir == 1):
        if found_vote: 
            raise HTTPException(status_code=status.HTTP_409_CONFLICT, 
                            detail=f"User {current_user.id} has already voted on post {vote.post_id}")
        
        new_vote = models.Votes(post_id = vote.post_id, user_id=current_user.id)
        db.add(new_vote)
        db.commit()
        return{"message":"successfully voted"}
    
    #to delete vote/unlike 
    else: 
        if not found_vote: 
            raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, 
                            detail=f"Vote does not exist")
        vote_query.delete(synchronize_session=False)
        db.commit()
        return{"message":"successfully vote deleted"} 