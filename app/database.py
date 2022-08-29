from distutils.command.config import config
from sqlalchemy import create_engine
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker
import time 
import psycopg2
from psycopg2.extras import RealDictCursor 
from .config import settings

#SQLALCHEMY_DATABASE_URL = "postgresql://username:password@postgresserver_ipaddress/db"
#SQLALCHEMY_DATABASE_URL = f'postgresql://postgres:password@localhost:5432/FastAPI'
#SQLALCHEMY_DATABASE_URL = f'postgresql://{settings.database_username}:{settings.database_password}@{settings.database_hostname}:{settings.database_port}/{settings.database_name}'
SQLALCHEMY_DATABASE_URL = f'postgres://mugammhobcdlcf:e260559259b9b5de545579f7af91c62016a5d25e329aa717ad5ef850464521e6@ec2-3-208-79-113.compute-1.amazonaws.com:5432/d2cqr3plq304c'

#responsible to SQLALchamy with Postgres DB 
engine = create_engine(SQLALCHEMY_DATABASE_URL) #for SQLlite this needs to add ", connect_args={"check_same_thread": False}"
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine) #to talk to DB 

Base = declarative_base() 

# Dependency
def get_db():
    db = SessionLocal() #session object is responsive for talking with DB 
    try:
        yield db
    finally:
        db.close()
        
# Connection with existing Database 
# while True:
#     try: 
#         conn = psycopg2.connect(host='localhost', database= 'FastAPI', user= 'postgres', 
#                                 password='password', cursor_factory=RealDictCursor)

#     #Open a cursor to perform database operations (SQL statement)
#         cur = conn.cursor()
#         print("Database Connection successful")
#         break
#     except Exception as error: 
#         print("Database Connection Failed")
#         print("Error : ", error) 
#         time.sleep(2) #for break for 2 seconds and re-try to connect database in the-
#                         #-while loop until is finds the connection and break the while loop. 

