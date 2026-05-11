from database import cursor, conn
from datetime import datetime

def insert_candidate(data):
    try:
        cursor.execute("""
        INSERT INTO candidates VALUES (?, ?, ?, ?, ?, ?)
        """, (
            data["name"],
            data["score"],
            ", ".join(data["strengths"]),
            ", ".join(data["gaps"]),
            data["profile_url"],
            datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        ))
        conn.commit()
        return "Saved"
    except:
        return "Candidate already exists"


def delete_candidate(name):
    cursor.execute("DELETE FROM candidates WHERE name LIKE ?", (f"%{name}%",))
    conn.commit()

    if cursor.rowcount == 0:
        return "No record found"
    return "Deleted successfully"


def get_all():
    cursor.execute("SELECT * FROM candidates")
    data = cursor.fetchall()
    return data if data else "No candidates in database"


def get_top3():
    cursor.execute("SELECT * FROM candidates ORDER BY score DESC LIMIT 3")
    data = cursor.fetchall()
    return data if data else "No candidates found"


def get_by_name(name): 
    cursor.execute("SELECT * FROM candidates WHERE name LIKE ?", (f"%{name}%",))
    data = cursor.fetchall()

    if not data:
        return "No record found for that candidate"

    return data