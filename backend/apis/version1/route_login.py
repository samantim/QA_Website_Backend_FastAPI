from fastapi.security import OAuth2PasswordBearer, OAuth2PasswordRequestForm
from fastapi import APIRouter, Depends, HTTPException, status
from schemas.users import User_Show
from schemas.login import Token
from jose import JWTError, jwt
from core.config import settings
from datetime import datetime, timedelta
from db.models.users import User
from db.repository.users import get_user_by_email, verify_user_by_email
from db.session import get_db
from sqlalchemy.orm import Session
from core.hashing import Hasher
from core.emailing import Email

login_router = APIRouter()

oauth2_scheme = OAuth2PasswordBearer(tokenUrl="/login/token")

def get_current_user(token : str = Depends(oauth2_scheme), db : Session = Depends(get_db)) -> User:
    authorization_ex = HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="Invalid credentials!")
    try:
        payload = jwt.decode(token, settings.JWT_SECRET_KEY,settings.JWT_ALGORITHMS)
        username = payload.get("sub")
        if not username:
            raise authorization_ex
        user = get_user_by_email(username, db)
        if not user:
            raise authorization_ex
        print(token)
        return user
    except JWTError:
        raise authorization_ex

def get_current_active_user(current_user : User = Depends(get_current_user)) -> User:
    if not current_user.is_active:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail="User is not activated!")
    return current_user

def create_access_token(data : dict, expire_delta : timedelta | None = None) -> str:
    expire = datetime.utcnow() + expire_delta if expire_delta else timedelta(minutes=30)
    to_encode = data.copy()
    to_encode.update({"exp" : expire})
    access_token = jwt.encode(to_encode, settings.JWT_SECRET_KEY, settings.JWT_ALGORITHMS)
    return access_token

def authenticate_user(username : str, plain_password : str, db : Session) -> User:
    user = get_user_by_email(username, db)
    if not user:
        return None
    if not Hasher.verify_password(plain_password, user.password):
        return None
    return user

def send_verification_email(email : str) -> bool:
    data = {"sub" : email}
    access_token = create_access_token(data, timedelta(minutes=settings.JWT_ACCESS_TOKEN_EXPIRE_MINUTE))
    url = "http://127.0.0.1:8000/login/verify?token=" + access_token
    email_body : str = "please click on this link to verify your email : \r\n" + url 
    email_sender = Email(settings.EMAIL_HOST, settings.EMAIL_PORT, settings.EMAIL_USERNAME, settings.EMAIL_PASSWORD)
    result = email_sender.send_email(settings.EMAIL_USERNAME, [email], "QA_Website [Email Verification]", email_body)
    return result

@login_router.get("/verify")
def verify_email(token : str, db : Session = Depends(get_db)):
    verify_ex = HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="Email verification failed!")
    try:
        payload = jwt.decode(token, settings.JWT_SECRET_KEY,settings.JWT_ALGORITHMS)
        username = payload.get("sub")
        if not username:
            raise verify_ex
        user = get_user_by_email(username, db)
        if not user:
            raise verify_ex
        if not verify_user_by_email(user, db):
            raise verify_ex
        return {"msg" : "Email verified seccessfully and user is now activated!"}
    except JWTError:
        raise verify_ex
    
@login_router.get("/me", response_model=User_Show)
def get_me(current_active_user : User = Depends(get_current_active_user)):
    return current_active_user

@login_router.post("/token", response_model=Token)
def login_for_access_token(form_data : OAuth2PasswordRequestForm = Depends(), db : Session = Depends(get_db)) -> Token:
    username = form_data.username
    password = form_data.password
    user = authenticate_user(username, password, db)
    if not user:
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="Username or password is incorrect!")
    if not user.is_active:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail="User is not activated!")
    data = {"sub" : username}
    access_token = create_access_token(data, timedelta(minutes=settings.JWT_ACCESS_TOKEN_EXPIRE_MINUTE))
    return {"access_token" : access_token,
            "token_type" : "bearer"}