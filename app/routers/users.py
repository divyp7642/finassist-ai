from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session

from app.database import get_db
from app.schemas import UserCreate
from app.services import user_service


router = APIRouter(
    prefix="/users",
    tags=["Users"]
)

@router.get("")
def get_users(db: Session = Depends(get_db)):
    return user_service.get_all_users(db)

@router.get("/{user_id}")
def get_user(
    user_id: int,
    db: Session = Depends(get_db)
):
    user = user_service.get_user_by_id(
        db,
        user_id
    )

    if user is None:
        raise HTTPException(
            status_code=404,
            detail="User not found"
        )

    return user

@router.post("", status_code=201)
def create_user(
    user: UserCreate,
    db: Session = Depends(get_db)
):
    new_user = user_service.create_user(
        db=db,
        name=user.name,
        email=user.email
    )

    if new_user is None:
        raise HTTPException(
            status_code=409,
            detail="Email already exists"
        )

    return new_user

@router.put("/{user_id}")
def update_user(
    user_id: int,
    updated_user: UserCreate,
    db: Session = Depends(get_db)
):
    user, error = user_service.update_user(
        db=db,
        user_id=user_id,
        name=updated_user.name,
        email=updated_user.email
    )

    if error == "user_not_found":
        raise HTTPException(
            status_code=404,
            detail="User not found"
        )

    if error == "email_exists":
        raise HTTPException(
            status_code=409,
            detail="Email already exists"
        )

    return user

@router.delete("/{user_id}")
def delete_user(
    user_id: int,
    db: Session = Depends(get_db)
):
    deleted = user_service.delete_user(
        db=db,
        user_id=user_id
    )

    if not deleted:
        raise HTTPException(
            status_code=404,
            detail="User not found"
        )

    return {"message": "User deleted successfully"}