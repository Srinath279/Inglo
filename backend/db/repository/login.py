from db.models.startup_users import StartUpUsers
from sqlalchemy.orm import Session


def get_user(username: str, db: Session):
    user = db.query(StartUpUsers).filter(StartUpUsers.email == username).first()
    return user
