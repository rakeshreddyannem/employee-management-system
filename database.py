import sqlite3 as sql
import os

DB_FILE = os.path.join(os.path.dirname(__file__), "employee_management.db")
SCHEMA_FILE = os.path.join(os.path.dirname(__file__), "schema.sql")

def get_connection():

    conn = sql.connect(DB_FILE)
    conn.execute("PRAGMA foreign_keys = ON;")
    conn.row_factory = sql.Row
    return conn

def init_db():
    conn = get_connection()

    with open(SCHEMA_FILE, 'r') as f:
        conn.executescript(f.read())
    
    conn.commit()
    conn.close()
    print(f"Database initialized in {DB_FILE}")

if __name__ == "__main__":
    init_db()


