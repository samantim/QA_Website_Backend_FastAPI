from db.base_class import Base
from sqlalchemy import Column, Integer, String, DateTime, Boolean, BigInteger
from sqlalchemy.orm import relationship

#it is inherited from Base which is an as_declarative -> makes it possible to create tables automatically
class User(Base):
    __tablename__ = "users" #name in db
    id = Column(Integer, primary_key=True)
    username = Column(String, nullable=False, unique=True)
    password = Column(String, nullable=False)
    email = Column(String, nullable=False, unique=True, index=True)
    is_active = Column(Boolean, default=False)
    is_admin = Column(Boolean, default=False)
    questions = relationship("Question", back_populates="asker")
    answers = relationship("Answer", back_populates="replier")