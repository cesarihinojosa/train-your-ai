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
#     join()
    
# def join():
#     username = current_user.first_name
#     room = random.randint(1, 100000000)
#     join_room(room)
#     print(username + ' has entered the room.', to=room)


@socketio.on("user_join")
def handle_user_join(username):
    print(f"user {username} joined")

@socketio.on("train")
@authenticated_only
def handle_train():
    start()