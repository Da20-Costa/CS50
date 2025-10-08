import os

from cs50 import SQL
from flask import Flask, flash, jsonify, redirect, render_template, request, session

# Configure application
app = Flask(__name__)

# Ensure templates are auto-reloaded
app.config["TEMPLATES_AUTO_RELOAD"] = True

# Configure CS50 Library to use SQLite database
db = SQL("sqlite:///birthdays.db")


@app.after_request
def after_request(response):
    """Ensure responses aren't cached"""
    response.headers["Cache-Control"] = "no-cache, no-store, must-revalidate"
    response.headers["Expires"] = 0
    response.headers["Pragma"] = "no-cache"
    return response

@app.route("/", methods=["GET", "POST"])
def index():
    if request.method == "POST":

        # TODO: Add the user's entry into the database
        name = request.form.get("friend")
        if not name:
            return render_template("error.html", message="Missing name")

        month = request.form.get("month")
        if not month:
            return render_template("error.html", message="Missing month")
        try:
            month = int(month)
        except ValueError:
            return render_template("error.html", message="Month must be an integer")
        if not 1 <= month <= 12:
            return render_template("error.html", message="Month must be between 1 and 12")

        day = request.form.get("day")
        if not day:
            return render_template("error.html", message="Missing day")
        try:
            day = int(day)
        except ValueError:
            return render_template("error.html", message="Day must be an integer")
        if not 1 <= day <= 31:
            return  render_template("error.html", message="Day must be between 1 and 31")

        repeatedBday = db.execute("SELECT id FROM birthdays WHERE name = ?", name.capitalize())

        if not repeatedBday:
            db.execute("INSERT INTO birthdays (name, month, day) VALUES (?, ?, ?)", name.capitalize(), month, day)
        else:
            db.execute("UPDATE birthdays SET month = ?, day = ? WHERE name = ?", month, day, name.capitalize())

        return redirect("/")

    else:

        # TODO: Display the entries in the database on index.html
        birthdays = db.execute("SELECT * FROM birthdays")

        return render_template("index.html", birthdays=birthdays)

@app.route("/delete", methods=["POST"])
def delete():
    idToDelete =request.form.get("id")

    if idToDelete:
        db.execute("DELETE FROM birthdays WHERE id=?", idToDelete)

    return redirect("/")


