from db.base_class import Base
from sqlalchemy import Column, Integer, String, DateTime, Boolean, BigInteger, ForeignKey
from sqlalchemy.orm import relationship

class Question(Base):
    __tablename__ = "questions"
    id = Column(BigInteger, primary_key=True)
    description = Column(String, nullable=False)
    date_posted = Column(DateTime, nullable=False)
    is_solved = Column(Boolean, default=False)
    attachment_path = Column(String)
    user_id = Column(Integer, ForeignKey("users.id"))
    asker = relationship("users", back_populates="questions")
    replies = relationship("answers", back_populates="question")