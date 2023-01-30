from pydantic import BaseModel, Field


class Token(BaseModel):
    access_token: str
    token_type: str


class UserBasicInfo(BaseModel):
    # id: str
    email: str
    # fullname: str
class Token(BaseModel):
    access_token: str
    token_type: str
    user_info: UserBasicInfo


class TokenData(BaseModel):
    email: str = None

class EmailRequest(BaseModel):
    email: str

class ResetPassword(BaseModel):
    new_password: str
    confirm_password: str

class ChangePassword(BaseModel):
    old_password: str = Field(..., example="old password")
    new_password: str = Field(..., example="new password")
    confirm_password: str = Field(..., example="confirm password")
