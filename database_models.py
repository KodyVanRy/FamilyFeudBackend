__author__ = 'kody'

from sqlalchemy import Column, Integer, String

from database import Base


class Survey(Base):
    __tablename__ = "survey"
    id = Column('id', Integer, primary_key=True)
    title = Column('title', String)
    answer_count = Column('answer_count', Integer, nullable=True)

    def __init__(self, title=None):
        self.title = title


class Answer(Base):
    # TODO need to add permissions (Create Job, Create Account, Create Kompany)
    __tablename__ = 'users'
    id = Column('id', Integer, primary_key=True)
    survey = Column('survey', Integer)
    answer = Column('answer', String)
    value = Column('value', Integer)

    def __init__(self, survey=None, answer=None, value=None):
        self.survey = survey
        self.answer = answer
        self.value = value