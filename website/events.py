from .extensions import socketio
from .agent import start

@socketio.on("connect")
def handle_connect():
    print("client connected")

@socketio.on("user_join")
def handle_user_join(username):
    print(f"user {username} joined")

@socketio.on("train")
def handle_train():
    start()