import functools
import random
from flask_login import current_user
from flask_socketio import disconnect, join_room
from .extensions import socketio
from .agent import start

def authenticated_only(f):
    @functools.wraps(f)
    def wrapped(*args, **kwargs):
        if not current_user.is_authenticated:
            disconnect()
        else:
            return f(*args, **kwargs)
    return wrapped

@socketio.on("connect")
@authenticated_only
def handle_connect():
    print(f"{current_user.first_name} connected")

@socketio.on("user_join")
def handle_user_join(username):
    print(f"user {username} joined")

@socketio.on("train")
@authenticated_only
def handle_train():
    start()