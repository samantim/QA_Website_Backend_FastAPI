from schemas.answers import Answer_Show
from sqlalchemy.orm import Session, Query
from datetime import datetime
from db.models.answers import Answer
from db.models.users import User
from db.models.questions import Question
from fastapi import UploadFile, File
from pathlib import Path

#create a new answer with attachment file
def create_answer(description : str, question_id : int, attachment : UploadFile, db : Session, current_active_user : User) -> Answer:
    answer = Answer(
        description =   description,
        question_id = question_id,
        date_posted = datetime.now(),
        user_id = current_active_user.id,
        is_correct = False,
        #attachment is optional
        attachment_path = attachment.filename if attachment else "" #in real project it is necessary to store files with new organized names
        )
    db.add(answer)
    db.commit()
    db.refresh(answer)
    #create path of new file in attachment folder placed in project root folder
    local_path : Path = Path(".")/"attachments"/attachment.filename
    #save attachment in hard disk
    save_attachment_file(attachment, local_path.absolute())
    #extracting current username, current question description and add it to answer dict for showing
    current_user : User = db.query(User).filter(User.id == current_active_user.id).first()
    answer.__dict__.update({"replier" : current_user.username})
    current_question : Question = db.query(Question).filter(Question.id == question_id).first()
    answer.__dict__.update({"question" : current_question.description})
    return answer

#save attachment in hard disk
def save_attachment_file(attachment : UploadFile, output_path : str):
    with open(output_path, "wb") as out_file:
        content = attachment.file.read()
        out_file.write(content)
        out_file.close()
    return True

#read all answer in answer_Show format
def read_answers(db: Session) -> Query[Answer_Show]:
    answers : list[Answer_Show] = db.query(
        Answer.description,
        Question.description.label("question"), #get from joined table (Question) with alias
        Answer.date_posted,
        Answer.is_correct,
        Answer.attachment_path,
        User.username.label("replier") #get from joined table (User) with alias
        ).join(User, Answer.user_id == User.id).join(Question, Answer.question_id == Question.id)
    return answers

#get all answers
def read_all_answers(db : Session) -> list[Answer_Show]:
    return read_answers(db).all()

#get an answer based on id
def read_answer_by_id(answer_id:int, db : Session) -> Answer_Show:
    return read_answers(db).filter(Answer.id == answer_id).first()

#delete an answer based on id
def delete_answer_by_id(answer_id : int, db : Session):
    answers =  db.query(Answer).filter(Answer.id == answer_id)
    if not answers.first():
        return False
    #for update and delete we should make a query which contains prefered results and then use its update or delete methods
    answers.delete()
    db.commit()
    return True