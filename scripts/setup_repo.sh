#!/bin/bash

# Create the main project folder
mkdir scientific_papers
cd scientific_papers

# Create the virtual environment
python3 -m venv venv
source venv/bin/activate

# Create the main application, database, and utility folders
mkdir app
mkdir app/db
mkdir app/utils

# Install required libraries
pip install psycopg2-binary sqlalchemy

# Create the main application file
cat << EOF > app/main.py
import os
from app.db.database import init_db, get_paper_key_concepts

def main():
    init_db()
    # Add your main application logic here

if __name__ == "__main__":
    main()
EOF

# Create the database configuration and handling files
cat << EOF > app/db/config.py
DATABASE_URI = "postgresql://username:password@localhost/dbname"
EOF

cat << EOF > app/db/database.py
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
EOF

# Create the utility functions file
cat << EOF > app/utils/convenience.py
from app.db.database import get_paper_key_concepts

def get_key_concepts(abbreviated_title):
    return get_paper_key_concepts(abbreviated_title)
EOF
