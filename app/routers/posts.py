from pyexpat import model
from fastapi import FastAPI, Response, status, HTTPException, Depends, APIRouter
from app import oauth2
from .. import models, schemas, oauth2 # .. means upper directory
from ..database import get_db
from sqlalchemy.orm import Session  
from typing import List, Optional
from sqlalchemy import func

router = APIRouter(
    prefix = "/posts", # /posts/{id}
    tags= ['Posts'] #documentation grp
)


#SQLalchemy test
#@router.get("/")
#def test_posts(db: Session = Depends(get_db), current_user: int= Depends(oauth2.get_current_user)): 
     #posts = db.query(models.Post).all()
     #return {"data": posts}
     
#Create Post
@router.post("/", status_code=status.HTTP_201_CREATED, response_model= schemas.Post)
def create_posts(post: schemas.PostCreate, db: Session = Depends(get_db), current_user: int= Depends(oauth2.get_current_user)):
    
    #cur.execute("""INSERT INTO posts (title, content, published) VALUES (%s, %s, %s) RETURNING * """, 
    #            (post.title, post.content, post.published)) #order matters 
    #new_posts = cur.fetchone()
    #anytime we make a change to the database, we need to commit to it  
    #conn.commit() 
    
    #user_id: int= Depends(oauth2.get_current_user) this line is used to verift the log in. 
    
   
    #new_posts = models.Post(title=post.title, content=post.content, published=post.published)
    # (**) this is going to uppack the all the fields/columns so we dont have to manually type it out
    # owner_id= current_user.id --this line works for creating post of the user. owner of the new post is the current user.
    new_post = models.Post(owner_id= current_user.id, **post.dict())
    db.add(new_post)
    db.commit() # #Commit to DB
    db.refresh(new_post) #retrive the data
    return new_post

#All Post Retrive 
# @router.get("/", response_model= List[schemas.Post])
# @router.get("/", response_model= List[schemas.PostOut])
@router.get("/", response_model= List[schemas.PostOut])
def get_post(db: Session = Depends(get_db), current_user: int= Depends(oauth2.get_current_user), limit: int = 20, skip: int = 0, search : Optional[str]= ""): #limit: int = 10 so that user can choose how many posts s/he wants to see
    
    #cur.execute("""SELECT * FROM posts """)
    #posts = cur.fetchall()
    #print(limit)
    
    #posts = db.query(models.Post).all()
    #posts = db.query(models.Post).filter(models.Post.title.contains(search)).limit(limit).offset(skip).all() #models.Post.title.contains(search) -- because we are going to search through titles
    
    #SQL joins in SQLAlchemy 
    posts = db.query(models.Post, func.count(models.Votes.post_id).label("votes")).join(
        models.Votes, models.Votes.post_id == models.Post.id, isouter=True).group_by(models.Post.id).filter(
        models.Post.title.contains(search)).limit(limit).offset(skip).all()
    
    return posts

#retriveing only your own posts (can not ahve both all post retrive nad own post retrive)
# @router.get("/", response_model= List[schemas.PostOut])
# def get_post(db: Session = Depends(get_db), current_user: int= Depends(oauth2.get_current_user)):

#     #posts = db.query(models.Post).filter(models.Post.owner_id == current_user.id).all()
    
#     posts = db.query(models.Post, func.count(models.Votes.post_id).label("votes")).join(
#         models.Votes, models.Votes.post_id == models.Post.id, isouter=True).group_by(models.Post.id).filter(
#         models.Post.owner_id == current_user.id).all()
    
#     return posts

#Single Post Retrive
@router.get("/{id}", response_model= schemas.PostOut)
def get_one_post(id: int, db: Session = Depends(get_db), current_user: int= Depends(oauth2.get_current_user)):
    # cur.execute("""SELECT * FROM posts WHERE id = %s """, (str(id))) # this is to avoid SQL injection
    # post = cur.fetchone() 
    
    #post = db.query(models.Post).filter(models.Post.id == id).first() #works like SQL WHERE. 
                                                            #.first() bring the first found result instead of all()
    
    posts = db.query(models.Post, func.count(models.Votes.post_id).label("votes")).join(
         models.Votes, models.Votes.post_id == models.Post.id, isouter=True).group_by(models.Post.id).filter(
         models.Post.id == id).first()
    
    if not posts:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, 
                            detail=f"Post with Id:{id} not found")
        
    return posts


#Update
@router.put("/{id}", response_model= schemas.Post)
def update_post(id: int, post:schemas.PostCreate, db: Session = Depends(get_db), current_user: int= Depends(oauth2.get_current_user)):

    # # cur.execute("""UPDATE posts SET title = %s, content= %s, published= %s WHERE id = %s RETURNING * """, 
    # #             (post.title, post.content, post.published, str(id))) #order matters 
    # # updated_post = cur.fetchone()
    # #anytime we make a change to the database, we need to commit to it  
    # conn.commit()
    
    updated_post_query = db.query(models.Post).filter(models.Post.id == id) 
    updated_post=updated_post_query.first()

    if updated_post == None: 
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, 
                            detail=f"Post with Id:{id} not found")
        
    #Update only your own post 
    
    #if updated_post.owner_id != current_user.id:
        #raise HTTPException(status_code=status.HTTP_403_FORBIDDEN, 
                            #detail=f"Not authorised to perform this operation")
        
    updated_post_query.update(post.dict(), synchronize_session=False)
    db.commit()
    db.refresh(updated_post_query.first()) #retrive the data
    
    return updated_post_query.first()

#Delete
@router.delete("/{id}", status_code=status.HTTP_204_NO_CONTENT)
def delete_post(id: int, db: Session = Depends(get_db), current_user: int= Depends(oauth2.get_current_user)):

    # cur.execute("""DELETe FROM posts WHERE id = %s RETURNING * """, (str(id))) # this is to avoid SQL injection
    # deleted_post = cur.fetchone()
    
    post_query = db.query(models.Post).filter(models.Post.id == id) 
    post = post_query.first() 
    
    if post == None: #checking if the first found result is none
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, 
                            detail=f"Post with Id:{id} does not exist")
    #Delete only your own post 
    
    #if post.owner_id != current_user.id:
        #raise HTTPException(status_code=status.HTTP_403_FORBIDDEN, 
                            #detail=f"Not authorised to perform this operation")
    
    post_query.delete(synchronize_session=False)
    db.commit()
    
    return Response(status_code=status.HTTP_204_NO_CONTENT)
