import os
from datetime import datetime
from sqlalchemy import create_engine, ForeignKey
from sqlalchemy import Column, Date, Integer, String, DateTime
from sqlalchemy.ext.declarative import declarative_base
from settings import settings

TOP_LEVEL_DIR = os.path.abspath(os.curdir)
engine = create_engine('sqlite:///' + settings['system']['dblocation']) #, echo=True
Base = declarative_base()

class clients(Base):
    __tablename__ = "clients"
    id = Column(Integer, primary_key=True)
    mac = Column(String, nullable=True)
    data = Column(String, nullable=True)

    def __init__(self, mac, data):
        self.mac = mac
        self.data = data

Base.metadata.create_all(engine)
