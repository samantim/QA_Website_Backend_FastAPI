from fastapi import APIRouter, Depends, HTTPException, status, UploadFile, Form, File
from schemas.answers import Answer_Show
from db.session import get_db
from sqlalchemy.orm import Session
from db.models.users import User
from apis.version1.route_login import get_current_active_user
from db.repository.answers import create_answer, read_all_answers, read_answer_by_id, delete_answer_by_id

answer_router = APIRouter()

#when using uploadfiles, we have to use forms as input
@answer_router.post("", response_model=Answer_Show)
def add_answer(description : str = Form(), question_id : int = Form(), attachment : UploadFile | None = File(None), db : Session = Depends(get_db), current_active_user : User = Depends(get_current_active_user)):
    answer = create_answer(description, question_id, attachment, db, current_active_user)
    if not answer:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail="Failed to create a answer!")
    return answer

#get all answers
@answer_router.get("/get/all", response_model=list[Answer_Show])
def show_all_answers(db : Session = Depends(get_db), current_active_user : User = Depends(get_current_active_user)):
    #only admin can get all answers
    if not current_active_user.is_admin:
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="Not authorized to retrieve all answers!")
    answers = read_all_answers(db)
    return answers

#get a answer
@answer_router.get("/{id}", response_model=Answer_Show)
def show_answer(answer_id : int, db : Session = Depends(get_db)):
    answer = read_answer_by_id(answer_id, db)
    if not answer:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=f"answer id {answer_id} not found!")
    return answer

#delete a answer
@answer_router.delete("/delete/{id}")
def delete_answer(answer_id : int, db : Session = Depends(get_db), current_active_user : User = Depends(get_current_active_user)):
    #only admin can delete a answers
    if not current_active_user.is_admin:
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="Not authorized to delete answers!")
    result = delete_answer_by_id(answer_id, db)
    if not result:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="No answer to delete!")
    return {"msg" : f"answer id {answer_id} seccessfully deleted!"}