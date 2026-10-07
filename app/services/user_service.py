from sqlalchemy.orm import Session

from app.repositories import user_repository

def get_all_users(db: Session):
    return user_repository.get_all_users(db)

def get_user_by_id(
    db: Session,
    user_id: int
):
    return user_repository.get_user_by_id(
        db,
        user_id
    )

def create_user(
    db: Session,
    name: str,
    email: str
):
    existing_user = user_repository.get_user_by_email(
        db,
        email
    )

    if existing_user is not None:
        return None

    return user_repository.create_user(
        db=db,
        name=name,
        email=email
    )

def update_user(
    db: Session,
    user_id: int,
    name: str,
    email: str
):
    user = user_repository.get_user_by_id(
        db,
        user_id
    )

    if user is None:
        return None, "user_not_found"

    existing_user = user_repository.get_user_by_email(
        db,
        email
    )

    if existing_user is not None and existing_user.id != user_id:
        return None, "email_exists"

    updated_user = user_repository.update_user(
        db=db,
        user=user,
        name=name,
        email=email
    )

    return updated_user, None

def delete_user(
    db: Session,
    user_id: int
):
    user = user_repository.get_user_by_id(
        db,
        user_id
    )

    if user is None:
        return False

    user_repository.delete_user(
        db=db,
        user=user
    )

    return True