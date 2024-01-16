from flask import Flask
from flask_login import LoginManager
from db_funcs import *

def create_app():
    app = Flask(__name__)
    app.config['SECRET_KEY'] = 'uwu'

    
    from .auth import auth

    app.register_blueprint(auth, url_prefix=('/'))

    # login_manager = LoginManager()
    # login_manager.login_view = 'auth.login'
    # login_manager.init_app(app)

    # @login_manager.user_loader
    # def load_user(username):
    #     return DBfuncs.findUser(username)


    return app