from flask import Flask
from db_funcs import *

def create_app():
    app = Flask(__name__)
    app.config['SECRET_KEY'] = 'uwu'

    from .auth import auth

    app.register_blueprint(auth, url_prefix=('/'))

    return app