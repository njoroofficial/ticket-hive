from fastapi import APIRouter, Depends, HTTPException, status
from sqlmodel import Session
from app.database_setup.database import get_session
from app.models.user import UserLogin, UserRead, UserRegister
from app.services.user_service import UserService

router = APIRouter(prefix="/auth", tags=["Auth"])


@router.post("/register", response_model=UserRead, status_code=status.HTTP_201_CREATED)
def register_user(user_data: UserRegister, session: Session = Depends(get_session)) -> UserRead:
    service = UserService(session)
    try:
        return service.register_user(user_data)
    except HTTPException:
        raise
    except RuntimeError as exc:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail="Unable to register user at this time.",
        ) from exc


@router.post("/login", status_code=status.HTTP_200_OK)
def login_user(user_data: UserLogin, session: Session = Depends(get_session)) -> dict:
    service = UserService(session)
    try:
        return service.login_user(user_data)
    except HTTPException:
        raise
    except RuntimeError as exc:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail="Unable to login user at this time.",
        ) from exc
