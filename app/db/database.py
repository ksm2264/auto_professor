import os
from sqlalchemy import create_engine, Column, Integer, String, Text, ARRAY
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker
from app.db.config import DATABASE_URI

Base = declarative_base()

class Paper(Base):
    __tablename__ = "papers"
    id = Column(Integer, primary_key=True)
    abbreviated_title = Column(String(255), unique=True, nullable=False)
    content = Column(Text, nullable=False)
    key_concepts = Column(ARRAY(String), nullable=False)

def init_db():
    engine = create_engine(DATABASE_URI)
    Base.metadata.create_all(engine)

def get_paper_key_concepts(abbreviated_title):
    engine = create_engine(DATABASE_URI)
    Session = sessionmaker(bind=engine)
    session = Session()

    paper = session.query(Paper).filter_by(abbreviated_title=abbreviated_title).first()
    if paper:
        return paper.key_concepts
    else:
        return None
