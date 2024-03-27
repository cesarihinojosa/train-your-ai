from flask import render_template, Blueprint

home = Blueprint('home', __name__)

@home.route("/")
def app_home():
    return render_template('base.html')

@home.route("/snake")
def snake():
    return render_template('snake.html')

@home.route("/index")
def index():
    return render_template('index.html')
