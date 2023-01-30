from pydantic import BaseModel, Field
from pydantic import EmailStr


# properties required during user creation
class InvestorUserCreate(BaseModel):
    email: EmailStr = Field(..., example="sjdecode@gmail.com")
    phone_number: str = Field(..., example="9812364802")
    password: str  = Field(..., example="sjdecode")


class ShowInvestorUser(BaseModel):
    # founder_name: str
    email: EmailStr
    is_active: bool

    class Config:  # to convert non dict obj to json
        orm_mode = True
