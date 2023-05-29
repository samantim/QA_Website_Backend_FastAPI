from pydantic import BaseModel
from datetime import datetime

class Question_Create(BaseModel):
    description : str
    attachment_path : str

class Question_Show(BaseModel):
    description : str
    date_posted : datetime
    is_solved : bool
    attachment_path : str
    asker : str

    #convert everything to json then pass it
    class Config:
        orm_mode = True