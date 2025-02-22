from flask import Flask, render_template, request, redirect, session
from werkzeug.security import generate_password_hash, check_password_hash
from cs50 import SQL
from flask_session import Session

# Initialize Flask application
app = Flask(__name__)

# Initialize CS50's SQL connection
db = SQL("sqlite:///database.db")

# Flask session configuration
app.config["SESSION_PERMANENT"] = False
app.config["SESSION_TYPE"] = "filesystem"
Session(app)
@app.route("/")
def index():
    """Home Page"""
    return render_template("login.html")


@app.route("/register", methods=["GET", "POST"])
def register():
    """User Registration"""
    if request.method == "POST":
        username = request.form.get("username")
        password = request.form.get("password")
        confirmation = request.form.get("confirmation")

        # Ensure username was provided
        if not username:
            return "Username is required", 400

        # Ensure password and confirmation match
        if password != confirmation:
            return "Passwords don't match", 400

        # Hash the password
        hashed_password = generate_password_hash(password)

        # Insert user into database
        try:
            db.execute("INSERT INTO users (username, hash) VALUES (?, ?)", username, hashed_password)
            return redirect("/login")  # Redirect to login page after registration
        except:
            return "Username already exists", 400

    return render_template("register.html")


@app.route("/login", methods=["GET", "POST"])
def login():
    """User Login"""
    if request.method == "POST":
        username = request.form.get("username")
        password = request.form.get("password")

        # Ensure username and password were provided
        if not username or not password:
            return "Username and password are required", 400

        # Retrieve the user from the database
        user = db.execute("SELECT * FROM users WHERE username = ?", username)
        
        # Ensure user exists and password matches
        if len(user) != 1 or not check_password_hash(user[0]["hash"], password):
            return "Invalid username or password", 400

        # Store user in session
        session["user_id"] = user[0]["id"]
        return render_template("intro_quiz")  # Redirect to dashboard after login

    return render_template("login.html")


@app.route("/dashboard")
def dashboard():
    """User Dashboard (Requires Login)"""
    if "user_id" not in session:
        return redirect("/login")  # If not logged in, redirect to login

    return render_template("dashboard.html")


@app.route("/logout")
def logout():
    """User Logout"""
    session.clear()  # Clear session
    return redirect("/")


# Route for the Thank You page (optional)
@app.route("/thank_you")
def thank_you():
    return "Thank you for your submission!"

if __name__ == "__main__":
    app.run(debug=True)


@app.route("/intro_quiz", methods=["GET", "POST"])
def intro_quiz():
    if request.method == "POST":
        # Retrieve form data
        username = request.form.get("username")
        medication = request.form.get("medication")
        times_per_day = request.form.get("times_per_day")
        email = request.form.get("email")

        # Assume quiz_id and question_number are being passed as part of the form (or set default values for now)
        quiz_id = 1  # Hardcoded quiz_id for now (adjust as needed)
        question_number = 1  # Assume first question (adjust as needed)

        # Insert form data into the quiz_answers table
        db.execute("""
        INSERT INTO quiz_answers (username, quiz_id, question_number, answer, time)
        VALUES (?, ?, ?, ?, CURRENT_TIMESTAMP)
        """, username, quiz_id, question_number, medication)

        # You can handle other answers here similarly if you have more questions

        # Redirect to a thank you page or another page after submission
        return render_template("pull_feeling_journal.html")

    # If the request is GET, simply render the form
    return render_template("form.html")

if __name__ == "__main__":
    app.run(debug=True)
