from db.models.startup_users import StartUpUsers
from sqlalchemy.orm import Session
from db.models.investor_users import InvestorUsers



def get_user(username: str,user: str, db: Session):
    if user == 'StartUpUsers':
        user = db.query(StartUpUsers).filter(StartUpUsers.email == username).first()
    elif user == 'InvestorUsers':
        user = db.query(InvestorUsers).filter(InvestorUsers.email == username).first()
    return user
