from .extensions import socketio

@socketio.on("connect")
def handle_connect():
    print("client connected")

@socketio.on("user_join")
def handle_user_join(username):
    print(f"user {username} joined")