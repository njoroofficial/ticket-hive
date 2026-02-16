from sqlmodel import SQLModel, create_engine, Session
from app.database_setup.models import Event

DATABASE_URL = "sqlite:///tickethive.db"

# Create the Engine
# This is the "plug" that connects to the socket.
engine = create_engine(DATABASE_URL, echo=True)

# Initialize 
# We run this on startup to create tables if they don't exist.
def create_db_and_tables():
    SQLModel.metadata.create_all(engine)

# Dependency
# This is a special function for FastAPI to get a fresh session for each request.
def get_session():
    with Session(engine) as session:
        yield session
