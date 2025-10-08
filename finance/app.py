import os

from cs50 import SQL
from flask import Flask, flash, redirect, render_template, request, session
from flask_session import Session
from werkzeug.security import check_password_hash, generate_password_hash

from helpers import apology, login_required, lookup, usd

# Configure application
app = Flask(__name__)

# Custom filter
app.jinja_env.filters["usd"] = usd

# Configure session to use filesystem (instead of signed cookies)
app.config["SESSION_PERMANENT"] = False
app.config["SESSION_TYPE"] = "filesystem"
Session(app)

# Configure CS50 Library to use SQLite database
db = SQL("sqlite:///finance.db")


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
    """Show portfolio of stocks"""
    #search user's stocks and shares
    stocks = db.execute("SELECT symbol, SUM(shares) as total_shares FROM transactions WHERE user_id=? GROUP BY symbol HAVING total_shares > 0", session["user_id"])

    #search user's total cash
    cash = db.execute("SELECT cash FROM users WHERE id=?", session["user_id"])[0]["cash"]

    #total value
    total_value = cash

    for stock in stocks:
        quote = lookup(stock["symbol"])
        stock["name"] = quote["name"]
        stock["price"] = quote["price"]
        stock["value"] = quote["price"] * stock["total_shares"]
        total_value += stock["value"]

    return render_template("index.html", stocks = stocks, cash = usd(cash), total_value = usd(total_value))


@app.route("/buy", methods=["GET", "POST"])
@login_required
def buy():
    if request.method == "POST":
        #Validate the inputs
        shares = request.form.get("shares")
        symbol = request.form.get("symbol").upper()
        if not symbol:
            return apology("Missing symbol", 400)
        if not shares:
            return apology("Missing shares", 400)
        if not shares.isdigit() or int(shares) <= 0:
            return apology("Shares must be a positive number", 400)

        #look up for the value
        quote = lookup(symbol)
        if quote is None:
            return apology("Symbol not found", 400)

        #obtaining the values of the quotes
        price = quote["price"]
        total_cost = int(shares) * price

        #Obtaining how much cash te does the user have
        cash = db.execute("SELECT cash FROM users WHERE id=?", session["user_id"])[0]["cash"]

        #checkin if the money suffices
        if cash < total_cost:
            return apology("Not enough cash", 400)

        #update the user's amount of money
        db.execute("UPDATE users SET cash = cash - ? WHERE id =?", total_cost, session["user_id"])

        #update transactions
        db.execute("INSERT INTO transactions (user_id, symbol, shares, price, type) VALUES (?, ?, ?, ?, 'purchase')", session["user_id"], symbol, shares, price)

        #confirms to the user that it was succesfull
        flash(f"Bought {shares} shares of {symbol} costing {usd(total_cost)}!")
        return redirect("/")

    else:
        return render_template("buy.html")


@app.route("/history")
@login_required
def history():
    """Show history of transactions"""
    transactions = db.execute("SELECT * FROM transactions WHERE user_id=? ORDER BY timestamp DESC", session["user_id"])

    return render_template("history.html", transactions=transactions)


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


@app.route("/quote", methods=["GET", "POST"])
@login_required
def quote():
    """Get stock quote."""
    #Get the quote with lookup
    if request.method == "POST":
        quote = lookup(request.form.get("symbol").upper())
        if not quote:
            return apology("Invalid symbol", 400)
        else:
            return render_template("quote.html", quote=quote)
    else:
        return render_template("quote.html")

@app.route("/register", methods=["GET", "POST"])
def register():
    """Register user"""
    #clear previous session
    session.clear()

    if request.method == "POST":
        #validation of the credentials
        if not request.form.get("username"):
            return apology("Missing username", 400)
        if not request.form.get("password"):
            return apology("Missing password", 400)
        if not request.form.get("confirmation"):
            return apology("Missing confirmation of password", 400)
        if request.form.get("password") != request.form.get("confirmation"):
            return apology("Password and confirmation don't match", 400)

        #search if the user already exists
        rows = db.execute("SELECT * FROM users WHERE username=?", request.form.get("username"))

        if len(rows) != 0:
            return apology("Username already in use", 400)

        #Register the user
        db.execute("INSERT INTO users (username, hash) VALUES (?, ?)", request.form.get("username"), generate_password_hash(request.form.get("password")))

        #Search the updated database
        rows = db.execute("SELECT * FROM users WHERE username=?", request.form.get("username"))

        #Create a new session for the user
        session["user_id"] = rows[0]["id"]

        #Go to the home page now logged in
        return redirect("/")

    else:
        return render_template("register.html")


@app.route("/sell", methods=["GET", "POST"])
@login_required
def sell():
    """Sell shares of stock"""
    #get user's purchased stocks
    stocks = db.execute("SELECT symbol, SUM(shares) as total_shares FROM transactions WHERE user_id=? GROUP BY symbol HAVING total_shares > 0", session["user_id"])

    if request.method == "POST":
        #user inputs what and how many they wanna sell
        shares = request.form.get("shares")
        symbol = request.form.get("symbol").upper()

        if not symbol:
            return apology("Missing symbol", 400)
        if not shares:
            return apology("Missing shares", 400)
        if not shares.isdigit() or int(shares) <= 0:
            return apology("Shares must be a positive number", 400)

        #shares must be an integer
        shares = int(shares)

        for stock in stocks:
            if stock["symbol"] == symbol:
                #validate if the user has enough shares
                if stock["total_shares"] < shares:
                    return apology("You don't have enough shares", 400)
                else:
                    quote = lookup(symbol)
                    price = quote["price"]
                    total_sale = shares * price

                    #update user's and money
                    db.execute("UPDATE users SET cash = cash + ? WHERE id=?", total_sale, session["user_id"])

                    #update transactions
                    db.execute("INSERT INTO transactions (user_id, symbol, shares, price, type) VALUES (?, ?, ?, ?, 'sale')", session["user_id"], symbol, shares, price)

                    #confirms to the user that it was succesfull
                    flash(f"Sold {shares} shares of {symbol} for {usd(total_sale)}!")
                    return redirect("/")
        return apology("Symbol not found", 400)
    else:
        return render_template("sell.html", stocks=stocks)

