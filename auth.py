from passlib.context import CryptContext
from sqlalchemy.orm import Session
from models import User

pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")


def verify_password(plain_password, hashed_password):
    return pwd_context.verify(plain_password, hashed_password)


def get_password_hash(password):
    return pwd_context.hash(password)


def authenticate_user(db: Session, username: str, password: str):
    user = db.query(User).filter(User.username == username).first()
    if not user:
        return False
    if not verify_password(password, user.password):
        return False
    return user


def create_user(db: Session, username: str, firstname: str, lastname: str, middlename: str, email: str, password: str):
    hashed_password = get_password_hash(password)
    db_user = User(username=username, firstname=firstname, lastname=lastname, middlename=middlename, email=email,
                   password=hashed_password)
    db.add(db_user)
    db.commit()
    db.refresh(db_user)
    return db_user
