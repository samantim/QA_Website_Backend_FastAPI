from pydantic import BaseModel
from datetime import datetime
from fastapi import UploadFile

#question show models based on pydantic
class Question_Show(BaseModel):
    description : str
    date_posted : datetime
    is_solved : bool
    attachment_path : str
    asker : str #this is a foreign value (user.name) from users table

    #convert everything to json then pass it
    class Config:
        orm_mode = True