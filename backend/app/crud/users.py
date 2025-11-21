from sqlalchemy.orm import Session
from app.models import User
import hashlib

def make_password_hash(password: str):
    return hashlib.sha256(password.encode("utf-8")).hexdigest()


def get_users(session: Session, limit: int, offset: int):
    results = session.query(User).limit(limit).offset(offset)
    return results.all()


def check_if_user_already_exists(session: Session, email: str):
    users = session.query(User).filter(User.email == email).all()
    return len(users) > 0


def get_user_by_email(session: Session, email: str):
    res = session.query(User).filter(User.email == email).all()
    if len(res) == 0:
        return None
    return res[0]


def create_user(session: Session, user: User):
    """Création de l'utilisateur, se charge de hash le password"""
    try:
        password = make_password_hash(user.password)
        user_db = User(
            email=user.email,
            password=password,
            role=user.role,
        )
        session.add(user_db)
        session.commit()
        session.refresh(user_db)
        return user_db
    except Exception:
        session.rollback()
        raise


def login(session: Session, email: str, password: str) -> User:
    password = make_password_hash(password)
    query = session.query(User).filter(User.email == email, User.password == password)
    results = query.all()
    if len(results) > 0:
        return results[0]
    return None


def update_user(session: Session, id: int, user: User):
    try:
        user_db = session.get(User, id)
        if user_db is None:
            return None

        if user.password is not None:
            user_db.password = make_password_hash(user.password)

        if user.role is not None:
            user_db.role = user.role

        session.add(user_db)
        session.commit()
        session.refresh(user_db)

        return user_db
    except Exception:
        session.rollback()
        raise