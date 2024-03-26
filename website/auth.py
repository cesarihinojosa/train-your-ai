from flask import Blueprint, render_template

auth = Blueprint('auth', __name__)

@auth.route("sign-in")
def sign_in():
    return render_template("signin.html")