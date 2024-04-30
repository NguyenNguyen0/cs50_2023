import os
import string

from cs50 import SQL
from flask import Flask, flash, redirect, render_template, request, session
from flask_session import Session
from werkzeug.security import check_password_hash, generate_password_hash

from helpers import apology, login_required, lookup, usd
from datetime import datetime

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


# save transaction to database
def save_transaction(userID, symbol, price, shares_trading, transacted):
    db.execute(
        "INSERT INTO history(userID, symbol, price, shares_trading, transacted) VALUES (?, ?, ?, ?, ?)",
        userID,
        symbol,
        price,
        shares_trading,
        transacted,
    )

def check_password(password):
    # the password not blank
    password.replace(" ", "")
    if password == "":
        return "the password must be filled!"

    # require password length 8
    if len(password) < 8:
        return "length of password must greater or equal 8"

    # require password have some numbers
    if not any(char.isdigit() for char in password):
        return "password must contain a digit"

    #require password have some special symbols
    special_chars = set(string.punctuation)
    if not any(char in special_chars for char in password):
        return "password must contain a special character"

    return ""

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
    # get stocks in database
    stocks = db.execute(
        """SELECT stocks.symbol, stocks.nameStock, stocks.shares, stocks.price FROM stocks
            JOIN users ON stocks.userID = users.id
            WHERE users.id = ? ;""",
        session["user_id"],
    )
    # if stocks is empty render blank table
    if stocks == []:
        return render_template("index.html")

    # cash balance
    total = 0
    for stock in stocks:
        stock["total"] = stock["price"] * stock["shares"]
        total += stock["total"]

    cash = 10000 - total
    db.execute("UPDATE users SET cash = ? WHERE id = ?;", cash, session["user_id"])

    # format the stock price and total
    for stock in stocks:
        stock["total"] = usd(stock["total"])
        stock["price"] = usd(stock["price"])

    # render table with stocks

    return render_template("index.html", stocks=stocks, cash=usd(cash))


@app.route("/buy", methods=["GET", "POST"])
@login_required
def buy():
    """Buy shares of stock"""
    if request.method == "POST":
        # get and check the symbol
        symbol = request.form.get("symbol")
        symbol = symbol.upper()

        if symbol == "":
            return apology("symbol is missing", 400)
        # check the symbol
        stock = lookup(symbol)
        if stock == None:
            return apology("invalid symbol", 400)

        # get and check the number of shares
        shares = request.form.get("shares")
        try:
            shares = int(shares)
        except ValueError:
            return apology("invalid number of shares!", 400)

        if shares == None or shares < 1:
            return apology("shares is missing", 400)

        # is enough cash to pay
        bought_cash = stock["price"] * shares
        cash = db.execute("SELECT cash FROM users WHERE id = ? ;", session["user_id"])

        if cash[0]["cash"] - bought_cash < 0:
            return apology("not enough cash to pay", 400)

        # check is the stock is already buy yet
        database_stock = db.execute(
            "SELECT * FROM stocks WHERE userID = ? AND symbol = ?;",
            session["user_id"],
            symbol,
        )

        # save stock to database
        if database_stock == []:
            # insert the stock to database
            db.execute(
                "INSERT INTO stocks(symbol, nameStock, shares, price, userID) VALUES (?, ?, ?, ?, ?);",
                stock["symbol"],
                stock["name"],
                shares,
                stock["price"],
                session["user_id"],
            )
        else:
            # update the record
            db.execute(
                "UPDATE stocks SET shares = shares + ? WHERE symbol = ? AND userID = ?;",
                shares,
                symbol,
                session["user_id"],
            )

        # update the user cash
        db.execute(
            "UPDATE users SET cash = cash - ? WHERE id = ?;",
            bought_cash,
            session["user_id"],
        )

        # save transaction to database
        now = datetime.now()
        now_str = now.strftime("%Y-%m-%d %H:%M:%S")

        save_transaction(session["user_id"], symbol, stock["price"], shares, now_str)

        # return to homepage
        return redirect("/"), flash("Bought!")
    else:
        return render_template("buy.html")


@app.route("/history")
@login_required
def history():
    """Show history of transactions"""

    # get the transactions and render
    transactions = db.execute(
        "SELECT symbol, shares_trading, price, transacted FROM history WHERE userID = ? ORDER BY historyID DESC",
        session["user_id"],
    )

    for i in range(0, len(transactions)):
        transactions[i]["price"] = usd(transactions[i]["price"])

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
            "SELECT * FROM users WHERE username = ?;", request.form.get("username")
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
        # get the info of the stock
        symbol = request.form.get("symbol")
        stock = lookup(symbol)

        # if the symbol is blank return a apology
        if stock == None:
            return apology("missing the symbol", 400)

        # format the price to usd
        stock["price"] = usd(stock["price"])

        return render_template("quote.html", stock=stock)
    else:
        return render_template("quote.html")


@app.route("/register", methods=["GET", "POST"])
def register():
    """Register user"""

    if request.method == "POST":
        # check the username is exists or not
        username = request.form.get("username")
        database_user = db.execute("SELECT username FROM users WHERE username = ?;", username)
        if username == "":
            return apology("the username must be filled!", 400)
        if database_user != []:
            return apology("the username has taken!", 400)

        # check the password is valid or not
        password = request.form.get("password")
        message = check_password(password)

        if message != "":
            return apology(message, 400)

        # check the confirm password match the password
        con_password = request.form.get("confirmation")
        if con_password != password:
            return apology("the confirm password is not matched!", 400)

        # save new user to database
        db.execute(
            "INSERT INTO users(username, hash) VALUES(?, ?);",
            username,
            generate_password_hash(password),
        )

        # return to homepage
        # register success, auto login fisrt time
        return login(), flash("Registered!")
    else:
        return render_template("register.html")


@app.route("/sell", methods=["GET", "POST"])
@login_required
def sell():
    """Sell shares of stock"""
    # get symbols from database
    stocks = db.execute(
        "SELECT symbol, shares, price FROM stocks WHERE userID = ?;", session["user_id"]
    )
    symbols = []
    # get the symbol list to render
    for stock in stocks:
        symbols.append(stock["symbol"])

    if request.method == "POST":
        # CHECK THE USER INPUT
        # check the number of share is valid or not
        symbol = request.form.get("symbol")
        shares = request.form.get("shares")
        shares = int(shares)

        # get the current shares in database
        current_shares = 0
        for stock in stocks:
            if stock["symbol"] == symbol:
                current_shares = stock["shares"]
                break

        # check shares is valid or not
        if shares > current_shares:
            return apology("too many shares", 400)

        # SELL THE STOCK
        if shares == current_shares:
            db.execute(
                "DELETE FROM stocks WHERE symbol = ? AND userID = ?;",
                symbol,
                session["user_id"],
            )
        else:
            db.execute(
                "UPDATE stocks SET shares = ? WHERE symbol = ? AND userID = ?;",
                current_shares - shares,
                symbol,
                session["user_id"],
            )

        # update the user cash
        current_stock = lookup(symbol)
        current_price = current_stock["price"]

        db.execute(
            "UPDATE users SET cash = cash + ? WHERE id = ?;",
            current_price,
            session["user_id"],
        )

        # save transaction to database
        now = datetime.now()
        now_str = now.strftime("%Y-%m-%d %H:%M:%S")
        stock = lookup(symbol)

        save_transaction(session["user_id"], symbol, current_price, -shares, now_str)

        return redirect("/"), flash("Sold!")
    else:
        return render_template("sell.html", symbols=symbols)


@app.route("/recover", methods=["GET", "POST"])
def recover():
    """Simple method to recover password"""
    # user must input the new password twice not similar to old password
    if request.method == "POST":
        # get username from form
        username = request.form.get("username")

        # username is NOT blank
        username.replace(" ", "")
        if username == "":
            return apology("the username must be filled!", 403)

        # get the username in database
        database_user = db.execute(
            "SELECT username, hash FROM users WHERE username = ? ;", username
        )

        # check the username is exist in database
        if database_user == []:
            return apology("the username is not exist", 404)

        # get the password
        new_password = request.form.get("password")
        confirmation = request.form.get("confirmation")

        # the password and confirmation not blank
        message = check_password(new_password)

        if message != "":
            return apology(message, 400)

        if confirmation == "":
            return apology("the confirm password must be filled!", 400)

        # confirmation and new_password must be similar
        if confirmation != new_password:
            return apology("the confirm password is not matched!", 400)

        # the new password is matched to old password
        old_hash = database_user[0]["hash"]

        if check_password_hash(old_hash, new_password):
            return apology("the new password must be difference to old!", 403)

        # set new password to user
        db.execute(
            "UPDATE users SET hash = ? WHERE username = ?;",
            generate_password_hash(new_password),
            username,
        )

        # session.clear()
        return login(), flash("Changed password successfully!")
    else:
        return render_template("recover.html")
