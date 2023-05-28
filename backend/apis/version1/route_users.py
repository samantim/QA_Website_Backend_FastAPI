from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session
from db.models.users import User
from db.session import get_db
from schemas.users import User_Create, User_Update, User_Show
from db.repository.users import create_user, update_user, read_all_users
from apis.version1.route_login import send_verification_email

user_router = APIRouter()

@user_router.post("/register", response_model=User_Show)
def register_user(user : User_Create, db : Session = Depends(get_db)):
    user = create_user(user=user, db = db)
    if not user:
        raise  HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Registration was not seccessful!")
    send_verification_email(user.email)
    return user

@user_router.put("/change/{id}")
def change_user(id : int, user : User_Update, db : Session = Depends(get_db)):
    result = update_user(user_id=id, user=user, db=db)
    if not result:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=f"User id {id} not found!")
    return {"msg" : "Successfully updated data."}   

@user_router.get("/get/all", response_model=list[User_Show])
def show_all_users(db : Session = Depends(get_db)) -> list[User]:
    users = read_all_users(db)
    return users