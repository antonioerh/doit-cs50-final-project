import re
from flask import redirect, render_template, session
from functools import wraps

def check_email(identifier):
    if re.match(r"^[^@]+@[^@]+\.[^@]+$", identifier):
        return True
    else:
        return False

def check_date(date):
    if re.match(r"^\d{4}-\d{2}-\d{2}$", date):
        return True
    else:
        return False

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
