from flask import Flask, render_template, request
from backend.gamepackage import get_data
from backend.agent import start
import subprocess

app = Flask(__name__)

@app.route("/")
def home():
    return render_template('index.html')

@app.route("/train", methods=['GET', 'POST'])
def train():
    if request.method == 'POST':
        pass #TODO: FIGURE OUT SUBPROCESS
    return render_template('snake.html')

@app.route("/update_ui")
def update_ui():
    data = get_data()
    return data

if __name__ == "__main__":
    app.run(debug=True)