from schemas.questions import Question_Show
from sqlalchemy.orm import Session, Query
from datetime import datetime
from db.models.questions import Question
from db.models.users import User
from fastapi import UploadFile, File
from pathlib import Path

#create a new question with attachment file
def create_question(description : str, attachment : UploadFile, db : Session, current_active_user : User) -> Question:
    question = Question(
        description =   description,
        date_posted = datetime.now(),
        user_id = current_active_user.id,
        is_solved = False,
        #attachment is optional
        attachment_path = attachment.filename if attachment else "" #in real project it is necessary to store files with new organized names
        )
    db.add(question)
    db.commit()
    db.refresh(question)
    #create path of new file in attachment folder placed in project root folder
    local_path : Path = Path(".")/"attachments"/attachment.filename
    #save attachment in hard disk
    save_attachment_file(attachment, local_path.absolute())
    #extracting current username and add it to question dict for showing
    current_username : User = db.query(User).filter(User.id == current_active_user.id).first()
    question.__dict__.update({"asker" : current_username.username})
    return question

#save attachment in hard disk
def save_attachment_file(attachment : UploadFile, output_path : str):
    with open(output_path, "wb") as out_file:
        content = attachment.file.read()
        out_file.write(content)
        out_file.close()
    return True

#read all question in Question_Show format
def read_questions(db: Session) -> Query[Question_Show]:
    questions : list[Question_Show] = db.query(
        Question.description,
        Question.date_posted,
        Question.is_solved,
        Question.attachment_path,
        User.username.label("asker") #get from joined table (User) with alias
        ).join(User, Question.user_id == User.id)
    return questions

#get all questions
def read_all_questions(db : Session) -> list[Question_Show]:
    return read_questions(db).all()

#get a question based on id
def read_question_by_id(question_id:int, db : Session) -> Question_Show:
    return read_questions(db).filter(Question.id == question_id).first()

#delete a question based on id
def delete_question_by_id(question_id : int, db : Session):
    questions =  db.query(Question).filter(Question.id == question_id)
    if not questions.first():
        return False
    #for update and delete we should make a query which contains prefered results and then use its update or delete methods
    questions.delete()
    db.commit()
    return True