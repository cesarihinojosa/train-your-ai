from flask import Flask, render_template, request, Blueprint
from .agent import start

home = Blueprint('home', __name__)

@home.route("/")
def app_home():
    return render_template('base.html')

@home.route("/train")
def train():
    return render_template('snake.html')

