from pydantic import BaseModel
from datetime import datetime

#question show models based on pydantic
class Answer_Show(BaseModel):
    description : str
    date_posted : datetime
    is_correct : bool
    attachment_path : str
    question : str #this is a foreign value (question.description) from question table
    replier : str #this is a foreign value (user.name) from users table

    #convert everything to json then pass it
    class Config:
        orm_mode = True