from sqlalchemy.orm import Session
from utils import hash_password, verify_password
from schemas import UserCreate, UserLogin, Token
from models import User

def get_user_by_name(db: Session, username: str) -> User | None:
    return db.query(User).filter(User.username == username).first()


def create_user(db: Session, user: UserCreate) -> User:
    new_user = User(username=user.username, password=hash_password(user.password), role=user.role)
    db.add(new_user)
    db.commit()
    db.refresh(new_user)
    return new_user

def authenticate_user(db: Session, user: UserLogin) -> User:
    db_user = get_user_by_name(db, user.username)
    if not db_user or not verify_password(user.password, db_user.password):
        return None
    return db_user