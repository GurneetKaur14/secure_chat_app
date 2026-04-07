import sqlite3
import os

# Get project root directory
BASE_DIR = os.path.abspath(os.path.join(os.path.dirname(__file__), '..'))

# Correct database path
DB_PATH = os.path.join(BASE_DIR, 'database', 'chat.db')

def connect_db():
    conn = sqlite3.connect(DB_PATH)
    return conn

def create_tables():
    conn = connect_db()
    cursor = conn.cursor()

    # Users table
    cursor.execute('''
    CREATE TABLE IF NOT EXISTS users (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        username TEXT UNIQUE,
        password TEXT
    )
    ''')

    # Messages table
    cursor.execute('''
    CREATE TABLE IF NOT EXISTS messages (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        username TEXT,
        message TEXT,
        timestamp DATETIME DEFAULT CURRENT_TIMESTAMP
    )
    ''')

# Function to save message to database
def save_message(username, message):
    conn = connect_db()
    cursor = conn.cursor()

    cursor.execute('''
    INSERT INTO messages (username, message)
    VALUES (?, ?)
    ''', (username, message))

    conn.commit()
    conn.close()
    
