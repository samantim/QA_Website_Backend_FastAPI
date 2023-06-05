from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session
from db.models.users import User
from db.session import get_db
from schemas.users import User_Create, User_Update, User_Show
from db.repository.users import create_user, update_user, read_all_users
from apis.version1.route_login import send_verification_email, get_current_active_user

user_router = APIRouter()

#take a user (in user_create model from schemas) and save it in db(all db transactions are be done in db.repositories)
@user_router.post("/register", response_model=User_Show)
def register_user(user : User_Create, db : Session = Depends(get_db)):
    #saving in db
    user = create_user(user=user, db = db)
    if not user:
        raise  HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail="Registration was not seccessful!")
    #sending a verification email -> method is placed in route_login
    send_verification_email(user.email)
    return user

#updating user info (Based of User_Update model only password and is_active can be updated->Optional)
@user_router.put("/change/{user_id}")
def change_user(user_id : int, user : User_Update, db : Session = Depends(get_db), current_active_user : User = Depends(get_current_active_user)):
    #get current_active_user as dependency and check if the current user is editing him/herself or admin user
    if not (current_active_user.id == user_id or current_active_user.is_admin):
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail=f"Not Authorized!")
    #updating in db
    result = update_user(user_id=user_id, user=user, db=db)
    if not result:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=f"User id {id} not found!")
    return {"msg" : "Successfully updated data."}
      

#get all users
@user_router.get("/get/all", response_model=list[User_Show])
def show_all_users(db : Session = Depends(get_db), current_active_user : User = Depends(get_current_active_user)) -> list[User]:
    #get current_active_user as dependency and check if it is admin user
    if not  current_active_user.is_admin:
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail=f"Not Authorized!")
    #read from db
    users = read_all_users(db)
    return users