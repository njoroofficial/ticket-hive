from fastapi import FastAPI
from contextlib import asynccontextmanager
from app.database_setup.database import create_db_and_tables, seed_admin_user
from app.api import event, user, booking


# The Startup Event
# It runs ONE time when the server starts to make sure our tables exist.
# The Lifespan Context Manager
@asynccontextmanager
async def lifespan(app: FastAPI):
    # Startup: Build the tables
    create_db_and_tables()
    seed_admin_user()
    yield
    # Shutdown: Nothing needed here!

app = FastAPI(lifespan=lifespan)

# Plug in the routes
app.include_router(user.router)
app.include_router(event.router)
app.include_router(booking.router)

@app.get("/")
def read_root():
    return {"message": "Welcome to TicketHive!", "status": "active"}

