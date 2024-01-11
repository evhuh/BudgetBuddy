from cs50 import SQL
from flask import Flask, redirect, render_template, request, session
from flask_session import Session
from werkzeug.security import check_password_hash, generate_password_hash

from helpers import apology, login_required, usd

# Configure application
app = Flask(__name__)

# Configure session to use filesystem (instead of signed cookies)
app.config["SESSION_PERMANENT"] = False
app.config["SESSION_TYPE"] = "filesystem"
Session(app)

# Configure CS50 Library to use SQLite database
db = SQL("sqlite:///budgetbuddy.db")


# Prevent caching; users see most up-to-date info
@app.after_request
def after_request(response):
    """Ensure responses aren't cached"""
    response.headers["Cache-Control"] = "no-cache, no-store, must-revalidate"
    response.headers["Expires"] = 0
    response.headers["Pragma"] = "no-cache"
    return response


# REGISTER
@app.route("/register", methods=["GET", "POST"])
def register():
    username = request.form.get("username")
    password = request.form.get("password")
    confirmation = request.form.get("confirmation")
    if request.method == "GET":
        return render_template("register.html")
    elif request.method == "POST":
        if not request.form.get("username"):
            return apology("Usernames are required")
        rows = db.execute("SELECT * FROM users WHERE username = ?", username)
        if len(rows) == 1:
            return apology("Username has been taken")
        elif not request.form.get("password"):
            return apology("Please input a password")
        # Make sure confirmation matches password
        if confirmation != password:
            return apology("Passwords do not match")
        # Add users' username and password to 'users' table
        else:
            # Hash password
            hash = generate_password_hash(password)
            db.execute(
                "INSERT INTO users (username, hash, budget) VALUES (?, ?, ?)",
                username,
                hash,
                0,
            )
            # Log user in --
            rows = db.execute("SELECT * FROM users WHERE username = ?", username)
            session["user_id"] = rows[0]["id"]
            # Redirect user to home page
            return redirect("/")


# LOGIN
@app.route("/login", methods=["GET", "POST"])
def login():
    # Forget any user_id
    session.clear()
    if request.method == "POST":
        if not request.form.get("username"):
            return apology("Please enter a username")
        elif not request.form.get("password"):
            return apology("Please enter a password")
        rows = db.execute(
            "SELECT * FROM users WHERE username = ?", request.form.get("username")
        )
        # Ensure username exists and password is correct
        if len(rows) != 1 or not check_password_hash(
            rows[0]["hash"], request.form.get("password")
        ):
            return apology("Username and password do not match")
        # Remember user that's logged in
        session["user_id"] = rows[0]["id"]
        # Redirect to main page
        return redirect("/")
    else:
        return render_template("login.html")


# LOGOUT
@app.route("/logout")
def logout():
    """Log user out"""
    # Forget user_id & redirect user to login page --
    session.clear()
    return redirect("/login")


# DASHBOARD
@app.route("/", methods=["GET"])
@login_required
def index():
    if request.method == "GET":
        user_id = session["user_id"]
        # Say hello to user --
        user = db.execute("SELECT username FROM users WHERE id = ?", user_id)[0][
            "username"
        ]
        # Budget --
        budget = db.execute("SELECT budget FROM users WHERE id = ?", user_id)[0][
            "budget"
        ]
        # Amount spent --
        input_db = db.execute("SELECT amount FROM input WHERE user_id = ?", user_id)
        spent = 0
        for row in input_db:
            spent += row["amount"]
        # Amount left --
        left = float(budget) - float(spent)
        # Check if over budget (Warning in HTML)
        if spent > budget:
            status = "Warning: Over budget!!"
        elif budget == 0:
            status = "Pending..."
        else:
            status = "On track :)"
        # Breakdown of spending by category --
        # liDict of categories and spendings per
        categories_spendings = db.execute(
            "SELECT category, SUM(amount) AS total_amount FROM input JOIN categories ON input.category_id = categories.id WHERE input.user_id = ? GROUP BY category",
            user_id,
        )
        # Make list of dictionaries to loop through in Jinja
        table = []
        for row in categories_spendings:
            dict = {}
            dict["category"] = row["category"]
            dict["amount"] = row["total_amount"]
            table.append(dict)
        # Progress Bar --
        budget_liDict = db.execute("SELECT amount FROM input")
        amount = 0
        for row in budget_liDict:
            amount += row["amount"]
        budget_amount = db.execute("SELECT budget FROM users WHERE id = ?", user_id)[0][
            "budget"
        ]
        # If works
        if amount and budget_amount:
            budgetSpent = round(amount / budget_amount * 100)
            print(budgetSpent)
        else:
            budgetSpent = 0
        return render_template(
            "index.html",
            usd=usd,
            user=user,
            budget=budget,
            spent=spent,
            status=status,
            left=left,
            table=table,
            budgetSpent=budgetSpent,
        )


# INFO
@app.route("/info", methods=["GET", "POST"])
@login_required
def info():
    user_id = session["user_id"]
    if request.method == "POST":
        # Set budget goal --
        if request.form.get("budget"):
            budget = float(request.form.get("budget"))
            print(budget)
            if budget is None:
                return apology("Please input a valid budget")
            # Update budget goal in db
            db.execute("UPDATE users SET budget = ? WHERE id = ?", budget, user_id)
            return redirect("/")
        # Expense input --
        if request.form.get("budget2"):
            category = str(request.form.get("category"))
            category_id = db.execute(
                "SELECT id FROM categories WHERE category = ?", category
            )[0]["id"]
            amount = request.form.get("budget2")
            name = request.form.get("budget22")
            db.execute(
                "INSERT INTO input (user_id, expense_name, category_id, amount) VALUES (?, ?, ?, ?)",
                user_id,
                name,
                category_id,
                amount,
            )
            return redirect("/")
        # Expense removal --
        if request.form.get("remove"):
            id = request.form.get("remove")
            db.execute("DELETE FROM input WHERE id = ?", id)
    # Table Toggle for Categories --
    cat_liDict = db.execute(
        "SELECT category FROM categories WHERE user_id = ? OR user_id IS NULL", user_id
    )
    # Display History Table --
    liDict = db.execute("SELECT * FROM input")
    table = []
    for row in liDict:
        dict = {}
        dict["id"] = row["id"]
        dict["category"] = db.execute(
            "SELECT category FROM categories WHERE id = ?", row["category_id"]
        )[0]["category"]
        dict["name"] = row["expense_name"]
        dict["amount"] = row["amount"]
        table.append(dict)
    return render_template("info.html", usd=usd, table=table, cat_liDict=cat_liDict)


# HISTORY
@app.route("/history", methods=["GET"])
@login_required
def hstory():
    user_id = session["user_id"]
    liDict = db.execute("SELECT * FROM input WHERE user_id = ?", user_id)
    table = []
    for row in liDict:
        dict = {}
        dict["id"] = row["id"]
        dict["category"] = db.execute(
            "SELECT category FROM categories WHERE id = ?", row["category_id"]
        )[0]["category"]
        dict["name"] = row["expense_name"]
        dict["amount"] = row["amount"]
        table.append(dict)
    return render_template("history.html", usd=usd, table=table)


# SETTINGS
@app.route("/settings", methods=["GET", "POST"])
@login_required
def settings():
    if request.method == "POST":
        user_id = session["user_id"]
        db.execute("DELETE FROM input WHERE user_id = ?", user_id)
        db.execute("UPDATE users SET budget = ? WHERE id = ?", 0, user_id)
        return redirect("/")
    else:
        return render_template("settings.html")
