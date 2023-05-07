import psycopg2
import toml
from typing import List

# Read PostgreSQL connection information from 'postgres_config/config.toml'
config = toml.load("postgres_config/config.toml")

host = config["host"]
port = config["port"]
database = config["database"]
user = config["user"]
password = config["password"]

def create_papers_table():
    conn = psycopg2.connect(host=host, port=port, dbname=database, user=user, password=password)
    cur = conn.cursor()

    cur.execute("""
    CREATE TABLE IF NOT EXISTS papers (
        id SERIAL PRIMARY KEY,
        tag VARCHAR(255) UNIQUE NOT NULL,
        contents TEXT NOT NULL,
        summary TEXT NOT NULL,
        key_concepts TEXT[] NOT NULL
    )
    """)

    conn.commit()
    cur.close()
    conn.close()

def insert_paper(tag: str, contents: str, summary: str, key_concepts: List[str]):
    conn = psycopg2.connect(host=host, port=port, dbname=database, user=user, password=password)
    cur = conn.cursor()

    cur.execute("""
    INSERT INTO papers (tag, contents, summary, key_concepts)
    VALUES (%s, %s, %s, %s)
    """, (tag, contents, summary, key_concepts))

    conn.commit()
    cur.close()
    conn.close()


if __name__ == '__main__':
    # Create the 'papers' table
    create_papers_table()

    # Insert a sample row into the 'papers' table
    sample_tag = "paper_1"
    sample_contents = "This is the content of the first paper."
    sample_summary = "This is a summary of the first paper."
    sample_key_concepts = ["concept1", "concept2", "concept3"]

    insert_paper(sample_tag, sample_contents, sample_summary, sample_key_concepts)
