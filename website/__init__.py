from flask import Flask
from .events import socketio
from . import agent
from . import game

def create_app():
    app = Flask(__name__)
    app.config["DEBUG"] = True
    app.config['SECRET_KEY'] = 'wdwehdi2hiouh3u'

    from .home import home
    app.register_blueprint(home, url_prefix='/')

    from .auth import auth
    app.register_blueprint(auth, url_prefix='/')

    socketio.init_app(app)

    return app