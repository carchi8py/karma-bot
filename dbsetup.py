from sqlalchemy import Column, ForeignKey, Integer, String, Date, DateTime, TIMESTAMP, Numeric
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import relationship
from sqlalchemy import create_engine

Base = declarative_base()


class Message(Base):
    """
    Message store the last time stamp that we saw in channel
    """
    # TODO: this currently only work with one channel if we have mutiple channels we will need to keep track of channels
    __tablename__ = 'message'
    id = Column(Integer, primary_key=True)
    timestamp = Column(TIMESTAMP, nullable=False)

class UserKarma(Base):
    __tablename__ = 'userkarma'
    id = Column(Integer, primary_key=True)
    username = Column(String, nullable=False)
    karma = Column(Numeric, default=0.0)


engine = create_engine('sqlite:///db.db')
Base.metadata.create_all(engine)
