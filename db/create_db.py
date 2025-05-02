import sqlite3
import os

# Ensure the db folder exists
os.makedirs('db', exist_ok=True)

# Connect to SQLite database (creates file if not exists)
conn = sqlite3.connect('db/quiz.db')
cursor = conn.cursor()

# Create questions table
cursor.execute("""CREATE TABLE IF NOT EXISTS questions (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    question TEXT NOT NULL,
    option_a TEXT NOT NULL,
    option_b TEXT NOT NULL,
    option_c TEXT NOT NULL,
    option_d TEXT NOT NULL,
    correct_option TEXT NOT NULL,
    flagged BOOLEAN DEFAULT 0
);""")

conn.commit()
conn.close()

print('Database and table created successfully.')
