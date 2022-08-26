from passlib.context import CryptContext 

#telling passlib what is the default hashing algorithm which is bcrypt
pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")

def hash(password: str): 
    return pwd_context.hash(password)

#verifying the password 
def verify(plain_passowrd, hashed_password): 
    return pwd_context.verify(plain_passowrd, hashed_password)