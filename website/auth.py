from flask import Blueprint, render_template, request, flash

auth = Blueprint('auth', __name__)

@auth.route("sign-in", methods=['GET', 'POST'])
def sign_in():
    if request.method == 'POST':
        first_name = request.form.get('first-name')
        grade_level = request.form.get('grade-level')
        if valid_input(first_name, grade_level):
            pass
    return render_template("signin.html")

@auth.route("log-in", methods=['GET', 'POST'])
def log_in():
    return render_template("login.html")

def valid_input(first_name, grade_level):
    if len(first_name) < 2:
        flash("first name must be greater than 1 character", category="error")
        return False
    elif len(grade_level) == 0:
        flash("grade level can't be empty", category="error")
        return False
    else:
        return True