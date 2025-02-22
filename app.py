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
    return render_template("index.html")


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
        return redirect("/dashboard")  # Redirect to dashboard after login

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


# Run the application
if __name__ == "__main__":
    app.run(debug=True)