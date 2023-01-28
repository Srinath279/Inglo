from core.hashing import Hasher
from core.phone import PhoneNumber
from db.models.investor_users import InvestorUsers
from schemas.investor_users import InvestorUserCreate
from sqlalchemy.orm import Session


def create_new_investor_user(user: InvestorUserCreate, db: Session):
    user = InvestorUsers(
        email=user.email,
        hashed_password=Hasher.get_password_hash(user.password),
        phone_number=PhoneNumber.validate_phone_number(user.phone_number, country_code='91'),
        is_active=True,
        is_superuser=False,
    )
    db.add(user)
    db.commit()
    db.refresh(user)
    return user


def get_user_by_email(email: str, db: Session):
    user = db.query(InvestorUsers).filter(InvestorUsers.email == email).first()
    return user
