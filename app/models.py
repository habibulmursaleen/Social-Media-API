from sqlalchemy import TIMESTAMP, Column, ForeignKey, Integer,String,Boolean
from sqlalchemy.sql.expression import null, text 
from sqlalchemy.orm import relationship
from .database import Base 

#model represents tables
class Post(Base): 
    __tablename__ = "posts"

    id = Column(Integer, primary_key = True, nullable = False)
    title = Column(String, nullable = False)
    content = Column(String, nullable = False)
    published = Column(Boolean, server_default= 'TRUE', nullable = False)
    created_at = Column(TIMESTAMP(timezone=True), nullable = False, 
                        server_default=text('now()'))
    owner_id = Column(Integer, ForeignKey("users.id", ondelete="CASCADE"), nullable = False) #foreign key add
    
    owner = relationship("Users")
    
class Users(Base): 
     __tablename__ = "users"
     
     id = Column(Integer, primary_key = True, nullable = False)
     email = Column(String, nullable = False, unique= True)
     password = Column(String, nullable = False)
     created_at = Column(TIMESTAMP(timezone=True), nullable = False, 
                         server_default=text('now()')) 
     phone_number = Column(String)
     
class Votes(Base): 
     __tablename__ = "votes"
     
     user_id = Column(Integer, ForeignKey("users.id", ondelete="CASCADE"), nullable = False, primary_key = True)
     post_id = Column(Integer, ForeignKey("posts.id", ondelete="CASCADE"), nullable = False, primary_key = True)
     