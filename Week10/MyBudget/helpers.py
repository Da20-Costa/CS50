import locale

from datetime import datetime
from flask import redirect, render_template, session
from functools import wraps


def apology(message, code=400):
    """Render message as an apology to user."""
    return render_template("apology.html", top=code, bottom=message), code


def login_required(f):
    """
    Decorate routes to require login.

    https://flask.palletsprojects.com/en/latest/patterns/viewdecorators/
    """

    @wraps(f)
    def decorated_function(*args, **kwargs):
        if session.get("user_id") is None:
            return redirect("/login")
        return f(*args, **kwargs)

    return decorated_function


def brl(value):
    """Format value as BRL."""
    return locale.currency(value, grouping=True)

def format_date(date_string):
    """Formata uma string de data/hora para o padrão dd/mm/YYYY."""
    if date_string:
        date_obj = datetime.strptime(date_string, '%Y-%m-%d %H:%M:%S')
        return date_obj.strftime('%m/%d/%Y')
    return ""
