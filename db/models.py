from sqlalchemy import Column, Integer, String
from sqlalchemy.ext.declarative import declarative_base
import uuid

Base = declarative_base()


class Knowledge(Base):
    __tablename__ = 'knowledge'

    id = Column(String(36), default=lambda: str(uuid.uuid4()), primary_key=True, unique=True,)
    user_id = Column(String)
    type = Column(Integer, default=1)
    question = Column(String)
    answer = Column(String)
