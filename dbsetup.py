from sqlalchemy import Column, ForeignKey, Integer, String, Date, DateTime, TIMESTAMP
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import relationship
from sqlalchemy import create_engine

Base = declarative_base()


class Message(Base):
    """
    Hotel store all the information on Vegas Hotels
    """
    __tablename__ = 'message'
    id = Column(Integer, primary_key=True)
    timestamp = Column(TIMESTAMP, nullable=False)


engine = create_engine('sqlite:///db.db')
Base.metadata.create_all(engine)
