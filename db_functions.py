import sqlite3
import pandas as pd

def connect_db():
    """
    Connects to database.
    """
    return sqlite3.connect("cs_hub.db")

def create_db():
    """
    Creates database if it doesn't exist.
    """
    conn = connect_db()
    cur = conn.cursor()
    cur.execute("""
                CREATE TABLE IF NOT EXISTS registration (
                username TEXT,
                coursecode TEXT
                ) 
            """)
    conn.commit()
    conn.close()
    
def clear_db():
    """
    Resets database by removing all entries.
    """
    conn = connect_db()
    cur = conn.cursor()
    cur.execute("DELETE FROM registration")
    conn.commit()
    conn.close()

def check_course_code(coursecode: str):
    """
    Checks that the coursecode is valid.
    """
    courses = [
            "CS 110", "CS 111", "CS 111", "CS 112", "CS 121",
            "CS 200", "CS 204", "CS 220", "CS 221", "CS 230",
            "CS 230", "CS 231", "CS 232", "CS 233", "CS 234",
            "CS 234", "CS 235", "CS 236", "CS 240", "CS 242",
            "CS 244", "CS 245", "CS 248", "CS 251", "CS 299",
            "CS 304", "CS 307", "CS 315", "CS 317", "CS 320",
            "CS 321", "CS 325", "CS 331", "CS 333", "CS 334",
            "CS 340", "CS 342", "CS 343", "CS 344", "CS 345",
            "CS 349", "CS 365", "CS 366"
            ]
    return coursecode in courses

def upload_registration(username: str, coursecode: str):
    """
    Uploads username coursecode pair to the database.
    """
    if check_course_code(coursecode):
        conn = connect_db()
        cur = conn.cursor()
        cur.execute("""INSERT INTO registration (name, coursecode)
                        VALUES (?,?) 
                        """, 
                        (username, coursecode)
                    )
        conn.commit()
        conn.close()

def delete_registration(username: str, course_code: str):
    """
    Delete a username coursecode pair from the database.
    """
    conn = connect_db()
    cur = conn.cursor()
    cur.execute("""DELETE FROM registration
                    WHERE username == ? AND coursecode == ?
                    """, 
                    (username, coursecode)
                )
    conn.commit()
    conn.close()
    return

def get_db():
    conn = connect_db()
    df = pd.read_sql_query("SELECT * FROM registration", conn)
    conn.close()
    return df

if __name__ == "__main__":
    # create_db()