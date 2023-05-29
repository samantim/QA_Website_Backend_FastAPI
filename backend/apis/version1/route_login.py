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

#used to find the token in get methods -> finding the current user
oauth2_scheme = OAuth2PasswordBearer(tokenUrl="/login/token")

#revealing the current user using jwt token decoded
def get_current_user(token : str = Depends(oauth2_scheme), db : Session = Depends(get_db)) -> User:
    authorization_ex = HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="Invalid credentials!")
    try:
        payload = jwt.decode(token, settings.JWT_SECRET_KEY,settings.JWT_ALGORITHMS)
        #"sub" is a keyword for username(email) in jwt tokens
        username = payload.get("sub")
        if not username:
            raise authorization_ex
        user = get_user_by_email(username, db)
        if not user:
            raise authorization_ex
        return user
    except JWTError:
        raise authorization_ex

#take a current_user as dependency and pass it if the user is active
def get_current_active_user(current_user : User = Depends(get_current_user)) -> User:
    if not current_user.is_active:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail="User is not activated!")
    return current_user

#building a jwt token with expire time
def create_access_token(data : dict, expire_delta : timedelta | None = None) -> str:
    expire = datetime.utcnow() + expire_delta if expire_delta else timedelta(minutes=30)
    to_encode = data.copy()
    #we should add expire time to data dict ("sub")
    #"exp" is also a keyword
    to_encode.update({"exp" : expire})
    access_token = jwt.encode(to_encode, settings.JWT_SECRET_KEY, settings.JWT_ALGORITHMS)
    return access_token

#take a username and password and authenticate it based on hashed_password stored in db
def authenticate_user(username : str, plain_password : str, db : Session) -> User:
    user = get_user_by_email(username, db)
    if not user:
        return None
    if not Hasher.verify_password(plain_password, user.password):
        return None
    return user

#sending an email containing the verification link (token) 
def send_verification_email(email : str) -> bool:
    data = {"sub" : email}
    access_token = create_access_token(data, timedelta(minutes=settings.JWT_ACCESS_TOKEN_EXPIRE_MINUTE))
    #a simle msg body
    url = "http://127.0.0.1:8000/login/verify?token=" + access_token
    email_body : str = "please click on this link to verify your email : \r\n" + url 
    email_sender = Email(settings.EMAIL_HOST, settings.EMAIL_PORT, settings.EMAIL_USERNAME, settings.EMAIL_PASSWORD)
    result = email_sender.send_email(settings.EMAIL_USERNAME, [email], "QA_Website [Email Verification]", email_body)
    return result

#take a jwt toke (which we send to user by email), verify the user and set is_active field True
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

#take token from then url ("/login/token") and extract the user and check if it is active, then pass it through
#this method use cascade dependencies
@login_router.get("/me", response_model=User_Show)
def get_me(current_active_user : User = Depends(get_current_active_user)):
    return current_active_user

#take a outh2 authentication form and authenticate user to give the access token
@login_router.post("/token", response_model=Token)
def login_for_access_token(form_data : OAuth2PasswordRequestForm = Depends(), db : Session = Depends(get_db)) -> Token:
    #.username and .password are predefined variables of the OAuth2PasswordRequestForm
    username = form_data.username
    password = form_data.password
    user = authenticate_user(username, password, db)
    if not user:
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="Username or password is incorrect!")
    if not user.is_active:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail="User is not activated!")
    #create the jwt access token -> to be clear : in our project always user.email use as a username not user.username!
    data = {"sub" : username}
    access_token = create_access_token(data, timedelta(minutes=settings.JWT_ACCESS_TOKEN_EXPIRE_MINUTE))
    return {"access_token" : access_token,
            "token_type" : "bearer"}