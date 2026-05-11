import sqlite3

conn = sqlite3.connect("candidates.db", check_same_thread=False)
cursor = conn.cursor()

cursor.execute("""
CREATE TABLE IF NOT EXISTS candidates (
    name TEXT UNIQUE,
    score INTEGER,
    strengths TEXT,
    gaps TEXT,
    profile_url TEXT,
    date TEXT
)
""")

conn.commit()