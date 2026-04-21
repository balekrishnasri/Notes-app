import sqlite3

def get_connection():
    conn = sqlite3.connect("users.db", check_same_thread=False)
    c = conn.cursor()
    c.execute("CREATE TABLE IF NOT EXISTS users (username TEXT PRIMARY KEY, password BLOB)")
    conn.commit()
    return conn