from pydantic import BaseModel

#token model 
class Token(BaseModel):
    access_token : str
    token_type : str