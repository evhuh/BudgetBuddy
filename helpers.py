from werkzeug.utils import escape
from functools import wraps
from flask import Flask, redirect, render_template, session


def apology(message):
    return render_template("apology.html", message = message)


# Decorator for routes that require a log in
def login_required(f):
    @wraps(f)
    def decorated_function(*args, **kwargs):
        if session.get("user_id") is None:
            return redirect("/login")
        return f(*args, **kwargs)

    return decorated_function


# Format value as USD
def usd(value):
    return f"${value:,.2f}"
