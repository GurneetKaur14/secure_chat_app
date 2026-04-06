import bcrypt
from database.db import connect_db

def register_user(username, password):
    conn = connect_db()
    cursor = conn.cursor()

    hashed_pw = bcrypt.hashpw(password.encode(), bcrypt.gensalt())

    try:
        cursor.execute("INSERT INTO users (username, password) VALUES (?, ?)",
                       (username, hashed_pw))
        conn.commit()
        return True
    except:
        return False
    finally:
        conn.close()

def login_user(username, password):
    conn = connect_db()
    cursor = conn.cursor()

    cursor.execute("SELECT password FROM users WHERE username = ?", (username,))
    result = cursor.fetchone()

    conn.close()

    if result:
        stored_pw = result[0]
        return bcrypt.checkpw(password.encode(), stored_pw)
    
    return False