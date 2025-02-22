from flask import Flask, render_template, request, redirect, session
from werkzeug.security import generate_password_hash
from your_database_module import db  # Replace with your actual DB module
from cs50 import SQL  # If you're using CS50's SQL database

app = Flask(__name__)

@app.route('/')
def home():
    return render_template("login.html")

@app.route("/register", methods=["GET", "POST"])
def register():
    """Register user"""
    if request.method == "POST":
        password = request.form.get("password")
        username = request.form.get("username")
        if not username:
            return apology("must provide username", 400)
        elif not password:
            return apology("must provide password", 400)
        elif not request.form.get("confirmation"):
            return apology("must confirm password", 400)
        elif password != request.form.get("confirmation"):
            return apology("passwords do not match", 400)

        hashed_password = generate_password_hash(password, method='scrypt', salt_length=16)
        try:
            db.execute("INSERT INTO users(username, hash) VALUES(?, ?)",
                       username.lower(), hashed_password)
        except ValueError:
            return apology("Username already taken", 400)

        else:
            user_id = db.execute(
                "SELECT id FROM users WHERE username = ? AND hash = ?", username, hashed_password)
            session["user_id"] = user_id[0]["id"]
            return redirect("/")

    else:
        return render_template("register.html")





@app.route('/daily_tracker')
def daily_tracker():
    return render_template('daily_tracker.html')





if __name__ == "__main__":
    app.run()