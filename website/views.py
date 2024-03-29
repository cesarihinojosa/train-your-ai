from flask import render_template, Blueprint

views = Blueprint('views', __name__)

@views.route("/")
def home():
    return render_template('home.html')

@views.route("/snake")
def snake():
    return render_template('snake.html')

@views.route("/intro")
def intro():
    return render_template('intro.html')

@views.route("/index")
def index():
    return render_template('index.html')
