import os

from cs50 import SQL
from flask import Flask, flash, redirect, render_template, request, session
from flask_session import Session
from werkzeug.security import check_password_hash, generate_password_hash

from helpers import apology, login_required, lookup, usd

# Configure application
app = Flask(__name__)

# Custom filter for formatting values as USD
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
    user_id = session["user_id"]

    # Calculate the number of shares per symbol (including buys and sells)
    stocks = db.execute("""
        SELECT symbol, SUM(shares) AS shares
        FROM transactions
        WHERE user_id = ?
        GROUP BY symbol
        HAVING SUM(shares) > 0
    """, user_id)

    portfolio = []
    total_value = 0

    for stock in stocks:
        symbol = stock["symbol"]
        shares = stock["shares"]
        quote = lookup(symbol)

        # Get the current price of the stock
        price = quote["price"]

        # Calculate the total value of the shares
        total_value += price * shares

        # Add stock information to the portfolio
        portfolio.append({
            "symbol": symbol,
            "name": quote["name"],
            "shares": shares,
            "price": price,
            "total": price * shares
        })

    # Get the user's cash balance
    cash = db.execute("SELECT cash FROM users WHERE id = ?", user_id)[0]["cash"]

    # Add the cash balance to the total value
    total_value += cash

    # Render the portfolio page with the stock information and cash balance
    return render_template("index.html", portfolio=portfolio, cash=cash, total_value=total_value)


@app.route("/buy", methods=["GET", "POST"])
@login_required
def buy():
    """Buy shares of a stock"""
    if request.method == "POST":
        # Get stock ticker and number of shares from the form
        symbol = request.form.get("symbol")
        shares = request.form.get("shares")

        # Check if the symbol and shares are provided
        if not symbol or not shares:
            return apology("Must provide symbol and number of shares", 400)

        # Check if shares is a valid number and greater than zero
        try:
            shares = int(shares)  # Convert shares to integer
        except ValueError:
            return apology("Shares must be a valid number", 400)

        if shares <= 0:
            return apology("Number of shares must be positive", 400)

        # Fetch the current price of the stock (you can use an API for this)
        stock = lookup(symbol)
        if stock is None:
            return apology("Invalid symbol", 400)

        price = stock["price"]
        total_cost = shares * price

        # Check if the user has enough cash
        user_id = session["user_id"]
        rows = db.execute("SELECT cash FROM users WHERE id = ?", user_id)
        cash = rows[0]["cash"]

        if total_cost > cash:
            return apology("Not enough cash", 400)

        # Update user's cash balance and record the transaction
        db.execute("UPDATE users SET cash = cash - ? WHERE id = ?", total_cost, user_id)
        db.execute("INSERT INTO transactions (user_id, symbol, shares, price) VALUES (?, ?, ?, ?)",
                   user_id, symbol, shares, price)

        flash(f"Purchased {shares} shares of {symbol} at ${price:.2f} per share")
        return redirect("/")

    return render_template("buy.html")


@app.route("/history")
@login_required
def history():
    """Show history of transactions"""
    user_id = session["user_id"]

    # Retrieve transaction history for the user
    transactions = db.execute(
        "SELECT symbol, shares, price, time FROM transactions WHERE user_id = ? ORDER BY time DESC", user_id)
    return render_template("history.html", transactions=transactions)


@app.route("/login", methods=["GET", "POST"])
def login():
    """Log user in"""

    # Forget any user_id
    session.clear()

    # User reached route via POST (as by submitting a form via POST)
    if request.method == "POST":
        # Ensure username and password are provided
        if not request.form.get("username"):
            return apology("must provide username", 403)
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
    if request.method == "POST":
        symbol = request.form.get("symbol").upper()
        quote = lookup(symbol)
        if not quote:
            return apology("Stock not found", 400)
        return render_template("quoted.html", quote=quote)
    else:
        return render_template("quote.html")


@app.route("/register", methods=["GET", "POST"])
def register():
    """Register user"""
    if request.method == "POST":
        username = request.form.get("username")
        password = request.form.get("password")
        confirmation = request.form.get("confirmation")

        # Ensure the required fields are provided
        if not username or not password or not confirmation:
            return apology("Must provide username and password", 400)

        # Ensure passwords match
        if password != confirmation:
            return apology("Passwords do not match", 400)

        # Check if the username already exists
        rows = db.execute("SELECT * FROM users WHERE username = ?", username)
        if len(rows) > 0:
            return apology("Username already exists", 400)

        # Hash the password and store the new user in the database
        hash = generate_password_hash(password)
        db.execute("INSERT INTO users (username, hash) VALUES (?, ?)", username, hash)

        flash("Registered!")
        return redirect("/login")
    else:
        return render_template("register.html")


@app.route("/sell", methods=["GET", "POST"])
@login_required
def sell():
    """Sell shares of stock"""
    if request.method == "POST":
        symbol = request.form.get("symbol").upper()
        shares = int(request.form.get("shares"))

        # Validate the stock symbol and number of shares
        if not symbol or not shares or shares <= 0:
            return apology("Invalid stock symbol or number of shares", 400)

        user_id = session["user_id"]

        # Get the number of shares owned for the given symbol
        owned_shares = db.execute("""
            SELECT SUM(shares) AS shares
            FROM transactions
            WHERE user_id = ? AND symbol = ?
            GROUP BY symbol
        """, user_id, symbol)[0]["shares"]

        # Check if the user owns enough shares to sell
        if owned_shares < shares:
            return apology("Not enough shares", 400)

        quote = lookup(symbol)
        price = quote["price"]
        total_value = price * shares

        # Update the user's cash balance and record the transaction
        db.execute("UPDATE users SET cash = cash + ? WHERE id = ?", total_value, user_id)
        db.execute("INSERT INTO transactions (user_id, symbol, shares, price) VALUES (?, ?, ?, ?)",
                   user_id, symbol, -shares, price)

        flash("Sold!")
        return redirect("/")
    else:
        user_id = session["user_id"]

        # Get the symbols of stocks that the user currently owns (those with positive shares)
        stocks = db.execute("""
            SELECT symbol
            FROM transactions
            WHERE user_id = ?
            GROUP BY symbol
            HAVING SUM(shares) > 0
        """, user_id)

        return render_template("sell.html", stocks=stocks)


@app.route("/change_password", methods=["GET", "POST"])
def change_password():
    """Allow users to change their password"""
    if request.method == "POST":
        old_password = request.form.get("old_password")
        new_password = request.form.get("new_password")
        confirmation = request.form.get("confirmation")

        # Check if all fields were filled in
        if not old_password or not new_password or not confirmation:
            return apology("Must provide old password, new password, and confirmation", 400)

        # Check if the new passwords match
        if new_password != confirmation:
            return apology("New passwords do not match", 400)

        user_id = request.form.get("username")  # Assuming username is provided for identification

        # Fetch the user's hashed password from the database
        rows = db.execute("SELECT hash FROM users WHERE username = ?", user_id)
        # Check if the old password provided is correct
        if not check_password_hash(rows[0]["hash"], old_password):
            return apology("Old password is incorrect", 400)

        # Update the password in the database
        db.execute("UPDATE users SET hash = ? WHERE username = ?",
                   generate_password_hash(new_password), user_id)

        flash("Password changed successfully!")
        return redirect("/login")  # Redirect back to login page after password change

    return render_template("change_password.html")
