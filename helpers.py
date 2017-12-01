from functools import wraps
from flask import Flask, flash, redirect, render_template, request, session
from flask_session import Session

def replace_spaces(word):
    answer = ""
    for letter in word:
        if letter == " ":
            answer = answer + "T"
        else:
            answer = answer + letter
    return answer

def login_required(f):
    """
    Decorate routes to require login.
    """
    @wraps(f)
    def decorated_function(*args, **kwargs):
        if session.get("user_id") is None:
            return redirect("/")
        return f(*args, **kwargs)
    return decorated_function
