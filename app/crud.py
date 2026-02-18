from sqlalchemy.orm import Session
from sqlalchemy import select
from .models import User
from .schemas import UserCreate, UserUpdate


def create_user(db: Session, data: UserCreate) -> User:
    user = User(email=str(data.email), full_name=data.full_name)
    db.add(user)
    db.commit()
    db.refresh(user)
    return user


def get_user(db: Session, user_id: int) -> User | None:
    return db.get(User, user_id)


def get_user_by_email(db: Session, email: str) -> User | None:
    return db.scalar(select(User).where(User.email == email))


def list_users(db: Session, skip: int = 0, limit: int = 50) -> list[User]:
    return list(db.scalars(select(User).offset(skip).limit(limit)))


def update_user(db: Session, user: User, data: UserUpdate) -> User:
    if data.email is not None:
        user.email = str(data.email)
    if data.full_name is not None:
        user.full_name = data.full_name
    db.commit()
    db.refresh(user)
    return user


def delete_user(db: Session, user: User) -> None:
    db.delete(user)
    db.commit()
