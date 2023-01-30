from pydantic import BaseModel
from pydantic import EmailStr


# properties required during user creation
class StartUpUserCreate(BaseModel):
    founder_name: str
    company_name: str
    phone_number: str
    email: EmailStr
    password: str


class ShowStartUpUser(BaseModel):
    founder_name: str
    email: EmailStr
    is_active: bool

    class Config:  # to convert non dict obj to json
        orm_mode = True
