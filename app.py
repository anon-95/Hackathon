from flask import Flask, render_template, request, redirect, session
from werkzeug.security import generate_password_hash
from cs50 import SQL  # If you're using CS50's SQL database

app = Flask(__name__)

db = SQL("sqlite:///database.db")


app.config["SESSION_PERMANENT"] = False
app.config["SESSION_TYPE"] = "filesystem"
Session(app)


@app.route('/')
def home():
    return render_template("login.html")

@app.route("/register", methods=["GET", "POST"])
def register():
    """Register user"""
    if request.method == "POST":
        username = request.form.get("username")
        password = request.form.get("password")
        confirmation = request.form.get("confirmation")

        if not username:
            return "must provide username", 400
        elif not password:
            return "must provide password", 400
        elif password != confirmation:
            return "Passwords do not match", 400
        
        # Hash the password
        hashed_password = generate_password_hash(password)

        # Insert the new user into the database
        db.execute("INSERT INTO users (username, hash) VALUES (?, ?)", username, hashed_password)

        # Get the user_id of the newly registered user
        user = db.execute("SELECT id FROM users WHERE username = ?", username)
        user_id = user[0]["id"]

        # Store user_id in the session
        session["user_id"] = user_id
        session["username"] = username

        return redirect("/")

    return render_template("register.html")

@app.route("/submit_quiz", methods=["POST"])
def submit_quiz():
    """Submit quiz answers"""
    username = session.get("username")
    if not username:
        return redirect("/login")

    quiz_id = request.form.get("quiz_id")
    answers = request.form.getlist("answers")  # Assume you're getting a list of answers

    # Get the user_id from the session
    user_id = session.get("user_id")

    for i, answer in enumerate(answers, start=1):
        # Insert each answer into the quiz_answers table with the user_id
        db.execute("""
        INSERT INTO quiz_answers (user_id, quiz_id, question_number, answer)
        VALUES (?, ?, ?, ?)
        """, user_id, quiz_id, i, answer)

    return redirect("/quiz_results")


@app.route('/daily_tracker')
def daily_tracker():
    return render_template('daily_tracker.html')





if __name__ == "__main__":
    app.run()