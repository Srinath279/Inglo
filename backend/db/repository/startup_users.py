from core.hashing import Hasher
from core.phone import PhoneNumber
from db.models.startup_users import StartUpUsers
from schemas.startup_users import StartUpUserCreate
from sqlalchemy.orm import Session


def create_new_startup_user(user: StartUpUserCreate, db: Session):
    user = StartUpUsers(
        founder_name=user.founder_name,
        company_name=user.company_name,
        phone_number= PhoneNumber.validate_phone_number(user.phone_number,country_code='91'),
        email=user.email,
        hashed_password=Hasher.get_password_hash(user.password),
        is_active=True,
        is_superuser=False,
    )
    db.add(user)
    db.commit()
    db.refresh(user)
    return user


def get_user_by_email(email: str, db: Session):
    user = db.query(StartUpUsers).filter(StartUpUsers.email == email).first()
    return user
