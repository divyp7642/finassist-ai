
from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session

from app.database import get_db
from app.schemas import UserRegister, UserLogin
from app.security import create_access_token
from app.services import user_service

from app.dependencies import get_current_user_id

router = APIRouter(prefix="/auth", tags=["Authentication"])


@router.post("/register", status_code=201)
def register_user(
    user: UserRegister,
    db: Session = Depends(get_db)
):
    new_user = user_service.register_user(
        db=db,
        name=user.name,
        email=user.email,
        password=user.password
    )

    if new_user is None:
        raise HTTPException(
            status_code=409,
            detail="Email already exists"
        )

    return {
        "id": new_user.id,
        "name": new_user.name,
        "email": new_user.email,
        "message": "User registered successfully"
    }


@router.post("/login")
def login_user(
    credentials: UserLogin,
    db: Session = Depends(get_db)
):
    user = user_service.authenticate_user(
        db=db,
        email=credentials.email,
        password=credentials.password
    )

    if user is None:
        raise HTTPException(
            status_code=401,
            detail="Invalid email or password",
            headers={"WWW-Authenticate": "Bearer"}
        )

    access_token = create_access_token(user.id)

    return {
        "access_token": access_token,
        "token_type": "bearer"
    }


@router.get("/me")
def get_my_profile(
    user_id: int = Depends(get_current_user_id)
):
    return {
        "message": "You are authenticated",
        "user_id": user_id
    }
