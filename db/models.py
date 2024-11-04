from sqlalchemy import Column, Integer, String
from sqlalchemy.ext.declarative import declarative_base

Base = declarative_base()


class Knowledge(Base):
    __tablename__ = 'knowledge'

    id = Column(String, primary_key=True)
    user_id = Column(String)
    question = Column(String)
    answer = Column(Integer)
