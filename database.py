from cs50 import SQL
# Initialize the database connection
db = SQL("sqlite:///database.db")
db.execute("PRAGMA foreign_keys = ON")

# Create the "users" table if it doesn't exist
db.execute("""
CREATE TABLE IF NOT EXISTS users (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    username TEXT UNIQUE NOT NULL,
    hash TEXT NOT NULL
);
""")

# Create the "quiz_answers" table if it doesn't exist
db.execute("""
CREATE TABLE IF NOT EXISTS quiz_answers (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    user_id INTEGER NOT NULL,
    quiz_id INTEGER NOT NULL,
    question_number INTEGER NOT NULL,
    answer TEXT NOT NULL,
    time TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    FOREIGN KEY(user_id) REFERENCES users(id) ON DELETE CASCADE
);
""")

