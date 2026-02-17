from passlib.context import CryptContext
from datetime import datetime, timedelta
from jose import jwt

# Configuration
SECRET_KEY = "dba458fa154c82e0e36458ddfaf66bccc6bd18cfa11106c12dd8a2e5cb5f9f78" 
ALGORITHM = "HS256"
ACCESS_TOKEN_EXPIRE_MINUTES = 30

# Setup the hashing engine (using bcrypt)
pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")


def hash_password(password: str) -> str:
    """
    Takes a plain password (e.g., 'secret123') 
    and returns a hashed string.
    """
    return pwd_context.hash(password)

def verify_password(plain_password: str, hashed_password: str) -> bool:
    """
    Checks if a plain password matches the stored hash.
    """
    return pwd_context.verify(plain_password, hashed_password)

def create_access_token(data: dict):
    """
    Generates a JWT Token (The Wristband).
    Encodes user data and an expiration time into a string.
    """

    to_encode = data.copy()
    
    # Set expiration time
    expire = datetime.utcnow() + timedelta(minutes=ACCESS_TOKEN_EXPIRE_MINUTES)
    to_encode.update({"exp": expire})
    
    # Sign the token
    encoded_jwt = jwt.encode(to_encode, SECRET_KEY, algorithm=ALGORITHM)
    return encoded_jwt