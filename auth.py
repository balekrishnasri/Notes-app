import bcrypt
from db import get_connection

def register_user(username, password):
    conn = get_connection()
    c = conn.cursor()

    c.execute("SELECT * FROM users WHERE username=?", (username,))
    if c.fetchone():
        conn.close()
        return False

    hashed = bcrypt.hashpw(password.encode(), bcrypt.gensalt())
    c.execute("INSERT INTO users VALUES (?, ?)", (username, hashed))
    conn.commit()
    conn.close()
    return True

def login_user(username, password):
    conn = get_connection()
    c = conn.cursor()

    c.execute("SELECT * FROM users WHERE username=?", (username,))
    data = c.fetchone()
    conn.close()

    if data:
        return bcrypt.checkpw(password.encode(), data[1])
    return False