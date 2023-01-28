from db.repository.startup_users import create_new_startup_user
from db.repository.investor_users import create_new_investor_user
from db.session import get_db
from fastapi import APIRouter
from fastapi import Depends
from schemas.startup_users import ShowStartUpUser
from schemas.startup_users import StartUpUserCreate
from sqlalchemy.orm import Session
from schemas.investor_users import ShowInvestorUser
from schemas.investor_users import InvestorUserCreate

router = APIRouter()


@router.post("/startup", response_model=ShowStartUpUser)
def create_startup_user(user: StartUpUserCreate, db: Session = Depends(get_db)):
    user = create_new_startup_user(user=user, db=db)
    return user


@router.post("/investor", response_model=ShowInvestorUser)
def create_investor_user(user: InvestorUserCreate, db: Session = Depends(get_db)):
    user = create_new_investor_user(user=user, db=db)
    return user