from datetime import timedelta
import uuid
from apis.utils import OAuth2PasswordBearerWithCookie
from core.config import settings
from core.hashing import Hasher
from core.security import create_access_token
from db.repository.login import get_user
from db.session import get_db
from fastapi import APIRouter
from fastapi import Depends
from fastapi import HTTPException
from fastapi import Response
from fastapi import status
from fastapi.security import OAuth2PasswordRequestForm
from jose import jwt
from jose import JWTError
from schemas.tokens import Token, EmailRequest
from sqlalchemy.orm import Session
from apis.exceptions.business import BusinessException

# from fastapi.security import OAuth2PasswordBearer


router = APIRouter()


def authenticate_user(username: str, password: str,user: str, db: Session = Depends(get_db)):
    user = get_user(username=username, user=user, db=db)
    # print(user)
    if not user:
        return False
    if not Hasher.verify_password(password, user.hashed_password):
        return False
    return user

def find_existed_user(email: str,user: str,db: Session = Depends(get_db)):
    if user == 'InvestorUsers':
        query = "select * from InvestorUsers where email=:email and status='1'"
    elif user == 'StartUpUsers':
        query = "select * from StartUpUsers where email=:email and status='1'"
    return db.fetch_one(query, values={"email": email})


def create_reset_code(request: EmailRequest, reset_code: str,db: Session = Depends(get_db)):
    query = "INSERT INTO codes VALUES (nextval('code_id_seq'), :email, :reset_code, '1', now() at time zone 'UTC')"
    return db.execute(query, values={"email": request.email, "reset_code": reset_code})

@router.post("/startup/token", response_model=Token)
def login_for_access_token(
    response: Response,
    form_data: OAuth2PasswordRequestForm = Depends(),
    db: Session = Depends(get_db)):
    user = authenticate_user(form_data.username, form_data.password, 'StartUpUsers', db)
    if not user:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Incorrect username or password",
        )
    access_token_expires = timedelta(minutes=settings.ACCESS_TOKEN_EXPIRE_MINUTES)
    access_token = create_access_token(
        data={"sub": user.email}, expires_delta=access_token_expires
    )
    response.set_cookie(
        key="access_token", value=f"Bearer {access_token}", httponly=True
    )

    results = {
        "access_token": access_token,
        "token_type": "bearer"
    }

    results.update({
        "user_info": {
            "email": user.email,
            # "fullname": user.fullname
        }
    })
    return results



@router.post("/investor/token", response_model=Token)
def login_for_access_token(
    response: Response,
    form_data: OAuth2PasswordRequestForm = Depends(),
    db: Session = Depends(get_db),
):
    user = authenticate_user(form_data.username, form_data.password, 'InvestorUsers', db)
    if not user:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Incorrect username or password",
        )
    access_token_expires = timedelta(minutes=settings.ACCESS_TOKEN_EXPIRE_MINUTES)
    access_token = create_access_token(
        data={"sub": user.email}, expires_delta=access_token_expires
    )
    response.set_cookie(
        key="access_token", value=f"Bearer {access_token}", httponly=True
    )

    results = {
        "access_token": access_token,
        "token_type": "bearer"
    }

    results.update({
        "user_info": {
            "email": user.email,
            # "fullname": user.fullname
        }
    })
    return results


oauth2_scheme = OAuth2PasswordBearerWithCookie(tokenUrl="/login/token")


def get_current_user_from_token(
    token: str = Depends(oauth2_scheme), db: Session = Depends(get_db)
):
    credentials_exception = HTTPException(
        status_code=status.HTTP_401_UNAUTHORIZED,
        detail="Could not validate credentials",
    )
    try:
        payload = jwt.decode(
            token, settings.SECRET_KEY, algorithms=[settings.ALGORITHM]
        )
        username: str = payload.get("sub")
        print("username/email extracted is ", username)
        if username is None:
            raise credentials_exception
    except JWTError:
        raise credentials_exception
    user = get_user(username=username, db=db)
    if user is None:
        raise credentials_exception
    return user


#
# @router.post("/auth/forgot-password")
# async def forgot_password(request: EmailRequest,db):
#     # Check exited user
#     user = await find_existed_user(request.email,'InvestorUsers', db)
#     if not user:
#         raise BusinessException(status_code=999, detail="User not found")
#
#     # Create reset code and save it in database
#     reset_code = str(uuid.uuid1())
#     await create_reset_code(request, reset_code,db)
#
#     # Sending email
#     subject = "Testing Email For Dev."
#     recipient = [request.email]
#     message = """
#     <!DOCTYPE html>
#     <html>
#     <title>Reset Password</title>
#     <body>
#     <div style="width:100%;font-family: monospace;">
#         <h1>Hello, {0:}</h1>
#         <p>Someone has requested a link to reset your password. If you requested this, you can change your password through the button below.</p>
#         <a href="http://127.0.0.1:8000/user/forgot-password?reset_password_token={1:}" style="box-sizing:border-box;border-color:#1f8feb;text-decoration:none;background-color:#1f8feb;border:solid 1px #1f8feb;border-radius:4px;color:#ffffff;font-size:16px;font-weight:bold;margin:0;padding:12px 24px;text-transform:capitalize;display:inline-block" target="_blank">Reset Your Password</a>
#         <p>If you didn't request this, you can ignore this email.</p>
#         <p>Your password won't change until you access the link above and create a new one.</p>
#     </div>
#     </body>
#     </html>
#     """.format(request.email, reset_code)
#     await emailUtil.send_email(subject, recipient, message)
#
#     return {
#         "code": 200,
#         "message": "We've sent an email with instructions to reset your password."
#     }
#
#
