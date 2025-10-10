import os
import locale

from cs50 import SQL
from flask import Flask, flash, redirect, render_template, request, session
from flask_session import Session
from werkzeug.security import check_password_hash, generate_password_hash
from datetime import datetime

from helpers import apology, login_required, brl, format_date

# Configure locale to brazilian portuguese
try:
    locale.setlocale(locale.LC_ALL, 'pt_BR.UTF-8')
except locale.Error:
    locale.setlocale(locale.LC_ALL, '')

# Configure application
app = Flask(__name__)

# Custom filter
app.jinja_env.filters["brl"] = brl
app.jinja_env.filters['dateformat'] = format_date

# Configure session to use filesystem (instead of signed cookies)
app.config["SESSION_PERMANENT"] = False
app.config["SESSION_TYPE"] = "filesystem"
Session(app)

# Configure CS50 Library to use SQLite database
db = SQL("sqlite:///budget.db")


@app.after_request
def after_request(response):
    """Ensure responses aren't cached"""
    response.headers["Cache-Control"] = "no-cache, no-store, must-revalidate"
    response.headers["Expires"] = 0
    response.headers["Pragma"] = "no-cache"
    return response


@app.route("/")
@login_required
def index():
    """Show user's financial dashboard"""

    # Get user's id from the session
    user_id = session["user_id"]

    # Current year and month
    current_year = datetime.now().year
    current_month = datetime.now().month

    # Search user's name for greeting
    username = db.execute("SELECT username FROM users WHERE id = ?", user_id)[0]["username"]

    # Total monthly income
    income_rows = db.execute(
        "SELECT SUM(amount) as total FROM transactions WHERE user_id = ? AND type = 'Income' AND strftime('%m', timestamp) = ? AND strftime('%Y', timestamp) = ?", user_id, str(current_month).zfill(2), str(current_year)
    )
    total_income = income_rows[0]["total"] or 0 # Use 0 if not incomes

    # Total monthly expenses
    expense_rows = db.execute(
      "SELECT SUM(amount) as total FROM transactions WHERE user_id = ? AND type = 'Expense' AND strftime('%m', timestamp) = ? AND strftime('%Y', timestamp) = ?", user_id, str(current_month).zfill(2), str(current_year)
    )
    total_expense = expense_rows[0]["total"] or 0 # Use 0 if not expenses

    # Balance
    balance = total_income - total_expense

    # Last 5 transactions
    recent_transactions = db.execute (
        "SELECT * FROM transactions WHERE user_id = ? ORDER BY timestamp DESC LIMIT 5", user_id
    )

    return render_template("index.html", username=username, total_income=total_income, total_expense=total_expense, balance=balance, recent_transactions=recent_transactions)


@app.route("/login", methods=["GET", "POST"])
def login():
    """Log user in"""

    # Forget any user_id
    session.clear()

    # User reached route via POST (as by submitting a form via POST)
    if request.method == "POST":
        # Ensure username was submitted
        if not request.form.get("username"):
            return apology("must provide username", 403)

        # Ensure password was submitted
        elif not request.form.get("password"):
            return apology("must provide password", 403)

        # Query database for username
        rows = db.execute(
            "SELECT * FROM users WHERE username = ?", request.form.get("username")
        )

        # Ensure username exists and password is correct
        if len(rows) != 1 or not check_password_hash(
            rows[0]["hash"], request.form.get("password")
        ):
            return apology("invalid username and/or password", 403)

        # Remember which user has logged in
        session["user_id"] = rows[0]["id"]

        # Redirect user to home page
        return redirect("/")

    # User reached route via GET (as by clicking a link or via redirect)
    else:
        return render_template("login.html")


@app.route("/logout")
def logout():
    """Log user out"""

    # Forget any user_id
    session.clear()

    # Redirect user to login form
    return redirect("/")


@app.route("/register", methods=["GET", "POST"])
def register():
    """Register user"""
    # clear previous session
    session.clear()

    if request.method == "POST":
        # validation of the credentials
        if not request.form.get("username"):
            return apology("Missing username", 400)
        if not request.form.get("password"):
            return apology("Missing password", 400)
        if not request.form.get("confirmation"):
            return apology("Missing confirmation of password", 400)
        if request.form.get("password") != request.form.get("confirmation"):
            return apology("Password and confirmation don't match", 400)

        # search if the user already exists
        rows = db.execute("SELECT * FROM users WHERE username=?", request.form.get("username"))

        if len(rows) != 0:
            return apology("Username already in use", 400)

        # Register the user
        db.execute("INSERT INTO users (username, hash) VALUES (?, ?)", request.form.get(
            "username"), generate_password_hash(request.form.get("password")))

        # Search the updated database
        rows = db.execute("SELECT * FROM users WHERE username=?", request.form.get("username"))

        # Create a new session for the user
        session["user_id"] = rows[0]["id"]

        # Go to the home page now logged in
        return redirect("/")

    else:
        return render_template("register.html")


@app.route("/add", methods=["GET", "POST"])
@login_required
def add():
    transactions = ["Income", "Expense"]
    categories = db.execute("SELECT * FROM CATEGORIES WHERE user_id IS NULL OR user_id = ?", session["user_id"])

    if request.method == "POST":
        # input of the value and the type of transaction
        amount = request.form.get("amount")
        transaction_type = request.form.get("type")
        description = request.form.get("description")
        category = request.form.get("category")

        if not amount:
            return apology("Missing value", 400)
        if not transaction_type:
            return apology("Missing type of transaction", 400)
        if not amount.isdigit() or float(amount) <= 0:
            return apology("Value must be a positive number", 400)
        if not category:
            return apology("Missing category", 400)
        if transaction_type not in ["Income", "Expense"]:
            return apology("Invalid transaction type", 400)

        try:
            amount = float(amount)
            if amount <= 0:
                raise ValueError
        except ValueError:
            return apology("Amount must be a positive number", 400)

        db.execute(
            "INSERT INTO transactions (user_id, description, amount, type, category) VALUES (?, ?, ?, ?, ?)", session["user_id"], description, amount, transaction_type,category
        )

        flash("Transaction added successfully!")
        return redirect("/")
    else:
        return render_template("add.html", transactions=transactions, categories=categories)


@app.route("/history")
@login_required
def history():
    """Show history of transactions"""
    # get the transactions table to be shown
    transactions = db.execute(
        "SELECT * FROM transactions WHERE user_id=? ORDER BY timestamp DESC", session["user_id"])

    return render_template("history.html", transactions=transactions)


@app.route("/categories", methods=["GET", "POST"])
@login_required
def categories():
    """Show and manage user's new categories"""

    if request.method == "POST":

        # Get user's new category
        new_category = request.form.get("category_name")

        if not new_category:
            return apology("Missing category name", 400)

        # Verify if category already exists
        existing = db.execute("SELECT * FROM categories WHERE user_id=? AND name=?", session["user_id"], new_category)
        if existing:
            return apology("Category already exists", 400)

        # Insert the new category
        db.execute("INSERT INTO categories (user_id, name) VALUES (?, ?)", session["user_id"], new_category)

        flash("Category added!")
        return redirect("/categories")

    else:
        # Get default and user's categories
        user_categories = db.execute("SELECT * FROM categories WHERE user_id IS NULL OR user_id=?", session["user_id"])
        return render_template("categories.html", categories=user_categories)


@app.route("/delete_category", methods = ["POST"])
@login_required
def delete_category():
    """Delete a user's custom category"""

    category_id = request.form.get("category_id")
