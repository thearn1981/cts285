import sqlite3

# Connect to (or create) the database file
conn = sqlite3.connect("users.db")
cursor = conn.cursor()

# Create a table for users
cursor.execute("""
CREATE TABLE IF NOT EXISTS users (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    username TEXT UNIQUE,
    password TEXT
)
""")

# Insert one test user (run this only once)
cursor.execute("INSERT OR IGNORE INTO users (username, password) VALUES (?, ?)", ("tessa", "password123"))

conn.commit()
conn.close()
