from pydantic import BaseModel
from pydantic import EmailStr


# properties required during user creation
class InvestorUserCreate(BaseModel):
    email: EmailStr
    phone_number: str
    password: str


class ShowInvestorUser(BaseModel):
    # founder_name: str
    email: EmailStr
    is_active: bool

    class Config:  # to convert non dict obj to json
        orm_mode = True
