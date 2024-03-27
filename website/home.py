from flask import Flask, render_template, request, Blueprint
from .agent import start

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
