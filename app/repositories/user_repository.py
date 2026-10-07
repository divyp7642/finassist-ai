from sqlalchemy.orm import Session

from app.models import User


def get_user_by_id(db: Session, user_id: int):
    return db.get(User, user_id)

def get_all_users(db: Session):
    return db.query(User).all()

def get_user_by_email(
    db: Session,
    email: str
):
    return db.query(User).filter(User.email == email).first()


def create_user(
    db: Session,
    name: str,
    email: str
):
    new_user = User(
        name=name,
        email=email
    )

    db.add(new_user)
    db.commit()
    db.refresh(new_user)

    return new_user

def update_user(
    db: Session,
    user: User,
    name: str,
    email: str
):
    user.name = name
    user.email = email

    db.commit()
    db.refresh(user)

    return user

def delete_user(
    db: Session,
    user: User
):
    db.delete(user)
    db.commit()