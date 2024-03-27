from flask import Blueprint, render_template, request, flash, redirect, url_for
from flask_login import login_user, login_required, logout_user, current_user
from . import db
from .dbmodels import User

auth = Blueprint('auth', __name__)

@auth.route("signin", methods=['GET', 'POST'])
def signin():
    if request.method == 'POST':
        first_name = request.form.get('first-name')
        grade_level = request.form.get('grade-level')
        if valid_input(first_name, grade_level):
            new_user = User(first_name=first_name, grade_level=grade_level)
            db.session.add(new_user)
            db.session.commit()
            login_user(new_user, remember=False)
            return redirect(url_for("home.index"))
    return render_template("signin.html")

#not being used at the moment
@auth.route("login", methods=['GET', 'POST'])
def login():
    return render_template("login.html")

@auth.route("logout")
def logout():
    logout_user()
    return redirect(url_for("auth.signin"))

def valid_input(first_name, grade_level):
    if len(first_name) < 2:
        flash("first name must be greater than 1 character", category="error")
        return False
    elif len(grade_level) == 0:
        flash("grade level can't be empty", category="error")
        return False
    else:
        return True