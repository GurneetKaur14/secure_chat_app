# Import bcrypt for secure password hashing
import bcrypt

# Import database connection function
from database.db import connect_db

# Function to register a new user
def register_user(username, password):
    # Connect to database
    conn = connect_db()
    cursor = conn.cursor()

    # Hash the password using bcrypt (adds salt automatically)
    hashed_pw = bcrypt.hashpw(password.encode(), bcrypt.gensalt())

    try:
        # Insert new user into users table
        cursor.execute(
            "INSERT INTO users (username, password) VALUES (?, ?)",
            (username, hashed_pw)
        )

        # Save changes
        conn.commit()
        return True

    except:
        # If username already exists (UNIQUE constraint fails)
        return False

    finally:
        # Always close the connection
        conn.close()

# Function to authenticate (login) user
def login_user(username, password):
    # Connect to database
    conn = connect_db()
    cursor = conn.cursor()

    # Fetch stored hashed password for given username
    cursor.execute(
        "SELECT password FROM users WHERE username = ?",
        (username,)
    )

    result = cursor.fetchone()

    # Close database connection
    conn.close()

    # If user exists
    if result:
        stored_pw = result[0]

        # Compare entered password with stored hashed password
        return bcrypt.checkpw(password.encode(), stored_pw)

    # If user not found
    return False