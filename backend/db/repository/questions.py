from schemas.questions import Question_Create, Question_Show
from sqlalchemy.orm import Session, Query
from datetime import datetime
from db.models.questions import Question
from db.models.users import User
from typing import Optional

def create_question(question : Question_Create, db : Session, current_active_user : User) -> Question:
    question = Question(
        description = question.description,
        date_posted = datetime.now(),
        user_id = current_active_user.id,
        is_solved = False,
        attachment_path = ""
        )
    db.add(question)
    db.commit()
    db.refresh(question)
    current_username : User = db.query(User).filter(User.id == current_active_user.id).first()
    question.__dict__.update({"asker" : current_username.username})
    return question

def read_questions(db: Session) -> Query[Question_Show]:
    questions : list[Question_Show] = db.query(
        Question.description,
        Question.date_posted,
        Question.is_solved,
        Question.attachment_path,
        User.username.label("asker")
        ).join(User, Question.user_id == User.id).filter()
    return questions

def read_all_questions(db : Session) -> list[Question_Show]:
    return read_questions(db).all()

def read_question_by_id(question_id:int, db : Session) -> Question_Show:
    return read_questions(db).filter(Question.id == question_id).first()

def delete_question_by_id(question_id : int, db : Session):
    questions =  db.query(Question).filter(Question.id == question_id)
    if not questions.first():
        return False
    questions.delete()
    db.commit()
    return True