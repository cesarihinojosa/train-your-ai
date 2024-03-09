from flask import Flask, render_template, request, Blueprint
from .agent import start

home = Blueprint('home', __name__)

@home.route("/")
def app_home():
    return render_template('index.html')

@home.route("/train", methods=['GET', 'POST'])
def train():
    if request.method == 'POST':
        start()
    return render_template('snake.html')

