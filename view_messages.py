from database.db import connect_db

conn = connect_db()
cursor = conn.cursor()

cursor.execute("SELECT * FROM messages")
rows = cursor.fetchall()

print("---- MESSAGES ----")
for row in rows:
    print(row)

conn.close()