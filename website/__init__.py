from flask import Flask
from db_funcs import *

def create_app():
    app = Flask(__name__)
    app.config['SECRET_KEY'] = 'uwu'
    #developer spesific file path 
    app.config['UPLOAD_FOLDER'] = '../test/website/static'

    from .auth import auth

    app.register_blueprint(auth, url_prefix=('/'))

    return app