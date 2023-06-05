from db.base_class import Base
from sqlalchemy import Column, Integer, String, DateTime, Boolean, BigInteger, ForeignKey
from sqlalchemy.orm import relationship

#it is inherited from Base which is an as_declarative -> makes it possible to create tables automatically
class Question(Base):
    __tablename__ = "questions" #name in db
    id = Column(Integer, primary_key=True)
    description = Column(String, nullable=False)
    date_posted = Column(DateTime, nullable=False)
    is_solved = Column(Boolean, default=False)
    attachment_path = Column(String)
    user_id = Column(Integer, ForeignKey("users.id"))
    asker = relationship("User", back_populates="questions")
    replies = relationship("Answer", back_populates="question")