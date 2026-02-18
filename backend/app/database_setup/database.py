from sqlmodel import SQLModel, create_engine, Session, select
from app.database_setup.schema import Event, User
from app.auth.security import hash_password
from dotenv import load_dotenv
from pathlib import Path
import os


# Load environment variables from .env
load_dotenv(dotenv_path=Path(__file__).resolve().parents[3] / ".env")

# Fetch variables
USER = os.getenv("user")
PASSWORD = os.getenv("password")
HOST = os.getenv("host")
PORT = os.getenv("port")
DBNAME = os.getenv("dbname")

DATABASE_URL = f"postgresql://{USER}:{PASSWORD}@{HOST}:{PORT}/{DBNAME}"


# Create the Engine
# This is the "plug" that connects to the socket.
engine = create_engine(DATABASE_URL, echo=True)

# Initialize 
# We run this on startup to create tables if they don't exist.
def create_db_and_tables():
    SQLModel.metadata.create_all(engine)

# Seed the default admin user
def seed_admin_user():
    ADMIN_EMAIL = "tickethiveadmin@gmail.com"
    ADMIN_PASSWORD = "tickecthive@admin"
    ADMIN_NAME = "TicketHive Admin"

    with Session(engine) as session:
        # Check if admin already exists
        statement = select(User).where(User.email == ADMIN_EMAIL)
        existing_admin = session.exec(statement).first()

        if existing_admin is None:
            admin_user = User(
                name=ADMIN_NAME,
                email=ADMIN_EMAIL,
                hashed_password=hash_password(ADMIN_PASSWORD),
                is_admin=True,
            )
            session.add(admin_user)
            session.commit()
           
# Dependency
# This is a special function for FastAPI to get a fresh session for each request.
def get_session():
    with Session(engine) as session:
        yield session
