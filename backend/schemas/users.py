from pydantic import BaseModel, EmailStr
from typing import Optional

#user create, update, show models based on pydantic

class User_Create(BaseModel):
    username : str
    email : EmailStr
    password : str

class User_Update(BaseModel):
    password : Optional[str]
    is_active : Optional[bool]

class User_Show(BaseModel):
    username : str
    email : str
    is_active : bool
    is_admin : bool

    #convert everything to json then pass it
    class Config:
        orm_mode = True