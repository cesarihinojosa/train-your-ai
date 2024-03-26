from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from os import path
from .events import socketio
from . import agent
from . import game

db = SQLAlchemy()
DB_NAME = "database.db"

def create_app():
    app = Flask(__name__)
    app.config["DEBUG"] = True
    app.config['SECRET_KEY'] = 'wdwehdi2hiouh3u'
    app.config['SQLALCHEMY_DATABASE_URI'] = f"sqlite:///{DB_NAME}"
    db.init_app(app)

    from .home import home
    app.register_blueprint(home, url_prefix='/')

    from .auth import auth
    app.register_blueprint(auth, url_prefix='/')

    from . import dbmodels
    with app.app_context():
        db.create_all()

    socketio.init_app(app)

    return app