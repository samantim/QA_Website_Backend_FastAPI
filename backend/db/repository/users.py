from schemas.users import User_Create, User_Update
from sqlalchemy.orm import Session, Query
from db.models.users import User
from core.hashing import Hasher

#all db transactions should be written here

#get query of user which makes it possible to update that user
def get_users(user_id : int, db : Session) -> Query[User]:
    return db.query(User).filter(User.id == user_id)

#create a new user -> used in registering
def create_user(user : User_Create, db : Session) -> User:
    user = User(
        username = user.username,
        password = Hasher.hash_password(user.password),
        email = user.email,
        is_active = False,
        is_admin = False
    )
    db.add(user)
    db.commit()
    db.refresh(user)
    return user

#updating a user info
def update_user(user_id : int, user : User_Update, db : Session) -> bool:
    found_user = get_users(user_id, db)
    if not found_user.first():
        return False
    #updating password is optional
    if user.password: 
        user.__dict__.update(password = Hasher.hash_password(user.password))
    else:
        user.__dict__.pop("password")

    user.__dict__.update(is_active = user.is_active)
    #only update fields which is given in input dic
    found_user.update(user.__dict__)
    db.commit()
    return True

#updating a user info
def make_user_admin(user_id : int, db : Session) -> bool:
    found_user = get_users(user_id, db)
    if not found_user.first():
        return False

    user = {"is_admin" : True}
    #only update fields which is given in input dic
    found_user.update(user)
    db.commit()
    return True

#get all users
def read_all_users(db : Session) -> list[User]:
    return db.query(User).all()

#finding a user based on email
def get_user_by_email(email : str, db : Session) -> User:
    return db.query(User).filter(User.email == email).first()

#activate then user if is not activated yet
def verify_user_by_email(user : User, db : Session) -> bool:
    if user.is_active:
        return False
    user_update = User_Update(is_active=True)
    result = update_user(user.id, user_update, db)
    return result
    