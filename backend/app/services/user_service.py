from fastapi import HTTPException, status
from app.auth.security import hash_password, verify_password, create_access_token
from app.models.user import UserRegister, UserLogin
from app.database_setup.schema import User
from sqlmodel import Session, select
from sqlalchemy.exc import SQLAlchemyError


class UserService:
    def __init__(self, session: Session):
        self._db = session

    # Register User
    def register_user(self, user_data: UserRegister) -> User:
        # Check if email already exists
        statement = select(User).where(User.email == user_data.email)
        existing_user = self._db.exec(statement).first()

        if existing_user:
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail="Email already registered",
            )

        # Hash the password
        hashed_pwd = hash_password(user_data.password)

        # Map register payload to DB user model
        new_user = User(
            name=user_data.name,
            email=user_data.email,
            hashed_password=hashed_pwd,
        )

        # Save to DB
        try:
            self._db.add(new_user)
            self._db.commit()
            self._db.refresh(new_user)
            return new_user
        except SQLAlchemyError as exc:
            self._db.rollback()
            raise RuntimeError("Failed to create user") from exc
        
    # Login User
    def login_user(self, user_data: UserLogin) -> dict:
        # Find user
        statement = select(User).where(User.email == user_data.email)
        user = self._db.exec(statement).first()

        # Check if user exists AND password matches
        if not user or not verify_password(user_data.password, user.hashed_password):
            raise HTTPException(status_code=401, detail="Invalid credentials")
        
        # Create the wristband (Token)
        access_token = create_access_token(data={"sub": user.email})

        # Return it to the frontend
        return {
            "access_token": access_token, 
            "token_type": "bearer",
            "user": {
                "name": user.name,
                "email": user.email,
            }
        }
    
