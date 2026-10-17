
from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session

from app.database import get_db
from app.dependencies import get_current_user_id
from app.schemas import UserCreate, UserResponse
from app.services import user_service


router = APIRouter(
    prefix="/users",
    tags=["Users"],
    dependencies=[Depends(get_current_user_id)]
)


# GET CURRENT USER
@router.get("", response_model=UserResponse)
def get_users(
    db: Session = Depends(get_db),
    current_user_id: int = Depends(get_current_user_id)
):
    user = user_service.get_user_by_id(
        db,
        current_user_id
    )

    if user is None:
        raise HTTPException(
            status_code=404,
            detail="User not found"
        )

    return user


# GET USER BY ID
@router.get("/{user_id}", response_model=UserResponse)
def get_user(
    user_id: int,
    db: Session = Depends(get_db),
    current_user_id: int = Depends(get_current_user_id)
):
    # Verify profile ownership
    if user_id != current_user_id:
        raise HTTPException(
            status_code=403,
            detail="You cannot access another user's profile"
        )

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


# UPDATE USER
@router.put("/{user_id}", response_model=UserResponse)
def update_user(
    user_id: int,
    updated_user: UserCreate,
    db: Session = Depends(get_db),
    current_user_id: int = Depends(get_current_user_id)
):
    # Verify profile ownership
    if user_id != current_user_id:
        raise HTTPException(
            status_code=403,
            detail="You cannot update another user's profile"
        )

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


# DELETE USER
@router.delete("/{user_id}")
def delete_user(
    user_id: int,
    db: Session = Depends(get_db),
    current_user_id: int = Depends(get_current_user_id)
):
    # Verify account ownership
    if user_id != current_user_id:
        raise HTTPException(
            status_code=403,
            detail="You cannot delete another user's account"
        )

    deleted = user_service.delete_user(
        db=db,
        user_id=user_id
    )

    if not deleted:
        raise HTTPException(
            status_code=404,
            detail="User not found"
        )

    return {
        "message": "User deleted successfully"
    }
