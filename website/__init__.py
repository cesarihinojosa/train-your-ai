from flask import Flask
from flask_socketio import SocketIO
from . import agent
from . import game

def create_app():
    app = Flask(__name__)
    app.config['SECRET_KEY'] = 'wdwehdi2hiouh3u'
    socketio = SocketIO(app)

    from .game import game
    app.register_blueprint(game, url_prefix='/')

    from .home import home
    app.register_blueprint(home, url_prefix='/')

    return app, socketio