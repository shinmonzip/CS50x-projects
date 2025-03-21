import os

from cs50 import SQL
from flask import Flask, redirect, render_template, request

# Configure application
app = Flask(__name__)

# Ensure templates are auto-reloaded
app.config["TEMPLATES_AUTO_RELOAD"] = True

# Configure CS50 Library to use SQLite database
db = SQL("sqlite:///birthdays.db")


@app.after_request
def after_request(response):
    """
    Ensure responses are not cached.
    """
    response.headers["Cache-Control"] = "no-cache, no-store, must-revalidate"
    response.headers["Expires"] = 0
    response.headers["Pragma"] = "no-cache"
    return response


@app.route("/", methods=["GET", "POST"])
def index():
    """
    Main route for managing birthdays.
    """
    if request.method == "POST":
        # Retrieve user input from the form
        name = request.form.get("name")
        month = request.form.get("month")
        day = request.form.get("day")

        # Validate user input
        if not name or not month or not day:
            return redirect("/")
        try:
            month = int(month)
            day = int(day)
        except ValueError:
            return redirect("/")
        if month < 1 or month > 12 or day < 1 or day > 31:
            return redirect("/")

        # Insert the new birthday into the database
        db.execute("INSERT INTO birthdays (name, month, day) VALUES(?, ?, ?)", name, month, day)

        return redirect("/")
    else:
        # Retrieve all birthdays from the database
        birthdays = db.execute("SELECT * FROM birthdays")
        return render_template("index.html", birthdays=birthdays)


@app.route("/delete", methods=["POST"])
def delete():
    """
    Route for deleting a birthday based on its ID.
    """
    birthday_id = request.form.get("id")
    if birthday_id:
        db.execute("DELETE FROM birthdays WHERE id = ?", birthday_id)
    return redirect("/")
